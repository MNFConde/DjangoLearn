from blogs.util import singleton_args, RegistryFactory, Registry
from typing import Any, Callable, Union, Protocol, TypeVar, Generic
from factory import LazyAttribute
from faker import Faker
import functools


class MyCallable(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


# 定义泛型类型变量，用于保留原始函数的参数和返回值类型
T = TypeVar("T", bound=Callable[..., Any])


class FunctionWrapper(Generic[T]):
    def __init__(self, func):
        # 保存原始函数
        self.func = func
        # 保持原函数的元信息（如 __name__, __doc__）
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        # 实际调用函数的地方
        return self.func(*args, **kwargs)

    def lazy(self, *args, **kwargs):
        return LazyAttribute(lambda i: self.func(*args, **kwargs))


class FakerRegistry(Registry):
    def return_registry_val(self, val: Callable[..., Any]):
        return FunctionWrapper(val)


SimpleFactoryFaker = RegistryFactory(FakerRegistry, Faker)


# @singleton_args
# class SimpleFactoryFaker:
#     """
#     a = Registry('test')
#     assert not hasattr(a.registry, 'f1')

#     @a('f1')
#     def func1():
#         return 1

#     assert a.f1() == func1()
#     """

#     def __init__(self, name: str = ""):
#         # name 参数是用来给 singleton_args 使用的，这里加入只是为了简化传参，给额外的这个参数找个地方
#         self.__registry: dict[str, LazyAttribute] = dict()
#         # 通过 self.faker 点符号来访问 Faker 类的方法和属性，与本类隔离
#         self.faker = Faker()

#     def __call__(self, name: str) -> Callable:
#         def decorator(fn: Callable[..., Any]) -> LazyAttribute:
#             # 这里并不需要额外在调用函数时增加行为，所以就不创建子函数来调用 fn
#             self.__registry[name] = fn
#             return fn

#         return decorator

#     def __getattr__(self, name: str, **kwargs) -> LazyAttribute:
#         """
#         为了兼容 hasatttr
#         """
#         try:
#             if name in self.__registry.keys():
#                 # 获取未绑定的函数
#                 unbound_method = self.__registry[name]
#                 # 创建一个绑定方法，将 self (SimpleFactoryFaker 实例) 绑定上去
#                 # MethodType(func, obj) 会返回一个已绑定的方法对象
#                 from types import MethodType

#                 faker_method = MethodType(unbound_method, self)
#             else:
#                 """
#                 这里需要 Faker.__getattr__
#                 1. getattr(self, name) 会导致递归
#                 2. getattr(super(), name) super() 不能通过 getattr 来获取动态属性，原因如下，
#                     class Faker:
#                         def __init__(self):
#                             # Faker 的方法不是直接定义在类中的
#                             # 而是通过 providers 动态添加的
#                             self.providers = []
#                             # 添加各种 provider
#                             self.add_provider(misc_provider)
#                             self.add_provider(person_provider)
#                             # ...

#                         def __getattr__(self, name):
#                             # 当访问不存在的属性时，从 providers 中查找
#                             for provider in self.providers:
#                                 if hasattr(provider, name):
#                                     return getattr(provider, name)
#                             raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

#                 3. Faker.__getattr__(self, name) 既可以访问父类的动态属性，又可以绕过递归 或者更简单的 super().__getattr__(name)
#                 """
#                 faker_method = getattr(self.faker, name)
#         except Exception as e:
#             raise AttributeError(e)


#         return LazyAttribute(
#             lambda i: faker_method(**kwargs)
#         )  # 这里不传 self 的原因：super().__getattr__(name) 返回的通常已经是一个绑定方法，对应的 self 已经绑定完毕
