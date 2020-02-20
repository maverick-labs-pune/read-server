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
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from academic_years.serializers import AcademicYearSerializer
from academic_years.models import AcademicYear
from read.utils import get_current_academic_year


class AcademicYearViewSet(ViewSet):

    def list(self, request):
        queryset = AcademicYear.objects.all()
        serializer = AcademicYearSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = AcademicYear.objects.all()
        item = get_object_or_404(queryset, key=pk)
        serializer = AcademicYearSerializer(item)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def get_current_academic_year(self, request):
        year = get_current_academic_year()
        try:
            academic_year = AcademicYear.objects.get(name=year)
        except AcademicYear.DoesNotExist as e:
            return Response(status=404, data={"message": str(e)})

        serializer = AcademicYearSerializer(academic_year)
        return Response(serializer.data)
