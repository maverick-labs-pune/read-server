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

import xlsxwriter
from io import BytesIO
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from svglib.svglib import svg2rlg
from reportlab.pdfbase.ttfonts import TTFont

from books.serializers import InventorySerializer

pdfmetrics.registerFont(TTFont('gargi-updated', 'utils/gargi-updated.ttf'))

from books.models import Book, Inventory, BookLevel
from classrooms.models import Classroom
from read.constants import USERS_EXCEL_FIELDS, FileType, USER_WORKSHEET_NAME, BOOK_WORKSHEET_NAME, \
    STUDENT_WORKSHEET_NAME, GroupType, BOOKS_EXCEL_FIELDS, STUDENTS_EXCEL_FIELDS, FEMALE, MALE, \
    INVENTORY_BOOK_WORKSHEET_NAME, INVENTORY_BOOKS_EXCEL_FIELDS, PROTECTION_OPTIONS, SCHOOL_WORKSHEET_NAME, \
    SCHOOLS_EXCEL_FIELDS, DESIRED_QR_WIDTH_AND_HEIGHT
from read_sessions.models import ReadSession
from schools.models import School, SchoolCategory, SchoolType, SchoolMedium
from students.models import Student
from users.models import User
from datetime import datetime


class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


def process_user_worksheet(users, output, workbook, worksheet, header):
    locked = workbook.add_format()
    locked.set_locked(True)
    unlocked = workbook.add_format()
    unlocked.set_locked(False)
    # Enable worksheet protection
    worksheet.protect(options=PROTECTION_OPTIONS)

    start_row = start_column = 0
    row, column = start_row, start_column

    length_key = 6
    length_username = 10
    length_first_name = 10
    length_middle_name = 11
    length_last_name = 10
    length_email = 15
    length_user_type = 10
    max_length_username = 40
    max_length_first_name = 40
    max_length_middle_name = 40
    max_length_last_name = 40
    max_length_email = 40
    max_length_user_type = 40

    for field in USERS_EXCEL_FIELDS:
        worksheet.write(row, column, field, header)
        column += 1

    row += 1

    for user in users:
        column = 0
        worksheet.write(row, column, user.key, locked)
        column += 1
        worksheet.write(row, column, user.username, unlocked)
        column += 1
        worksheet.write(row, column, user.first_name, unlocked)
        column += 1
        worksheet.write(row, column, user.middle_name, unlocked)
        column += 1
        worksheet.write(row, column, user.last_name, unlocked)
        column += 1
        worksheet.write(row, column, user.email, unlocked)
        column += 1

        if len(user.groups.all()) == 1:
            group = user.groups.first()
            group_type = get_group_type_from_name(group.name)
            if group_type:
                worksheet.write(row, column, group_type.value, locked)
                if group_type.value and len(group_type.value) > length_user_type:
                    length_user_type = len(group_type.value)

        if user.username and len(user.username) > length_username:
            length_username = len(user.username)

        if user.first_name and len(user.first_name) > length_first_name:
            length_first_name = len(user.first_name)

        if user.middle_name and len(user.middle_name) > length_middle_name:
            length_middle_name = len(user.middle_name)

        if user.last_name and len(user.last_name) > length_last_name:
            length_last_name = len(user.last_name)

        if user.email and len(user.email) > length_email:
            length_email = len(user.email)

        row += 1

    for extra_fields in range(0, 1000):
        column = 0
        worksheet.write(row, column, "", locked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        row += 1

    worksheet.set_column('A:A', length_key)
    worksheet.set_column('B:B', length_username if length_username < max_length_username else max_length_username)
    worksheet.set_column('C:C',
                         length_first_name if length_first_name < max_length_first_name else max_length_first_name)
    worksheet.set_column('D:D',
                         length_middle_name if length_middle_name < max_length_middle_name else max_length_middle_name)
    worksheet.set_column('E:E', length_last_name if length_last_name < max_length_last_name else max_length_last_name)
    worksheet.set_column('F:F', length_email if length_email < max_length_email else max_length_email)
    worksheet.set_column('G:G', length_user_type if length_user_type < max_length_user_type else max_length_user_type)
    workbook.close()

    return output.getvalue()


def process_book_worksheet(books, output, workbook, worksheet, header):
    locked = workbook.add_format()
    locked.set_locked(True)
    unlocked = workbook.add_format()
    unlocked.set_locked(False)
    # Enable worksheet protection
    worksheet.protect(options=PROTECTION_OPTIONS)

    start_row = start_column = 0
    row, column = start_row, start_column

    length_key = 6
    length_name = 10
    length_level = 10
    length_author = 11
    length_publisher = 11
    length_price = 10
    max_length_name = 40
    max_length_author = 40
    max_length_publisher = 40

    for field in BOOKS_EXCEL_FIELDS:
        worksheet.write(row, column, field, header)
        column += 1

    row += 1

    for book in books:
        column = 0
        worksheet.write(row, column, book.key, locked)
        column += 1
        worksheet.write(row, column, book.name, unlocked)
        column += 1
        book_level = get_book_level_display_name(book)
        worksheet.write(row, column, book_level, unlocked)
        column += 1
        worksheet.write(row, column, book.author, unlocked)
        column += 1
        worksheet.write(row, column, book.publisher, unlocked)
        column += 1
        worksheet.write(row, column, book.price, unlocked)
        column += 1

        if book.name and len(book.name) > length_name:
            length_name = len(book.name)

        if book.author and len(book.author) > length_author:
            length_author = len(book.author)

        if book.publisher and len(book.publisher) > length_publisher:
            length_publisher = len(book.publisher)

        row += 1

    for extra_fields in range(0, 1000):
        column = 0
        worksheet.write(row, column, "", locked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        row += 1

    worksheet.set_column('A:A', length_key)
    worksheet.set_column('B:B', length_name if length_name < max_length_name else max_length_name)
    worksheet.set_column('C:C', length_level)
    worksheet.set_column('D:D', length_author if length_author < max_length_author else max_length_author)
    worksheet.set_column('E:E',
                         length_publisher if length_publisher < max_length_publisher else max_length_publisher)
    worksheet.set_column('F:F', length_price)
    workbook.close()

    return output.getvalue()


def process_inventory_book_worksheet(inventory_books, output, workbook, worksheet, header):
    locked = workbook.add_format()
    locked.set_locked(True)
    unlocked = workbook.add_format()
    unlocked.set_locked(False)
    # Enable worksheet protection
    worksheet.protect(options=PROTECTION_OPTIONS)

    start_row = start_column = 0
    row, column = start_row, start_column

    length_key = 6
    length_serial_number = 20
    max_length_serial_number = 40
    length_status = 10
    length_year = 14

    for field in INVENTORY_BOOKS_EXCEL_FIELDS:
        worksheet.write(row, column, field, header)
        column += 1

    row += 1

    for inventory in inventory_books:
        column = 0
        worksheet.write(row, column, inventory.key, locked)
        column += 1
        worksheet.write(row, column, str(inventory.serial_number), unlocked)
        length_serial_number = len(str(inventory.serial_number))
        column += 1
        worksheet.write(row, column, get_inventory_status(inventory.status), unlocked)
        column += 1
        year = ""
        if inventory.added_date_time:
            year = inventory.added_date_time.strftime("%Y")
        worksheet.write(row, column, year, unlocked)
        column += 1
        row += 1

    for extra_fields in range(0, 1000):
        column = 0
        worksheet.write(row, column, "", locked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        row += 1

    worksheet.set_column('A:A', length_key)
    worksheet.set_column('B:B',
                         length_serial_number if length_serial_number < max_length_serial_number else max_length_serial_number)
    worksheet.set_column('C:C', length_status)
    worksheet.set_column('D:D', length_year)
    workbook.close()

    return output.getvalue()


def process_school_worksheet(schools, output, workbook, worksheet, header):
    locked = workbook.add_format()
    locked.set_locked(True)
    unlocked = workbook.add_format()
    unlocked.set_locked(False)
    # Enable worksheet protection
    worksheet.protect(options=PROTECTION_OPTIONS)

    start_row = start_column = 0
    row, column = start_row, start_column

    length_school_key = 6
    length_school_name = 10
    length_school_address = 10
    length_school_pin_code = 10
    length_school_ward_number = 15
    length_school_school_number = 15
    length_school_school_category = 8
    length_school_school_type = 6
    length_school_medium = 10
    length_school_organization_name = 20
    length_school_year_of_intervention = 20

    max_length_school_key = length_school_key
    max_length_school_name = 50
    max_length_school_address = 50
    max_length_school_pin_code = 10
    max_length_school_ward_number = 15
    max_length_school_school_number = 15
    max_length_school_school_category = 8
    max_length_school_school_type = 6
    max_length_school_medium = 10
    max_length_school_organization_name = 20
    max_length_school_year_of_intervention = 20

    for field in SCHOOLS_EXCEL_FIELDS:
        worksheet.write(row, column, field, header)
        column += 1

    row += 1

    for school in schools:
        column = 0
        worksheet.write(row, column, school.key, locked)
        column += 1
        worksheet.write(row, column, school.name, unlocked)
        column += 1
        worksheet.write(row, column, school.address, unlocked)
        column += 1
        worksheet.write(row, column, school.pin_code, unlocked)
        column += 1
        worksheet.write(row, column, school.ward_number, unlocked)
        column += 1
        worksheet.write(row, column, school.school_number, unlocked)
        column += 1
        category = get_school_category_display_name(school)
        worksheet.write(row, column, category, unlocked)
        column += 1
        school_type = get_school_type_display_name(school)
        worksheet.write(row, column, school_type, unlocked)
        column += 1
        medium = get_school_medium_display_name(school)
        worksheet.write(row, column, medium, unlocked)
        column += 1
        worksheet.write(row, column, school.organization_name, unlocked)
        column += 1
        year = ""
        if school.year_of_intervention:
            year = school.year_of_intervention.strftime("%Y")
        worksheet.write(row, column, year, unlocked)
        column += 1
        row += 1

        if school.key and len(school.key) > length_school_key:
            length_school_key = len(school.key)
        if school.name and len(school.name) > length_school_name:
            length_school_name = len(school.name)
        if school.address and len(school.address) > length_school_address:
            length_school_address = len(school.address)
        if school.pin_code and len(str(school.pin_code)) > length_school_pin_code:
            length_school_pin_code = len(str(school.pin_code))
        if school.ward_number and len(school.ward_number) > length_school_ward_number:
            length_school_ward_number = len(school.ward_number)
        if school.school_number and len(school.school_number) > length_school_school_number:
            length_school_school_number = len(school.school_number)
        if category and len(category) > length_school_school_category:
            length_school_school_category = len(category)
        if school_type and len(school_type) > length_school_school_type:
            length_school_school_type = len(school_type)
        if medium and len(medium) > length_school_medium:
            length_school_medium = len(medium)
        if school.organization_name and len(school.organization_name) > length_school_organization_name:
            length_school_organization_name = len(school.organization_name)

    for extra_fields in range(0, 1000):
        column = 0
        for field in SCHOOLS_EXCEL_FIELDS:
            if column == 0:
                worksheet.write(row, column, "", locked)
            else:
                worksheet.write(row, column, "", unlocked)
            column += 1

        row += 1

    worksheet.set_column('A:A', length_school_key)
    worksheet.set_column('B:B',
                         length_school_name if length_school_name < max_length_school_name else max_length_school_name)
    worksheet.set_column('C:C',
                         length_school_address if length_school_address < max_length_school_address else max_length_school_address)
    worksheet.set_column('D:D',
                         length_school_pin_code if length_school_pin_code < max_length_school_pin_code else max_length_school_pin_code)
    worksheet.set_column('E:E',
                         length_school_ward_number if length_school_ward_number < max_length_school_ward_number else max_length_school_ward_number)
    worksheet.set_column('F:F',
                         length_school_school_number if length_school_school_number < max_length_school_school_number else max_length_school_school_number)
    worksheet.set_column('G:G',
                         length_school_school_category if length_school_school_category < max_length_school_school_category else max_length_school_school_category)
    worksheet.set_column('H:H',
                         length_school_school_type if length_school_school_type < max_length_school_school_type else max_length_school_school_type)
    worksheet.set_column('I:I',
                         length_school_medium if length_school_medium < max_length_school_medium else max_length_school_medium)
    worksheet.set_column('J:J',
                         length_school_organization_name if length_school_organization_name < max_length_school_organization_name else max_length_school_organization_name)
    worksheet.set_column('K:K',
                         length_school_year_of_intervention if length_school_year_of_intervention < max_length_school_year_of_intervention else max_length_school_year_of_intervention)
    workbook.close()

    return output.getvalue()


def process_student_worksheet(students, output, workbook, worksheet, header):
    locked = workbook.add_format()
    locked.set_locked(True)
    unlocked = workbook.add_format()
    unlocked.set_locked(False)
    unlocked_dob = workbook.add_format()
    unlocked_dob.set_locked(False)
    unlocked_dob.set_num_format("yyyy-mm-dd")
    # Enable worksheet protection
    worksheet.protect(options=PROTECTION_OPTIONS)

    start_row = start_column = 0
    row, column = start_row, start_column

    length_student_key = 6
    length_student_first_name = 12
    length_student_middle_name = 14
    length_student_last_name = 12
    length_student_address = 10
    length_student_gender = 8
    length_student_mother_tongue = 14
    length_student_birth_date = 10
    length_student_has_attended_preschool = 20
    max_length_student_first_name = 20
    max_length_student_middle_name = 20
    max_length_student_last_name = 20
    max_length_student_address = 20
    max_length_student_gender = length_student_gender
    max_length_student_mother_tongue = 20
    max_length_student_birth_date = length_student_birth_date
    max_length_student_has_attended_preschool = length_student_has_attended_preschool

    for field in STUDENTS_EXCEL_FIELDS:
        worksheet.write(row, column, field, header)
        column += 1

    row += 1

    for student in students:
        column = 0
        worksheet.write(row, column, student.key, locked)
        column += 1
        worksheet.write(row, column, student.first_name, unlocked)
        column += 1
        worksheet.write(row, column, student.middle_name, unlocked)
        column += 1
        worksheet.write(row, column, student.last_name, unlocked)
        column += 1
        worksheet.write(row, column, student.address, unlocked)
        column += 1
        if student.gender == FEMALE:
            gender = "Female"
        elif student.gender == MALE:
            gender = "Male"
        else:
            gender = "Unknown"
        worksheet.write(row, column, gender, unlocked)
        column += 1
        worksheet.write(row, column, student.mother_tongue, unlocked)
        column += 1
        birth_date = ""
        if student.birth_date:
            birth_date = student.birth_date
        worksheet.write_datetime(row, column, birth_date, unlocked_dob)
        column += 1
        has_attended_preschool = "No"
        if student.has_attended_preschool:
            has_attended_preschool = "Yes"
        worksheet.write(row, column, has_attended_preschool, unlocked)
        column += 1

        if student.first_name and len(student.first_name) > length_student_first_name:
            length_student_first_name = len(student.first_name)
        if student.middle_name and len(student.middle_name) > length_student_middle_name:
            length_student_middle_name = len(student.middle_name)
        if student.last_name and len(student.last_name) > length_student_last_name:
            length_student_last_name = len(student.last_name)
        if student.address and len(student.address) > length_student_address:
            length_student_address = len(student.address)
        if student.gender and len(student.gender) > length_student_gender:
            length_student_gender = len(student.gender)
        if student.mother_tongue and len(student.mother_tongue) > length_student_mother_tongue:
            length_student_mother_tongue = len(student.mother_tongue)

        row += 1

    for extra_fields in range(0, 100):
        column = 0
        worksheet.write(row, column, "", locked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked)
        column += 1
        worksheet.write(row, column, "", unlocked_dob)
        column += 1
        worksheet.write(row, column, "", unlocked)
        row += 1

    worksheet.set_column('A:A', length_student_key)
    worksheet.set_column('B:B',
                         length_student_first_name if length_student_first_name < max_length_student_first_name else max_length_student_first_name)
    worksheet.set_column('C:C',
                         length_student_middle_name if length_student_middle_name < max_length_student_middle_name else max_length_student_middle_name)
    worksheet.set_column('D:D',
                         length_student_last_name if length_student_last_name < max_length_student_last_name else max_length_student_last_name)
    worksheet.set_column('E:E',
                         length_student_address if length_student_address < max_length_student_address else max_length_student_address)
    worksheet.set_column('F:F',
                         length_student_gender if length_student_gender < max_length_student_gender else max_length_student_gender)
    worksheet.set_column('G:G',
                         length_student_mother_tongue if length_student_mother_tongue < max_length_student_mother_tongue else max_length_student_mother_tongue)
    worksheet.set_column('H:H',
                         length_student_birth_date if length_student_birth_date < max_length_student_birth_date else max_length_student_birth_date)
    worksheet.set_column('I:I',
                         length_student_has_attended_preschool if length_student_has_attended_preschool < max_length_student_has_attended_preschool else max_length_student_has_attended_preschool)
    workbook.close()

    return output.getvalue()


def write_to_excel(export_type, data):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    if export_type == FileType.USER:
        worksheet = workbook.add_worksheet(USER_WORKSHEET_NAME)
        return process_user_worksheet(data, output, workbook, worksheet, header)
    elif export_type == FileType.BOOK:
        worksheet = workbook.add_worksheet(BOOK_WORKSHEET_NAME)
        return process_book_worksheet(data, output, workbook, worksheet, header)
    elif export_type == FileType.STUDENT:
        worksheet = workbook.add_worksheet(STUDENT_WORKSHEET_NAME)
        return process_student_worksheet(data, output, workbook, worksheet, header)
    elif export_type == FileType.INVENTORY:
        worksheet = workbook.add_worksheet(INVENTORY_BOOK_WORKSHEET_NAME)
        return process_inventory_book_worksheet(data, output, workbook, worksheet, header)
    elif export_type == FileType.SCHOOL:
        worksheet = workbook.add_worksheet(SCHOOL_WORKSHEET_NAME)
        return process_school_worksheet(data, output, workbook, worksheet, header)


def get_ngo_specific_group_name(group_type, ngo_key):
    return group_type.value + " " + ngo_key


def get_group_type_from_name(group_name):
    if not group_name:
        return None
    try:
        for group in GroupType:
            if group_name.lower().find(group.value.lower()) != -1:
                return group
    except AttributeError:
        return None


def create_file_upload_error(index, key, message):
    return {str(index): {key: [message]}}


def create_file_upload_serializer_error(index, serializer_errors):
    return {str(index): serializer_errors}


def get_inventory_status(status):
    if not status:
        return None
    for status_code, status_name in Inventory.STATUSES:
        if status.lower() == status_name.lower():
            return status_code
        if status == status_code:
            return status_name
    return None


def get_group_type_from_request_user(user):
    groups = user.groups.all()
    group_names = [group.name for group in groups]
    if len(group_names) == 1:
        group_name = group_names[0]
        return get_group_type_from_name(group_name)
    else:
        return None


def request_user_belongs_to_ngo(request, ngo):
    if request.user and request.user.ngo and request.user.ngo.id == ngo.id:
        return True
    return False


def request_user_belongs_to_book_ngo(request, book):
    if request.user and request.user.ngo.id == book.ngo.id:
        return True
    return False


def request_user_belongs_to_books_ngo(request, book_keys):
    if request.user and request.user.ngo:
        for book_key in book_keys:
            if not Book.objects.filter(key=book_key, ngo=request.user.ngo).exists():
                return False
        return True
    return False


def request_user_belongs_to_user_ngo(request, user):
    if request.user:
        if request.user.ngo:
            if User.objects.filter(id=user.id, ngo=request.user.ngo).exists():
                return True
        else:
            group_type = get_group_type_from_request_user(request.user)
            if group_type == GroupType.READ_ADMIN:
                return True
    return False


def request_user_belongs_to_users_ngo(request, user_keys):
    if request.user:
        if request.user.ngo:
            for user_key in user_keys:
                if not User.objects.filter(key=user_key, ngo=request.user.ngo).exists():
                    return False
            return True
        else:
            group_type = get_group_type_from_request_user(request.user)
            if group_type == GroupType.READ_ADMIN:
                return True
    return False


def request_user_ngo_belongs_to_student_ngo(request, student):
    if request.user and request.user.ngo:
        return Student.objects.filter(id=student.id,
                                      classroomacademicyear__classroom__school__ngo=request.user.ngo).exists()
    return False


def request_user_ngo_belongs_to_students_ngo(request, student_keys):
    if request.user and request.user.ngo:
        for student_key in student_keys:
            if not Student.objects.filter(key=student_key,
                                          classroomacademicyear__classroom__school__ngo=request.user.ngo).exists():
                return False
        return True
    return False


def request_user_ngo_belongs_to_school_ngo(request, school):
    if request.user and request.user.ngo:
        return School.objects.filter(id=school.id, ngo=request.user.ngo).exists()
    return False


def request_user_ngo_belongs_to_schools_ngo(request, school_keys):
    if request.user and request.user.ngo:
        for school_key in school_keys:
            if not School.objects.filter(key=school_key, ngo=request.user.ngo).exists():
                return False
        return True
    return False


def request_user_belongs_to_read_session_ngo(request, session):
    if request.user and request.user.ngo:
        return ReadSession.objects.filter(id=session.id,
                                          readsessionclassroom__classroom__school__ngo=request.user.ngo).exists()
    return False


def request_user_belongs_to_read_sessions_ngo(request, session_keys):
    if request.user and request.user.ngo:
        for session_key in session_keys:
            if not ReadSession.objects.filter(key=session_key,
                                              readsessionclassroom__classroom__school__ngo=request.user.ngo).exists():
                return False
        return True
    return False


def request_user_belongs_to_classroom_ngo(request, classroom):
    if request.user and request.user.ngo:
        return Classroom.objects.filter(id=classroom.id, school__ngo=request.user.ngo).exists()
    return False


def request_user_belongs_to_classrooms_ngo(request, classroom_keys):
    if request.user and request.user.ngo:
        for classroom_key in classroom_keys:
            if not Classroom.objects.filter(key=classroom_key, school__ngo=request.user.ngo).exists():
                return False
        return True
    return False


def create_serializer_error(serializer):
    return {'message': serializer.errors}


def create_response_error(error):
    return {'message': str(error)}


def create_response_data(data):
    return {'message': data}


def get_school_category_display_name(school):
    for name, display_name in SchoolCategory.CATEGORIES:
        if school.school_category.name == name:
            return display_name
    return None


def get_school_type_display_name(school):
    for name, display_name in SchoolType.TYPES:
        if school.school_type.name == name:
            return display_name
    return None


def get_school_medium_display_name(school):
    for name, display_name in SchoolMedium.MEDIUMS:
        if school.medium.name == name:
            return display_name
    return None


def get_school_category(school_categories, school_category_name):
    if not school_category_name:
        return None
    school_category_internal_name = None
    for internal_name, school_category_display_name in SchoolCategory.CATEGORIES:
        if school_category_display_name.lower() == school_category_name.lower():
            school_category_internal_name = internal_name
            break

    if not school_category_internal_name:
        return None

    for school_category in school_categories:
        if school_category.name == school_category_internal_name:
            return school_category
    return None


def get_school_type(school_types, school_type_name):
    if not school_type_name:
        return None
    school_type_internal_name = None
    for internal_name, school_type_display_name in SchoolType.TYPES:
        if school_type_display_name.lower() == school_type_name.lower():
            school_type_internal_name = internal_name
            break

    if not school_type_internal_name:
        return None

    for school_type in school_types:
        if school_type.name == school_type_internal_name:
            return school_type
    return None


def get_school_medium(mediums, medium_name):
    if not medium_name:
        return None
    medium_internal_name = None
    for internal_name, medium_display_name in SchoolMedium.MEDIUMS:
        if medium_display_name.lower() == medium_name.lower():
            medium_internal_name = internal_name
            break

    if not medium_internal_name:
        return None

    for medium in mediums:
        if medium.name == medium_internal_name:
            return medium

    return None


def get_valid_school_categories():
    school_categories = []
    for internal_name, school_category_display_name in SchoolCategory.CATEGORIES:
        school_categories.append(school_category_display_name)
    return school_categories


def get_valid_school_types():
    school_types = []
    for internal_name, school_type_display_name in SchoolType.TYPES:
        school_types.append(school_type_display_name)
    return school_types


def get_valid_school_mediums():
    mediums = []
    for internal_name, medium_display_name in SchoolMedium.MEDIUMS:
        mediums.append(medium_display_name)
    return mediums


def get_book_level(book_levels, level_name):
    if not level_name:
        return None
    level_internal_name = None
    for internal_name, book_level_display_name in BookLevel.BOOK_LEVELS:
        if book_level_display_name.lower() == level_name.lower():
            level_internal_name = internal_name
            break

    if not level_internal_name:
        return None

    for book_level in book_levels:
        if book_level.name == level_internal_name:
            return book_level

    return None


def get_valid_book_levels():
    book_levels = []
    for internal_name, book_level_display_name in BookLevel.BOOK_LEVELS:
        book_levels.append(book_level_display_name)
    return book_levels


def get_book_level_display_name(book):
    for name, display_name in BookLevel.BOOK_LEVELS:
        if book.level and book.level.name == name:
            return display_name
    return None


def get_valid_inventory_statuses():
    inventory_statuses = []
    for internal_name, inventory_status_display_name in Inventory.STATUSES:
        inventory_statuses.append(inventory_status_display_name)
    return inventory_statuses


def get_valid_user_types():
    user_types = [GroupType.NGO_ADMIN.value, GroupType.SUPERVISOR.value, GroupType.BOOK_FAIRY.value]
    return user_types


def write_to_pdf(my_canvas, svg, qr_label, i):
    i = i % 63
    columns = 7
    x_offset = 10
    y_offset = 30
    height = 85
    qr_x = ((i % columns) * height) + x_offset
    qr_label_x = ((i % columns) * height) + x_offset
    qr_y = ((int(i / columns)) * height) + y_offset
    qr_label_y = ((int(i / columns)) * height) + DESIRED_QR_WIDTH_AND_HEIGHT + y_offset
    drawing = scale(svg2rlg(svg))

    renderPDF.draw(drawing, my_canvas, qr_x, qr_y, showBoundary=False)
    my_canvas.setFont('gargi-updated', 6)

    label_first_line_length = 20
    label_second_line_length = 40
    label_third_line_length = 60
    # Logic for printing label
    qr_label_length = len(qr_label)
    if qr_label_length <= label_first_line_length:
        my_canvas.drawString(qr_label_x, qr_label_y, qr_label[:qr_label_length])
    elif qr_label_length <= label_second_line_length:
        my_canvas.drawString(qr_label_x, qr_label_y, qr_label[:label_first_line_length])
        my_canvas.drawString(qr_label_x, qr_label_y + 10, qr_label[label_first_line_length:qr_label_length])
    elif qr_label_length <= label_third_line_length:
        my_canvas.drawString(qr_label_x, qr_label_y, qr_label[:label_first_line_length])
        my_canvas.drawString(qr_label_x, qr_label_y + 10,
                             qr_label[label_first_line_length:label_second_line_length])
        my_canvas.drawString(qr_label_x, qr_label_y + 20, qr_label[label_second_line_length:qr_label_length])
    else:
        my_canvas.drawString(qr_label_x, qr_label_y, qr_label[:label_first_line_length])
        my_canvas.drawString(qr_label_x, qr_label_y + 10,
                             qr_label[label_first_line_length:label_second_line_length])
        my_canvas.drawString(qr_label_x, qr_label_y + 20, qr_label[label_second_line_length:label_third_line_length])


def scale(drawing):
    # return drawing
    """
    Scale a reportlab.graphics.shapes.Drawing()
    object while maintaining the aspect ratio
    """
    scaling_factor = DESIRED_QR_WIDTH_AND_HEIGHT / drawing.width
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing


def get_current_academic_year():
    current = datetime.now()
    current_year = current.year
    next_year = current_year + 1
    # Start date with April and end with March
    start_date = datetime(year=current_year, month=5, day=1)
    end_date = datetime(year=next_year, month=4, day=30)
    current_year_format = int(current.strftime("%y"))

    if start_date <= current <= end_date:
        year = "AY %s-%s" % (current_year_format, current_year_format + 1)
    else:
        year = "AY %s-%s" % (current_year_format - 1, current_year_format)

    return year


def create_inventory(book, serial_number, ngo):
    existing_inventory_with_same_serial_number = Inventory.objects.filter(book__ngo=ngo,
                                                                          serial_number=serial_number).exists()
    if existing_inventory_with_same_serial_number:
        print("Existing " + str(serial_number))
        return False ,[]

    new_inventory_data = {"status": Inventory.GOOD, "serial_number": serial_number, "book_id": book.id,
                          "added_date_time": None}
    serializer = InventorySerializer(data=new_inventory_data)
    if serializer.is_valid():
        serializer.save()
        print("Created inventory " + str(serial_number))
        return False, []
    else:
        print(serializer.errors)
        return True , serializer.errors

