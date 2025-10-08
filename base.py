# base.py
from abc import ABC, abstractmethod

class MuseumItem(ABC):
    def __init__(self, title, views):
        self.title = title
        self.views = views

    @abstractmethod
    def get_type_name(self):
        pass

    def __str__(self):
        return f"{self.get_type_name()} «{self.title}» — {self.views} человек"

    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}', views={self.views})"