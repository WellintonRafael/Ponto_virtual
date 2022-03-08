"""A concise way to express patterns of values to match for tests.

This module exports a special object named `_`, which is an instance of a
Matcher and can be used to make more Matchers, and the `match` function,
which checks a value against a matcher.

`_` on its own matches anything:

    match(3, _)  # True

You can use `_` with comparison operators:

    match(3, _ < 5)  # True
    match(8, _ < 5)  # False

For matching strings, you can use `.starting_with` or `.ending_with`:

    match('abcd', _.starting_with('a'))  # True
    match('abcd', _.ending_with('ff'))  # False

You can also compose structures out of matchers and values:

    match([1, 2, 3], [1, 2, 3])  # True
    match([1, 2, 3], [1, _, 3])  # True
    match([1, 2, 3], [1, _, _ < 8])  # True
    match([1, 2, 9], [1, _, _ < 8])  # False
    match({'a': 1, 'b': 2}, {'a': _, 'b': 2})  # True
    match({'a': 1, 'b': 2}, {'a': _ > 5, 'b': 2})  # False

You can use the special value `...` (Python's Ellipsis) to match only part
of a list, set, or dictionary:

    match([1, 2, 3, 4], [1, 2, ...])  # True
    match([1, 2, 3, 4], [1, ..., 4])  # True
    match([1, 2, 3, 4], [..., 3, 4])  # True
    match({'a': 1, 'b': 2}, {'a': 1, ...:...})  # True

"""

import re

__all__ = ['_', 'match']

class Matcher:
    """A Matcher is simply a predicate returning a boolean.  The base matcher,
    `_`, is pronounced "anything", and the methods are named accordingly, e.g.
    "_ < 3" reads as "anything less than 3", "_.ending_with('foo')" reads as
    "anything ending with 'foo'", and so on."""

    def __init__(self, *predicates):
        self.predicates = predicates

    def __repr__(self):
        # TODO
        return '<Matcher>'

    def __call__(self, x):
        return all(pred(x) for pred in self.predicates)

    def __and__(self, predicate):
        return Matcher(*(self.predicates + (predicate,)))

    def __or__(self, predicate):
        return Matcher(lambda x: self(x) or predicate(x))

    def __gt__(self, other):
        return self & (lambda x: x > other)

    def __lt__(self, other):
        return self & (lambda x: x < other)

    def __ge__(self, other):
        return self & (lambda x: x >= other)

    def __le__(self, other):
        return self & (lambda x: x <= other)

    def __ne__(self, other):
        return self & (lambda x: x != other)

    def of_type(self, type_):
        return self & (lambda x: isinstance(x, type_))

    def empty(self):
        return self & (lambda x: len(x) == 0)

    def nonempty(self):
        return self & (lambda x: len(x) > 0)

    def starting_with(self, other):
        return self.of_type(type(other)) & (lambda x: x.startswith(other))

    def ending_with(self, other):
        return self.of_type(type(other)) & (lambda x: x.endswith(other))

    def containing(self, other):
        return self & (lambda x: other in x)

    def with_attrs(self, **kwargs):
        return self & (lambda x: all(
            hasattr(x, name) and match(getattr(x, name), value)
            for name, value in kwargs.items()))

    def __truediv__(self, pattern):
        """Matches a string (the entire string) against a regular expression.
        Mnemonic: / is reminiscent of slashes signifying a regex in /foo/."""
        regex = re.compile('^' + pattern + '$')
        return self.of_type(type(pattern)) & regex.match

def match(value, other):
    """Checks whether a value satisfies a matcher,equals a specific value,
    or matches a structure composed of matchers and/or values."""
    if isinstance(other, Matcher):
        return other(value)
    if isinstance(other, (set, tuple, list, dict)):
        if type(value) != type(other):
            return False
        need_equal_length = True
        if ... in other:
            need_equal_length = False
        if isinstance(other, dict):
            if ... in other.values():
                need_equal_length = False
        if need_equal_length and len(value) != len(other):
            return False
    if isinstance(other, set):
        return all(any(match(element, oe) for element in value)
                   for oe in other if oe != ...)
    if isinstance(other, (tuple, list)):
        if other.count(...) > 1:
            raise RuntimeError("don't know how to match multiple ellipses")
        if ... in other:
            gap = other.index(...)
            pre, post = other[:gap], other[gap + 1:]
            return ((match(value[:len(pre)], pre) if pre else True) and
                    (match(value[-len(post):], post) if post else True))
        return all(match(element, oe) for element, oe in zip(value, other))
    if isinstance(other, dict):
        return all(key in value and match(value[key], ov)
                   for key, ov in other.items()
                   if key != ... and ov != ...)
    return value == other

# The base matcher, which matches anything.
_ = Matcher()
