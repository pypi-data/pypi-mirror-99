# contextdiff.__main__


# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>
#
# This script compares Cisco IOS configuration files and outputs a
# configuration file which will convert the former into the latter.



import net_contextdiff

import argparse
import re
import sys

import yaml

from net_contextdiff.iosparser import CiscoIOSConfig
from net_contextdiff.iosdiff import CiscoIOSDiffConfig



# --- constants ---



# PLATFORMS = dict
#
# This dictionary specifies the available platforms available to compare
# configurations in.  The dictionary is keyed on the user-specified platform
# name and specifies two values in a tuple, giving the object classes to be
# used for that platform: the first is the parser an the second is the
# difference comparator.

PLATFORMS = {
    "ios": (CiscoIOSConfig, CiscoIOSDiffConfig)
}



# --- command line arguments ---



# create the parser and add in the available command line options

parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a module
    # directory will use '__main__' by default - this name isn't necessarily
    # correct, but it looks better than that
    prog="net-contextdiff",

    # we want the epilog help output to be printed as it and not reformatted or
    # line wrapped
    formatter_class=argparse.RawDescriptionHelpFormatter,

    epilog="""\
Exclude items are added using the -x and -y options: they consist of paths
through the configuration structure with levels separated by colons.  For
example, excluding "interface:Vlan100" will avoid changes to the VLAN 100
interface.

The -e option is useful to add comments to conversions to indicate what path
matched a particular conversion, so excludes can be constructed.

Note that exclude items are case-sensitive and must be matched exactly.
""")


parser.add_argument(
    "-x", "--exclude",
    metavar="PATH",
    dest="exclude_items",
    nargs="+",
    help="add exclude item for parts of the configuration which will "
         "be omitted from the comparison (these will be added to those "
         "read from a file with the -y option, if both are used)")

parser.add_argument(
    "-y", "--exclude-filename",
    metavar="FILENAME",
    dest="exclude_filename",
    help="read exclude items from file")

parser.add_argument(
    "-e", "--explain",
    action="store_true",
    help="explain which converter paths match a configuration change")

parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="when generating configuration for multiple devices, don't "
         "print the name of each device, as it's generated")

parser.add_argument(
    "-O", "--no-output",
    action="store_true",
    help="")

parser.add_argument(
    "-X", "--debug-excludes",
    action="store_true",
    help="dump the tree of items to be excluded from the comparions")

parser.add_argument(
    "-P", "--debug-parser",
    action="store_true",
    help="enable debugging of contextual parsing; assumed by default "
         "if only a 'from' file is specified")

parser.add_argument(
    "-C", "--debug-config",
    action="store_true",
    help="dump the configuration dictionary after parsing")

parser.add_argument(
    "-D", "--debug-diff",
    action="store_true",
    help="dump the difference (removes and updates) between the from "
         "and to configurations")

parser.add_argument(
    "-V", "--debug-convert",
    action="count",
    default=0,
    help="enable debugging of the difference converstion action "
         "processing (multiple levels increase verbosity up to a "
         "maximum of 2)")

parser.add_argument(
    "platform",
    choices=PLATFORMS,
    help="platform used for configuration files")

parser.add_argument(
    "from_filename",
    metavar="from",
    help="initial ('from') configuration file; '%%' can be used to "
         "substitute in the name of the device into the filename")

parser.add_argument(
    "to_filename",
    nargs="?",
    default=None,
    metavar="to",
    help="destination ('to') configuration file; '%%' can be used to "
         "substitute in the name of the device into the filename; if "
         "omitted just parse the file and assume 'debug' mode")

parser.add_argument(
    "output_filename",
    nargs="?",
    metavar="output",
    help="write differences configuration to named file instead of "
         "stdout; '%%' can be used to substitute in the name of the "
         "device into the filename")

parser.add_argument(
    "devicenames",
    metavar="devicename",
    nargs="*",
    help="name(s) of the device(s) to calculate differences in the "
         "configuration for")

parser.add_argument(
    "--version",
    action="version",
    version=("%(prog)s " + net_contextdiff.__version__))


# parse the supplied command line against these options, storing the results

args = parser.parse_args()

config_parser_class, config_diff_class = PLATFORMS[args.platform]

exclude_items = args.exclude_items
exclude_filename = args.exclude_filename
explain = args.explain
quiet = args.quiet
no_output = args.no_output
debug_excludes = args.debug_excludes
debug_parser = args.debug_parser
debug_config = args.debug_config
debug_diff = args.debug_diff
debug_convert = args.debug_convert
from_filename = args.from_filename
to_filename = args.to_filename
output_filename = args.output_filename
devicenames = args.devicenames


# check a couple of nonsensical configurations aren't being use related
# to multiple devices

if len(devicenames) == 0:
    if from_filename.find("%") != -1:
        print("warning: no device names specified, so operating on a single "
              "file, yet 'from' filename has '%' character - no substitution "
              "will be performed",
              file=sys.stderr)

    if to_filename and (to_filename.find("%") != -1):
        print("warning: no device names specified, so operating on a single "
              "file, yet 'to' filename has '%' character - no substitution "
              "will be performed",
              file=sys.stderr)

    if output_filename and (output_filename.find("%") != -1):
        print("warning: no device names specified, so operating on a single "
              "file, yet 'output' filename has '%' character - no "
              "substitution will be performed",
              file=sys.stderr)


elif len(devicenames) > 1:
    if from_filename.find("%") == -1:
        print("warning: multiple device names specified but 'from' filename "
              "does not contain '%' - same file will be read",
              file=sys.stderr)

    if to_filename and (to_filename.find("%") == -1):
        print("warning: multiple device names specified but 'to' filename "
              "does not contain '%' - same file will be read",
              file=sys.stderr)


    if not output_filename:
        print("warning: multiple device names specified but outputting to "
              "standard output - all configurations will be concatenated",
              file=sys.stderr)

    elif output_filename.find("%") == -1:
        print("error: multiple device names specified but 'output' filename "
              "does not contain '%' - same file would be overwritten",
              file=sys.stderr)

        exit(1)



# --- setup ---



# create the diff object

diff = config_diff_class(explain, debug_config, debug_diff, debug_convert)


# read the excludes for what to include/exclude in the comparison

if exclude_items:
    # add the exclude items specified directly on the command line (do
    # this before reading those from a file, if specified, below)
    diff.add_excludes(exclude_items)

if exclude_filename:
    diff.read_excludes(exclude_filename)

if debug_excludes:
    print(">> exclude items:", yaml.dump(diff.get_excludes(),
          default_flow_style=False), sep="\n", file=sys.stderr)



# --- compare ---



def diffconfig(from_filename, to_filename, output_filename=None,
               no_output=False):

    """This function compares the 'from' and 'to' configurations for
    the specified device and writes a difference configuration file
    (one that transforms the configuration of a running device from the
    'from' to the 'to' state).

    The filenames for the configuration files, as well as the output
    are taken from the arguments parsed above and stored in global
    variables used directly by this function.

    The function returns True iff the parsing and comparison succeeded.
    Most problems result in the function aborting with an exception,
    but some minor warnings may be ignored and the program continue
    with devices.
    """

    # this function makes use of global variables defined outside it so
    # must appear here in the code


    # read in the 'from' and 'to' configurations

    from_cfg = config_parser_class(from_filename, debug_parser)

    to_cfg = (config_parser_class(to_filename, debug_parser)
                  if to_filename else None)


    # find the differences

    diffs = diff.convert(from_cfg, to_cfg)


    # if output is suppressed, just stop with success here

    if no_output:
        return True


    # write the differences to a file or standard output

    if output_filename:
        if debug_convert:
            print("debug: writing to output file: %s" % output_filename,
                  file=sys.stderr)

        with open(output_filename, "w") as output_file:
            if diffs:
                print(diffs, file=output_file)

    else:
        if debug_convert:
            print("debug: writing to standard output", file=sys.stderr)

        if diffs:
            print(diffs)


    return True



# this flag will change to False if any configuration fails to generate and
# is used to affect the return code from the script

complete_success = True


if devicenames:
    for devicename in devicenames:
        if not quiet:
            print(devicename)

        complete_success = diffconfig(
                               from_filename.replace("%", devicename),
                               to_filename.replace("%", devicename),
                               output_filename.replace("%", devicename))


else:
    complete_success = diffconfig(
        from_filename, to_filename, output_filename, no_output)


exit(0 if complete_success else 1)
