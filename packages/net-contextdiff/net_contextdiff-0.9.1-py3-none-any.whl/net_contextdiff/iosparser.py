# iosparser.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration module.

This module parses Cisco IOS configuration files into a dictionary.
"""



# --- imports ---



import re

from deepops import deepsetdefault
from netaddr import IPNetwork

from .configparser import IndentedContextualCommand, IndentedContextualConfig



# --- constants ---



# interface names and their canonical representations - the canonical
# versions don't have to be how Cisco IOS always displays them, in any
# particular context, but just so they can consistently matched against
#
# TODO: this (and the calling function) should really be more general
# and handle regular expressions

_INTERFACE_CANONICALS = {
    "ethernet": "Eth",
    "fastethernet": "Fa",
    "gigabitethernet": "Gi",
    "tengigabitethernet": "Te",
    "fortygigabitethernet": "Fo",
    "port-channel": "Po",
    "vl": "Vlan"
}



# _SERVICE_PORTS = dict
#
# Dictionary mapping service names (as displayed/usable in an access-
# list rule) into a port number.
#
# TODO: this list is not complete but parses all the rules we currently
# have in use.  It should be expanded at some point to all services.

_SERVICE_PORTS = {
    "bootps": 67,
    "bootpc": 68,
    "discard": 9,
    "domain": 53,
    "ftp": 21,
    "ftp-data": 20,
    "gopher": 70,
    "ident": 113,
    "isakmp": 500,
    "lpd": 515,
    "mail": 25,
    "non500-isakmp": 4500,
    "ntp": 123,
    "smtp": 25,
    "snmp": 161,
    "tftp": 69,
    "www": 80
}



# --- functions ---



def _expand_set(s):
    """This function exapands a string giving a set of numbers,
    separated by commas, which can include ranges from low to high,
    using hyphens.  The return value will be the set of numbers
    expressed.

    For example, given a string of "1,3-5", a set containing 1, 3, 4
    and 5 will be returned.
    """

    t = set()

    for i in s.split(","):
        i_range = i.split("-")

        if len(i_range) == 1:
            t.add(int(i))
        else:
            t.update(range(int(i_range[0]), int(i_range[1]) + 1))

    return t



def _ipnet4_to_ios(ipnet4):
    """This method converts an IPv4 IPNetwork object into its canonical
    representation in Cisco IOS in a standard access-list.

    Conversions are '0.0.0.0/0' to 'any' and single host networks (i.e.
    simple addresses) into a plain address with no mask.
    """

    if ipnet4 == IPNetwork("0.0.0.0/0"):
        return "any"

    if ipnet4.prefixlen == 32:
        return str(ipnet4.ip)

    return str(ipnet4.ip) + " " + str(ipnet4.hostmask)



def _service_to_port(service):
    """Converts a Cisco service named 'service' (as displayed/usable in
    an access-list rule) into a port number and return it as an
    integer.

    If the service name is not defined, it is assumed to already be
    numeric and is converted to an integer and returned.  If this
    conversion fails, an exception will be raised (whch probably
    indicates a service that is missing from the list).
    """

    return _SERVICE_PORTS.get(service) or int(service)



# IPV4 STANDARD ACCESS CONTROL LIST RULES



# regular expression for matching an IPv4 standard ACL rule, compiled
# once for efficiency

_IPACL_STD_RULE_RE = re.compile(
    r"^"
    r"(?P<action>permit|deny)"
    r" +"

    # we match "0.0.0.0 255.255.255.255" as "any" because the
    # netaddr module assumes the mask is a netmask (= /32) rather
    # than a hostmask, in this case
    r"((?P<any>any|0\.0\.0\.0 255\.255\.255\.255)|"
        r"(?:host )?(?P<host>[0-9.]+)|"
        r"(?P<net>[0-9.]+) (?P<mask>[0-9.]+))"

    r"$")


def _ipacl_std_rule_parse(rule):
    """Parse an IPv4 standard ACL rule, returning a 2-element tuple
    consisting of the action ('permit' or 'deny') and an IPNetwork
    object, specifying the address/network to match.
    """


    match = _IPACL_STD_RULE_RE.match(rule)

    if not match:
        raise ValueError(
            "failed to parse IPv4 standard ACL rule: " + rule)


    # match some special cases and, if not those, match as a
    # network/hostmask

    if match.group("any"):
        ipnet4 = IPNetwork("0.0.0.0/0")

    elif match.group("host"):
        ipnet4 = IPNetwork(match.group("host"))

    else:
        ipnet4 = IPNetwork(match.group("net") + "/" + match.group("mask"))


    return match.group("action"), ipnet4



def _ipacl_std_canonicalize(l):
    """This function sorts an IPv4 standard access-list into a canoncial
    form so two lists can be compared.  The list is supplied and
    returned as a new list of IOS rules.  Note that it is not sorted in
    place), as parsed by _ipacl_std_rule_parse().

    IPv4 standard ACLs are complicated in IOS due to its tendancy to
    reorganise the rules, after they're entered.  It always preserves
    the semantics of the list (never putting an overlapping 'permit' and
    'deny' in the wrong order), but it can move rules which don't
    interact around.  Presumably this is done to optimise processing.

    The solution adopted here is to build the ACLs up in blocks.  Each
    block is a set of rules where the address portions don't overlap;
    these are built, sorting each block into address order, before
    adding the sorted rules in the block into the resulting list.

    The result is lists which are not necessarily in the same order as
    they were constructed, nor how IOS stores them, but two lists should
    at least be in the same order so they can be directly compared.

    This function is applied to each list, after the configuration is
    read, and the returned list used to replace the order in which the
    rules were read.
    """


    # initialise the returned (canonical list)
    result = []

    # initialise the current block of non-overlapping rules
    block = []

    # go through the rules in the supplied list
    for rule in l:
        # parse the rule into action string and IPNetwork
        action, net = _ipacl_std_rule_parse(rule)

        # find out if this rule overlaps with the network of a rule
        # already in the block
        overlap = [ None for _, chk_net
                         in block
                         if ((net.first <= chk_net.last)
                             and (net.last >= chk_net.first)) ]

        if overlap:
            # we had an overlap, add the current block to the returned
            # list and reinitialise it with just this new rule
            result.extend(block)
            block = [(action, net)]

        else:
            # add this rule to the current block and re-sort it on the
            # addresses of the rules in it
            block.append( (action, net) )
            block.sort(key=(lambda rule: rule[1]))

    # we've reached the end, so store the rules in the current block on
    # the end of the list
    result.extend(block)

    # convert the rules back into IOS text format and return them as a
    # list
    return [ (action + " " + _ipnet4_to_ios(net)) for action, net in result ]



# IPV4 EXTENDED ACCESS CONTROL LIST RULES



# regular expression for matching an IPv4 extended ACL rule, compiled
# once for efficiency

_IPACL_EXT_RULE_RE = re.compile(
    r"^"
    r"(?P<action>permit|deny)"
    r" +"
    r"(?P<protocol>ip|icmp|tcp|udp|igmp|pim|gre|esp)"
    r" "
    r"(?P<src_addr>any|host ([0-9.]+)|([0-9.]+) ([0-9.]+))"
    r"( ("
        # 'eq' and 'neq' can support a list of services - we need to match
        # them non-greedy
        r"((?P<src_port_listop>eq|neq) (?P<src_port_list>\S+( \S+)*?))|"

        r"((?P<src_port_1op>lt|gt) (?P<src_port_num>\S+))|"
        r"range (?P<src_port_low>\S+) (?P<src_port_high>\S+)"
    r"))?"
    r" "
    r"(?P<dst_addr>any|host ([0-9.]+)|([0-9.]+) ([0-9.]+))"
    r"( ("
        r"((?P<dst_port_listop>eq|neq) (?P<dst_port_list>\S+( \S+)*?))|"
        r"((?P<dst_port_1op>lt|gt) (?P<dst_port_num>\S+))|"
        r"range (?P<dst_port_low>\S+) (?P<dst_port_high>\S+)|"
        r"(?P<icmp_type>echo(-reply)?)"
    r"))?"
    r"(?P<established> established)?"
    r"(?P<qos> (dscp \S+))?"
    r"(?P<log> (log|log-input))?"
    r"$"
)


def _ipacl_ext_rule_parse(rule):
    """Parse an IPv4 extended ACL rule, returning a 'normalised'
    form of the rule as a string.  The normalised form should allow
    two ACL rules which mean the same thing to be compared using a
    simple string comparison.

    This process mainly involves extracting the port entries and
    [potentially] translating them into port numbers, if they're named
    services (which can be used in rules, plus IOS will translate a
    numbered service to a name, if one matches).

    Note that no attempt is made to check the rule for validity.
    """


    match = _IPACL_EXT_RULE_RE.match(rule)

    if not match:
        raise ValueError(
            "failed to parse IPv4 extended ACL rule: " + rule)


    action, protocol, src_addr, dst_addr = match.group(
        "action", "protocol", "src_addr", "dst_addr")


    # match.group() will return an error if a named group does not exist
    # in the regexp; match.groupdict(), however, will return a default
    # value (None, if not specified) for named groups that do not exist
    #
    # as such, we need to check if the retrieved groups are blank or
    # not, for optional/alternative parts of a rule

    groups = match.groupdict()


    src_port = ""

    if groups["src_port_listop"]:
        # if 'eq' or 'neq' was found for the source port, it will be one
        # or more services, separated by spaces - we need to split the
        # list up and turn each one into a port number, then join the
        # list back together again

        src_port = (
            " %s %s" % (
                groups["src_port_listop"],
                " ".join([str(_service_to_port(s))
                              for s
                              in groups["src_port_list"].split(" ")])))

    elif groups["src_port_1op"]:
        src_port = " %s %d" % (
                       groups["src_port_1op"],
                       _service_to_port(groups["src_port_num"]))

    elif groups["src_port_low"]:
        src_port = " range %d %d" % (
                        _service_to_port(groups["src_port_low"]),
                        _service_to_port(groups["src_port_high"]))


    dst_port = ""

    if groups["dst_port_listop"]:
        dst_port = (
            " %s %s" % (
                groups["dst_port_listop"],
                " ".join([str(_service_to_port(s))
                              for s
                              in groups["dst_port_list"].split(" ")])))

    elif groups["dst_port_1op"]:
        dst_port = " %s %d" % (
                        groups["dst_port_1op"],
                        _service_to_port(groups["dst_port_num"]))

    elif groups["dst_port_low"]:
        dst_port = " range %d %d" % (
                        _service_to_port(groups["dst_port_low"]),
                        _service_to_port(groups["dst_port_high"]))

    # the destination port could also be an ICMP message type
    elif groups["icmp_type"]:
        dst_port = " " + groups["icmp_type"]


    established = groups["established"] or ""

    qos = groups["qos"] or ""

    log = groups["log"] or ""


    return (action + " " + protocol
            + " " + src_addr + src_port
            + " " + dst_addr + dst_port + established + qos + log)



# IPV6 EXTENDED ACCESS CONTROL LIST RULES



# regular expression for matching an IPv6 access-list rule, compiled
# once for efficiency
#
# TODO: we know this doesn't match some of the more complicated rules
# (such as the CP policing ones matching ICMPv6 types) but we're
# excluding those in the output, anyway, so we just ignore them - as
# such, we don't match the end of string ('$')

_ACL6_RULE_RE = re.compile(
    r"^"
    r"(?P<action>permit|deny)"
    r"( "
        r"(?P<protocol>ipv6|icmp|tcp|udp|\d+)"
    r")?"
    r" "
    r"(?P<src_addr>any|host [0-9A-Fa-f:]+|[0-9A-Fa-f:]+/\d+)"
    r"( ("
        r"((?P<src_port_1op>eq|lt|gt|neq) (?P<src_port_num>\S+))|"
        r"range (?P<src_port_low>\S+) (?P<src_port_high>\S+)"
    r"))?"
    r" "
    r"(?P<dst_addr>any|host [0-9A-Fa-f:]+|[0-9A-Fa-f:]+/\d+)"
    r"( ("
        r"((?P<dst_port_1op>eq|lt|gt|neq) (?P<dst_port_num>\S+))|"
        r"range (?P<dst_port_low>\S+) (?P<dst_port_high>\S+)|"
        r"(?P<icmp_type>echo(-reply)?)"
    r"))?"
    r"(?P<established> established)?"
    r"(?P<log> (log|log-input))?"
)


def _acl6_rule_parse(rule):
    """Parse an IPv6 ACL rule, returning a 'normalised' form of the rule
    as a string.  The normalised form should allow two ACL rules which
    mean the same thing to be compared using a simple string comparison.

    This process mainly involves extracting the port entries and
    [potentially] translating them into port numbers, if they're named
    services (which can be used in rules, plus IOS will translate a
    numbered service to a name, if one matches).

    Note that no attempt is made to check the rule for validity.
    """


    match = _ACL6_RULE_RE.match(rule)

    if not match:
        raise ValueError("failed to parse IPv6 ACL rule: " + rule)


    action, protocol, src_addr, dst_addr = match.group(
        "action", "protocol", "src_addr", "dst_addr")


    # if the protocol was not specified, we default to 'ipv6'

    if protocol is None:
        protocol = "ipv6"


    # lower case the source and destination addresses since IPv6
    # addresses can either be in upper or lower case (usually upper, in
    # IOS); we choose lower here, though, to avoid upper-casing the
    # keywords 'host' and 'any'

    src_addr = src_addr.lower()
    dst_addr = dst_addr.lower()


    # match.group() will return an error if a named group does not exist
    # in the regexp; match.groupdict(), however, will return a default
    # value (None, if not specified) for named groups that do not exist
    #
    # as such, we need to check if the retrieved groups are blank or
    # not, for optional/alternative parts of a rule

    groups = match.groupdict()


    src_port = ""

    if groups["src_port_num"]:
        src_port = " %s %d" % (
                       groups["src_port_1op"],
                       _service_to_port(groups["src_port_num"]))

    elif groups["src_port_low"]:
        src_port = " range %d %d" % (
                       _service_to_port(groups["src_port_low"]),
                       _service_to_port(groups["src_port_high"]))


    dst_port = ""

    if groups["dst_port_num"]:
        dst_port = " %s %d" % (
                       groups["dst_port_1op"],
                       _service_to_port(groups["dst_port_num"]))

    elif groups["dst_port_low"]:
        dst_port = " range %d %d" % (
                       _service_to_port(groups["dst_port_low"]),
                       _service_to_port(groups["dst_port_high"]))


    elif groups["icmp_type"]:
        dst_port = " " + groups["icmp_type"]


    established = groups["established"] or ""

    log = groups["log"] or ""


    return (action + " " + protocol
            + " " + src_addr + src_port
            + " " + dst_addr + dst_port + established)



# --- configuration command classes ---



# _cmds = []
#
# This is a list of classes, one for each IOS configuration mode
# command.  The command classes are defined at the global level and
# added to this list.
#
# The CiscoIOSConfig class adds these to the object upon instantiation,
# by the _add_commands() method.
#
# This was done to make it clearer how the commands are implemented.

_cmds = []



# _Cmd is created to be a shorthand for the IndentedContextualCommand
# class as we'll be using it a lot

_Cmd = IndentedContextualCommand



# SYSTEM



class _Cmd_Comment(_Cmd):
    cmd = r"!.*"

_cmds.append(_Cmd_Comment)


class _Cmd_Hostname(_Cmd):
    cmd = r"hostname (?P<hostname>\S+)"

    def action(self, groups, cfg, params):
        cfg["hostname"] = groups["hostname"]

_cmds.append(_Cmd_Hostname)



# INTERFACE ...



class _Cmd_Int(_Cmd):
    cmd = r"interface (?P<name>\S+)"
    enter_context = "interface"

    def action(self, groups, cfg, params):
        name = groups["name"]

        # we need to canonicalise the type of an interface as they can
        # be specified in various shorthand forms, and in mixed case
        #
        # the canonical form is '<type><number>'; the type is first
        # character capitalised
        #
        # TODO: we really should handle this more flexibly, with a
        # central funcation matching regexps of the interface name
        match = re.match(r"^([-a-z]+)([0-9/.]*)$", name.lower())
        if match:
            _type, num = match.groups()
            _type = _INTERFACE_CANONICALS.get(_type, _type).capitalize()
            name = _type + num

        return deepsetdefault(cfg, "interface", name)

_cmds.append(_Cmd_Int)


class _CmdContext_Int(_Cmd):
    context = "interface"


class _Cmd_Int_CDPEna(_CmdContext_Int):
    cmd = r"(?P<no>no )?cdp enable"

    def action(self, groups, cfg, params):
        # we allow CDP to be 'no cdp enable' to clear the CDP status
        cfg["cdp-enable"] = not groups["no"]

_cmds.append(_Cmd_Int_CDPEna)


class _Cmd_Int_ChnGrp(_CmdContext_Int):
    cmd = r"channel-group (?P<id>\d+)(?P<mode> .+)?"

    def action(self, groups, cfg, params):
        cfg["channel-group"] = int(groups["id"]), groups["mode"]

_cmds.append(_Cmd_Int_ChnGrp)


class _Cmd_Int_Desc(_CmdContext_Int):
    cmd = r"description (?P<description>.+)"

    def action(self, groups, cfg, params):
        cfg["description"] = groups["description"]

_cmds.append(_Cmd_Int_Desc)


class _Cmd_Int_Encap(_CmdContext_Int):
    cmd = r"encapsulation (?P<encap>dot1q \d+( native)?)"

    def action(self, groups, cfg, params):
        # lower case the encapsulation definition as IOS stores 'dot1q'
        # as 'dot1Q'
        cfg["encap"] = groups["encap"].lower()

_cmds.append(_Cmd_Int_Encap)


class _Cmd_Int_HlprAddr(_CmdContext_Int):
    cmd = r"ip helper-address (?P<helper_addr>(global )?\S+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("ip-helper-addr", set()).add(groups["helper_addr"])

_cmds.append(_Cmd_Int_HlprAddr)


class _Cmd_Int_IPAccGrp(_CmdContext_Int):
    cmd = r"ip access-group (?P<access_group>\S+) (?P<direction>in|out)"

    def action(self, groups, cfg, params):
        cfg.setdefault("ip-access-group", {})[groups["direction"]] = (
            groups["access_group"])

_cmds.append(_Cmd_Int_IPAccGrp)


class _Cmd_Int_IPAddr(_CmdContext_Int):
    cmd = r"ip address (?P<addr>\S+ \S+)"

    def action(self, groups, cfg, params):
        cfg["ip-addr"] = groups["addr"]

_cmds.append(_Cmd_Int_IPAddr)


class _Cmd_Int_IPAddrSec(_CmdContext_Int):
    cmd = r"ip address (?P<addr>\S+ \S+) secondary"

    def action(self, groups, cfg, params):
        # secondary address - record it in a list
        cfg.setdefault("ip-addr-sec", set()).add(groups["addr"])

_cmds.append(_Cmd_Int_IPAddrSec)


class _Cmd_Int_IP6Addr(_CmdContext_Int):
    cmd = r"ipv6 address (?P<addr>\S+)"

    def action(self, groups, cfg, params):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-addr", set()).add(groups["addr"].lower())

_cmds.append(_Cmd_Int_IP6Addr)


class _Cmd_Int_ServPol(_CmdContext_Int):
    cmd = r"service-policy (?P<policy>.+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("service-policy", set()).add(groups["policy"])

_cmds.append(_Cmd_Int_ServPol)


class _Cmd_Int_Shutdown(_CmdContext_Int):
    cmd = r"(?P<no>no )?shutdown"

    def action(self, groups, cfg, params):
        if groups["no"]:
            # we allow interfaces to be 'no shutdown' so have to clear
            # the shutdown option
            cfg.pop("shutdown", None)
        else:
            cfg["shutdown"] = None

_cmds.append(_Cmd_Int_Shutdown)


class _Cmd_Int_StandbyIP(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) ip (?P<addr>\S+)"

    def action(self, groups, cfg, params):
        deepsetdefault(
            cfg, "standby", int(groups["grp"]))["ip"] = groups["addr"]

_cmds.append(_Cmd_Int_StandbyIP)


class _Cmd_Int_StandbyIPSec(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) ip (?P<addr>\S+) secondary"

    def action(self, groups, cfg, params):
        deepsetdefault(
            cfg, "standby", int(groups["grp"]), "ip-sec", last=set()).add(
                groups["addr"])

_cmds.append(_Cmd_Int_StandbyIPSec)


class _Cmd_Int_SwPortTrkNtv(_CmdContext_Int):
    cmd = r"switchport trunk native vlan (?P<vlan>\d+)"

    def action(self, groups, cfg, params):
        cfg["swport-trunk-native"] = int(groups["vlan"])

_cmds.append(_Cmd_Int_SwPortTrkNtv)


class _Cmd_Int_SwPortTrkAlw(_CmdContext_Int):
    cmd = r"switchport trunk allowed vlan (add )?(?P<vlans>[0-9,-]+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("swport-trunk-allow", set()).update(
            _expand_set(groups["vlans"]))

_cmds.append(_Cmd_Int_SwPortTrkAlw)


class _Cmd_Int_VRF(_CmdContext_Int):
    cmd = (r"vrf forwarding (?P<vrf>\S+)")

    def action(self, groups, cfg, params):
        cfg["vrf-forwarding"] = groups["vrf"]

_cmds.append(_Cmd_Int_VRF)


class _Cmd_Int_XConn(_CmdContext_Int):
    cmd = r"xconnect (?P<remote>[0-9.]+ \d+ .+)"

    def action(self, groups, cfg, params):
        cfg["xconnect"] = groups["remote"]

_cmds.append(_Cmd_Int_XConn)



# IP ACCESS-LIST STANDARD



class _Cmd_ACLStdRule(_Cmd):
    cmd = r"access-list (?P<num>\d{1,2}|1[3-9]\d{2}) (?P<rule>.+)"

    def action(self, groups, cfg, params):
        deepsetdefault(cfg, "ip-acl-std", groups["num"], last=[]).append(
            groups["rule"])

_cmds.append(_Cmd_ACLStdRule)


class _Cmd_IPACL_Std(_Cmd):
    cmd = r"ip access-list standard (?P<name>.+)"
    enter_context = "ip-acl-std"

    def action(self, groups, cfg, params):
        return deepsetdefault(cfg, "ip-acl-std", groups["name"], last=[])

_cmds.append(_Cmd_IPACL_Std)


class _Cmd_IPACL_Std_Rule(_Cmd):
    context = "ip-acl-std"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def action(self, groups, cfg, params):
        cfg.append(groups["rule"])

_cmds.append(_Cmd_IPACL_Std_Rule)


class _Cmd_ACLExtRule(_Cmd):
    cmd = r"access-list (?P<num>1\d{2}|2[0-6]\d{2}) (?P<rule>.+)"

    def action(self, groups, cfg, params):
        deepsetdefault(cfg, "ip-acl-ext", groups["num"], last=[]).append(
            _ipacl_ext_rule_parse(groups["rule"]))

_cmds.append(_Cmd_ACLExtRule)


class _Cmd_IPACL_Ext(_Cmd):
    cmd = r"ip access-list extended (?P<name>.+)"
    enter_context = "ip-acl-ext"

    def action(self, groups, cfg, params):
        name = groups["name"]
        return deepsetdefault(cfg, "ip-acl-ext", name, last=[])

_cmds.append(_Cmd_IPACL_Ext)


class _Cmd_IPACL_Ext_Rule(_Cmd):
    context = "ip-acl-ext"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def action(self, groups, cfg, params):
        cfg.append(_ipacl_ext_rule_parse(groups["rule"]))

_cmds.append(_Cmd_IPACL_Ext_Rule)



# IPV6 ACCESS-LIST ...



class _Cmd_IP6ACL(_Cmd):
    cmd = r"ipv6 access-list (?P<name>.+)"
    enter_context = "ipv6-acl"

    def action(self, groups, cfg, params):
        name = groups["name"]
        return deepsetdefault(cfg, "ipv6-acl", name, last=[])

_cmds.append(_Cmd_IP6ACL)


class _Cmd_IP6ACL_Rule(_Cmd):
    context = "ipv6-acl"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def action(self, groups, cfg, params):
        cfg.append(_acl6_rule_parse(groups["rule"]))

_cmds.append(_Cmd_IP6ACL_Rule)



# IP[V6] PREFIX-LIST ...



class _Cmd_IPPfx(_Cmd):
    cmd = r"ip prefix-list (?P<list>\S+) (seq \d+ )?(?P<rule>.+)"

    def action(self, groups, cfg, params):
        list_ = groups["list"]

        deepsetdefault(cfg, "ip-pfx", list_, last=[]).append(groups["rule"])

_cmds.append(_Cmd_IPPfx)


class _Cmd_IP6Pfx(_Cmd):
    cmd = r"ipv6 prefix-list (?P<list>\S+) (seq \d+ )?(?P<rule>.+)"

    def action(self, groups, cfg, params):
        list_ = groups["list"]

        deepsetdefault(cfg, "ipv6-pfx", list_, last=[]).append(
            groups["rule"].lower())

_cmds.append(_Cmd_IP6Pfx)



# IP[V6] ROUTE ...



class _Cmd_IPRoute(_Cmd):
    cmd = r"ip route (?P<route>.+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("ip-route", set()).add(groups["route"])

_cmds.append(_Cmd_IPRoute)


class _Cmd_IP6Route(_Cmd):
    cmd = r"ipv6 route (?P<route>.+)"

    def action(self, groups, cfg, params):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-route", set()).add(groups["route"].lower())

_cmds.append(_Cmd_IP6Route)



# [NO] SPANNING-TREE ...



class _Cmd_NoSTP(_Cmd):
    cmd = r"no spanning-tree vlan (?P<tags>[-0-9,]+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("no-stp", set()).update(_expand_set(groups["tags"]))

_cmds.append(_Cmd_NoSTP)


class _Cmd_STPPriority(_Cmd):
    cmd = r"spanning-tree vlan (?P<tags>[-0-9,]+) priority (?P<priority>\d+)"

    def action(self, groups, cfg, params):
        priority = groups["priority"]

        cfg_stp_pri = cfg.setdefault("stp-priority", {})
        for tag in _expand_set(groups["tags"]):
            cfg_stp_pri[int(tag)] = int(priority)

_cmds.append(_Cmd_STPPriority)



# VLAN ...



class _Cmd_VLAN(_Cmd):
    cmd = r"vlan (?P<tag>\d+)"
    enter_context = "vlan"

    def action(self, groups, cfg, params):
        tag = int(groups["tag"])

        # create the VLAN configuration entry, setting an 'exists' key
        # as we might stop other information in here that isn't in the
        # VLAN definition itself in IOS (e.g. STP priority) in future
        cfg_vlan = deepsetdefault(cfg, "vlan", tag)
        cfg_vlan["exists"] = None

        return cfg_vlan

_cmds.append(_Cmd_VLAN)


class _CmdContext_VLAN(_Cmd):
    context = "vlan"

class _Cmd_VLAN_Name(_CmdContext_VLAN):
    cmd = r"name (?P<name>\S+)"

    def action(self, groups, cfg, params):
        cfg["name"] = groups["name"]

_cmds.append(_Cmd_VLAN_Name)



# --- classes ----



class CiscoIOSConfig(IndentedContextualConfig):
    "This concrete class parses Cisco IOS configuration files."


    def _add_commands(self):
        """This method is called by the constructor to add commands for
        the IOS platform.

        The commands are stored in a global (to the module) level list
        of classes.
        """

        for cmd_class in _cmds:
            self._add_command(cmd_class)


    def _post_parse_file(self):
        """Extend the inherited method to flush any pending IPv4
        standard ACL rules into the configuration.
        """

        super()._post_parse_file()

        # go through the pending IPv4 standard ACLs and store them (we
        # convert this to a list as _acl4_std_flush() will change the
        # dictionary during iteration and we only need the names)
        if "ip-acl-std" in self:
            ip_acl_std = self["ip-acl-std"]
            for name in ip_acl_std:
                ip_acl_std[name] = _ipacl_std_canonicalize(ip_acl_std[name])
