# conftest.py
# from blogs.tests.stub.stub_faker import FactoryFaker
from faker import Faker
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_django_environment():
    """
    设置 Django 测试环境
    """
    Faker.seed(0)

    yield

    # 恢复设置
    print("Django 测试环境清理完成")
