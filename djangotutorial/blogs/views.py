from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

test_data = {
    "datetime": datetime.now(),
    "tag_list": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "title": "title_test",
    "excerpt": "123123123123123123123123123123",
    "author": "123123",
}


# Create your views here.
def index_page(request):
    context = {
        "article_info_list": [test_data, test_data],
    }
    return render(request, "blogs/index.html", context)
