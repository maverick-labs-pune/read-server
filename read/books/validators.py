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

from read.constants import BOOKS_EXCEL_FIELDS, INVENTORY_BOOKS_EXCEL_FIELDS, SCHOOLS_EXCEL_FIELDS, \
    BOOKS_AND_INVENTORY_EXCEL_FIELDS


def validate_add_book_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    value = data.get('name')
    if not value:
        return False, "Invalid book name"

    return True, "No error"


def validate_book_file_import(request):
    data = request.FILES
    if not data:
        return False, "Empty data"

    return True, "No error"


def validate_book_file_excel_content(rows):
    if len(rows) == 0:
        return False, "Empty rows"
    header_row = [cell.value for cell in rows[0]]
    if header_row != BOOKS_EXCEL_FIELDS:
        return False, "Error in header"

    return True, "No error"


def validate_book_and_inventory_file_excel_content(rows):
    if len(rows) == 0:
        return False, "Empty rows"
    header_row = [cell.value for cell in rows[0]]
    if header_row != BOOKS_AND_INVENTORY_EXCEL_FIELDS:
        return False, "Error in header"

    return True, "No error"


def validate_inventory_book_file_excel_content(rows):
    if len(rows) == 0:
        return False, "Empty rows"
    header_row = [cell.value for cell in rows[0]]
    if header_row != INVENTORY_BOOKS_EXCEL_FIELDS:
        return False, "Error in header"

    return True, "No error"


def validate_school_file_excel_content(rows):
    if len(rows) == 0:
        return False, "Empty rows"
    header_row = [cell.value for cell in rows[0]]
    if header_row != SCHOOLS_EXCEL_FIELDS:
        return False, "Error in header"

    return True, "No error"
