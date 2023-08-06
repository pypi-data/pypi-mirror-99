# iosdiff.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration differences module.

This module compares two configurations for Cisco IOS devices and
produces a delta configuration.
"""



# --- imports ---



import re

from .configdiff import DiffConvert, DiffConfig, pathstr



# --- functions ---



def _print_list(l, prefix="", start=None, step=10):
    """This function 'prints' a list of strings 'l' by adding a prefix
    onto the start of each entry and numbering them.  It's used to
    render IP access-lists and prefix-lists.

    The 'prefix' is a fixed string and defaults to the empty string.
    This is correct for access-lists but could be set to 'ip prefix-list
    NAME' for a prefix-list.  If this contains text, it will most likely
    need to end with a space to separate it from the rest of the string.

    The 'start' and 'step' arguments control the numbering of the
    entries and are added next.  If a start value is not specified, it
    defaults to the step value; the step value defaults to 10.

    A space and the entry value is then added.

    The resulting 'printed' list is then returned to be added to the
    configuration.
    """

    if start is None:
        start = step

    # initialise the result list
    r = []

    n = start
    for i in l:
        r.append(prefix + str(n) + " " + i)
        n += step

    return r



def _isintphysical(i):
    """This function returns if a particular interface is physical or
    not.  The names it matches are those that the are used as the
    canonical ones in the parser.
    """

    return re.match("^(Mgmt|Eth|Fa|Gi|Te|Fo)\d", i)



# --- converter classes ---



# _cvtrs = []
#
# This is a list of converter classes to be added to the
# CiscoIOSConfigDiff object by the _add_converters() method.  Each
# class will be instantiated and added.

_cvtrs = []



# SYSTEM



class _Cvtr_Hostname(DiffConvert):
    path = "hostname",

    def remove(self, cfg, diff, args):
        return "no hostname"

    def update(self, cfg, diff, args):
        return "hostname " + diff

_cvtrs.append(_Cvtr_Hostname)



# INTERFACE ...



class _Cvtr_Int(DiffConvert):
    path = "interface", None

    def remove(self, cfg, diff, args):
        name, = args

        # only remove the interface if it's not physical
        if _isintphysical(name):
            return

        # remove if interface no longer exists, or exists flag has gone
        if (not diff) or ("exists" in diff):
            return "no interface " + name

    def update(self, cfg, diff, args):
        name, = args
        if "exists" in diff:
            return "interface " + name

_cvtrs.append(_Cvtr_Int)


# we put the 'interface / shutdown' at the start to shut it down before
# we do any [re]configuration

class _Cvtr_Int_Shutdown(DiffConvert):
    path = "interface", None, "shutdown"
    name = "shutdown"

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " shutdown"

_cvtrs.append(_Cvtr_Int_Shutdown)


class _Cvtr_Int_CDPEna(DiffConvert):
    path = "interface", None, "cdp-enable"

    def remove(self, cfg, diff, args):
        name, = args
        # if the 'cdp enable' option is not present, that doesn't mean
        # it's disabled but just that it's not specified, so we assume
        # the default is for it to be enabled
        return "interface " + name, " cdp enable"

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " %scdp enable" % ("" if cfg else "no ")

#_cvtrs.append(_Cvtr_Int_CDPEna)


class _Cvtr_Int_ChnGrp(DiffConvert):
    path = "interface", None, "channel-group"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no channel-group"

    def update(self, cfg, diff, args):
        name, = args
        id_, mode = cfg
        return ("interface " + name, " channel-group %d%s"
                    % (id_, mode if mode else ""))

_cvtrs.append(_Cvtr_Int_ChnGrp)


class _Cvtr_Int_Desc(DiffConvert):
    path = "interface", None, "description"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no description"

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " description " + diff

_cvtrs.append(_Cvtr_Int_Desc)


class _Cvtr_Int_Encap(DiffConvert):
    path = "interface", None, "encap"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no encapsulation " + cfg

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " encapsulation " + diff

_cvtrs.append(_Cvtr_Int_Encap)


class _Cvtr_Int_IPAccGrp(DiffConvert):
    path = "interface", None, "ip-access-group"

    def remove(self, cfg, diff, args):
        name, = args
        l = ["interface " + name]
        # if there are differences, just removed the specific group(s);
        # if the whole block is gone, remove all groups there before
        for dir in sorted(diff if diff else cfg):
            l.append(" no ip access-group " + dir)
        return l

    def update(self, cfg, diff, args):
        name, = args
        l = ["interface " + name]
        for dir in sorted(diff):
            l.append(" ip access-group %s %s" % (diff[dir], dir))
        return l

_cvtrs.append(_Cvtr_Int_IPAccGrp)


class _Cvtr_Int_IPAddr(DiffConvert):
    path = "interface", None, "ip-addr"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no ip address"

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " ip address " + diff

_cvtrs.append(_Cvtr_Int_IPAddr)


class _Cvtr_Int_IPAddrSec(DiffConvert):
    path = "interface", None, "ip-addr-sec"

    def remove(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        for addr in sorted(diff if diff else cfg):
            l.append(" no ip address %s secondary" % addr)
        return l

    def update(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        for addr in sorted(diff):
            l.append(" ip address %s secondary" % addr)
        return l

_cvtrs.append(_Cvtr_Int_IPAddrSec)


class _Cvtr_Int_IPHlp(DiffConvert):
    path = "interface", None, "ip-helper-addr"

    def remove(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        if not diff:
            l.append(" no ip helper-address")
        else:
            l.extend([ (" no ip helper-address " + a) for a in diff ])
        return l

    def update(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        l.extend([ (" ip helper-address " + a) for a in diff ])
        return l

_cvtrs.append(_Cvtr_Int_IPHlp)


class _Cvtr_Int_IP6Addr(DiffConvert):
    path = "interface", None, "ipv6-address"

    def remove(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        for addr in sorted(diff if diff else cfg):
            l.append(" no ipv6 address " + addr)
        return l

    def update(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        for addr in sorted(diff):
            l.append(" ipv6 address " + addr)
        return l

_cvtrs.append(_Cvtr_Int_IP6Addr)


class _Cvtr_Int_ServPol(DiffConvert):
    path = "interface", None, "service-policy"

    def remove(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        for policy in sorted(diff if diff else cfg):
            l.append(" no service-policy " + policy)
        return l

    def update(self, cfg, diff, args):
        name, = args
        l = ["interface %s" % name]
        for policy in sorted(diff):
            l.append(" service-policy " + policy)
        return l

_cvtrs.append(_Cvtr_Int_ServPol)


class _Cvtr_Int_StandbyIP(DiffConvert):
    path = "interface", None, "standby", None, "ip"

    def remove(self, cfg, diff, args):
        name, grp = args
        return "interface " + name, " no standby %d ip" % grp

    def update(self, cfg, diff, args):
        name, grp = args
        return "interface " + name, " standby %d ip %s" % (grp, diff)

#_cvtrs.append(_Cvtr_Int_StandbyIP)


class _Cvtr_Int_StandbyIPSec(DiffConvert):
    path = "interface", None, "standby", None, "ip-sec"

    def remove(self, cfg, diff, args):
        name, grp = args
        l = ["interface " + name]
        for addr in sorted(diff if diff else cfg):
            l.append(" no standby %d ip %s secondary" % (grp, addr))
        return l

    def update(self, cfg, diff, args):
        name, grp = args
        l = ["interface " + name]
        for addr in sorted(diff):
            l.append(" standby %d ip %s secondary" % (grp, addr))
        return l

#_cvtrs.append(_Cvtr_Int_StandbyIPSec)


class _Cvtr_Int_SwPortTrkNtv(DiffConvert):
    # we just match the interface as we need to look inside it to see if
    # the interface is part of a channel group
    path = "interface", None
    ext = "swport-trunk-native",

    def remove(self, cfg, diff, args):
        name, = args

        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in cfg:
            return None

        return "interface " + name, " no switchport trunk native vlan"

    def update(self, cfg, diff, args):
        name, = args

        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in cfg:
            return None

        return ("interface " + name,
                " switchport trunk native vlan " + self.get_ext(diff))

_cvtrs.append(_Cvtr_Int_SwPortTrkNtv)


class _Cvtr_Int_SwPortTrkAlw(DiffConvert):
    # we just match the interface as we need to look inside it to see if
    # the interface is part of a channel group
    path = "interface", None
    ext = "swport-trunk-allow",

    def remove(self, cfg, diff, args):
        name, = args

        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in cfg:
            return None

        l = ["interface " + name]
        if not self.get_ext(diff):
            l.append(" switchport trunk allowed vlan none")
        else:
            for tag in sorted(self.get_ext(diff)):
                l.append(" switchport trunk allowed vlan remove %d" % tag)
        return l

    def update(self, cfg, diff, args):
        name, = args

        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in cfg:
            return None

        l = ["interface " + name]
        for tag in sorted(self.get_ext(diff)):
            l.append(" switchport trunk allowed vlan add %d" % tag)
        return l

_cvtrs.append(_Cvtr_Int_SwPortTrkAlw)


class _Cvtr_Int_VRFFwd(DiffConvert):
    path = "interface", None, "vrf-forwarding"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no vrf forwarding"

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " vrf forwarding " + diff
        # TODO: need to find some way to trigger reapplication of IP
        # information (address, HSRP, etc.)

_cvtrs.append(_Cvtr_Int_VRFFwd)


class _Cvtr_Int_XConn(DiffConvert):
    path = "interface", None, "xconnect"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no xconnect"

    def update(self, cfg, diff, args):
        name, = args
        return "interface " + name, " xconnect " + diff

_cvtrs.append(_Cvtr_Int_XConn)


# we put the 'interface / no shutdown' at the end to only enable the
# interface once it's been correctly [re]configured

class _Cvtr_Int_NoShutdown(DiffConvert):
    path = "interface", None, "shutdown"
    name = "no-shutdown"

    def remove(self, cfg, diff, args):
        name, = args
        return "interface " + name, " no shutdown"

_cvtrs.append(_Cvtr_Int_NoShutdown)



# IP[V6] ACCESS-LIST ...



class _Cvtr_IPACL_Std(DiffConvert):
    path = "ip-acl-std", None

    def remove(self, cfg, diff, args):
        name, = args
        return (["no ip access-list standard " + name]
                + _print_list(cfg, "!- "))

    def update(self, cfg, diff, args):
        name, = args
        return ["ip access-list standard " + name] + _print_list(cfg, " ")

_cvtrs.append(_Cvtr_IPACL_Std)


class _Cvtr_IPACL_Ext(DiffConvert):
    path = "ip-acl-ext", None

    def remove(self, cfg, diff, args):
        # include the old list commented out, for comparison
        name, = args
        return (["no ip access-list extended " + name]
                + _print_list(cfg, "!- "))

    def update(self, cfg, diff, args):
        name, = args
        return ["ip access-list extended " + name] + _print_list(diff, " ")

_cvtrs.append(_Cvtr_IPACL_Ext)


class _Cvtr_IPV6ACL_Ext(DiffConvert):
    path = "ipv6-acl", None

    def remove(self, cfg, diff, args):
        name, = args
        return (["no ipv6 access-list " + name]
                + _print_list(cfg, "!- "))

    def update(self, cfg, diff, args):
        name, = args
        return ["ipv6 access-list " + name] + _print_list(diff, " ")

_cvtrs.append(_Cvtr_IPV6ACL_Ext)



# IP[V6] PREFIX-LIST ...



class _Cvtr_IPPfxList(DiffConvert):
    path = "ip-pfx", None

    def remove(self, cfg, diff, args):
        # include the old list commented out, for comparison
        name, = args
        return (["no ip prefix-list " + name]
                + _print_list(cfg, "!- ", step=5))

    def update(self, cfg, diff, args):
        name, = args
        return _print_list(diff, "ip prefix-list %s seq " % name, step=5)

_cvtrs.append(_Cvtr_IPPfxList)


class _Cvtr_IPV6PfxList(DiffConvert):
    path = "ipv6-pfx", None

    def remove(self, cfg, diff, args):
        # include the old list commented out, for comparison
        name, = args
        return (["no ipv6 prefix-list " + name]
                + _print_list(cfg, "!- ", step=5))

    def update(self, cfg, diff, args):
        name, = args
        return _print_list(diff, "ipv6 prefix-list %s seq " % name, step=5)

_cvtrs.append(_Cvtr_IPV6PfxList)



# IP[V6] ROUTE ...



class _Cvtr_IPRoute(DiffConvert):
    path = "ip-route", None

    def remove(self, cfg, diff, args):
        route, = args
        return "no ip route " + route

    def update(self, cfg, diff, args):
        route, = args
        return "ip route " + route

_cvtrs.append(_Cvtr_IPRoute)


class _Cvtr_IP6Route(DiffConvert):
    path = "ipv6-route", None

    def remove(self, cfg, diff, args):
        route, = args
        return "no ipv6 route " + route

    def update(self, cfg, diff, args):
        route, = args
        return "ipv6 route " + route

_cvtrs.append(_Cvtr_IP6Route)



# [NO] SPANNING-TREE ...



class _Cvtr_NoSTP(DiffConvert):
    path = "no-stp", None

    def remove(self, cfg, diff, args):
        tag, = args
        # removing 'no spanning-tree' enables spanning-tree
        return "spanning-tree vlan " + str(tag)

    def update(self, cfg, diff, args):
        tag, = args
        # adding 'no spanning-tree' disables spanning-tree
        return "no spanning-tree vlan " + str(tag)

_cvtrs.append(_Cvtr_NoSTP)


class _Cvtr_STP_Pri(DiffConvert):
    path = "stp-priority", None

    def remove(self, cfg, diff, args):
        tag, = args
        return "no spanning-tree vlan %d priority" % tag

    def update(self, cfg, diff, args):
        tag, = args
        return "spanning-tree vlan %d priority %d" % (tag, diff)

_cvtrs.append(_Cvtr_STP_Pri)



# VLAN ...



class _Cvtr_Vlan(DiffConvert):
    path = "vlan", None

    def remove(self, cfg, diff, args):
        tag, = args
        return "no vlan %d" % tag

    def update(self, cfg, diff, args):
        tag, = args
        if diff and ("exists" in diff):
            return "vlan %d" % tag

_cvtrs.append(_Cvtr_Vlan)


class _Cvtr_Vlan_Name(DiffConvert):
    path = "vlan", None, "name"

    def remove(self, cfg, diff, args):
        tag, = args
        return "vlan %d" % tag, " no name"

    def update(self, cfg, diff, args):
        tag, = args
        return "vlan %d" % tag, " name " + diff

_cvtrs.append(_Cvtr_Vlan_Name)



# --- context parser ---



class CiscoIOSDiffConfig(DiffConfig):
    """This class is used to compare two IOS configuration files and
    generate a configuration file to transform one into the other.
    """


    def _add_converters(self):
        "This method adds the converters for Cisco IOS."

        for cvt_class in _cvtrs:
            self._add_converter(cvt_class())


    def _explain_comment(self, path):
        """This method overrides the empty inherited one to return a
        Cisco IOS comment giving the matched path.
        """

        return "! => " + pathstr(path)


    def init_excludes(self):
        """This method extends the inherited one to add some default
        excludes for the default CoPP (Control Plane Policing) IPv4
        extended and IPv6 ACLs.
        """

        super().init_excludes()

        self._excludes.update({
            "ip-acl-ext": {
                "acl-copp-match-igmp": {},
                "acl-copp-match-pim-data": {},
            },
            "ipv6-acl": {
                "acl-copp-match-mld": {},
                "acl-copp-match-ndv6": {},
                "acl-copp-match-ndv6hl": {},
                "acl-copp-match-pimv6-data": {},
            },
        })
