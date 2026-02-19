from blogs import util
from blogs.models import Article, Tag
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
from random import randint

test_data = {
    "datetime": datetime.now(),
    "tag_list": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "title": "title_test",
    "excerpt": "123123123123123123123123123123",
    "author": "123123",
}

test_tag_list = [
    util.TagData("tag1", "link1"),
    util.TagData("tag2", "link1"),
    util.TagData("tag3", "link1"),
    util.TagData("tag4", "link1"),
    util.TagData("tag5", "link1"),
]

test_context = [
    util.ArticleData(
        datetime.now(),
        test_tag_list[randint(0, 3) : randint(3, len(test_tag_list))],
        "123123",
        "123123123123132",
        "123",
    ),
    util.ArticleData(
        datetime.now(),
        test_tag_list[randint(0, 3) : randint(3, len(test_tag_list))],
        "123123",
        "123123123123132",
        "123",
    ),
    util.ArticleData(
        datetime.now(),
        test_tag_list[randint(0, 3) : randint(3, len(test_tag_list))],
        "123123",
        "123123123123132",
        "123",
    ),
    util.ArticleData(
        datetime.now(),
        test_tag_list[randint(0, 3) : randint(3, len(test_tag_list))],
        "123123",
        "123123123123132",
        "123",
    ),
    util.ArticleData(
        datetime.now(),
        test_tag_list[randint(0, 3) : randint(3, len(test_tag_list))],
        "123123",
        "123123123123132",
        "123",
    ),
]


# Create your views here.
def index_page(request):
    # 获取所有文章
    article_list = Article.objects.all().order_by("-created_time")

    # 分页：每页 10 篇
    paginator = Paginator(article_list, 10)
    # 获取当前页码
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "article_info_list": test_context,
        "blogs_page_info": {
            "page_obj": page_obj,
            "paginator": paginator,
        },
        "tag_list": test_tag_list,
    }

    return render(request, "blogs/index.html", context)
