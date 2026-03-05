from blogs.tests.stub.stub_model import BaseTestModel
from blogs.tests.stub.stub_faker import SimpleFactoryFaker

# from blogs.util import Registry
from django.db import models
from factory.django import DjangoModelFactory
import pytest
from faker import Faker
from datetime import datetime


factory_faker = SimpleFactoryFaker()


@pytest.mark.django_db
class TestModel(BaseTestModel):
    """
    测试用 Model
    """

    basic_boolean = models.BooleanField("boolean")
    basic_inteage = models.IntegerField("int")
    name = models.CharField("name")
    e_mail = models.EmailField("email")
    text = models.TextField("txt")
    datetime = models.DateTimeField("datetime")
    url = models.URLField("url")


@pytest.mark.django_db
def test_factory_faker_default():
    class TestFactory(DjangoModelFactory):
        class Meta:
            model = TestModel

        basic_boolean = factory_faker.boolean.lazy()
        basic_inteage = factory_faker.random_int.lazy()
        name = factory_faker.name.lazy()
        e_mail = factory_faker.email.lazy()
        text = factory_faker.text.lazy()
        datetime = factory_faker.date_time.lazy()
        url = factory_faker.url.lazy()

    a = TestFactory()

    # 创建字段
    assert a.basic_boolean
    assert a.basic_inteage == 6890
    assert a.name == "Vincent Tucker"
    assert a.e_mail == "tammy59@example.org"
    assert (
        a.text
        == "Example sense peace economy. Work special total financial role together range. Nice government first policy daughter need kind."
    )
    assert a.datetime == datetime(2004, 7, 25, 22, 23, 39)
    assert a.url == "https://www.arnold-mann.net/"

    # LazyAttribute
    b = TestFactory()
    assert a.name != b.name


@pytest.mark.django_db
def test_factory_faker_extend():
    @factory_faker("status_code")
    def status_code(self):
        """自定义 HTTP 状态码"""
        return self.faker.random_element([200, 201, 400, 401, 404, 500])

    class TestFactory(DjangoModelFactory):
        class Meta:
            model = TestModel

        basic_boolean = factory_faker.boolean.lazy()
        basic_inteage = factory_faker.status_code.lazy()
        name = factory_faker.name.lazy()
        e_mail = factory_faker.email.lazy()
        text = factory_faker.text.lazy()
        datetime = factory_faker.date_time.lazy()
        url = factory_faker.url.lazy()

    a = TestFactory()

    assert a.basic_inteage in [200, 201, 400, 401, 404, 500]
