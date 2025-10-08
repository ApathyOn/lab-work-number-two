# article.py
from base import Viewable

class Article(Viewable):
    def get_type_name(self):
        return "Статья"