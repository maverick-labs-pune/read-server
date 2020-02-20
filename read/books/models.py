#  Copyright (c) 2020. Maverick Labs
#    This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as,
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext

from read.constants import PUBLIC_KEY_LENGTH_BOOK, LENGTH_BOOK_NAME_FIELD, LENGTH_BOOK_AUTHOR_FIELD, \
    LENGTH_BOOK_PUBLISHER_FIELD, BOOK_LEVEL_1, BOOK_LEVEL_2, BOOK_LEVEL_3, BOOK_LEVEL_4
from users.permissions import PERMISSION_CAN_IMPORT_BOOKS, PERMISSION_CAN_EXPORT_BOOKS


def generate_book_key():
    return get_random_string(PUBLIC_KEY_LENGTH_BOOK)


class Book(models.Model):
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_BOOK, default=generate_book_key, unique=True)
    name = models.CharField(max_length=LENGTH_BOOK_NAME_FIELD, null=False, blank=False)
    author = models.CharField(max_length=LENGTH_BOOK_AUTHOR_FIELD, null=True, blank=True)
    level = models.ForeignKey('books.BookLevel', null=True, blank=True, on_delete=models.PROTECT)
    ngo = models.ForeignKey('ngos.NGO', blank=False, null=False, on_delete=models.PROTECT)
    publisher = models.CharField(max_length=LENGTH_BOOK_PUBLISHER_FIELD, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True, null=False)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        permissions = (
            PERMISSION_CAN_IMPORT_BOOKS[0:2],
            PERMISSION_CAN_EXPORT_BOOKS[0:2],
        )


class BookLevel(models.Model):
    BOOK_LEVELS = (
        (BOOK_LEVEL_1, "Level 1"),
        (BOOK_LEVEL_2, "Level 2"),
        (BOOK_LEVEL_3, "Level 3"),
        (BOOK_LEVEL_4, "Level 4"),
    )
    name = models.CharField(max_length=100, null=False, blank=False, choices=BOOK_LEVELS)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book_levels'


class Inventory(models.Model):
    GOOD = 'go'
    DAMAGED = 'da'
    LOST = 'lo'
    STATUSES = (
        (GOOD, "Good"),
        (DAMAGED, "Damaged"),
        (LOST, "Lost"),
    )
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_BOOK, default=generate_book_key, unique=True)
    book = models.ForeignKey('books.Book', null=False, blank=False, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=30, null=False, blank=False)
    added_date_time = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUSES, null=False, blank=False)
    is_active = models.BooleanField(default=True, blank=True, null=False)
    creation_time = models.DateTimeField(null=True, auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'inventory'
        unique_together = ('book', 'serial_number')
