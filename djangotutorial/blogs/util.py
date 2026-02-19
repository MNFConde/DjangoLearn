from dataclasses import dataclass
from datetime import datetime


@dataclass
class TagData:
    name: str
    link: str


@dataclass
class ArticleData:
    datetime_info: datetime
    tag_list: list[TagData]
    title: str
    excerpt: str
    article_link: str
