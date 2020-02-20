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
from rest_framework.serializers import ModelSerializer

from books.models import Inventory
from books.serializers import InventorySerializer, InventoryActionSerializer
from read.constants import REGULAR, EVALUATION
from read_sessions.models import StudentEvaluations, StudentFeedback, ReadSession
from students.models import Student
from django.db.models import Q


class StudentSerializer(ModelSerializer):
    academic_year = SerializerMethodField(read_only=True)

    def get_academic_year(self, obj):
        if obj.classroomacademicyear_set.first():
            return obj.classroomacademicyear_set.first().academic_year.name
        else:
            return None

    class Meta:
        model = Student
        depth = 2
        fields = '__all__'


class StudentFeedBackBookSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super(StudentFeedBackBookSerializer, self).__init__(*args, **kwargs)

    inventory = SerializerMethodField(read_only=True)

    def get_inventory(self, obj):
        query_set = Inventory.objects.filter(readsessionfeedbackbook__student__key=obj.key,
                                             readsessionfeedbackbook__read_session__key=self.session)
        serializer = InventorySerializer(query_set, many=True)

        return serializer.data

    class Meta:
        model = Student
        depth = 2
        exclude = ('id',)


class StudentHomeLendingInventoryBookSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super(StudentHomeLendingInventoryBookSerializer, self).__init__(*args, **kwargs)

    inventory = SerializerMethodField(read_only=True)

    def get_inventory(self, obj):
        query_set = Inventory.objects.filter(readsessionhomelendingbook__student__key=obj.key,
                                             readsessionhomelendingbook__read_session__key=self.session)
        serializer = InventoryActionSerializer(query_set, many=True, session=self.session)
        return serializer.data

    class Meta:
        model = Student
        depth = 2
        exclude = ('id',)


class StudentSubmitEvaluationAndBookSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super(StudentSubmitEvaluationAndBookSerializer, self).__init__(*args, **kwargs)

    is_evaluated = SerializerMethodField(read_only=True)

    def get_is_evaluated(self, obj):
        print(obj, self.session)
        if self.session.type == REGULAR:
            return StudentFeedback.objects.filter(student=obj, read_session=self.session).exists()
        elif self.session.type == EVALUATION:
            return StudentEvaluations.objects.filter(student=obj, read_session=self.session).exists()

    class Meta:
        model = Student
        depth = 2
        exclude = ('id',)


class StudentLevelSerializer(ModelSerializer):
    academic_year = SerializerMethodField(read_only=True)
    level = SerializerMethodField(read_only=True)

    def get_academic_year(self, obj):
        if obj.classroomacademicyear_set.first():
            return obj.classroomacademicyear_set.first().academic_year.name
        else:
            return None

    def get_level(self, obj):
        level = ReadSession.objects.filter(
            Q(studentevaluations__student=obj) | Q(studentfeedback__student=obj)
        ).values('studentevaluations__level__en_in', 'studentfeedback__level__en_in').order_by(
            '-start_date_time').first()

        if level:
            if level['studentevaluations__level__en_in']:
                return level['studentevaluations__level__en_in']
            elif level['studentfeedback__level__en_in']:
                return level['studentfeedback__level__en_in']
            else:
                return None
        else:
            return None

    class Meta:
        model = Student
        depth = 2
        fields = '__all__'
