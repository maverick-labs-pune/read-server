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

def validate_add_classroom_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    # Validate first_name
    value = data.get('school')
    if not value:
        return False, "Invalid school"

    # Validate last_name
    value = data.get('standard')
    if not value:
        return False, "Invalid standard"

    return True, "No error"


def validate_student_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    value = data.get('first_name')
    if not value:
        return False, "Invalid first name"

    value = data.get('last_name')
    if not value:
        return False, "Invalid last name"

    value = data.get('address')
    if not value:
        return False, "Invalid address"

    value = data.get('gender')
    if not value:
        return False, "Invalid gender"

    value = data.get('mother_tongue')
    if not value:
        return False, "Invalid mother tongue"

    value = data.get('birth_date')
    if not value:
        return False, "Invalid birth date"

    value = data.get('academic_year')
    if not value:
        return False, "Invalid academic year"

    value = data.get('classroom')
    if not value:
        return False, "Invalid classroom"

    return True, "No errors"


def validate_students_file_import(request):
    data = request.FILES
    if not data:
        return False, "Empty file"

    data = request.POST
    if not data:
        return False, "Empty data"

    value = data.get('academic_year')
    if not value:
        return False, "Invalid Academic year"

    return True, "No errors"


def validate_students_file_export(request):
    data = request.GET
    if not data:
        return False, "Empty data"

    value = data.get('academic_year')
    if not value:
        return False, "Invalid Academic year"

    return True, "No errors"
