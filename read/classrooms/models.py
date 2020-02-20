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

from read.constants import PUBLIC_KEY_LENGTH_CLASSROOM


def generate_classroom_key():
    return get_random_string(PUBLIC_KEY_LENGTH_CLASSROOM)


class Classroom(models.Model):
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_CLASSROOM, default=generate_classroom_key, unique=True)
    school = models.ForeignKey('schools.School', null=False, blank=False, on_delete=models.PROTECT)
    standard = models.ForeignKey('schools.Standard', null=False, blank=False, on_delete=models.PROTECT)
    division = models.CharField(max_length=20, null=True, blank=True)
    # TODO Decide max length of notes
    notes = models.CharField(max_length=200, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'classrooms'


class ClassroomAcademicYear(models.Model):
    academic_year = models.ForeignKey('academic_years.AcademicYear', null=False, blank=False, on_delete=models.PROTECT)
    classroom = models.ForeignKey('classrooms.Classroom', null=False, blank=False, on_delete=models.PROTECT)
    student = models.ForeignKey('students.Student', null=False, blank=False, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'classroom_academic_years'
        unique_together = ('academic_year', 'classroom', 'student')
