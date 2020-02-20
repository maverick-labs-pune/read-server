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

from read.constants import PUBLIC_KEY_LENGTH_NGO, PUBLIC_KEY_LENGTH_LEVEL


def generate_ngo_key():
    return get_random_string(PUBLIC_KEY_LENGTH_NGO)


class NGO(models.Model):
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_NGO, default=generate_ngo_key, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False,unique=True)
    address = models.CharField(max_length=200, null=False, blank=False)
    logo = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ngos'

    def __str__(self):
        return self.name


class Level(models.Model):
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_LEVEL, default=generate_ngo_key, unique=True)
    rank = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True, blank=True)
    mr_in = models.CharField(max_length=50, null=False, blank=False)
    en_in = models.CharField(max_length=50, null=False, blank=False)
    ngo = models.ForeignKey('ngos.NGO', null=False, blank=False, on_delete=models.PROTECT)
    is_evaluation = models.BooleanField(default=False, blank=True)
    is_regular = models.BooleanField(default=False, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'levels'
        unique_together= ('ngo','rank',)

    def __str__(self):
        return self.en_in

