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

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from academic_years.models import AcademicYear
from classrooms.models import Classroom, ClassroomAcademicYear
from classrooms.serializers import ClassroomAcademicYearSerializer
from classrooms.validators import validate_student_request
from read.constants import ERROR_403_JSON
from read.utils import create_response_error, request_user_ngo_belongs_to_student_ngo, \
    request_user_ngo_belongs_to_students_ngo, get_current_academic_year
from students.models import Student
from students.serializers import StudentSerializer
from users.permissions import PERMISSION_CAN_VIEW_STUDENT, has_permission, PERMISSION_CAN_CHANGE_STUDENT, \
    CanChangeStudent, CanDeleteStudent


class StudentViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_VIEW_STUDENT):
            return Response(status=403, data=ERROR_403_JSON())

        queryset = Student.objects.all()
        student = get_object_or_404(queryset, key=pk)

        if not request_user_ngo_belongs_to_student_ngo(request, student):
            return Response(status=403, data=ERROR_403_JSON())

        # Getting all information related to Student
        resultset = ClassroomAcademicYear.objects.filter(student=student)
        serializer = ClassroomAcademicYearSerializer(resultset, many=True)
        return Response(serializer.data[0])

    def update(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_CHANGE_STUDENT):
            return Response(status=403, data=ERROR_403_JSON())
        # Validating student data
        is_valid, error = validate_student_request(request)
        if not is_valid:
            return Response(status=400, data=create_response_error(error))

        # Checking if student, classroom and academic year is preset in db
        classroom_key = request.data.get('classroom')
        academic_year_key = request.data.get('academic_year')
        try:
            student = Student.objects.get(key=pk)

            if not request_user_ngo_belongs_to_student_ngo(request, student):
                return Response(status=403, data=ERROR_403_JSON())

            classroom = Classroom.objects.get(key=classroom_key)
            academic_year = AcademicYear.objects.get(key=academic_year_key)
            classroom_academic_year = ClassroomAcademicYear.objects.get(student=student)
        except Student.DoesNotExist:
            return Response(status=404)

        serializer = StudentSerializer(student, data=request.data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                data = request.data.copy()
                data["student_id"] = student.id
                data["academic_year_id"] = academic_year.id
                data["classroom_id"] = classroom.id
                classroom_academic_year_serializer = ClassroomAcademicYearSerializer(classroom_academic_year, data=data)
                if classroom_academic_year_serializer.is_valid():
                    classroom_academic_year_serializer.save()
                    return Response(status=204)
                else:
                    return Response(classroom_academic_year_serializer.errors, status=400)
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=['POST'], permission_classes=[CanChangeStudent])
    def mark_as_dropout(self, request, pk=None):
        academic_year_key = request.data.get('academicYear')
        current_academic_year_name = get_current_academic_year()
        try:
            student = Student.objects.get(key=pk)
            academic_year = AcademicYear.objects.get(key=academic_year_key)
            current_academic_year = AcademicYear.objects.get(name=current_academic_year_name)
            classroom_academic_year = ClassroomAcademicYear.objects.get(student__key=student.key,
                                                                        academic_year__key=academic_year.key)
        except (Student.DoesNotExist, AcademicYear.DoesNotExist, ClassroomAcademicYear.DoesNotExist) as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_ngo_belongs_to_student_ngo(request, student):
            return Response(status=403, data=ERROR_403_JSON())

        if current_academic_year.key == academic_year.key:
            classroom_academic_year.is_active = False
            classroom_academic_year.save()
            student.is_dropout = True
            student.is_active = False
            student.save()
            return Response(status=200)
        else:
            return Response(status=400, data=create_response_error("Cannot mark student as dropout for previous year"))

    @action(detail=False, methods=['POST'], permission_classes=[CanDeleteStudent])
    def deactivate_students(self, request):
        students = request.data.get('students')
        student_keys = json.loads(students)

        if not request_user_ngo_belongs_to_students_ngo(request, student_keys):
            return Response(status=403, data=ERROR_403_JSON())

        students_list = Student.objects.filter(key__in=student_keys, )
        for student in students_list:
            student.is_active = False
            student.save()
        return Response(status=204)
