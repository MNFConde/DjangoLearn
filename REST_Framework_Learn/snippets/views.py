from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User
from snippets.permission import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """
    根路径，客户端访问这个地址，就知道都有什么东西可以访问
    """
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


class SnippetViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。

    另外我们还提供了一个额外的`highlight`操作。
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    @action(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    此视图自动提供`list`和`detail`操作
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
