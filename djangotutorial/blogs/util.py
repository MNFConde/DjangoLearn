from dataclasses import dataclass
from datetime import datetime
from typing import Any, Type, TypeVar, Generic

T = TypeVar("T")


@dataclass
class TagData:
    name: str
    link: str


@dataclass
class ArticleData:
    datetime_info: datetime
    tag_list: list[TagData]
    title: str
    excerpt: str
    article_link: str


class singleton_args(Generic[T]):
    def __init__(self, cls: Type[T]):
        self._cls = cls
        self._instances: dict[tuple, Any] = {}

    def __call__(self, *args, **kwargs) -> T:
        # 获取函数的参数默认值，不然无法提取默认值的情况
        import inspect

        sig = inspect.signature(self._cls.__init__)
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        # 创建包含默认值的完整参数键
        key = tuple(sorted(bound_args.arguments.items()))

        if key not in self._instances:
            self._instances[key] = self._cls(*args, **kwargs)
        return self._instances[key]

    def __instancecheck__(self, instance: Any) -> bool:
        return isinstance(instance, self._cls)

    def clear(self) -> None:
        self._instances.clear()
