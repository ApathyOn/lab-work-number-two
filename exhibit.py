# exhibit.py
from base import MuseumItem

class Exhibit(MuseumItem):
    def get_type_name(self):
        return "Экспонат"