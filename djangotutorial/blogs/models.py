from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    """
    tag 数据库模型类

    一个 tag 可以对应：
        - 多个文章
    """

    tag_name = models.CharField("标签名", max_length=30, unique=True)

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    """
    文章 数据库模型类

    一篇文章可以对应：
        - 一个作者
        - 多个 tag
        - 一个分类
    """

    author = models.ForeignKey(
        User, verbose_name="作者", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField("标题", max_length=200)
    content = models.TextField("正文")
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("最后更新时间", auto_now=True)
    good_count = models.IntegerField("点赞次数")
    tag = models.ManyToManyField(Tag, related_name="articles")

    def __str__(self):
        return f"由 {self.author} 创作的 《{self.title}》"

    class Meta:
        indexes = [
            models.Index(
                fields=["title", "created_time", "updated_time"], name="normal"
            ),
        ]
