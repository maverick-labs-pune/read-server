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

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from books.models import Book, Inventory
from ngos.models import NGO, Level
from read.constants import REGULAR, EVALUATION, ERROR_403_JSON, BOOK_LENDING, ERROR_400_JSON
from read.utils import create_response_error, request_user_belongs_to_ngo, request_user_belongs_to_read_session_ngo, \
    request_user_belongs_to_read_sessions_ngo, create_response_data
from read_sessions.models import ReadSession, ReadSessionBookFairy, ReadSessionClassroom, StudentFeedback, \
    ReadSessionFeedbackBook, StudentEvaluations, ReadSessionHomeLendingBook
from read_sessions.serializers import ReadSessionSerializer, ReadSessionBookFairySerializer, \
    ReadSessionClassroomSerializer, StudentFeedbackSerializer, ReadSessionFeedbackBookSerializer, \
    StudentEvaluationsSerializer, StudentEvaluationsFeedbackBookSerializer, StudentFeedbackAndFeedbackBookSerializer, \
    ReadSessionHomeLendingBookSerializer, StudentHomeLendingBookSerializer
from students.models import Student
from students.serializers import StudentSubmitEvaluationAndBookSerializer
from users.permissions import PERMISSION_CAN_VIEW_READ_SESSION, has_permission, CanViewReadSession, CanChangeReadSession

logger = logging.getLogger(__name__)


class ReadSessionViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_VIEW_READ_SESSION):
            return Response(status=403, data=ERROR_403_JSON())
        queryset = ReadSession.objects.all()
        session = get_object_or_404(queryset, key=pk)

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        serializer = ReadSessionSerializer(session)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, permission_classes=[CanViewReadSession])
    def session_classrooms(self, request, pk=None):
        ngo_key = request.GET.get('ngo')
        try:
            session = ReadSession.objects.get(key=pk)
            NGO.objects.get(key=ngo_key)
        except (ReadSession.DoesNotExist, NGO.DoesNotExist) as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        # Getting read session classrooms from read session key
        read_session_classrooms = ReadSessionClassroom.objects.filter(read_session__key=pk,
                                                                      classroom__is_active=True,
                                                                      classroom__school__is_active=True,
                                                                      classroom__school__ngo__is_active=True,
                                                                      classroom__classroomacademicyear__is_active=True,
                                                                      classroom__school__ngo__key=ngo_key).distinct()
        serializer = ReadSessionClassroomSerializer(read_session_classrooms, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, permission_classes=[CanViewReadSession])
    def session_book_fairies(self, request, pk=None):
        ngo_key = request.GET.get('ngo')
        try:
            session = ReadSession.objects.get(key=pk)
            NGO.objects.get(key=ngo_key)
        except (ReadSession.DoesNotExist, NGO.DoesNotExist) as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        # Getting read session book fairies from read session key
        read_session_book_fairies = ReadSessionBookFairy.objects.filter(read_session__key=pk,
                                                                        book_fairy__is_active=True,
                                                                        book_fairy__ngo__key=ngo_key)
        serializer = ReadSessionBookFairySerializer(read_session_book_fairies, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def delete_sessions(self, request, pk=None):
        session_keys = request.data.get('keys')
        sessions = json.loads(session_keys)

        if not request_user_belongs_to_read_sessions_ngo(request, sessions):
            return Response(status=403, data=ERROR_403_JSON())

        sessions_list = ReadSession.objects.filter(key__in=sessions)
        try:
            with transaction.atomic():
                for session in sessions_list:
                    student_feedback = StudentFeedback.objects.filter(read_session=session).exists()
                    feedback_book = ReadSessionFeedbackBook.objects.filter(read_session=session).exists()
                    if session.type == REGULAR:
                        student_evaluations = StudentFeedback.objects.filter(read_session=session).exists()
                    elif session.type == EVALUATION:
                        student_evaluations = StudentEvaluations.objects.filter(read_session=session).exists()
                    else:
                        logger.error("Incorrect session type during delete_sessions")
                        raise ValueError
                    if student_feedback:
                        logger.error("student_feedback exists during delete_sessions")
                        raise ValueError
                    if student_evaluations:
                        logger.error("student_evaluations exists during delete_sessions")
                        raise ValueError
                    if feedback_book:
                        logger.error("feedback_book exists during delete_sessions")
                        raise ValueError

                    session_classroom = ReadSessionClassroom.objects.filter(read_session=session)
                    session_book_fairy = ReadSessionBookFairy.objects.filter(read_session=session)
                    session_classroom.delete()
                    session_book_fairy.delete()
                    session.delete()

                return Response(status=204)
        except Exception:
            return Response(status=500, data=create_response_data("Cannot delete sessions"))

    @action(methods=['GET'], detail=True)
    def get_student_evaluation(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        if session.type == REGULAR:
            query_set = StudentFeedback.objects.filter(read_session__key=pk)
            serializer = StudentFeedbackAndFeedbackBookSerializer(query_set, many=True)
        elif session.type == EVALUATION:
            query_set = StudentEvaluations.objects.filter(read_session__key=pk)
            serializer = StudentEvaluationsFeedbackBookSerializer(query_set, many=True)
        else:
            return Response(status=400, data=create_response_data(ERROR_400_JSON()))
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def evaluate_students(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        if session.is_verified:
            return Response(status=500, data=create_response_data("Session already verified. Cannot save"))

        data = request.data.get('body')
        try:
            with transaction.atomic():
                for item in data:

                    student_key = item.get('student')
                    level_key = item.get('level')
                    inventory_books = item.get('book')
                    is_evaluated = item.get('isEvaluated')
                    attendance = item.get('attendance')
                    comments = item.get('comments')
                    student = Student.objects.get(key=student_key)

                    if session.type == REGULAR:
                        if attendance:
                            level = Level.objects.get(key=level_key, is_regular=True, ngo=request.user.ngo)
                            if is_evaluated:
                                # Delete old entries from tables and adding new
                                student_feedbacks = StudentFeedback.objects.filter(student__key=student_key,
                                                                                   read_session__key=pk)
                                student_feedbacks.delete()

                                feedback_books = ReadSessionFeedbackBook.objects.filter(student__key=student_key,
                                                                                        read_session__key=pk)
                                feedback_books.delete()

                            feedback_data = {"student_id": student.id, "level_id": level.id,
                                             "read_session_id": session.id,
                                             "attendance": attendance, "comments": comments}

                            student_feedback_serializer = StudentFeedbackSerializer(data=feedback_data)

                            if student_feedback_serializer.is_valid():
                                student_feedback_serializer.save()
                                if inventory_books is not None:
                                    for book_inventory_data in inventory_books:
                                        inventory_key = book_inventory_data.get('inventory')
                                        book_key = book_inventory_data.get('book')
                                        book = Book.objects.get(key=book_key)
                                        inventory = Inventory.objects.get(key=inventory_key)
                                        feedback_data["book_id"] = book.id
                                        feedback_data["inventory_id"] = inventory.id
                                        feedback_book_serializer = ReadSessionFeedbackBookSerializer(data=feedback_data)
                                        if feedback_book_serializer.is_valid():
                                            feedback_book_serializer.save()
                        else:
                            # If student is absent mark level as None
                            feedback_data = {"student_id": student.id, "level_id": None,
                                             "read_session_id": session.id,
                                             "attendance": attendance, "comments": comments}

                            student_feedback_serializer = StudentFeedbackSerializer(data=feedback_data)
                            if student_feedback_serializer.is_valid():
                                student_feedback_serializer.save()

                    elif session.type == EVALUATION:
                        if attendance:
                            level = Level.objects.get(key=level_key, is_evaluation=True, ngo=request.user.ngo)
                            if is_evaluated:
                                # Delete old entries from tables and adding new
                                student_evaluations = StudentEvaluations.objects.filter(student__key=student_key,
                                                                                        read_session__key=pk)
                                student_evaluations.delete()

                                feedback_books = ReadSessionFeedbackBook.objects.filter(student__key=student_key,
                                                                                        read_session__key=pk)
                                feedback_books.delete()

                            evaluation_data = {"student_id": student.id, "level_id": level.id,
                                               "read_session_id": session.id,
                                               "attendance": attendance, "comments": comments}

                            student_evaluation_serializer = StudentEvaluationsSerializer(data=evaluation_data)

                            if student_evaluation_serializer.is_valid():
                                student_evaluation_serializer.save()
                                if inventory_books is not None:
                                    for book_inventory_data in inventory_books:
                                        inventory_key = book_inventory_data.get('inventory')
                                        book_key = book_inventory_data.get('book')
                                        book = Book.objects.get(key=book_key)
                                        inventory = Inventory.objects.get(key=inventory_key)
                                        evaluation_data["book_id"] = book.id
                                        evaluation_data["inventory_id"] = inventory.id
                                        feedback_book_serializer = ReadSessionFeedbackBookSerializer(
                                            data=evaluation_data)
                                        if feedback_book_serializer.is_valid():
                                            feedback_book_serializer.save()
                        else:
                            # If student is absent mark level as None
                            evaluation_data = {"student_id": student.id, "level_id": None,
                                               "read_session_id": session.id,
                                               "attendance": attendance, "comments": comments}
                            student_evaluation_serializer = StudentEvaluationsSerializer(data=evaluation_data)

                            if student_evaluation_serializer.is_valid():
                                student_evaluation_serializer.save()

            return Response(status=200, data=create_response_data("Saved"))
        except (Book.DoesNotExist, Student.DoesNotExist, Level.DoesNotExist) as e:
            return Response(status=400, data=create_response_error(e))

    @action(detail=True, methods=['POST'])
    def submit_evaluations(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_data(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        if session.is_verified:
            return Response(status=500, data=create_response_error("Session already verified. Cannot submit"))

        data = request.data.get('body')
        try:
            with transaction.atomic():
                for item in data:

                    student_key = item.get('student')
                    level_key = item.get('level')
                    inventory_books = item.get('book')
                    is_evaluated = item.get('isEvaluated')
                    attendance = item.get('attendance')
                    comments = item.get('comments')
                    student = Student.objects.get(key=student_key)
                    if session.type == REGULAR:
                        if attendance:
                            level = Level.objects.get(key=level_key, is_regular=True, ngo=request.user.ngo)
                            if is_evaluated:
                                # Delete old entries from tables and adding new
                                student_feedbacks = StudentFeedback.objects.filter(student__key=student_key,
                                                                                   read_session__key=pk)
                                student_feedbacks.delete()

                                feedback_books = ReadSessionFeedbackBook.objects.filter(student__key=student_key,
                                                                                        read_session__key=pk)
                                feedback_books.delete()

                            feedback_data = {"student_id": student.id, "level_id": level.id,
                                             "read_session_id": session.id,
                                             "attendance": attendance, "comments": comments}

                            student_feedback_serializer = StudentFeedbackSerializer(data=feedback_data)

                            if student_feedback_serializer.is_valid():
                                student_feedback_serializer.save()
                                if inventory_books is not None:
                                    for book_inventory_data in inventory_books:
                                        inventory_key = book_inventory_data.get('inventory')
                                        book_key = book_inventory_data.get('book')
                                        book = Book.objects.get(key=book_key)
                                        inventory = Inventory.objects.get(key=inventory_key)
                                        feedback_data["book_id"] = book.id
                                        feedback_data["inventory_id"] = inventory.id
                                        feedback_book_serializer = ReadSessionFeedbackBookSerializer(data=feedback_data)
                                        if feedback_book_serializer.is_valid():
                                            feedback_book_serializer.save()
                        else:
                            # If student is absent mark level as None
                            feedback_data = {"student_id": student.id, "level_id": None,
                                             "read_session_id": session.id,
                                             "attendance": attendance, "comments": comments}
                            student_feedback_serializer = StudentFeedbackSerializer(data=feedback_data)
                            student_feedback_serializer.is_valid()
                            if student_feedback_serializer.is_valid():
                                student_feedback_serializer.save()

                    elif session.type == EVALUATION:
                        if attendance:
                            level = Level.objects.get(key=level_key, is_evaluation=True, ngo=request.user.ngo)
                            if is_evaluated:
                                # Delete old entries from tables and adding new
                                student_evaluations = StudentEvaluations.objects.filter(student__key=student_key,
                                                                                        read_session__key=pk)
                                student_evaluations.delete()

                                feedback_books = ReadSessionFeedbackBook.objects.filter(student__key=student_key,
                                                                                        read_session__key=pk)
                                feedback_books.delete()

                            evaluation_data = {"student_id": student.id, "level_id": level.id,
                                               "read_session_id": session.id,
                                               "attendance": attendance, "comments": comments}

                            student_evaluation_serializer = StudentEvaluationsSerializer(data=evaluation_data)

                            if student_evaluation_serializer.is_valid():
                                student_evaluation_serializer.save()
                                if inventory_books is not None:
                                    for book_inventory_data in inventory_books:
                                        inventory_key = book_inventory_data.get('inventory')
                                        book_key = book_inventory_data.get('book')
                                        book = Book.objects.get(key=book_key)
                                        inventory = Inventory.objects.get(key=inventory_key)
                                        evaluation_data["book_id"] = book.id
                                        evaluation_data["inventory_id"] = inventory.id
                                        feedback_book_serializer = ReadSessionFeedbackBookSerializer(
                                            data=evaluation_data)
                                        if feedback_book_serializer.is_valid():
                                            feedback_book_serializer.save()
                        else:
                            # If student is absent mark level as None
                            evaluation_data = {"student_id": student.id, "level_id": None,
                                               "read_session_id": session.id,
                                               "attendance": attendance, "comments": comments}
                            student_evaluation_serializer = StudentEvaluationsSerializer(data=evaluation_data)
                            if student_evaluation_serializer.is_valid():
                                student_evaluation_serializer.save()

                # check if every student has been evaluated.
                students = Student.objects.filter(
                    classroomacademicyear__classroom__readsessionclassroom__read_session=session, is_dropout=False,
                    classroomacademicyear__academic_year__key=session.academic_year.key)
                students_new = StudentSubmitEvaluationAndBookSerializer(students, many=True, session=session).data
                all_students_evaluated = True
                for student in students_new:
                    if not student.get('is_evaluated'):
                        all_students_evaluated = False
                        break
                if all_students_evaluated:
                    session.is_evaluated = True
                    session.submitted_by_book_fairy = request.user
                    session.save()
                    return Response(status=200, data=create_response_data("Submitted to supervisor for verification."))
                else:
                    raise Exception('All students have not been evaluated.')

        except (Book.DoesNotExist, Student.DoesNotExist, Level.DoesNotExist, Inventory.DoesNotExist, Exception) as e:
            return Response(status=400, data=create_response_error(e))

    @action(methods=['POST'], detail=True)
    def mark_session_as_verified(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        if session.is_evaluated:
            session.is_verified = True
            session.verified_by_supervisor = request.user
            session.save()
            return Response(status=200)
        else:
            return Response(status=400, data=create_response_data("Cannot mark session as verified, because session "
                                                                  "is not evaluated"))

    @action(methods=['POST'], detail=True, permission_classes=[CanChangeReadSession])
    def mark_session_as_cancelled(self, request, pk=None):
        comments = request.data.get('comments')
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))
        if comments is None:
            return Response(status=400, data=create_response_error("Enter comments for cancelling session."))
        if session.is_verified or session.is_evaluated:
            return Response(status=400, data=create_response_error("Cannot cancel session, because session is already "
                                                                   "evaluated/verified."))
        session.is_cancelled = True
        session.notes = comments
        session.save()
        return Response(status=204)

    @action(methods=['POST'], detail=True, permission_classes=[CanChangeReadSession])
    def add_comment_on_session(self, request, pk=None):
        comments = request.data.get('comments')
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        session.notes = comments
        session.save()
        return Response(status=204)

    @action(methods=['GET'], detail=True)
    def get_home_lending_books(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        # if not request_user_belongs_to_read_session_ngo(request, session):
        #     return Response(status=403, data=ERROR_403_JSON())

        if session.type != BOOK_LENDING:
            return Response(status=400, data=ERROR_400_JSON())

        query_set = ReadSessionHomeLendingBook.objects.filter(read_session__key=pk).order_by('student').distinct('student')
        serializer = StudentHomeLendingBookSerializer(query_set, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def save_home_lending_books(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        if session.type != BOOK_LENDING:
            return Response(status=400, data=ERROR_400_JSON())

        if session.is_verified:
            return Response(status=500, data=create_response_data("Session already verified. Cannot save"))

        data = request.data.get('body')
        try:
            with transaction.atomic():
                for item in data:

                    student_key = item.get('student')
                    inventory_books = item.get('book')
                    is_evaluated = item.get('isEvaluated')
                    student = Student.objects.get(key=student_key)

                    if is_evaluated:
                        # Delete old entries from tables and adding new
                        home_lending_books = ReadSessionHomeLendingBook.objects.filter(student__key=student_key,
                                                                                       read_session__key=pk)
                        home_lending_books.delete()

                    home_lending_book_data = {"student_id": student.id,
                                              "read_session_id": session.id}

                    if inventory_books is not None:
                        for book_inventory_data in inventory_books:
                            inventory_key = book_inventory_data.get('inventory')
                            book_key = book_inventory_data.get('book')
                            book_action = book_inventory_data.get('action')
                            if book_action != ReadSessionHomeLendingBook.LEND and book_action != ReadSessionHomeLendingBook.COLLECT:
                                return Response(status=400, data=create_response_data("Incorrect book lending action"))
                            book = Book.objects.get(key=book_key)
                            inventory = Inventory.objects.get(key=inventory_key)
                            home_lending_book_data["book_id"] = book.id
                            home_lending_book_data["inventory_id"] = inventory.id
                            home_lending_book_data["action"] = book_action
                            feedback_book_serializer = ReadSessionHomeLendingBookSerializer(data=home_lending_book_data)
                            if feedback_book_serializer.is_valid():
                                feedback_book_serializer.save()

            return Response(status=200, data=create_response_data("Saved"))
        except (Book.DoesNotExist, Student.DoesNotExist, Level.DoesNotExist) as e:
            return Response(status=400, data=create_response_error(e))

    @action(detail=True, methods=['POST'])
    def submit_home_lending_books(self, request, pk=None):
        try:
            session = ReadSession.objects.get(key=pk)
        except ReadSession.DoesNotExist as e:
            return Response(status=404, data=create_response_data(e))

        if not request_user_belongs_to_read_session_ngo(request, session):
            return Response(status=403, data=ERROR_403_JSON())

        if session.type != BOOK_LENDING:
            return Response(status=400, data=ERROR_400_JSON())

        if session.is_verified:
            return Response(status=500, data=create_response_error("Session already verified. Cannot submit"))

        data = request.data.get('body')
        try:
            with transaction.atomic():
                for item in data:

                    student_key = item.get('student')
                    inventory_books = item.get('book')
                    is_evaluated = item.get('isEvaluated')
                    student = Student.objects.get(key=student_key)

                    if is_evaluated:
                        # Delete old entries from tables and adding new
                        home_lending_books = ReadSessionHomeLendingBook.objects.filter(student__key=student_key,
                                                                                       read_session__key=pk)
                        home_lending_books.delete()

                    home_lending_book_data = {"student_id": student.id,
                                              "read_session_id": session.id}

                    if inventory_books is not None:
                        for book_inventory_data in inventory_books:
                            inventory_key = book_inventory_data.get('inventory')
                            book_key = book_inventory_data.get('book')
                            book_action = book_inventory_data.get('action')
                            if book_action != ReadSessionHomeLendingBook.LEND and book_action != ReadSessionHomeLendingBook.COLLECT:
                                return Response(status=400, data=create_response_data("Incorrect book lending action"))
                            book = Book.objects.get(key=book_key)
                            inventory = Inventory.objects.get(key=inventory_key)
                            home_lending_book_data["book_id"] = book.id
                            home_lending_book_data["inventory_id"] = inventory.id
                            home_lending_book_data["action"] = book_action
                            feedback_book_serializer = ReadSessionHomeLendingBookSerializer(data=home_lending_book_data)
                            if feedback_book_serializer.is_valid():
                                feedback_book_serializer.save()

                session.is_evaluated = True
                session.submitted_by_book_fairy = request.user
                session.save()
                return Response(status=200, data=create_response_data("Submitted to supervisor for verification."))

        except (Book.DoesNotExist, Student.DoesNotExist, Level.DoesNotExist, Inventory.DoesNotExist, Exception) as e:
            return Response(status=400, data=create_response_error(e))
