from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    """
    将 Markdown 文本转换为 HTML
    """
    # extensions 参数用于启用额外的语法扩展，例如代码高亮、表格等
    return mark_safe(
        markdown.markdown(
            text,
            extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.codehilite",
                "markdown.extensions.toc",
                "nl2br",
                "fenced_code",
            ],
        )
    )


@register.filter(name="excerpt")
def get_excerpt(text):
    """
    取正文前 n 个字符作为摘要
    """

    return text[:200] + "..."
