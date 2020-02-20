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

from rest_framework.fields import BooleanField
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from academic_years.models import AcademicYear
from classrooms.models import Classroom, ClassroomAcademicYear
from schools.models import School, Standard
from schools.serializers import SchoolSerializer
from students.models import Student


class ClassroomSerializer(ModelSerializer):
    lookup_field = 'key'
    pk_field = 'key'

    school = SchoolSerializer(read_only=True)
    school_key = SlugRelatedField(slug_field="key", queryset=School.objects.all(), source="school")
    standard_id = SlugRelatedField(slug_field="id", queryset=Standard.objects.all(), source="standard")
    is_active = BooleanField(default=True, read_only=True)

    class Meta:
        model = Classroom
        depth = 2
        exclude = ('id',)


class ClassroomTableSerializer(ModelSerializer):
    standard = StringRelatedField()

    class Meta:
        model = Classroom
        fields = ('key', 'standard', 'division',)


class ClassroomAcademicYearSerializer(ModelSerializer):
    academic_year_id = SlugRelatedField(slug_field="id", queryset=AcademicYear.objects.all(), source="academic_year")
    classroom_id = SlugRelatedField(slug_field="id", queryset=Classroom.objects.all(), source="classroom")
    student_id = SlugRelatedField(slug_field="id", queryset=Student.objects.all(), source="student")

    class Meta:
        model = ClassroomAcademicYear
        depth = 2
        exclude = ('id',)
