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

from read.constants import PUBLIC_KEY_LENGTH_SCHOOL, SCHOOL_MEDIUM_ENGLISH, SCHOOL_MEDIUM_MARATHI, SCHOOL_MEDIUM_URDU, \
    SCHOOL_TYPE_PCMC, SCHOOL_TYPE_PMC, SCHOOL_TYPE_ZP, SCHOOL_TYPE_PRIVATE, SCHOOL_CATEGORY_BOYS, SCHOOL_CATEGORY_GIRLS, \
    SCHOOL_CATEGORY_CO_ED, LENGTH_SCHOOL_NAME_FIELD, LENGTH_SCHOOL_ADDRESS_FIELD, SCHOOL_MEDIUM_HINDI, \
    SCHOOL_MEDIUM_KANNADA
from users.permissions import PERMISSION_CAN_IMPORT_SCHOOLS, PERMISSION_CAN_EXPORT_SCHOOLS


def generate_school_key():
    return get_random_string(PUBLIC_KEY_LENGTH_SCHOOL)


class School(models.Model):
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_SCHOOL, default=generate_school_key, unique=True)
    name = models.CharField(max_length=LENGTH_SCHOOL_NAME_FIELD, null=False, blank=False)
    address = models.CharField(max_length=LENGTH_SCHOOL_ADDRESS_FIELD, null=False, blank=False)
    pin_code = models.IntegerField(null=False, blank=False)
    ward_number = models.CharField(max_length=30, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    school_number = models.CharField(max_length=30, null=True, blank=True)
    ngo = models.ForeignKey('ngos.NGO', null=False, blank=False, on_delete=models.PROTECT)
    school_category = models.ForeignKey('schools.SchoolCategory', null=False, blank=False, on_delete=models.PROTECT)
    school_type = models.ForeignKey('schools.SchoolType', null=False, blank=False, on_delete=models.PROTECT)
    organization_name = models.CharField(max_length=100, null=True, blank=True)
    year_of_intervention = models.DateField(null=True, blank=True)
    medium = models.ForeignKey('schools.SchoolMedium', null=False, blank=False, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'schools'
        permissions = (
            PERMISSION_CAN_IMPORT_SCHOOLS[0:2],
            PERMISSION_CAN_EXPORT_SCHOOLS[0:2],
        )


class SchoolAcademicYear(models.Model):
    school = models.ForeignKey('schools.School', null=False, blank=False, on_delete=models.PROTECT)
    academic_year = models.ForeignKey('academic_years.AcademicYear', null=False, blank=False, on_delete=models.PROTECT)
    number_of_classes = models.IntegerField(null=True, blank=True)
    number_of_classrooms_available = models.IntegerField(null=True, blank=True)
    number_of_classrooms_used = models.IntegerField(null=True, blank=True)
    number_of_teachers = models.IntegerField(null=True, blank=True)
    number_of_toilets = models.IntegerField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_academic_years'


class SchoolCategory(models.Model):
    CATEGORIES = (
        (SCHOOL_CATEGORY_BOYS, "Boys"),
        (SCHOOL_CATEGORY_GIRLS, "Girls"),
        (SCHOOL_CATEGORY_CO_ED, "Co-Ed")
    )
    name = models.CharField(max_length=100, null=False, blank=False, choices=CATEGORIES)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_categories'


class SchoolType(models.Model):
    TYPES = (
        (SCHOOL_TYPE_PCMC, "PCMC"),
        (SCHOOL_TYPE_PMC, "PMC"),
        (SCHOOL_TYPE_ZP, "ZP"),
        (SCHOOL_TYPE_PRIVATE, "Private"),
    )
    name = models.CharField(max_length=100, null=False, blank=False, choices=TYPES)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_types'


class SchoolMedium(models.Model):
    MEDIUMS = (
        (SCHOOL_MEDIUM_ENGLISH, "English"),
        (SCHOOL_MEDIUM_MARATHI, "Marathi"),
        (SCHOOL_MEDIUM_URDU, "Urdu"),
        (SCHOOL_MEDIUM_HINDI, "Hindi"),
        (SCHOOL_MEDIUM_KANNADA, "Kannada"),
    )
    name = models.CharField(max_length=100, null=False, blank=False, choices=MEDIUMS)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_mediums'


class Standard(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'standards'


class SchoolFunders(models.Model):
    funder = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.PROTECT)
    school = models.ForeignKey('schools.School', null=False, blank=False, on_delete=models.PROTECT)
    academic_year = models.ForeignKey('academic_years.AcademicYear', null=False, blank=False, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_funders'


class ClassroomFunders(models.Model):
    funder = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.PROTECT)
    classroom = models.ForeignKey('classrooms.Classroom', null=False, blank=False, on_delete=models.PROTECT)
    academic_year = models.ForeignKey('academic_years.AcademicYear', null=False, blank=False, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'classroom_funders'
