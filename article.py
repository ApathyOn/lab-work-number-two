# article.py
from base import MuseumItem

class Article(MuseumItem):
    def get_type_name(self):
        return "Статья"