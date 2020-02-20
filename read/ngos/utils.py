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

from django.db.models import Q
from rest_framework import pagination

from books.models import Book
from books.serializers import BookSerializer
from classrooms.models import ClassroomAcademicYear
from classrooms.serializers import ClassroomAcademicYearSerializer
from read.constants import GroupType
from read_sessions.models import ReadSessionClassroom, ReadSession
from read_sessions.serializers import ReadSessionClassroomSerializer, ReadSessionSerializer
from schools.models import School
from schools.serializers import SchoolSerializer
from students.models import Student
from users.models import User
from users.serializers import UserSerializer


def switch(model):
    cases = {
        "school": search_school,
        "book": search_book,
        "student": search_student,
        "user": search_user,
        "session": search_session
    }
    return cases.get(model, invalid)


def search_school(filters, ngo, request):
    name = filters.get('name', None)
    sort = filters.get('sort', None)
    schools = School.objects.filter(name__icontains=name, ngo__key=ngo, is_active=True, ngo__is_active=True).order_by(
        sort)
    paginator = pagination.PageNumberPagination()
    result = paginator.paginate_queryset(schools, request)
    serializer = SchoolSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


def search_book(filters, ngo, request):
    name = filters.get('name', None)
    sort = filters.get('sort', None)
    books = Book.objects.filter((Q(name__icontains=name) | Q(publisher__icontains=name)), ngo__key=ngo, is_active=True,
                                ngo__is_active=True).order_by(sort)
    paginator = pagination.PageNumberPagination()
    result = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


def search_student(filters, ngo, request):
    name = filters.get('name', None)
    school = filters.get('school', None)
    academic_year = filters.get('academicYear', None)
    order = filters.get('order', None)
    sort = filters.get('sort', None)
    order_by = student_sort_by_value(sort, order)
    print(filters)
    common_filters = {
        'classroom__is_active': True,
        'classroom__school__is_active': True,
        'classroom__school__ngo__key': ngo,
        'classroom__school__ngo__is_active': True
    }
    paginator = pagination.PageNumberPagination()

    if name and school and academic_year:
        students = Student.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name), is_active=True)
        classroom_academic_year = ClassroomAcademicYear.objects.filter(student__in=students,
                                                                       classroom__school__key=school,
                                                                       academic_year__key=academic_year,
                                                                       **common_filters).order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif name and academic_year:
        students = Student.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name), is_active=True)
        classroom_academic_year = ClassroomAcademicYear.objects.filter(student__in=students,
                                                                       academic_year__key=academic_year,
                                                                       **common_filters).order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif school and academic_year:
        classroom_academic_year = ClassroomAcademicYear.objects.filter(classroom__school__key=school,
                                                                       student__is_active=True,
                                                                       academic_year__key=academic_year,
                                                                       **common_filters
                                                                       ).order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
        return serializer.data
    elif name:
        students = Student.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name), is_active=True)
        classroom_academic_year = ClassroomAcademicYear.objects.filter(student__in=students,
                                                                       **common_filters).order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif school:
        classroom_academic_year = ClassroomAcademicYear.objects.filter(classroom__school__key=school,
                                                                       student__is_active=True,
                                                                       **common_filters
                                                                       ).order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif academic_year:
        classroom_academic_year = ClassroomAcademicYear.objects.filter(student__is_active=True,
                                                                       academic_year__key=academic_year,
                                                                       **common_filters,
                                                                       ).order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        classroom_academic_year = ClassroomAcademicYear.objects.filter(**common_filters, student__is_active=True) \
            .order_by(order_by)
        result = paginator.paginate_queryset(classroom_academic_year, request)
        serializer = ClassroomAcademicYearSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


def search_user(filters, ngo, request):
    name = filters.get('name', None)
    sort = filters.get('sort', None)
    sort_by = user_sort_by_value(sort)
    paginator = pagination.PageNumberPagination()
    users = User.objects.filter((Q(first_name__icontains=name) | Q(last_name__icontains=name)),
                                ngo__key=ngo,
                                ngo__is_active=True,
                                is_active=True).order_by(sort_by)
    results = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)


def search_session(filters, ngo, request):
    school = filters.get('school')
    book_fairy = filters.get('fairy')
    academic_year = filters.get('academicYear')
    classroom = filters.get('classroom')
    start_date = filters.get('start')
    end_date = filters.get('end')

    order = filters.get('order', None)
    sort = filters.get('sort', None)
    order_by = session_sort_by_value(sort, order)
    paginator = pagination.PageNumberPagination()
    school_filters = {
        'readsessionclassroom__classroom__school__key': school,
        'readsessionclassroom__classroom__school__is_active': True,
        'readsessionclassroom__classroom__is_active': True,
        'readsessionclassroom__classroom__school__ngo__key': ngo,
        'readsessionclassroom__classroom__school__ngo__is_active': True,
    }
    book_fairy_filters = {'readsessionbookfairy__book_fairy__key': book_fairy,
                          'readsessionbookfairy__book_fairy__is_active': True}
    academic_year_filters = {'academic_year__key': academic_year}

    classroom_filter = {
        "readsessionclassroom__classroom__key": classroom
    }

    start_date_filters = {
        'start_date_time__gte': start_date
    }

    end_date_filters = {
        'end_date_time__lte': end_date
    }

    dates_in_between = {
        'start_date_time__range': (start_date, end_date)
    }

    if school and book_fairy and academic_year:
        if classroom:
            school_filters.update(classroom_filter)
        read_session = ReadSession.objects.filter(**school_filters,
                                                  **book_fairy_filters,
                                                  **academic_year_filters).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if school and book_fairy:
        if classroom:
            school_filters.update(classroom_filter)
        read_session = ReadSession.objects.filter(**school_filters, **book_fairy_filters).distinct().order_by(
            order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if school and academic_year:
        if classroom:
            school_filters.update(classroom_filter)
        read_session = ReadSession.objects.filter(**school_filters, **academic_year_filters).distinct().order_by(
            order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if book_fairy and academic_year:
        read_session = ReadSession.objects.filter(**book_fairy_filters, **academic_year_filters).distinct().order_by(
            order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if book_fairy and start_date and end_date:
        read_session = ReadSession.objects.filter(**book_fairy_filters, **dates_in_between).distinct().order_by(
            order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if book_fairy and start_date:
        read_session = ReadSession.objects.filter(**book_fairy_filters, **start_date_filters).distinct().order_by(
            order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if book_fairy and end_date:
        read_session = ReadSession.objects.filter(**book_fairy_filters, **end_date_filters).distinct().order_by(
            order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if start_date and end_date:
        read_session = ReadSession.objects.filter(**dates_in_between).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if start_date:
        read_session = ReadSession.objects.filter(**start_date_filters).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if end_date:
        read_session = ReadSession.objects.filter(**end_date_filters).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if school:
        if classroom:
            school_filters.update(classroom_filter)
        read_session_school = ReadSession.objects.filter(**school_filters).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session_school, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if book_fairy:
        read_session = ReadSession.objects.filter(**book_fairy_filters).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    if academic_year:
        read_session = ReadSession.objects.filter(**academic_year_filters).distinct().order_by(order_by)
        result = paginator.paginate_queryset(read_session, request)
        serializer = ReadSessionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    read_sessions = ReadSession.objects.filter(readsessionclassroom__classroom__school__ngo__key=ngo).order_by(
        order_by).distinct()
    result = paginator.paginate_queryset(read_sessions, request)
    serializer = ReadSessionSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


def invalid(filters=None, ngo=None):
    return []


def get_group_name(groups):
    group_names = [group.name for group in groups]
    group_name = group_names[0]
    default_group_names = [group_type.value for group_type in GroupType]
    user_group_name = None
    for default_group_name in default_group_names:
        if group_name.find(default_group_name) != -1:
            user_group_name = default_group_name
            break
    return user_group_name


def student_sort_by_value(sort_by, order):
    print(order)
    order_by = None
    if sort_by == 'first_name' or sort_by == 'name':
        order_by = 'student__first_name'
    if sort_by == 'last_name':
        order_by = 'student__last_name'
    if sort_by == 'birth_date':
        order_by = 'student__birth_date'
    if sort_by == 'gender':
        order_by = 'student__gender'
    if sort_by == 'address':
        order_by = 'student__address'
    if sort_by == 'school':
        order_by = 'classroom__school__name'
    if sort_by == 'standard':
        order_by = 'classroom__standard__name'
    if sort_by == 'division':
        order_by = 'classroom__division'
    if order == 'true':
        return '-' + order_by
    return order_by


def session_sort_by_value(sort_by, order):
    order_by = None

    if sort_by == 'dateTime':
        order_by = 'start_date_time'
    if sort_by == 'school':
        order_by = 'readsessionclassroom__classroom__school__name'
    if sort_by == 'standard':
        order_by = 'readsessionclassroom__classroom__standard__name'
    if sort_by == 'fairy':
        order_by = 'readsessionbookfairy__book_fairy__first_name'
    if sort_by == 'type':
        order_by = 'type'
    if sort_by == 'academicYear':
        order_by = 'readsessionclassroom__classroom__classroomacademicyear__academic_year__name'

    if order == 'true':
        return '-' + order_by
    return order_by


def user_sort_by_value(sort_by):
    if sort_by == 'user_type':
        return 'groups__name'

    if sort_by == '-user_type':
        return '-groups__name'

    return sort_by
