import os

from flask_login import current_user

from dikureads import app
from dikureads.queries import get_book_shelfs

class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, str(item.shelf_id), item.shelf_name)

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]

def get_label_name(string):
    return string.replace("_", " ").capitalize()

class ModelChoices2:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]

user_id = current_user.id if current_user else None
print(user_id)
bookshelfs = get_book_shelfs(user_id)
bookshelfs = [Book_shelf(bookshelf).shelf_name for bookshelf in bookshelfs]

UserTypeChoices = ModelChoices2(bookshelfs)

#UserTypeChoices = ModelChoices2(['Farmer', 'Customer'])