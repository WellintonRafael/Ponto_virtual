from stubs import stub

class Foo:
    def __init__(self, label):
        self.label = label

    def m(self, x):
        return self.label, x + 1

    @staticmethod
    def sm(x):
        return x - 1

    @classmethod
    def cm(cls, x):
        return cls.__name__, x


def test_instance_method_stub():
    foo = Foo('a')
    assert foo.m(3) == ('a', 4)

    with stub[foo.m] >> 9:
        assert foo.m(3) == 9
    assert foo.m(3) == ('a', 4)

    with stub[Foo.m] | (lambda self, x: (self.label, x + 2)):
        assert foo.m(3) == ('a', 5)
    assert foo.m(3) == ('a', 4)


def test_static_method_stub():
    foo = Foo('a')
    assert foo.sm(3) == 2

    with stub[foo.sm] >> 9:
        assert foo.sm(3) == 9
    assert foo.sm(3) == 2

    with stub[Foo.sm] | (lambda x: x - 2):
        assert foo.sm(3) == 1
    assert foo.sm(3) == 2


def test_class_method_stub():
    foo = Foo('a')
    assert Foo.cm(3) == ('Foo', 3)
    assert foo.cm(3) == ('Foo', 3)

    with stub[Foo.cm] | (lambda cls, x: (cls.__name__, x * 2)):
        assert Foo.cm(3) == ('Foo', 6)
        assert foo.cm(3) == ('Foo', 6)
    assert Foo.cm(3) == ('Foo', 3)
    assert foo.cm(3) == ('Foo', 3)
