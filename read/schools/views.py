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

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from read.common import convert_to_dropdown
from read.constants import ERROR_403_JSON
from read.utils import request_user_ngo_belongs_to_schools_ngo, request_user_ngo_belongs_to_school_ngo, \
    create_serializer_error
from schools.models import School, SchoolAcademicYear, SchoolCategory, SchoolType, SchoolMedium, Standard, \
    SchoolFunders, ClassroomFunders
from schools.serializers import SchoolSerializer, SchoolAcademicYearSerializer, SchoolCategorySerializer, \
    SchoolTypeSerializer, SchoolMediumSerializer, StandardSerializer, SchoolFundersSerializer, \
    ClassroomFundersSerializer
from users.permissions import has_permission, \
    PERMISSION_CAN_VIEW_SCHOOL, PERMISSION_CAN_CHANGE_SCHOOL, CanViewSchool, CanDeleteSchool


class SchoolViewSet(ViewSet):

    def list(self, request):
        if not has_permission(request, PERMISSION_CAN_VIEW_SCHOOL):
            return Response(status=403, data=ERROR_403_JSON())
        queryset = School.objects.all()
        serializer = SchoolSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_VIEW_SCHOOL):
            return Response(status=403, data=ERROR_403_JSON())
        queryset = School.objects.all()
        item = get_object_or_404(queryset, key=pk)
        serializer = SchoolSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_CHANGE_SCHOOL):
            return Response(status=403, data=ERROR_403_JSON())

        school_category_key = request.data.get('school_category')
        school_type_key = request.data.get('school_type')
        medium_key = request.data.get('medium')

        try:
            school = School.objects.get(key=pk)
            if not request_user_ngo_belongs_to_school_ngo(request, school):
                return Response(status=403, data=ERROR_403_JSON())

            school_category = SchoolCategory.objects.get(name=school_category_key)
            school_type = SchoolType.objects.get(name=school_type_key)
            medium = SchoolMedium.objects.get(name=medium_key)
        except (SchoolCategory.DoesNotExist, SchoolType.DoesNotExist, SchoolMedium.DoesNotExist) as e:
            return Response(status=404)

        data = request.data.copy()
        data['school_category_id'] = school_category.id
        data['school_type_id'] = school_type.id
        data['medium_id'] = medium.id
        data['latitude'] = None
        data['longitude'] = None
        serializer = SchoolSerializer(school, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data=create_serializer_error(serializer), status=400)

    @action(detail=False, methods=['POST'], permission_classes=[CanDeleteSchool])
    def deactivate_school(self, request, pk=None):
        keys = request.data.get('keys')
        school_keys = json.loads(keys)

        if not request_user_ngo_belongs_to_schools_ngo(request, school_keys):
            return Response(status=403, data=ERROR_403_JSON())

        schools = School.objects.filter(key__in=school_keys)
        for school in schools:
            school.is_active = False
            school.save()
        return Response(status=204)

    @action(detail=False, methods=['GET'], permission_classes=[CanViewSchool])
    def get_school_mediums(self, request):
        mediums = convert_to_dropdown(SchoolMedium.MEDIUMS)
        return Response(mediums)

    @action(detail=False, methods=['GET'], permission_classes=[CanViewSchool])
    def get_school_categories(self, request):
        categories = convert_to_dropdown(SchoolCategory.CATEGORIES)
        return Response(categories)

    @action(detail=False, methods=['GET'], permission_classes=[CanViewSchool])
    def get_school_types(self, request):
        types = convert_to_dropdown(SchoolType.TYPES)
        return Response(types)


class SchoolAcademicYearViewSet(ViewSet):

    def list(self, request):
        queryset = SchoolAcademicYear.objects.all()
        serializer = SchoolAcademicYearSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SchoolAcademicYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = SchoolAcademicYear.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SchoolAcademicYearSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = SchoolAcademicYear.objects.get(pk=pk)
        except SchoolAcademicYear.DoesNotExist:
            return Response(status=404)
        serializer = SchoolAcademicYearSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = SchoolAcademicYear.objects.get(pk=pk)
        except SchoolAcademicYear.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SchoolCategoryViewSet(ViewSet):

    def list(self, request):
        queryset = SchoolCategory.objects.all()
        serializer = SchoolCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = SchoolCategory.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SchoolCategorySerializer(item)
        return Response(serializer.data)


class SchoolTypeViewSet(ViewSet):

    def list(self, request):
        queryset = SchoolType.objects.all()
        serializer = SchoolTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = SchoolType.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SchoolTypeSerializer(item)
        return Response(serializer.data)


class SchoolMediumViewSet(ViewSet):

    def list(self, request):
        queryset = SchoolMedium.objects.all()
        serializer = SchoolMediumSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = SchoolMedium.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SchoolMediumSerializer(item)
        return Response(serializer.data)


class StandardViewSet(ViewSet):

    def list(self, request):
        queryset = Standard.objects.all()
        serializer = StandardSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Standard.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = StandardSerializer(item)
        return Response(serializer.data)


class SchoolFundersViewSet(ViewSet):

    def list(self, request):
        queryset = SchoolFunders.objects.all()
        serializer = SchoolFundersSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SchoolFundersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = SchoolFunders.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SchoolFundersSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = SchoolFunders.objects.get(pk=pk)
        except SchoolFunders.DoesNotExist:
            return Response(status=404)
        serializer = SchoolFundersSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = SchoolFunders.objects.get(pk=pk)
        except SchoolFunders.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ClassroomFundersViewSet(ViewSet):

    def list(self, request):
        queryset = ClassroomFunders.objects.all()
        serializer = ClassroomFundersSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClassroomFundersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = ClassroomFunders.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ClassroomFundersSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = ClassroomFunders.objects.get(pk=pk)
        except ClassroomFunders.DoesNotExist:
            return Response(status=404)
        serializer = ClassroomFundersSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = ClassroomFunders.objects.get(pk=pk)
        except ClassroomFunders.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
