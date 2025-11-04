from abc import ABC, abstractmethod

class MuseumItem(ABC):
    def init(self, title, rating=None):
        self.title = title
        self.rating = rating

    @abstractmethod
    def get_type_name(self):
        pass

    def str(self):
        rating_str = f" — {self.rating}/10" if self.rating is not None else " — оценка не выставлена"
        return f"{self.get_type_name()} «{self.title}»{rating_str}"

    def repr(self):
        return f"{self.class.name}(title='{self.title}', rating={self.rating})"