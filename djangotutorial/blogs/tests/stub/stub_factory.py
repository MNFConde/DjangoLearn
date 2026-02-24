from blogs.models import (
    Article,
    Tag,
)
from blogs.tests.stub.stub_faker import SimpleFactoryFaker
from django.contrib.auth.models import User
import factory
from factory.django import DjangoModelFactory
from faker.providers import BaseProvider


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """设置密码"""
        self.set_password(extracted or "defaultpass123")


# class TagFactory(DjangoModelFactory):
#     class Meta:
#         model = Tag


#     tag_name =
class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    author = factory.SubFactory(UserFactory)
