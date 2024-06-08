import os

from dikureads import app


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.shelf_id, item.shelf_name)

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]



