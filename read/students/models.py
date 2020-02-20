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
from django.utils.translation import gettext as _

from read.constants import PUBLIC_KEY_LENGTH_STUDENT, MALE, FEMALE
from users.permissions import PERMISSION_CAN_IMPORT_STUDENTS, PERMISSION_CAN_EXPORT_STUDENTS


def generate_student_key():
    return get_random_string(PUBLIC_KEY_LENGTH_STUDENT)


class Student(models.Model):
    GENDERS = (
        (MALE, _("MALE")),
        (FEMALE, _("FEMALE")),
    )
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_STUDENT, default=generate_student_key, unique=True)
    first_name = models.CharField(max_length=100,null=False, blank=False)
    middle_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100,null=False, blank=False)
    address = models.CharField(max_length=300, blank=False)
    gender = models.CharField(max_length=10, choices=GENDERS,null=False, blank=False)
    mother_tongue = models.CharField(max_length=50,null=False, blank=False)
    birth_date = models.DateField(null=False,blank=False)
    is_dropout = models.BooleanField(default=False, blank=False)
    has_attended_preschool = models.BooleanField(null=True,blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def name(self):
        return ''.join(
            [self.first_name, ' ', self.middle_name, ' ', self.last_name])

    class Meta:
        db_table = 'students'
        permissions = (
            PERMISSION_CAN_IMPORT_STUDENTS[0:2],
            PERMISSION_CAN_EXPORT_STUDENTS[0:2],
        )
