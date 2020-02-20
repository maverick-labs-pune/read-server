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
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ngos.models import NGO
from ngos.serializers import NGOSerializer
from schools.models import School, SchoolAcademicYear, SchoolCategory, SchoolType, SchoolMedium, Standard, \
    SchoolFunders, ClassroomFunders


class SchoolSerializer(ModelSerializer):
    ngo = NGOSerializer(read_only=True)
    ngo_key = SlugRelatedField(source='ngo', slug_field='key', queryset=NGO.objects.all())
    school_category_id = SlugRelatedField(source="school_category", slug_field="id",
                                          queryset=SchoolCategory.objects.all())
    school_type_id = SlugRelatedField(source="school_type", slug_field="id", queryset=SchoolType.objects.all())
    medium_id = SlugRelatedField(source="medium", slug_field="id", queryset=SchoolMedium.objects.all())
    is_active = BooleanField(default=True)

    class Meta:
        model = School
        depth = 1
        exclude = ('id',)


class SchoolAcademicYearSerializer(ModelSerializer):
    school = SchoolSerializer()

    class Meta:
        model = SchoolAcademicYear
        fields = '__all__'


class SchoolCategorySerializer(ModelSerializer):
    class Meta:
        model = SchoolCategory
        fields = '__all__'


class SchoolTypeSerializer(ModelSerializer):
    class Meta:
        model = SchoolType
        fields = '__all__'


class SchoolMediumSerializer(ModelSerializer):
    class Meta:
        model = SchoolMedium
        fields = '__all__'


class StandardSerializer(ModelSerializer):
    is_active = BooleanField(default=True)

    class Meta:
        model = Standard
        depth = 2
        fields = '__all__'


class SchoolFundersSerializer(ModelSerializer):
    class Meta:
        model = SchoolFunders
        depth = 2
        fields = '__all__'


class ClassroomFundersSerializer(ModelSerializer):
    class Meta:
        model = ClassroomFunders
        depth = 2
        fields = '__all__'
