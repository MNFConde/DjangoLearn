from blogs.models import Article, Tag
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.
def index_page(request):
    # 获取所有文章
    article_list = Article.objects.all().order_by("-created_time")

    # 分页：每页 10 篇
    paginator = Paginator(article_list, 3)
    # 获取当前页码
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # 1. 使用 annotate 创建一个名为 'article_count' 的临时字段
    #    该字段统计每个 Tag 关联的 Article 数量（利用 related_name 'articles'）
    # 2. 使用 order_by 对这个临时字段进行排序
    #    加上 '-' 表示降序（从多到少），去掉 '-' 则是升序
    tags = Tag.objects.annotate(article_count=Count("articles")).order_by(
        "-article_count", "tag_name"
    )
    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "tag_list": tags,
    }

    return render(request, "blogs/index.html", context)


def blog_page(request, article_id: int):
    article = Article.objects.get(pk=article_id)

    context = {"article_info": article}

    return render(request, "blogs/blog_text.html", context)
