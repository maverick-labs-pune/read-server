
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

def validate_add_ngo_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    # Validate first_name
    value = data.get('name')
    if not value:
        return False, "Name field required"

    # Validate last_name
    value = data.get('address')
    if not value:
        return False, "Address field required"

    return True, "No error"

def validate_change_ngo_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    # Validate first_name
    value = data.get('name')
    if not value:
        return False, "Name field required"

    # Validate last_name
    value = data.get('address')
    if not value:
        return False, "Address field required"

    value = data.get('logo')
    if not value:
        return False, "Logo field required"

    value = data.get('description')
    if not value:
        return False, "Description field required"

    return True, "No error"
