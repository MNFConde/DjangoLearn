from dataclasses import dataclass
from datetime import datetime
from typing import Any, Type, TypeVar, Generic, Callable, Union, overload
import functools
import inspect

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
    """
    使用方法：
        @singleton_args
        class B:
            def __init__(self, x, y=0):
                self.x = x
                self.y = y

        a1 = B(1)  # 创建新实例
        a2 = B(1)  # 返回相同实例
        a3 = B(2)  # 创建新实例
        a4 = B(1, y=0)  # 返回与a1相同的实例
        a5 = B(1, y=1)  # 创建新实例
    """

    def __init__(self, cls: Type[T]):
        self._cls = cls
        self._instances: dict[tuple, Any] = {}

        # 1. 获取原始 __init__ 的签名
        original_sig = inspect.signature(cls.__init__)

        # 2. 移除第一个参数 (self)
        params = [p for name, p in original_sig.parameters.items() if name != "self"]

        # 3. 创建新的签名对象（不包含 self）
        new_sig = original_sig.replace(parameters=params)

        # 4. 复制元数据
        functools.update_wrapper(
            self,
            cls.__init__,
            assigned=(
                "__module__",
                # "__name__",
                # "__qualname__",
                "__annotations__",
                "__doc__",
            ),
            updated=(),
        )

        # 5. 设置处理过的签名
        self.__signature__ = new_sig

    # 使用 overload 告诉类型检查器：这个类的行为就像 T 类的构造函数
    @overload
    def __call__(self, *args: Any, **kwargs: Any) -> T: ...

    def __call__(self, *args, **kwargs) -> T:
        # 获取函数的参数默认值，不然无法提取默认值的情况
        sig = inspect.signature(self._cls.__init__)
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        # 创建包含默认值的完整参数键
        key = tuple(sorted(bound_args.arguments.items()))

        if key not in self._instances:
            instance = self._cls(*args, **kwargs)
            # 将原始类 __init__ 的签名复制到返回的实例上
            # 这样 help(instance) 或 IDE 提示时就会显示 Registry 的 __init__ 参数
            functools.update_wrapper(
                instance,
                self._cls.__init__,
                assigned=(
                    "__module__",
                    "__name__",
                    "__qualname__",
                    "__annotations__",
                    "__doc__",
                ),
                updated=(),
            )
            # 手动设置 __signature__，因为 update_wrapper 默认不处理它
            instance.__signature__ = sig
            self._instances[key] = instance
        return self._instances[key]

    def __instancecheck__(self, instance: Any) -> bool:
        return isinstance(instance, self._cls)

    def clear(self) -> None:
        self._instances.clear()


@singleton_args
class Registry:
    """
    a = Registry('test')
    assert not hasattr(a.registry, 'f1')

    @a('f1')
    def func1():
        return 1

    assert a.f1() == func1()
    """

    def __init__(
        self, name: str = "", parent_class: Union[None, type] = None, *args, **kwargs
    ):
        # name 参数是用来给 singleton_args 使用的，这里加入只是为了简化传参，给额外的这个参数找个地方
        self.__registry: dict[str, Callable[..., Any]] = dict()
        # 通过 self.faker 点符号来访问 Faker 类的方法和属性，与本类隔离
        self.parent_instance = parent_class(*args, **kwargs)

    def __call__(self, name: str) -> Callable:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            # 这里并不需要额外在调用函数时增加行为，所以就不创建子函数来调用 fn
            self.__registry[name] = fn
            return fn

        return decorator

    def __getattr__(self, name: str, **kwargs) -> Callable[..., Any]:
        """
        为了兼容 hasatttr
        """
        if name in self.__registry.keys():
            return self.__registry[name]
        return getattr(self.parent_instance, name)
