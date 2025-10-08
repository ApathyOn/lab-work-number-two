# exhibit.py
from base import Viewable

class Exhibit(Viewable):
    def get_type_name(self):
        return "Экспонат"