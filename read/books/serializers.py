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

from rest_framework.fields import BooleanField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from books.models import Book, Inventory, BookLevel
from ngos.models import NGO
from rest_framework.relations import SlugRelatedField

from read_sessions.models import ReadSessionHomeLendingBook


class BookSerializer(ModelSerializer):
    ngo_id = SlugRelatedField(source='ngo', slug_field='id', queryset=NGO.objects.all())
    is_active = BooleanField(default=True)
    book_level_id = SlugRelatedField(source="level", slug_field="id", queryset=BookLevel.objects.all(), allow_null=True,required=False)

    class Meta:
        model = Book
        depth = 2
        exclude = ('id',)


class InventorySerializer(ModelSerializer):
    book_id = SlugRelatedField(source='book', slug_field="id", queryset=Book.objects.all())
    is_active = BooleanField(default=True)

    class Meta:
        model = Inventory
        depth = 1
        exclude = ('id',)


class InventoryActionSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super(InventoryActionSerializer, self).__init__(*args, **kwargs)

    action = SerializerMethodField(read_only=True)

    def get_action(self, obj):
        read_session_home_lending_book = ReadSessionHomeLendingBook.objects.filter(read_session__key=self.session,
                                                              inventory=obj).first()

        return read_session_home_lending_book.action if read_session_home_lending_book else None

    book_id = SlugRelatedField(source='book', slug_field="id", queryset=Book.objects.all())
    is_active = BooleanField(default=True)

    class Meta:
        model = Inventory
        depth = 1
        exclude = ('id',)
