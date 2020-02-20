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
from django.utils.translation import gettext as _

from read.constants import PUBLIC_KEY_LENGTH_SESSION, REGULAR, EVALUATION, LENGTH_NOTE_FIELD, BOOK_LENDING


def generate_session_key():
    return get_random_string(PUBLIC_KEY_LENGTH_SESSION)


class ReadSession(models.Model):
    Type = (
        (REGULAR, _("READ_SESSION_REGULAR")),
        (EVALUATION, _("READ_SESSION_EVALUATION")),
        (BOOK_LENDING, _("READ_SESSION_BOOK_LENDING")),
    )
    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_SESSION, default=generate_session_key, unique=True)
    academic_year = models.ForeignKey('academic_years.AcademicYear', null=False, blank=False, on_delete=models.PROTECT)
    start_date_time = models.DateTimeField(null=False, blank=False)
    end_date_time = models.DateTimeField(null=False, blank=False)
    type = models.CharField(max_length=30, choices=Type, null=False, blank=False)
    is_evaluated = models.BooleanField(default=False, blank=False)
    is_verified = models.BooleanField(default=False, blank=False)
    is_cancelled = models.BooleanField(default=False, blank=False)
    notes = models.CharField(max_length=LENGTH_NOTE_FIELD, null=True, blank=True)
    submitted_by_book_fairy = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.PROTECT,
                                                related_name='book_fairy')
    verified_by_supervisor = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.PROTECT,
                                               related_name='supervisor')
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'read_sessions'


class ReadSessionBookFairy(models.Model):
    read_session = models.ForeignKey('read_sessions.ReadSession', null=False, blank=False, on_delete=models.PROTECT)
    book_fairy = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'read_session_book_fairies'


class ReadSessionClassroom(models.Model):
    read_session = models.ForeignKey('read_sessions.ReadSession', null=False, blank=False, on_delete=models.PROTECT)
    classroom = models.ForeignKey('classrooms.Classroom', null=False, blank=False, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'read_session_classrooms'


class StudentFeedback(models.Model):
    student = models.ForeignKey('students.Student', null=False, blank=False, on_delete=models.PROTECT)
    read_session = models.ForeignKey('read_sessions.ReadSession', null=False, blank=False, on_delete=models.PROTECT)
    level = models.ForeignKey('ngos.Level', null=True, blank=True, on_delete=models.PROTECT)
    attendance = models.BooleanField(default=False, blank=False)
    comments = models.CharField(max_length=LENGTH_NOTE_FIELD, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_feedback'


class ReadSessionFeedbackBook(models.Model):
    read_session = models.ForeignKey('read_sessions.ReadSession', null=False, blank=False, on_delete=models.PROTECT)
    book = models.ForeignKey('books.Book', null=False, blank=False, on_delete=models.PROTECT)
    inventory = models.ForeignKey('books.Inventory', null=True, blank=True, on_delete=models.PROTECT)
    student = models.ForeignKey('students.Student', null=False, blank=False, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'read_session_feedback_books'


class ReadSessionHomeLendingBook(models.Model):
    LEND = 'le'
    COLLECT = 'co'
    STATUSES = (
        (LEND, "Lend"),
        (COLLECT, "Collect"),
    )
    read_session = models.ForeignKey('read_sessions.ReadSession', null=False, blank=False, on_delete=models.PROTECT)
    book = models.ForeignKey('books.Book', null=False, blank=False, on_delete=models.PROTECT)
    inventory = models.ForeignKey('books.Inventory', null=True, blank=True, on_delete=models.PROTECT)
    student = models.ForeignKey('students.Student', null=False, blank=False, on_delete=models.PROTECT)
    action = models.CharField(max_length=2, choices=STATUSES, null=False, blank=False)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'read_session_home_lending_books'
        unique_together = ('read_session', 'inventory','student')


class StudentEvaluations(models.Model):
    student = models.ForeignKey('students.Student', null=False, blank=False, on_delete=models.PROTECT)
    read_session = models.ForeignKey('read_sessions.ReadSession', null=False, blank=False, on_delete=models.PROTECT)
    level = models.ForeignKey('ngos.Level', null=True, blank=True, on_delete=models.PROTECT)
    attendance = models.BooleanField(default=False, blank=False)
    comments = models.CharField(max_length=LENGTH_NOTE_FIELD, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_evaluations'
