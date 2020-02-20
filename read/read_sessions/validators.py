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

def validate_add_session_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    value = data.get('academic_year')
    if not value:
        return False, "Invalid academic_year"

    value = data.get('dates')
    if not value:
        return False, "Invalid date time"

    value = data.get('classrooms')
    if not value:
        return False, "Invalid classrooms"

    value = data.get('fairies')
    if not value:
        return False, "Invalid fairies"

    return True, "No error"