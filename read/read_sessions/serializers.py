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

from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from django.db.models import Q
from academic_years.models import AcademicYear
from books.models import Book, Inventory
from classrooms.models import Classroom
from ngos.models import Level
from read.constants import REGULAR, EVALUATION, SESSION_ATTENDED, SESSION_NOT_ATTENDED
from read_sessions.models import ReadSession, ReadSessionBookFairy, ReadSessionClassroom, StudentFeedback, \
    ReadSessionFeedbackBook, StudentEvaluations, ReadSessionHomeLendingBook
from students.models import Student
from students.serializers import StudentSerializer, StudentFeedBackBookSerializer, \
    StudentHomeLendingInventoryBookSerializer, StudentLevelSerializer
from users.models import User


class ReadSessionSerializer(ModelSerializer):
    academic_year_id = SlugRelatedField(source='academic_year', slug_field='id', queryset=AcademicYear.objects.all())

    class Meta:
        model = ReadSession
        depth = 3
        fields = '__all__'

        extra_fields = ['readsessionclassroom_set', 'readsessionbookfairy_set']

    # Adding extra fields which are not present in fields
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ReadSessionSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class ReadSessionBookFairySerializer(ModelSerializer):
    read_session_id = SlugRelatedField(source="read_session", slug_field="id", queryset=ReadSession.objects.all())
    user_id = SlugRelatedField(source="book_fairy", slug_field="id", queryset=User.objects.all())

    class Meta:
        model = ReadSessionBookFairy
        depth = 2
        exclude = ('id',)


class ReadSessionClassroomSerializer(ModelSerializer):
    read_session_id = SlugRelatedField(source="read_session", slug_field="id", queryset=ReadSession.objects.all())
    classroom_id = SlugRelatedField(source="classroom", slug_field="id", queryset=Classroom.objects.all())
    students = SerializerMethodField(read_only=True)

    def get_students(self, obj):
        query_set = Student.objects.filter(classroomacademicyear__classroom__readsessionclassroom__id=obj.id,
                                           classroomacademicyear__academic_year__key=obj.read_session.academic_year.key)
        serializer = StudentLevelSerializer(query_set, many=True)
        return serializer.data

    class Meta:
        model = ReadSessionClassroom
        depth = 2
        exclude = ('id',)


class StudentFeedbackSerializer(ModelSerializer):
    read_session_id = SlugRelatedField(source="read_session", slug_field="id", queryset=ReadSession.objects.all())
    student_id = SlugRelatedField(source="student", slug_field="id", queryset=Student.objects.all())
    level_id = SlugRelatedField(source="level", slug_field="id", queryset=Level.objects.all(), allow_empty=True,
                                allow_null=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = StudentFeedback
        depth = 2
        exclude = ('id',)


class ReadSessionFeedbackBookSerializer(ModelSerializer):
    read_session_id = SlugRelatedField(source="read_session", slug_field="id", queryset=ReadSession.objects.all())
    student_id = SlugRelatedField(source="student", slug_field="id", queryset=Student.objects.all())
    book_id = SlugRelatedField(source="book", slug_field="id", queryset=Book.objects.all())
    inventory_id = SlugRelatedField(source="inventory", slug_field="id", queryset=Inventory.objects.all())

    class Meta:
        model = ReadSessionFeedbackBook
        depth = 2
        exclude = ('id',)


class ReadSessionHomeLendingBookSerializer(ModelSerializer):
    read_session_id = SlugRelatedField(source="read_session", slug_field="id", queryset=ReadSession.objects.all())
    student_id = SlugRelatedField(source="student", slug_field="id", queryset=Student.objects.all())
    book_id = SlugRelatedField(source="book", slug_field="id", queryset=Book.objects.all())
    inventory_id = SlugRelatedField(source="inventory", slug_field="id", queryset=Inventory.objects.all())

    class Meta:
        model = ReadSessionHomeLendingBook
        depth = 2
        exclude = ('id',)


class StudentEvaluationsSerializer(ModelSerializer):
    read_session_id = SlugRelatedField(source="read_session", slug_field="id", queryset=ReadSession.objects.all())
    student_id = SlugRelatedField(source="student", slug_field="id", queryset=Student.objects.all())
    level_id = SlugRelatedField(source="level", slug_field="id", queryset=Level.objects.all(), allow_empty=True,
                                allow_null=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = StudentEvaluations
        depth = 2
        exclude = ('id',)


class StudentEvaluationsFeedbackBookSerializer(ModelSerializer):
    student = SerializerMethodField(read_only=True)

    def get_student(self, obj):
        serializer = StudentFeedBackBookSerializer(obj.student, read_only=True, session=obj.read_session.key)
        return serializer.data

    class Meta:
        model = StudentEvaluations
        depth = 2
        exclude = ('id',)


class StudentFeedbackAndFeedbackBookSerializer(ModelSerializer):
    student = SerializerMethodField(read_only=True)

    def get_student(self, obj):
        serializer = StudentFeedBackBookSerializer(obj.student, read_only=True, session=obj.read_session.key)
        return serializer.data

    class Meta:
        model = StudentFeedback
        depth = 2
        exclude = ('id',)


class StudentHomeLendingBookSerializer(ModelSerializer):
    student = SerializerMethodField(read_only=True)

    def get_student(self, obj):
        serializer = StudentHomeLendingInventoryBookSerializer(obj.student, read_only=True,
                                                               session=obj.read_session.key)
        return serializer.data

    class Meta:
        model = ReadSessionHomeLendingBook
        depth = 2
        exclude = ('id', 'read_session', 'book', 'inventory')


class ReadSessionBookFairyReportSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.attendance = kwargs.pop('attendance', None)
        super(ReadSessionBookFairyReportSerializer, self).__init__(*args, **kwargs)

    students = SerializerMethodField(read_only=True)

    def get_students(self, obj):

        if self.attendance == SESSION_ATTENDED:
            queryset = Student.objects.filter(
                Q(
                    classroomacademicyear__classroom__readsessionclassroom__read_session__studentfeedback__attendance=True)
                |
                Q(
                    classroomacademicyear__classroom__readsessionclassroom__read_session__studentevaluations__attendance=True),
                classroomacademicyear__classroom__readsessionclassroom__read_session__key=obj.key)
        elif self.attendance == SESSION_NOT_ATTENDED:
            queryset = Student.objects.filter(
                Q(
                    classroomacademicyear__classroom__readsessionclassroom__read_session__studentfeedback__attendance=False)
                |
                Q(
                    classroomacademicyear__classroom__readsessionclassroom__read_session__studentfeedback__attendance=False),
                classroomacademicyear__classroom__readsessionclassroom__read_session__key=obj.key)
        else:
            queryset = Student.objects.filter(
                classroomacademicyear__classroom__readsessionclassroom__read_session__key=obj.key)

        student_response = []
        for student in queryset:
            if student.studentfeedback_set.filter(
                    read_session=obj).first() is not None or student.studentevaluations_set.filter(read_session=obj).first() is not None:

                books = ReadSessionFeedbackBook.objects.filter(student=student, read_session=obj)\
                    .distinct('book__name').values_list('book__name', flat=True)

                student_level = {"name": student.first_name + " " + student.last_name,
                                 "datetime": obj.start_date_time.strftime(
                                     "%a %d %b %H:%M") + " - " + obj.end_date_time.strftime("%H:%M"),
                                 "books": books}

                if obj.type == REGULAR:
                    level = student.studentfeedback_set.filter(read_session=obj).first().level
                    student_level["level"] = "NA" if level is None else student.studentfeedback_set.filter(
                        read_session=obj).first().level.en_in
                    student_level["comments"] = student.studentfeedback_set.filter(read_session=obj).first().comments
                    student_level["attendance"] = student.studentfeedback_set.filter(
                        read_session=obj).first().attendance

                if obj.type == EVALUATION:
                    level = student.studentfeedback_set.filter(read_session=obj).first().level
                    student_level["level"] = "NA" if level is None else student.studentevaluations_set.filter(
                        read_session=obj).first().level.en_in
                    student_level["comments"] = student.studentevaluations_set.filter(read_session=obj).first().comments
                    student_level["attendance"] = student.studentevaluations_set.filter(
                        read_session=obj).first().attendance

                student_response.append(student_level)
        return student_response

    class Meta:
        model = ReadSession
        fields = ('key', 'students', 'type')
