from django.db import models


class BaseTestModel(models.Model):
    """基础测试模型"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = "blogs"
