from blogs.util import singleton_args
from random import randint
from typing import Any, Type, TypeVar, Generic, Callable
from factory import LazyAttribute
from faker import Faker

test_tag_list = (
    "Python",
    "C++",
    "Rust",
    "Go",
    "Django",
    "Flask",
    "Pytest",
)


@singleton_args
class FactoryFaker(Faker):
    def __init__(self, name: str = ""):
        self.__registry: dict[str, Callable[..., Any]] = dict()
        self._name: str = name
        super().__init__()

    def __call__(self, name: str) -> Callable:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            # 这里并不需要额外在调用函数时增加行为，所以就不创建子函数来调用 fn
            self.__registry[name] = fn
            return fn

        return decorator

    def __getitem__(self, name: str) -> Callable[..., Any]:
        return self.__registry[name]

    def __setitem__(self, name: str, value: Callable[..., Any]) -> None:
        self.__registry[name] = value

    @property
    def registry(self) -> dict[str, Callable[..., Any]]:
        return self.__registry

    def __getattr__(self, name: str) -> Any:
        """
        为了兼容 hasatttr
        """
        try:
            if name in self.__registry.keys():
                return self.__registry[name]
            else:
                return super().__getattr__(name)
        except Exception as e:
            raise AttributeError(e)
