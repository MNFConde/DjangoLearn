import os
import django
from pathlib import Path
import sys

# 1. 获取脚本所在目录的上一级目录
# 假设脚本位于 script/insert_data.py，则 .parent 是 script/，.parent.parent 是项目根目录 DjangoLearn/
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. 将项目根目录添加到 Python 的搜索路径中
# 这样 import djangotutorial 才能找到
sys.path.append(str(BASE_DIR))

# 3. 设置 Django 的环境变量
# 注意：这里必须指向你的 settings.py 文件
# 如果你的 settings.py 位于 djangotutorial/djangotutorial/settings.py
# 那么路径应该是 'djangotutorial.djangotutorial.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangotutorial.settings")

# 4. 初始化 Django
django.setup()


# 5. 导入模型
# 确保 djangotutorial.blogs 是正确的路径
from blogs.models import Article, Tag
from blogs.tests.stub.stub_faker import SimpleFactoryFaker
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

Faker.seed(0)

factory_faker = SimpleFactoryFaker()

author_obj, created = User.objects.get_or_create(username="zhangsan")
tag_objs = Tag.objects.all()


def add_data(db_len: int = 10):
    # 遍历并创建
    for item in range(db_len):
        # 使用 get_or_create 避免重复插入（根据 title 判断是否存在）

        obj, created = Article.objects.get_or_create(
            author=author_obj,
            title=factory_faker.faker.text(max_nb_chars=40),
            content=factory_faker.faker.text(max_nb_chars=1000),
            created_time=factory_faker.faker.date_time(
                tzinfo=timezone.get_current_timezone()
            ),
            updated_time=factory_faker.faker.date_time(
                tzinfo=timezone.get_current_timezone()
            ),
            good_count=factory_faker.faker.random_int(),
        )

        # ManyToManyField
        obj.tag.set(list(factory_faker.faker.random_sample(list(tag_objs))))

        if created:
            print(f"成功插入: {obj.title}")
        else:
            print(f"数据已存在，跳过: {obj.title}")


if __name__ == "__main__":
    add_data()
