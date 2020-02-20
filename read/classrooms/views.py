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

import base64

import datetime
from django.db import transaction, DatabaseError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from openpyxl import load_workbook
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from academic_years.models import AcademicYear
from classrooms.models import Classroom, ClassroomAcademicYear
from classrooms.schemas import ClassroomSchema
from classrooms.serializers import ClassroomSerializer, ClassroomAcademicYearSerializer
from classrooms.validators import validate_student_request, \
    validate_students_file_export, validate_students_file_import
from read.constants import FileType, STUDENT_WORKSHEET_NAME, FEMALE, MALE, ERROR_403_JSON, DEFAULT_WORKSHEET_NAME
from read.utils import write_to_excel, create_file_upload_error, create_file_upload_serializer_error, \
    create_response_data, create_serializer_error, create_response_error, request_user_belongs_to_classroom_ngo
from students.models import Student
from students.serializers import StudentSerializer
from students.validators import validate_student_file_excel_content
from users.permissions import CanImportStudent, CanExportStudent, PERMISSION_CAN_VIEW_SCHOOL, has_permission, \
    CanDeleteClassroom, CanAddStudent


class ClassroomViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_VIEW_SCHOOL):
            return Response(status=403, data=ERROR_403_JSON())
        queryset = Classroom.objects.all()
        item = get_object_or_404(queryset, key=pk)
        serializer = ClassroomSerializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], permission_classes=[CanDeleteClassroom])
    def deactivate_classroom(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(key=pk)
        except Classroom.DoesNotExist:
            return Response(status=404)

        if not request_user_belongs_to_classroom_ngo(request, classroom):
            return Response(status=403, data=ERROR_403_JSON())

        classroom.delete()
        return Response(status=204)

    @action(detail=True, methods=['POST'], permission_classes=[CanAddStudent], schema=ClassroomSchema.add_students())
    def add_student(self, request, pk=None):
        is_valid, error = validate_student_request(request)
        if not is_valid:
            return Response(status=400, data=create_response_data(error))

        academic_year_key = request.data.get('academic_year')
        try:
            classroom = Classroom.objects.get(key=pk)
            academic_year = AcademicYear.objects.get(key=academic_year_key)
        except (Classroom.DoesNotExist, AcademicYear.DoesNotExist):
            return Response(status=404)

        if not request_user_belongs_to_classroom_ngo(request, classroom):
            return Response(status=403, data=ERROR_403_JSON())

        data = request.data.copy()
        with transaction.atomic():
            student_serializer = StudentSerializer(data=data)
            if student_serializer.is_valid():
                student_serializer.save()
                classroom_data = request.data.copy()
                classroom_data['student_id'] = student_serializer.data.get('id')
                classroom_data['academic_year_id'] = academic_year.id
                classroom_data['classroom_id'] = classroom.id
                classroom_serializer = ClassroomAcademicYearSerializer(data=classroom_data)
                if classroom_serializer.is_valid():
                    classroom_serializer.save()
                    return Response(status=200)
                else:
                    return Response(status=400, data=create_serializer_error(classroom_serializer))
            else:
                return Response(status=400, data=create_serializer_error(student_serializer))

    @action(methods=['POST'], detail=True, permission_classes=[CanImportStudent])
    def import_students(self, request, pk=None):
        is_valid, error_message = validate_students_file_import(request)
        if not is_valid:
            return Response(status=400, data=create_response_data(error_message))

        try:
            classroom = Classroom.objects.get(key=pk)
        except Classroom.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_classroom_ngo(request, classroom):
            return Response(status=403, data=ERROR_403_JSON())

        academic_year_key = request.POST.get('academic_year')
        try:
            academic_year = AcademicYear.objects.get(key=academic_year_key)
        except AcademicYear.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        file_in_memory = request.FILES['file'].read()
        workbook = load_workbook(filename=BytesIO(file_in_memory))
        try:
            worksheet = workbook[STUDENT_WORKSHEET_NAME]
        except KeyError as e:
            pass

        try:
            worksheet = workbook[DEFAULT_WORKSHEET_NAME]
        except KeyError as e:
            return Response(create_response_data("Incorrect excel sheet name"))
        rows = list(worksheet.rows)
        is_valid, error_message = validate_student_file_excel_content(rows)
        if not is_valid:
            return Response(status=400, data=create_response_data(error_message))

        response = []
        try:
            with transaction.atomic():
                error_in_file = False
                for index, row in enumerate(rows):
                    if index == 0:
                        continue
                    key = str(row[0].value).strip() if row[0].value else None
                    first_name = str(row[1].value).strip() if row[1].value else None
                    middle_name = str(row[2].value).strip() if row[2].value else None
                    last_name = str(row[3].value).strip() if row[3].value else None
                    address = str(row[4].value).strip() if row[4].value else None
                    gender = str(row[5].value).strip() if row[5].value else None
                    mother_tongue = str(row[6].value).strip() if row[6].value else None
                    birth_date_string = row[7].value
                    has_attended_preschool = str(row[8].value).strip() if row[8].value else None

                    if key is None and first_name is None and last_name is None and gender is None and birth_date_string is None:
                        continue

                    if gender and gender.lower() == "female":
                        gender = FEMALE
                    elif gender and gender.lower() == "male":
                        gender = MALE
                    else:
                        error_in_file = True
                        response.append(create_file_upload_error(index, 'gender', 'Value must be Female or Male'))
                        continue

                    birth_date = None
                    if birth_date_string:
                        try:
                            if type(birth_date_string) is not datetime.datetime:
                                birth_date_string = birth_date_string.strip() if row[7].value else None
                                birth_date = datetime.datetime.strptime(birth_date_string, "%Y-%m-%d").date()
                            else:
                                birth_date = birth_date_string.date()
                        except ValueError:
                            error_in_file = True
                            response.append(create_file_upload_error(index, 'birth_date', 'Value must be yyyy-mm-dd'))
                            continue
                    else:
                        error_in_file = True
                        response.append(create_file_upload_error(index, 'birth_date', 'Value must be yyyy-mm-dd'))
                        continue

                    if has_attended_preschool:
                        if has_attended_preschool.lower() == "yes":
                            has_attended_preschool = True
                        elif has_attended_preschool.lower() == "no":
                            has_attended_preschool = False
                        else:
                            error_in_file = True
                            response.append(create_file_upload_error(index, 'has_attended_preschool',
                                                                     'Value must be yes or no'))
                            continue

                    student_data = {
                        'first_name': first_name,
                        'middle_name': middle_name,
                        'last_name': last_name,
                        'address': address,
                        'gender': gender,
                        'mother_tongue': mother_tongue,
                        'birth_date': birth_date,
                        'has_attended_preschool': has_attended_preschool,
                    }

                    if key:
                        student = Student.objects.filter(key=key).first()
                        if not student:
                            # Student does not exist
                            error_in_file = True
                            response.append(create_file_upload_error(index, 'key',
                                                                     'Student with specified key does not exist'))
                            continue

                        student_serializer = StudentSerializer(student, data=student_data)
                        if student_serializer.is_valid():
                            student_serializer.save()
                        else:
                            response.append(create_file_upload_serializer_error(index, student_serializer.errors))

                        classroom_academic_year, created = ClassroomAcademicYear.objects.get_or_create(
                            student=student,
                            classroom=classroom,
                            academic_year=academic_year,
                        )
                    else:

                        # Create the student and add him/her to the classroomacademicyear
                        student_serializer = StudentSerializer(data=student_data)
                        if student_serializer.is_valid():
                            # Check if another student with the same credentials exists
                            students = Student.objects.filter(first_name=first_name, last_name=last_name, gender=gender)
                            duplicate_students = ClassroomAcademicYear.objects.filter(student__in=students,
                                                                                      classroom=classroom,
                                                                                      academic_year=academic_year)
                            if duplicate_students:
                                response.append(create_file_upload_error(index, 'student',
                                                                         'Student with the same name, gender and dob exists in the same classroom'))
                            else:
                                student = student_serializer.save()
                                ClassroomAcademicYear.objects.create(
                                    student=student,
                                    classroom=classroom,
                                    academic_year=academic_year,
                                )
                                print("Creating new students:")
                        else:
                            error_in_file = True
                            response.append(create_file_upload_serializer_error(index, student_serializer.errors))

                if error_in_file:
                    raise DatabaseError
        except DatabaseError:
            pass

        return Response(status=200, data=create_response_data(response))

    @action(methods=['GET'], detail=True, permission_classes=[CanExportStudent])
    def export_students(self, request, pk=None):
        is_valid, error_message = validate_students_file_export(request)
        if not is_valid:
            return Response(status=400, data=create_response_data(error_message))
        try:
            classroom = Classroom.objects.get(key=pk)
        except Classroom.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_classroom_ngo(request, classroom):
            return Response(status=403, data=ERROR_403_JSON())

        academic_year_key = request.GET.get('academic_year')
        try:
            academic_year = AcademicYear.objects.get(key=academic_year_key)
        except AcademicYear.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        students_in_classroom = ClassroomAcademicYear.objects.filter(classroom=classroom,
                                                                     academic_year=academic_year,
                                                                     student__is_active=True).all()
        students = [student_in_classroom.student for student_in_classroom in students_in_classroom]
        excel_data = write_to_excel(FileType.STUDENT, students)
        base64_excel_data = base64.b64encode(excel_data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + STUDENT_WORKSHEET_NAME + '.xlsx'
        response.write(base64_excel_data)
        return response

    @action(detail=True, methods=['GET'])
    def students(self, request, pk=None):
        academic_year_key = request.GET.get('academic_year')
        try:
            classroom = Classroom.objects.get(key=pk)
            AcademicYear.objects.get(key=academic_year_key)
        except (Classroom.DoesNotExist, AcademicYear.DoesNotExist) as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_classroom_ngo(request, classroom):
            return Response(status=403, data=ERROR_403_JSON())

        students = Student.objects.filter(is_active=True,
                                          is_dropout=False,
                                          classroomacademicyear__classroom__key=pk,
                                          classroomacademicyear__classroom__is_active=True,
                                          classroomacademicyear__academic_year__key=academic_year_key)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def delete_student(self, request, pk=None):
        student_key = request.data.get('student')
        try:
            student = Student.objects.get(key=student_key)
            classroom = Classroom.objects.get(key=pk)

        except (Student.DoesNotExist, Classroom.DoesNotExist) as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_classroom_ngo(request, classroom):
            return Response(status=403, data=ERROR_403_JSON())

        # TODO check if student belongs to previous academic years if yes don't delete student
        try:
            is_student_present_in_classroom = ClassroomAcademicYear.objects.get(student=student, classroom=classroom)
        except ClassroomAcademicYear.DoesNotExist:
            return Response(status=404, data=create_response_data("Student Does not belong to this classroom"))
        is_student_present_in_classroom.delete()
        return Response(status=204)
