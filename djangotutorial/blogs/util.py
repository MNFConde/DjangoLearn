from dataclasses import dataclass
from datetime import datetime
from typing import Any, Type, TypeVar, Callable, Union
import inspect
from abc import ABC, abstractmethod

T = TypeVar("T")

parent_class = None


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


def singleton_args(cls: Type[T]) -> Type[T]:
    """
    类装饰器：基于初始化参数实现单例，返回一个继承原始类的子类，以此保证提示的正确。
    """

    class Wrapper(cls):  # 继承原始类
        instances: dict[tuple, Any] = {}

        def __new__(cls, *args: Any, **kwargs: Any) -> Any:
            # 生成缓存键（注意参数顺序）
            sig = inspect.signature(cls.__init__)
            bound_args = sig.bind_partial(cls, *args, **kwargs)
            bound_args.apply_defaults()

            # 创建包含默认值的完整参数键
            key = str(tuple(sorted(bound_args.arguments.items())))
            if key not in cls.instances:
                # 创建新实例（__init__ 会在之后自动调用）
                instance = super().__new__(cls)
                cls.instances[key] = instance
            return cls.instances[key]

        @classmethod
        def clear_cache(cls) -> None:
            """清空缓存（类方法）"""
            cls.instances.clear()

    # 复制元数据，使 Wrapper 看起来更像原始类
    Wrapper.__name__ = cls.__name__
    Wrapper.__doc__ = cls.__doc__
    Wrapper.__module__ = cls.__module__
    # 复制其他可能需要的属性（如 __annotations__）
    if hasattr(cls, "__annotations__"):
        Wrapper.__annotations__ = cls.__annotations__

    return Wrapper


class Registry(ABC):
    """
    a = Registry('test')
    assert not hasattr(a.registry, 'f1')

    @a('f1')
    def func1():
        return 1

    assert a.f1() == func1()
    """

    registry_cls_dict: dict[str, Callable[..., Any]] = dict()

    def __init__(self, name: str = "", *args, **kwargs):
        # if not hasattr(self, "registry_cls_dict"):
        # name 参数是用来给 singleton_args 使用的，这里加入只是为了简化传参，给额外的这个参数找个地方
        # Registry.registry_cls_dict: dict[str, Callable[..., Any]] = dict()
        # 通过 self.faker 点符号来访问 Faker 类的方法和属性，与本类隔离
        if hasattr(type(self), "_parent_class"):
            # 如果没有设置 _parent_class，使用默认值 None
            self.parent_instance = self._parent_class(*args, **kwargs)
        else:
            self.parent_instance = None

    def __call__(self, name: str) -> Callable:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            # 这里并不需要额外在调用函数时增加行为，所以就不创建子函数来调用 fn
            Registry.registry_cls_dict[name] = fn
            return fn

        return decorator

    def __dir__(self) -> list[str]:
        # 获取父类属性、注册的函数名、以及 parent_instance 的属性
        base_attrs = super().__dir__()
        registry_keys = list(Registry.registry_cls_dict.keys())
        parent_attrs = dir(self.parent_instance) if self.parent_instance else []
        # 合并去重
        return sorted(set(base_attrs + registry_keys + parent_attrs))

    def __getattr__(self, name: str, **kwargs) -> Callable[..., Any]:
        """
        为了兼容 hasatttr
        """
        if name in Registry.registry_cls_dict.keys():
            return self.return_registry_val(Registry.registry_cls_dict[name])
        return self.return_registry_val(getattr(self.parent_instance, name))

    @abstractmethod
    def return_registry_val(self, val: Any): ...


class RegistrySimple(Registry):
    def return_registry_val(self, val: Any):
        return val


def RegistryFactory(
    registry_class: type = RegistrySimple, parent_class: Union[None, type] = None
):
    @singleton_args
    class Warpper(registry_class):
        if parent_class:
            _parent_class = parent_class
        pass

    return Warpper
