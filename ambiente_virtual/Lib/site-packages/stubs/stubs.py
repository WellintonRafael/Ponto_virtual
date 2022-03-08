"""Handy tools for setting up stubs and mocks.

This module exports two special objects, `stub` and `expect`, which can be
used to stub out functions or methods.  To replace a function with a stub,
start a context block using `with`, then `stub` or `expect`, then the function
wrapped in square brackets.  By default, the stub returns None.  Upon exiting
the context block, the original function is restored.  It looks like this:

    def f(x): return x * 2

    with stub[f]:
        print(f(3))  # prints None
    print f(3))  # prints 6

To make the stub return a constant, write `>>` and the return value:

    with stub[f] >> 5:
        print(f(3))  # prints 5
    print(f(3))  # prints 6

The function object is replaced in the namespace where it was defined.  If
the function has been imported into a different namespace, that namespace
won't be affected; you can specify the namespace by providing a string path
to the function instead of the function itself:

    # --- a.py ---
    def f(x): return x * 2

    # --- b.py ---
    from a import f

    # --- c.py ---
    import a
    import b

    with stub[b.f] >> 5:
        print(a.f(3))  # stub, prints 5
        print(b.f(3))  # unaffected, prints 6

    with stub['b.f'] >> 5:
        print(a.f(3))  # unaffected, prints 6
        print(b.f(3))  # stub, prints 5

You can also stub out a method on a class or an instance:

    class Foo:
        def f(self, x):
            return x * 3

    foo = Foo()
    with stub[foo.f] >> 8:
        print(foo.f(3))  # stub, prints 8
        bar = Foo()
        print(bar.f(3))  # original, prints 9
    print(foo.f(3))  # original, prints 9

    with stub[Foo.f] >> 8:
        print(foo.f(3))  # original, prints 9
        bar = Foo()
        print(bar.f(3))  # stub, prints 8
    print(foo.f(3))  # original, prints 9

In all the examples above, the stub is invoked regardless of any arguments or
keyword arguments.  You can specify expected arguments after the function:

    with stub[f](3) >> 5:
        with stub[f](4) >> 1:
            print(f(4))  # prints 1
            print(f(4))  # prints 1
            print(f(3))  # prints 5
            print(f(1))  # AssertionError: Unexpected call

Matchers (see matchers.py) are accepted in the argument specification, giving
you lots of expressive power.  The matchers are tested in order starting from
the innermost context and proceeding outward; always specify the most specific
matchers on the inside:

    with stub[f] >> 0:
        with stub[f](_ > 3) >> 7:
            with stub[f](1, ..., foo=[5, 10 < _ < 20]) >> -1:
                print(f(1))  # prints 0
                print(f(2))  # prints 0
                print(f(3))  # prints 0
                print(f(4))  # prints 7
                print(f(1, 2, 3, foo=[5, 13]))  # prints -1

To invoke another function instead of returning a constant, use the `|`
operator instead (mnemonic: the stub pipes its arguments to the new function):

    def g(x): return x + 1

    with stub[f] | g:
        print(f(3))  # prints 4
    print(f(3))  # prints 6

To raise an exception instead of returning anything, use the `^` operator
(mnemonic: `^` points up to raise):

    with stub[f] | f:
        with stub[f](0) ^ ValueError('Zero is not allowed!')
            print(f(2))  # prints 4
            print(f(1))  # prints 2
            print(f(0))  # ValueError: Zero is not allowed!

When you use `|` to replace a method on a class, you should provide a function
that takes the same arguments as in the original method definition (i.e. with
an initial `self` argument for an instance method; an initial `cls` argument
for a class method, or no initial `self` or `cls` argument for a static method).
However, do not annotate your function with `@staticmethod` or `@classmethod`;
it will be automatically converted to the same kind of method as the method
being replaced:

    class Foo:
        def f(self, x):
            return x * 3

        @staticmethod
        def g(x):
            return x + 2

    foo = Foo()
    with stub[Foo.f] | (lambda self, x: x * 4):  # takes a self argument, like f
        print(foo.f(2))  # stub, prints 8
    print(foo.f(2))  # original, prints 6

    with stub[Foo.g] | (lambda x: x + 3):  # takes no self argument, like g
        print(foo.g(2))  # stub, prints 5
    print(foo.g(2))  # original, prints 4

When you set up a stub with `stub`, it doesn't care whether the function is
called at all, or called many times.  Its job is just to replace the behaviour
of the function; it will only complain if the stub is called with arguments
for which no behaviour has been specified.  In the last example above, the
outermost context `with stub[f] | f` causes the stub to fall back to calling
the original `f` for any arguments other than 0.

`expect` can be used in all the same ways as `stub` above, but unlike `stub`,
it requires exactly one call with arguments matching the specified pattern
to occur within the `expect` context:

    with stub[f](5) >> 5:
        with expect[f](6) >> 5:
            print(f(5))  # prints 5
        # AssertionError: Missing expected call to f(6)

When multiple `expect` contexts are present, the calls are expected to occur
in exactly the specified order:

    with expect[f](1) >> 1, expect[f](2) >> 2, expect[f](3) >> 3:
        print(f(1))  # prints 1
        print(f(3))  # AssertionError: Unexpected call to f(3); expecting f(2)
"""

import inspect
from .matchers import match
import sys
import types

__all__ = ['expect', 'stub']

class StubWrapper:
    """Implements the `stub` object, which when indexed with a function
    like `stub[foo]`, sets up the function to be replaced with a stub."""
    def __getitem__(self, target):
        return Invocation(get_pointer(target), False, None, ..., _=...)

class ExpectWrapper:
    """Implements the `expect` object, which when indexed with a function
    like `expect[foo]`, sets up the function to be replaced with a stub
    that expects exactly one call matching a specified pattern."""
    def __getitem__(self, target):
        return Invocation(get_pointer(target), True, None, ..., _=...)

def get_pointer(target):
    if isinstance(target, str):
        parts = target.split('.')
        assert len(parts) >= 2
        namespace = sys.modules[parts[0]]
        for part in parts[1:-1]:
            namespace = getattr(namespace, part)
        return Pointer(namespace, parts[-1])

    if isinstance(target, Stub):
        return target.pointer

    if inspect.ismethod(target):
        namespace = target.__self__
        name = target.__name__
    elif hasattr(target, '__module__'):
        namespace = sys.modules[target.__module__]
        for part in target.__qualname__.split('.')[:-1]:
            namespace = getattr(namespace, part)
        name = target.__name__
        assert getattr(namespace, name) is target
    else:
        raise TypeError('%r cannot be stubbed out' % target)
    return Pointer(namespace, name)

class Pointer:
    """A pointer to a function or method to be stubbed out in a namespace.

    This is designed to work either on normal read-write namespaces (like
    modules and instances) or on namespaces with read-only __dict__s (like
    classes), where the values are not data descriptors (i.e. they may or
    may not have __get__, but most not have __set__); hence the deliberate
    the deliberate asymmetry between Pointer.get and Pointer.setattr.
    Functions are never data descriptors, so this works fine for functions,
    instance methods, static methods, and class methods."""

    # A sentinel value that indicates when an attribute is missing.
    MISSING = object()

    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    def __repr__(self):
        namespace_repr = getattr(self.namespace, __name__, repr(self.namespace))
        return '%s.%s' % (namespace_repr, self.name)

    def get(self):
        # We access the __dict__ to get the underlying value.  This lets us
        # detect whether a method in a class is an instance method, a static
        # method, or a class method.
        return (self.namespace.__dict__[self.name]
                if self.name in self.namespace.__dict__
                else Pointer.MISSING)

    def setattr(self, value):
        # We're assuming the namespace dict might be read-only (e.g. a class
        # __dict__), so we can't write directly into the __dict__, and that
        # the value has no __set__, so it is safe to use setattr.
        if value is Pointer.MISSING:
            delattr(self.namespace, self.name)
        else:
            setattr(self.namespace, self.name, value)

class Invocation:
    """A context manager that describes a possible way that a function can be
    invoked, and stubs out the function to handle that invocation."""
    def __init__(self, pointer, required, delegate, *args, **kwargs):
        self.pointer = pointer
        self.required = required
        self.delegate = delegate or (lambda *args, **kwargs: None)
        self.args = args
        self.kwargs = kwargs
        self.original = None
        self.invoked = False

    def __repr__(self):
        return '%r(%s)' % (self.pointer, format_args(self.args, self.kwargs))

    def __call__(self, *args, **kwargs):
        return Invocation(self.pointer, self.required, None, *args, **kwargs)

    def __or__(self, delegate):
        return Invocation(
            self.pointer, self.required, delegate, *self.args, **self.kwargs)

    def __rshift__(self, return_value):
        return self | (lambda *args, **kwargs: return_value)

    def __xor__(self, exception):
        return self | make_raiser(exception)

    def __enter__(self):
        self.current = getattr(self.pointer.namespace, self.pointer.name)
        if isinstance(self.current, Stub):
            self.current.add_invocation(self)
        else:
            self.original = self.pointer.get()
            stub = Stub(self.pointer, self)
            if isinstance(self.original, staticmethod):
                stub = staticmethod(stub)
            if isinstance(self.original, classmethod):
                stub = classmethod(stub)
            self.pointer.setattr(stub)

    def __exit__(self, etype, evalue, tb):
        if self.original is not None:
            self.pointer.setattr(self.original)
        else:
            self.current.remove_invocation(self)
        if self.required and not self.invoked and not evalue:
            raise AssertionError('Missing expected call to %r' % self)

    def matches(self, args, kwargs):
        return match(args, self.args) and match(kwargs, self.kwargs)

class Stub:
    """A stub that takes the place of a function or method."""
    def __init__(self, pointer, *invocations):
        self.pointer = pointer
        self.required_invocations = []
        self.optional_invocations = []
        for invocation in invocations:
            self.add_invocation(invocation)

    def __get__(self, obj, objtype=None):
        return self if obj is None else types.MethodType(self, obj)

    def __call__(self, *args, **kwargs):
        for invocation in self.optional_invocations:
            if invocation.matches(args, kwargs):
                return invocation.delegate(*args, **kwargs)
        if self.required_invocations:
            invocation = self.required_invocations.pop(0)
            if invocation.matches(args, kwargs):
                invocation.invoked = True
                return invocation.delegate(*args, **kwargs)
            raise AssertionError('Unexpected call to %r(%s); expecting %r' % (
                self.pointer, format_args(args, kwargs), invocation
            ))
        raise AssertionError('Unexpected call to %r(%s)' % (
            self.pointer, format_args(args, kwargs)
        ))

    def add_invocation(self, invocation):
        if invocation.required:
            self.required_invocations.append(invocation)
        else:
            self.optional_invocations.insert(0, invocation)

    def remove_invocation(self, invocation):
        self.optional_invocations = [
            i for i in self.optional_invocations if i is not invocation]
        self.required_invocations = [
            i for i in self.required_invocations if i is not invocation]

def format_args(args, kwargs):
    """Formats args and kwargs the way they look in a function call."""
    return ', '.join([repr(arg) for arg in args] +
                     ['%s=%r' % item for item in sorted(kwargs.items())])

def make_raiser(exception):
    def raiser(*args, **kwargs):
        raise exception
    return raiser

stub = StubWrapper()
expect = ExpectWrapper()
