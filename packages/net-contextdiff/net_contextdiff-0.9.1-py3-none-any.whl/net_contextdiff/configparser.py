# configparser.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Contextual configuration module.

This module contains an abstract class to parse and represent
configuration files that use indented blocks to indicate the context of
commands.
"""



# --- imports ---



import re
import sys



# --- classes ---



class IndentedContextualCommand:
    """This is an abstract class that represents a command from a
    configuration file using indented contexts.

    It includes the context in which it occurs (the indented block), a
    regular expression to match it (which will include groups to extract
    parameters from), if it enters a subcontext and an action method to
    run, if there is a match (which might store configuration
    information).

    Actual commands will inherit from this and override or implement
    some of the constants:

    context -- the context (indented section name) in which the command
    applies; the default is '.', which represents the top level (no
    indent, i.e. no subcontext)

    cmd -- an uncompiled regular expression string which fully matches
    (with re.fullmatch()) the command, case insensitively

    enter_context -- if not Null, it will be a string specifying the
    subcontext to enter, if the command matches

    In addtion, the action() method is likely to need to be implemented.
    """


    context = "."
    cmd = None
    enter_context = None


    def __init__(self):
        """The constructor simply compiles the string-based regular
        expression and stores it once, for performance.
        """

        self._cmd_re = re.compile(r"^" + self.cmd + r"$", re.IGNORECASE)


    def action(self, groups, cfg, params):
        """The action() method will be called when the command is
        matched.  It will typically be used to update the configuration
        dictionary.

        The default is not to do anything - child classes will likely
        need to implement this.

        The configuration dictionary supplied to this function is not
        necessarily the entire configuration for the device but what is
        returned by the action() method of the parent context.  This
        allows a parent context to pass on just the configuration
        dictionary for a portion of the device, such as an individual
        interface.  This makes it easier to update the correct portion
        of the configuration, without having to index through the entire
        structure.

        In addition, a dictionary of 'parameters' are supplied to the
        action() method.  This is cumulative over the parent contexts
        and can be used to record things like the interface name
        entered.  This may not be required, if the configuration
        dictionary for that element is sufficient, but is useful where
        the subcontext need to know something about a command in a
        parent context.  When subcontexts are exited, the parameters for
        the parent context are restored.

        Keyword arguments:

        groups -- the re.Match.groupdict() returned after matching the
        command regular expression

        cfg -- the dictionary for this part of the configuration, or the
        the full configuration, as returned by the parent context's
        action() method

        params -- the stored parameters for this context

        The return value is the dictionary to use as the 'cfg' argument
        of any subcontext action() calls, or None if the same
        configuration dictionary as the parent context is to be used.
        """

        pass


    def match(self, line):
        """This method returns if this command matches the supplied
        command line.  The regular expression must be matched
        in its entirity (it uses re.fullmatch()) and does not include
        any leading indenting due to the context.
        """

        return self._cmd_re.fullmatch(line)



class IndentedContextualConfig(dict):
    """The abstract base class for an indent-based contextual
    configuration.

    Indent-based configurations use levels of indenting to indicate
    context - e.g.:

      interface X
       description Y
       shutdown

    This shows that the 'description' and 'shutdown' commands apply to
    the interface named in the previous line.

    The parser in this class makes use of this property to match only
    the commands which are applicable in this context the configuration
    is in.  When the indenting level decreases, the contexts are exited
    and commands for the appropriate parent context will be matched.

    Child classes implement the platform-specific commands (e.g. one to
    handle Cisco IOS configuration files).
    """


    def __init__(self, filename=None, debug=False):
        """Initialise the object by calling _add_commands() to add the
        commands for this configuration platform.

        If a filename (and optional debug argument) are supplied, the
        parse_file() method is called with these.
        """


        # _parser = {}
        #
        # command parsing is handled through a dictionary indexed by
        # the name of the context and then having a list of Indented-
        # ContextualCommand objects for that context, to be processed in
        # turn
        #
        # the command dictionary is initialised with a single context
        # of '.' (the top level context) containing no commands - new
        # contexts will be created, as required, but we need to start
        # with this as the matching function assumes it exists

        self._parser = {
            ".": []
        }


        # add the commands for this particular instance

        self._add_commands()


        if filename:
            self.parse_file(filename, debug)


    def _add_commands(self):
        """This method should be implemented by child classes to add
        commands to the parser.

        In the abstract class, it does nothing.
        """

        pass


    def _add_command(self, cmd_class):
        """This method adds a single IndentedContextualCommand class to
        the parser, given the class: an object of that class will be
        instantiated and added to the appropriate context in the
        command dictionary.
        """

        # if the context doesn't exist yet, create it with an empty list
        # of commands
        self._parser.setdefault(cmd_class.context, [])

        # instantiate the command object and append it to this context's
        # command list
        self._parser[cmd_class.context].append(cmd_class())


    def parse_file(self, filename, debug=False):
        """Parse a device configuration file and stores it in the
        object.  If there is any configuration already in the object,
        it will be added to it.

        Keyword arguments:

        filename -- name of the file to read

        debug -- if set to True, explain the parsing process, showing
        the contexts and matching commands
        """


        file = open(filename, "r")


        # the context stack stores the contexts for each level of
        # indentation in the file so far: as contexts are entered, they
        # are pushed onto it and, as they are left, they are popped off
        #
        # the top of the stack represents the current context
        #
        # each level is a dictionary with the following keys:
        #
        # * indent - the number of leading spaces for the command which
        #   started this context (so commands within it will have more
        #   than this number of spaces)
        #
        # * name - the name of the context (as matched in Indented-
        #   ContextualCommand)
        #
        # * config - the configuration for the current context
        #
        # * params - the parameters accumulated as subcontexts are
        #   entered (and passed to the IndentedContextualCommand
        #   object's action() method)
        #
        # the list is initialised with the top level context (no indent)

        contexts = [{
            # the top level has a negative indent so all commands are
            # within in
            "indent": -1,

            # the top level has the special name '.'
            "name": ".",

            # the configuration starts by being the entire dictionary
            "config": self,

            # the parameter list starts out empty
            "params": {}
        }]


        for line in file:
            # skip blank lines (or lines consisting solely of spaces)

            if not line.lstrip():
                continue


            # remove the trailing newline (but not any trailing spaces,
            # in case they're important)

            line = line.rstrip("\n")


            if debug:
                print("\n" + line, file=sys.stderr)


            # strip the leading spaces from the line and calculate the
            # indent level based on this

            line_strip = line.lstrip(" ")
            line_indent = len(line) - len(line_strip)


            # keep popping contexts until the level of indent of the
            # line is greater than the top context on the stack (in
            # which case, we've found the context this command is in)

            while contexts[-1]["indent"] >= line_indent:
                contexts.pop()


            # get the current context (we need this a lot, so it makes
            # the code clearer to do it here)

            context = contexts[-1]


            # start building a dictionary for the new context with
            # default values - we may replace some of these, if we find
            # a matching command

            new_context = {
                # the indent level of this context is that of this line
                "indent": line_indent,

                # the new context doesn't yet have name (and may not
                # have one, if we can't find one)
                "name": None,

                # keep the same configuration element
                "config": context["config"]
            }


            if debug:
                print(">> context:", context["name"] or "(none)",
                      file=sys.stderr)


            # skip to the next line, if the current context if it has no
            # name specified (so there can't be any commands)
            #
            # note that we only switch to a context if there are any
            # commands registered in it, so we don't need to check for
            # that here: only that the context is not None

            if not context["name"]:
                continue


            # go through the commands in this context, seeing if the
            # line matches one of them

            for command in self._parser[context["name"]]:
                match = command.match(line_strip)

                if match:
                    if debug:
                        print("=> matches /^" + str(command.cmd) + "$/",
                                file=sys.stderr)


                    # get the parameters for the current context and
                    # [shallow] copy them, so we can add additional
                    # ones, if required

                    context_params = context["params"].copy()


                    # call the action() method for this command

                    new_config = command.action(
                        match.groupdict(), context["config"], context_params)


                    # if this command specifies a new [sub] context is
                    # to be entered, change to that

                    if command.enter_context:
                        # if there are no commands registered for the
                        # new context, we can't enter it, so don't
                        # bother completing the new context information
                        #
                        # (the main loop assumes that the context
                        # exists, so this avoids that check by leaving
                        # the name None, from the default)

                        if command.enter_context not in self._parser:
                            if debug:
                                print("!> new context:",
                                        command.enter_context,
                                        "unknown - ignoring",
                                        file=sys.stderr)

                            break


                        if debug:
                            print("*> entering context:",
                                  command.enter_context,
                                  file=sys.stderr)


                        new_context["name"] = command.enter_context


                        # use a more-specific configuration element
                        # dictionary, if one was returned by the
                        # action() method

                        if new_config is not None:
                            new_context["config"] = new_config


                        new_context["params"] = context_params


                    # since we've found a matching command, don't bother
                    # looking for any more

                    break

                else:
                    if debug:
                        print("-> no match /^" + str(command.cmd) + "$/",
                                file=sys.stderr)


            else:
                if debug:
                    print("=> no matches", file=sys.stderr)


            # store the new context on the stack

            contexts.append(new_context)


        file.close()


        # perform any post-parsing processing

        self._post_parse_file()


    def _post_parse_file(self):
        """This method is called after parsing a file into the
        configuration dictionary with parse_file() (or as part of the
        constructor).

        In this abstract class, it does nothing, but can be overridden
        in child classes to perform any necessary processing.
        """

        pass
