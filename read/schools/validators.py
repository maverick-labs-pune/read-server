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

def validate_add_school_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    value = data.get('name')
    if not value:
        return False, "Invalid school name"

    value = data.get('address')
    if not value:
        return False, "Invalid school address"

    value = data.get('pin_code')
    if not value:
        return False, "Invalid school pincode"

    value = data.get('school_category')
    if not value:
        return False, "Invalid school category"

    value = data.get('school_type')
    if not value:
        return False, "Invalid school type"

    value = data.get('medium')
    if not value:
        return False, "Invalid medium"

    return True, "No error"


