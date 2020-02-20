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

from read.constants import PUBLIC_KEY_LENGTH_ACADEMIC_YEAR


def generate_academic_year_key():
    return get_random_string(PUBLIC_KEY_LENGTH_ACADEMIC_YEAR)


class AcademicYear(models.Model):
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_ACADEMIC_YEAR, default=generate_academic_year_key, unique=True)
    name = models.CharField(max_length=20,null=False,blank=False)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_years'

    def __str__(self):
        return self.name
