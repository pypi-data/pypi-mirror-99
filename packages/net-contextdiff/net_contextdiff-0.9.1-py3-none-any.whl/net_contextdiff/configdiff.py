# configdiff.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from copy import deepcopy
import re
import sys

from deepops import deepremoveitems, deepmerge, deepdiff, deepsetdefault, deepget
import yaml



# --- functions ---



def pathstr(path, wildcard_indices=set()):
    """This function converts a path, which is a list of items of
    various types (typically strings and integers), into a string,
    useful for debugging messages.

    The items are separated by commas and elements which are None are
    converted to a '*' since they're wildcards.

    If the index of the item in the path is in the wildcard_indices
    list, that item is prefixed with "*=" to show it matched a wildcard.
    The default for this parameter is an empty list, which causes no
    index to match.

    If we just printed the list, it would by in the more verbose Python
    format, with surrounding square brackets, quotes around strings and
    None for a wildcard, which is a little less readable.
    """

    return ":".join([ ("*=" if i in wildcard_indices else "") + str(v)
                            for i, v in enumerate(path) ])



# --- classes ---



class DiffConvert:
    """This abstract class handles converting the difference between a
    'from' configuration item to the corresponding 'to' configuration
    item.

    The main difference process will use deepops.deepdiff() to work out
    what has been removed and what updated (added/changed) between the
    two configurations.

    Individual differences are checked using child classes, which
    specify the part of the configuration directionaries where they
    occur and the remove() and update() methods called.  For example, if
    the hostname is changed, a 'hostname' converter would specify the
    part of the configuration dictionary where the hostname is stored
    and the update() method would return the commands required to change
    it to the new value.

    The child classes will override the following values:

    path -- a tuple giving the path of keys through the dictionaries to
    match for these actions; these can be literal keys or the value
    None, if that level of the path is to wildcard match all keys (for
    example, all interfaces); the part of the configuration dictionary
    that matches this path will be passed as the 'cfg' and 'diff'
    parameters to the action functions

    ext -- an extension to path which must be matched, but this part is
    not used to further specify the part of the dictionaries passed to
    the action functions for the 'cfg' and 'diff' parameters: this is
    useful when a higher level in the configuration dictionary is
    required in the action function

    name -- if there is more than one action acting at a particular path
    point, this can be defined to differentiate them: it's useful when
    using the insert_before parameter, but isn't needed if the order
    does not matter (except for ease of debugging, to clarify which
    converter is being called)

    insert_before -- if this rule needs to happen prior to the actions
    of another rule, this 2-tuple gives the (path, name) before the
    earlier rule; None means the order does not matter

    In addition the remove() and update() methods will likely need to be
    implemented.
    """


    path = None
    ext = tuple()
    name = None
    insert_before = None


    def __init__(self):
        """The constructor just precalculates some details to optimise
        the repeated processing of the converter matches.
        """

        # store the full path, including the extension
        self.path_full = self.path + self.ext

        # store the number of elements in the path
        self.path_len = len(self.path)

        # store the set of indices of wildcard elements of the path (we
        # need these to get the argument list to pass to the converter
        # action methods)
        self.wildcard_indices = {
            i for i, v in enumerate(self.path_full) if v is None }


    def pathmatches(self, d):
        """This method takes a dictionary and returns any matches for
        the path in it, as a list of paths; each path is, itself, a
        list of keys.

        If any of the elements of the path are None, this is treated as
        a wildcard and will match all keys at that level.

        If there are no matching entries, the returned list will be
        empty.

        The returned list of matches is not guaranteed to be in any
        particular order.
        """


        def _pathmatches(d, path):
            """This function is used to recursively step along the
            paths.
            """

            # if the path is finished, return a single result with an
            # empty list, as there are no more path elements
            #
            # note that this is different from an empty list (which
            # would mean no matches
            if not path:
                return [ [] ]

            # get the path head and tail to make things easier to read
            path_head, path_tail = path[0], path[1:]

            # if this element is not a type we can iterate or search
            # through (we've perhaps reached a value or a None), or the
            # dictionary is empty, there are no matches, so just return
            # an empty list (which will cause all higher levels in the
            # path that matched to be discarded, giving no resulsts)
            if not isinstance(d, (dict, list, set)) or (not d):
                return []

            # if the path element is None, we're doing a wildcard match
            if path_head is None:
                # initialise an empty list for all returned matching
                # results
                results = []

                # go through all the keys at this level in the dictonary
                for d_key in d:
                    # are there levels below this one?
                    if path_tail:
                        # yes - recursively get the matches from under
                        # this key
                        for matches in _pathmatches(d[d_key], path_tail):
                            # add this match to the list of matches,
                            # prepending this key onto the start of the
                            # path
                            results.append([d_key] + matches)
                    else:
                        # no - just add this result (this is a minor
                        # optimisation, as well as avoiding an error by
                        # trying to index into a non-dict type), above
                        results.append([d_key])

                return results

            # we have a literal key to match - if it's found,
            # recursively get the matches under this level
            if path_head in d:
                return [ ([path_head] + matches)
                             for matches
                             in _pathmatches(d[path_head], path_tail) ]

            # we have no matches, return the empty list
            return []

        # start mathcing with the full path
        return _pathmatches(d, self.path_full)


    def remove(self, cfg, diff, args):
        """The remove() method is called when the specified path is in
        the remove differences (i.e. it's in the 'from' configuration
        but not in the 'to' configuration).

        Keyword arguments:

        cfg -- the value of the dictionary item at the matching path in
        the 'from' configuration dictionary (sometimes, the full details
        of the old configuration may be required to remove it)

        diff -- the value of the dictionary item at the matching path in
        the remove differences dictionary (sometimes, it's necessary to
        know only what is removed from the new configuration)

        args -- [only] the arguments in the path which were matched with
        wildcards; if there were no wildcards, this list will be empty

        The return value is the commands to insert into the
        configuration to convert it.  This can either be a simple
        string, in the case of only one line being required, or an
        iterable containing one string per line.  If the return value is
        None, it is an indication nothing needed to be done.  An empty
        string or iterable indicates the update did something, which did
        not change the configuration (this may have semantic
        differences).
        """

        pass


    def update(self, cfg, diff, args):
        """The update() method is called when the specified path is in
        the update differences (i.e. it's in the 'to' configuration but
        not in the 'from' configuration, or the value differs between
        the two and needed to be changed).

        Keyword arguments:

        cfg -- the value of the dictionary item at the matching path in
        the 'to' configuration dictionary (sometimes, teh full details
        of the new configuration may be required to update it)

        diff -- the value of the dictionary item at the matching path in
        the update differences dictionary

        args -- [only] the arguments in the path which were matched with
        wildcards; if there were no wildcards, this list will be empty

        The return value is the commands to insert into the
        configuration to convert it.  This can either be a simple
        string, in the case of only one line being required, or an
        iterable containing one string per line.  If the return value is
        None, it is an indication nothing needed to be done.  An empty
        string or iterable indicates the update did something, which did
        not change the configuration (this may have semantic
        differences).
        """

        pass


    def get_cfg(self, cfg, match):
        """This method returns the configuration to be passed to the
        converter's action methods [remove() and update()].

        By default, it indexes through the configuration using the path
        in the converter.  Converters may wish to override this, in some
        cases, for performance (perhaps if the entire configuration is
        to be returned).

        If the specified match path is not found, or there was a problem
        indexing along the path, None is returned, rather than an
        exception raised.
        """

        # try to get the specified matching path
        try:
            return deepget(cfg, *match[0 : self.path_len])

        except TypeError:
            # we got a TypeError so make the assumption that we've hit
            # a non-indexable element (such as a set) as the final
            # element of the path, so just return None
            return None


    def get_ext(self, cfg):
        """This method gets the extension part of the path, given a
        configuration dictionary starting at the path (i.e. what is
        passed as 'cfg' and 'diff' in the action methods).

        An action method [remove() or update()] can use this to get the
        extension portion without needing to explicitly index through
        it.
        """

        return deepget(cfg, *self.ext)


    def get_wildcard_args(self, match):
        """This method returns a list of the wildcarded parts of the
        specified match as a list.  For example, if the path of this
        converter is 'interface', None) and the match is ['interface',
        'Vlan100'], the returned result will be ['Vlan100'].  This is
        used to supply the 'args' parameter to action methods.
        """

        return [ match[i] for i in self.wildcard_indices ]



class DiffConfig:
    """This abstract class is used to represent a configuration
    difference processor that can convert a configuration from one to
    another, using a method (which can be called once for each pair of
    configuration files).

    It encapsulates the rules for exluding items from the comparison.
    """


    def __init__(self, init_explain=False, init_debug_config=False,
                       init_debug_diff=False, init_debug_convert=0):

        """The constructor initialises the exclude list to empty and
        adds and converters using _add_converters().  It also stores
        some settings controlling the level of information describing
        the conversion process, based on the command line arguments:

        init_explain=False -- include comments in the output
        configuration changes that explain the differences being matched
        by the DiffConvert objects (if available).

        init_debug_config=False -- dump the 'from' and 'to'
        configurations (after exludes) to stderr

        init_debug_diff=False -- dump the differences (remove and update
        configurations) to stderr

        init_debug_convert=0 -- level of debugging information for the
        conversion process: >= 1: include steps, >= 2: include 'cfg' and
        'diff' parameters
        """

        # store the [initial] settings for the conversion process
        self._explain = init_explain
        self._debug_config = init_debug_config
        self._debug_diff = init_debug_diff
        self._debug_convert = init_debug_convert

        # initialise the dictionary of excludes, which will be passed
        # to deepremoveitems()
        self.init_excludes()

        # initialise the list of converters and add them
        self._cvtrs = []
        self._add_converters()


    def _add_converters(self):
        """This method adds the converters for a particular object to
        the list used by the convert() method, usually by calling
        _add_converter() for each (see that method).

        The base class does nothing but child classes will implement it
        as they require.
        """

        pass


    def _add_converter(self, cvtr):
        """Add an individual convert object, a child of the
        DiffConverter class, to the list of converters to be used by the
        convert() method.

        If the converter has an 'insert_before' entry that is not None,
        the converter will be inserted in the postition immediately
        before the existing entry with that name.  If that entry cannot
        be found, a KeyError will be raised.
        """

        if not cvtr.insert_before:
            # no 'insert_before' - just add it to the end
            self._cvtrs.append(cvtr)

        else:
            # 'insert_before' so we need to find that entry

            # get the indexes and entries in the converter list
            for pos, chk_cvtr in enumerate(self._cvtrs):
                # if this entry is the one we're inserting before, put
                # it here and stop
                if chk_cvtrs.name == cvtrs.insert_before:
                    self._cvtrs.insert(pos, cvtr)
                    break

            else:
                # we got the end of the list and didn't find it, so
                # raise an exception
                raise KeyError("cannot find existing converter with name: "
                               + cvtr.insert_before)


    def _explain_comment(self, path):
        """This method returns a comment or other configuration item
        explaining the path supplied (which will typically be a match
        against a converter).  The path is supplied a list of levels and
        converted to a string using pathstr().

        Child classes can override this to provide a comment appropriate
        for their platform.

        If the function returns None, no comment is inserted.
        """

        return None


    def _changes_begin(self):
        """This method returns a head (beginning) for a generated
        changes configuration file as an iterable of strings.

        In the abstract class, it returns None (which does not add
        anything) but, in child classes it may return a beginning line
        or similar.

        Note that if there are no changes, this will not be included in
        an otherwise empty file.
        """

        return []


    def _changes_end(self):
        """This method returns a tail (ending) for a generated changes
        configuration file as an iterable of strings.

        In the abstract class, it returns None (which does not add
        anything) but, in child classes it may return an 'end' line or
        similar.

        Note that if there are no changes, this will not be included in
        an otherwise empty file.
        """

        return []


    def init_excludes(self):
        """This method initialises the excludes dictionary.  In the base
        class, it the resets it to an empty dictionary, but child
        classes can extend this to add some default exclusions for
        standard system configuration entries which should not be
        changed.

        It is normally only called by the constructor but can be called
        later, to clear the excludes list before adding more (if
        required).
        """

        self._excludes = {}


    def add_exclude(self, path):
        """Add a single exclude item to the dictionary.  The exclude is
        supplied as a string, with the levels in the path of the
        configuration dictionary separated by colons (":"), and then
        added to the excludes dictionary.
        """

        # start at the top of the excludes dictionary
        excludes_sub = self._excludes

        # work through the levels in the exclude item path
        for level in path.split(":"):
            # create this level of the excludes dictionary as a new
            # empty dictionary and move down to it for the next level
            excludes_sub = excludes_sub.setdefault(level, {})


    def add_excludes(self, paths):
        """Add a list of exclude items as strings to the excludes, using
        add_exclude().
        """

        for path in paths:
            self.add_exclude(path)


    def read_excludes(self, filename):
        """Read a list of exclude items from a file and add them to the
        excludes dictionary using add_exclude().

        A hash ('#') and anything following it is stripped out as a
        comment.  Trailing whitespace is also removed.  Blank lines
        (including those created by the above actions) are skipped.
        """

        # work through the lines in the file
        for l in open(filename):
            # strip out anything following a '#' (indicating comment)
            # and any trailing whitespace
            l = re.sub("#.*", "", l)
            l = l.rstrip()

            # if the line is not blank, add it as an exclude item
            if l:
                self.add_exclude(l)


    def read_excludes_yaml(self, filename, path=None):
        """Read a list of exclude items from a YAML file and add them to
        the excludes dictionary.

        The path parameter specifies the key in the dictionary where the
        excludes are specified.  This is useful if the dictionary is
        also contains other data (such as the inventory).  The path is
        specified a list of keys, separated by colons.  If the path is
        None or otherwise False, the top of the dictionary is used.
        """


        # try to read in the YAML excludes file

        try:
            f = yaml.safe_load(open(filename))

        except yaml.parser.ParserError as exception:
            raise ValueError("failed parsing YAML excludes file: %s: %s"
                                 % (filename, exception))


        # if no path was specified, just use the entire file, else get
        # the key given

        if not path:
            deepmerge(self._excludes, f)
        else:
            deepmerge(self._excludes,
                      deepget(f, *path.split(":"), default_error=True))


    def get_excludes(self):
        "This method just returns the excludes dictionary."

        return self._excludes


    def convert(self, from_cfg, to_cfg):
        """This method processes the conversion from the 'from'
        configuration to the 'to' configuration, removing excluded parts
        of each and calling the applicable converters' action methods.

        Note that, if excludes are used, the configurations will be
        modified in place by a deepremoveitems().  They will need to be
        copy.deepcopy()ed before passing them in, if this is
        undesirable.

        The returned value is a single big string of all the
        configuration changes that need to be made.
        """


        # remove any excludes from the 'from' config

        deepremoveitems(from_cfg, self._excludes)

        if self._debug_config:
            print(">> 'from' configuration:",
                yaml.dump(from_cfg, default_flow_style=False), sep="\n",
                file=sys.stderr)


        # if no 'to' config was specified, stop here (we assume we're
        # just testing, parsing and excluding items from the 'from'
        # configuration and stopping

        if not to_cfg:
            return None


        # remove any excludes from the 'to' config

        deepremoveitems(to_cfg, self._excludes)

        if self._debug_config:
            print(">> 'to' configuration:",
                yaml.dump(to_cfg, default_flow_style=False), sep="\n",
                file=sys.stderr)


        # use deepdiff() to work out the differences between the two
        # configuration dictionaries - what must be removed and what
        # needs to be added or updated

        remove_cfg, update_cfg = deepdiff(from_cfg, to_cfg)

        if self._debug_diff:
            print("=> differences - remove:",
                  yaml.dump(remove_cfg, default_flow_style=False),
                  "=> differences - update (add/change):",
                  yaml.dump(update_cfg, default_flow_style=False),
                  sep="\n", file=sys.stderr)


        # initialise the list of changes (the returned configuration
        # conversions)

        changes = []


        # go through the list of converter objects

        for cvtr in self._cvtrs:
            if self._debug_convert:
                print(">> checking difference:",
                      pathstr([ "*" if i is None else i for i in cvtr.path ]),
                      "name:", cvtr.name, file=sys.stderr)


            # get all the remove and update matches for this converter
            # and combine them into one list, discarding any duplicates
            #
            # we do this rather than processing each list one after the
            # other so we combine removes and updates on the same part
            # of the configuration together

            remove_matches = cvtr.pathmatches(remove_cfg)
            update_matches = cvtr.pathmatches(update_cfg)

            all_matches = []
            for match in sorted(remove_matches + update_matches):
                if match not in all_matches:
                    all_matches.append(match)


            # go through all matches

            for match in all_matches:
                # handle REMOVE conversions, if matching

                if match in remove_matches:
                    if self._debug_convert:
                        print("=> remove match:",
                              pathstr(match, cvtr.wildcard_indices),
                              file=sys.stderr)


                    # get elements in the path matching wildcards

                    args = cvtr.get_wildcard_args(match)


                    # get the 'from' and 'remove' parts of the
                    # configuration and remove difference dictionaries,
                    # for the path specified in the converter (ignoring
                    # the extension 'ext')

                    cvtr_cfg = cvtr.get_cfg(from_cfg, match)
                    cvtr_diff = cvtr.get_cfg(remove_cfg, match)

                    if self._debug_convert >= 2:
                        print("-> from configuration:",
                            yaml.dump(
                                cvtr_cfg, default_flow_style=False),
                            "-> remove configuration:",
                            yaml.dump(
                                cvtr_diff, default_flow_style=False),
                            sep="\n", file=sys.stderr)


                    # call the remove converter action method using the
                    # corresponding entry from the 'from' configuration

                    change = cvtr.remove(cvtr_cfg, cvtr_diff, args)


                    # if some changes were returned by the action, add
                    # them

                    if change is not None:
                        # the return can be either a simple string or a
                        # list of strings - if it's a string, make it a
                        # list of one so we can do the rest the same way

                        if isinstance(change, str):
                            change = [change]

                        if self._debug_convert:
                            print("\n".join(change), file=sys.stderr)


                        # add a comment, explaining the match, if
                        # enabled

                        if self._explain:
                            comment = self._explain_comment(match)
                            if comment:
                                changes.append(comment)


                        # store this change on the end of the list of
                        # changes so far

                        changes.extend(change)
                        changes.append("")

                    else:
                        if self._debug_convert:
                            print("-> no action", file=sys.stderr)


                # handle UPDATE conversions, if matching

                if match in update_matches:
                    if self._debug_convert:
                        print("=> update match:",
                              pathstr(match, cvtr.wildcard_indices),
                              file=sys.stderr)


                    args = cvtr.get_wildcard_args(match)


                    # get the 'from' and 'update' parts of the
                    # configuration and update difference dictionaries,
                    # for the path specified in the converter (ignoring
                    # the extension 'ext')

                    cvtr_cfg = cvtr.get_cfg(to_cfg, match)
                    cvtr_diff = cvtr.get_cfg(update_cfg, match)

                    if self._debug_convert >= 2:
                        print("-> to configuration:",
                            yaml.dump(
                                cvtr_cfg, default_flow_style=False),
                            "-> update configuration:",
                            yaml.dump(
                                cvtr_diff, default_flow_style=False),
                            sep="\n", file=sys.stderr)


                    # call the update converter action method

                    change = cvtr.update(cvtr_cfg, cvtr_diff, args)


                    if change is not None:
                        if isinstance(change, str):
                            change = [change]

                        if self._debug_convert:
                            print("\n".join(change), file=sys.stderr)


                        if self._explain:
                            comment = self._explain_comment(match)
                            if comment:
                                changes.append(comment)


                        changes.extend(change)
                        changes.append("")

                    else:
                        if self._debug_convert:
                            print("-> no action", file=sys.stderr)


            # print a blank line if debugging, just to space things out
            # nicely

            if self._debug_convert:
                print(file=sys.stderr)

        # if nothing was generated, just return nothing

        if not changes:
            return None


        # return the change lines concatenated into a big, multiline
        # string, along with the begin and end blocks

        return "\n".join(self._changes_begin() + changes + self._changes_end())
