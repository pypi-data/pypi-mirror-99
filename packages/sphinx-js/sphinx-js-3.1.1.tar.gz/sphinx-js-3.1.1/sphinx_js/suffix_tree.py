class SuffixTree(object):
    """A suffix tree in which you can use anything hashable as a path segment
    and anything at all as a value

    """
    def __init__(self):
        #: Internal structure is like... ::
        #:
        #:     Tree = {value?: Any,
        #:             subtree?: {segmentFoo: Tree, segmentBar: Tree, ...}}
        #
        #: A Tree can have a value key, a subtree key, or both. Subtree dicts
        #: always have at least 1 key. Every subtree has at least one value,
        #: directly or indirectly. ``self._tree`` itself is a Tree.
        self._tree = {}

    def add(self, unambiguous_segments, value):
        """Add an item to the tree.

        :arg unambiguous_segments: A list of path segments that correspond
            uniquely to the stored value
        :arg value: Any value you want to fetch by path

        """
        tree = self._tree
        for seg in reversed(unambiguous_segments):
            tree = tree.setdefault('subtree', {}).setdefault(seg, {})
        if 'value' in tree:
            raise PathTaken(unambiguous_segments)
        else:
            tree['value'] = value

    def add_many(self, segments_and_values):
        """Add a batch of items to the tree all at once, and collect any
        errors.

        :arg segments_and_values: An iterable of (unambiguous segment path,
            value)

        If any of the segment paths are duplicates, raise PathsTaken.

        """
        conflicts = []
        for segs, value in segments_and_values:
            try:
                self.add(segs, value)
            except PathTaken as conflict:
                conflicts.append(conflict.segments)
        if conflicts:
            raise PathsTaken(conflicts)

    def get_with_path(self, segments):
        """Return the value stored at a path ending in the given segments,
        along with the full path found.

        :arg segments list: A possibly ambiguous suffix of a path

        If no paths are found with the given suffix, raise SuffixNotFound. If
        multiple are found, raise SuffixAmbiguous. This is true even if
        the given suffix is a full path to a value: we want to flag the
        ambiguity to the user, even if it might sometimes be more convenient to
        assume the intention was to present a full path.

        """
        # Keep walking down subtrees (returning NotFound if failed) until we
        # run out of segs:
        tree = self._tree
        for seg in reversed(segments):
            try:
                tree = tree['subtree'][seg]
            except KeyError:
                raise SuffixNotFound(segments)

        # If there's only a value there, return it:
        if 'value' in tree:
            if 'subtree' in tree:
                raise SuffixAmbiguous(segments, list(tree['subtree'].keys()), or_ends_here=True)
            return tree['value'], segments

        # Else if there's a subtree, follow its 1-key subtrees forever, since
        # there's no ambiguity there:
        additional_segments = []
        while len(tree.get('subtree', {})) == 1:
            only_key = next(iter(tree['subtree'].keys()))
            tree = tree['subtree'][only_key]
            additional_segments.append(only_key)

        # If we arrived at a spot with multiple possiblities, yell:
        if len(tree.get('subtree', {})) > 1:
            raise SuffixAmbiguous(segments, list(tree['subtree'].keys()))

        # Otherwise, return the found value. There must always be a value here
        # because add() always eventually adds a value after a chain of
        # subtrees. If there were multiple subrees from here, we would have
        # raised SuffixAmbiguous above. If there were a single one, we would
        # have followed it. So, since subtrees always eventually terminate in a
        # value, we must be at one now.
        return tree['value'], (list(reversed(additional_segments)) + segments)

    def get(self, segments):
        return self.get_with_path(segments)[0]


class SuffixError(Exception):
    def __init__(self, segments):
        self.segments = segments

    def __str__(self):
        return self._message % ''.join(self.segments)


class PathTaken(SuffixError):
    """Attempted to add a suffix that was already in the tree."""
    _message = 'Attempted to add a path already in the suffix tree: %s.'


class PathsTaken(Exception):
    """One or more JS objects had the same paths.

    Rolls up multiple PathTaken exceptions for mass reporting.

    """
    def __init__(self, conflicts):
        """
        :arg conflicts: A list of paths, each given as a list of segments
        """
        self.conflicts = conflicts

    def __str__(self):
        return ('Your code contains multiple documented objects at each of '
                "these paths:\n\n  %s\n\nWe won't know which one you're "
                'talking about.' %
                '\n  '.join(''.join(c) for c in self.conflicts))


class SuffixNotFound(SuffixError):
    """No keys ended in the given suffix."""
    _message = 'No path found ending in %s.'


class SuffixAmbiguous(SuffixError):
    """There were multiple keys found ending in the suffix."""

    def __init__(self, segments, next_possible_keys, or_ends_here=False):
        super(SuffixAmbiguous, self).__init__(segments)
        self.next_possible_keys = next_possible_keys
        self.or_ends_here = or_ends_here

    def __str__(self):
        ends_here_msg = ' Or it could end without any of them.' if self.or_ends_here else ''
        return 'Ambiguous path: %s could continue as any of %s.%s' % (''.join(self.segments), self.next_possible_keys, ends_here_msg)
