from blogs.util import singleton_args, RegistryFactory
import pytest


def test_singleton_args():
    @singleton_args
    class clsA:
        def __init__(self, a: int, b: str = "a"):
            self.a = a
            self.b = b

    a = clsA(1)
    b = clsA(1)
    c = clsA(2)
    assert a is b
    assert a is not c
    assert b is not c

    d = clsA(1, "a")
    assert a is d

    e = clsA(2, "b")
    f = clsA(2, "b")
    g = clsA(3, "b")
    h = clsA(3, "c")

    assert e is f
    assert e is not g
    assert f is not h


def test_registry():
    test_registry_cls = RegistryFactory()
    a = test_registry_cls("test")
    assert not hasattr(a, "f1")

    @a("f1")
    def func1():
        return 1

    assert a.f1() == func1()

    b = test_registry_cls("test")
    assert a is b
    assert a.f1() == b.f1()

    pass
