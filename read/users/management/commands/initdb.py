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

import logging

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from academic_years.models import AcademicYear
from books.models import BookLevel
from read.constants import MEDIUMS, SCHOOL_TYPES, SCHOOL_CATEGORY, STANDARDS, GroupType, ACADEMIC_YEARS, BOOK_LEVELS
from schools.models import SchoolMedium, SchoolType, SchoolCategory, Standard
from users.permissions import PERMISSIONS_READ_ADMIN


class Command(BaseCommand):
    help = 'Creates groups in the database if not created'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        try:
            django_group = Group.objects.get(name=GroupType.READ_ADMIN.value)
            self.stdout.write(self.style.SUCCESS('Group "%s" exists in database' % GroupType.READ_ADMIN.value))
        except Exception:
            Group.objects.create(name=GroupType.READ_ADMIN.value)
            self.stdout.write(self.style.SUCCESS('Added Group "%s" to database' % GroupType.READ_ADMIN.value))

        for book_level in BOOK_LEVELS:
            try:
                BookLevel.objects.get(name=book_level)
                self.stdout.write(self.style.SUCCESS('Book level "%s" exists in database' % book_level))
                continue
            except BookLevel.DoesNotExist:
                BookLevel.objects.create(name=book_level)
                self.stdout.write(self.style.SUCCESS('Book level "%s" medium to database' % book_level))

        for medium in MEDIUMS:
            try:
                SchoolMedium.objects.get(name=medium)
                self.stdout.write(self.style.SUCCESS('Medium "%s" exists in database' % medium))
                continue
            except SchoolMedium.DoesNotExist:
                SchoolMedium.objects.create(name=medium)
                self.stdout.write(self.style.SUCCESS('Added "%s" medium to database' % medium))

        for types in SCHOOL_TYPES:
            try:
                SchoolType.objects.get(name=types)
                self.stdout.write(self.style.SUCCESS('School type "%s" exists in database' % types))
                continue
            except SchoolType.DoesNotExist:
                SchoolType.objects.create(name=types)
                self.stdout.write(self.style.SUCCESS('Added "%s" school type to database' % types))

        for category in SCHOOL_CATEGORY:
            try:
                SchoolCategory.objects.get(name=category)
                self.stdout.write(self.style.SUCCESS('School category "%s" exists in database' % category))
                continue
            except SchoolCategory.DoesNotExist:
                SchoolCategory.objects.create(name=category)
                self.stdout.write(self.style.SUCCESS('Added "%s" school category to database' % category))

        for standard in STANDARDS:
            try:
                Standard.objects.get(name=standard)
                self.stdout.write(self.style.SUCCESS('Standard "%s" exists in database' % standard))
                continue
            except Standard.DoesNotExist:
                Standard.objects.create(name=standard)
                self.stdout.write(self.style.SUCCESS('Added "%s" standard to database' % standard))

        for academic_year in ACADEMIC_YEARS:
            try:
                AcademicYear.objects.get(name=academic_year)
                self.stdout.write(self.style.SUCCESS('Academic year "%s" exists in database' % academic_year))
                continue
            except AcademicYear.DoesNotExist:
                AcademicYear.objects.create(name=academic_year)
                self.stdout.write(self.style.SUCCESS('Added "%s" Academic year to database' % academic_year))

        try:
            read_admin_group = Group.objects.get(name=GroupType.READ_ADMIN.value)
            for code_name, name, _ in PERMISSIONS_READ_ADMIN:
                try:
                    permission = Permission.objects.get(codename=code_name, name=name)
                    read_admin_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS('Added "%s" permission to read_admin_group' % name))
                except Permission.DoesNotExist:
                    logging.warning("Permission not found with codename '{}' name '{}'.".format(code_name, name))
                    continue


        except Group.DoesNotExist:
            self.stdout.write(self.style.SUCCESS('Group "READ ADMIN" does not exist in database'))
        #
        #
        # try:
        #     ngo_admin_group = Group.objects.get(name=NGO_ADMIN)
        #     for code_name, name, _ in PERMISSIONS_NGO_ADMIN:
        #         try:
        #             model_add_perm = Permission.objects.get(codename=code_name, name=name)
        #             ngo_admin_group.permissions.add(model_add_perm)
        #             self.stdout.write(self.style.SUCCESS('Added "%s" permission to ngo_admin_group' % name))
        #         except Permission.DoesNotExist:
        #             logging.warning("Permission not found with codename '{}' name '{}'.".format(code_name, name))
        #             continue
        #
        #
        # except Group.DoesNotExist:
        #     self.stdout.write(self.style.SUCCESS('Group "READ ADMIN" does not exist in database'))
