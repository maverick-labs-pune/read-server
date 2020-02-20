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

from read.constants import GROUPS


def validate_user_type(user_type):
    groups = [group.value for group in GROUPS]
    try:
        groups.index(user_type)
    except ValueError:
        return False, 'Invalid user type'
    return True, 'User type is preset'


def validate_add_ngo_user_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    # Validate first_name
    value = data.get('first_name')
    if not value:
        return False, "Invalid first_name"

    # Validate last_name
    value = data.get('last_name')
    if not value:
        return False, "Invalid last_name"

    # TODO Validate email
    value = data.get('email')
    if not value:
        return False, "Invalid email"

    # Validate username
    value = data.get('username')
    if not value:
        return False, "Invalid username"

    # Validate password
    value = data.get('password')
    if not value:
        return False, "Invalid password"

    # Validate User's Type
    value = data.get('user_type')
    if not value:
        return False, "Invalid User's Type"

    return True, "No error"


def validate_deactivate_ngo_admin_request(request):
    data = request.data
    if not data:
        return False, "Empty data"

    # Validate first_name
    value = data.get('user_key')
    if not value:
        return False, "Invalid user_key"

    return True, "No error"


def validate_ngo_user(request):
    user = request.user
    if not user.is_authenticated:
        return False, "Invalid User"

    ngo = user.ngo
    if not ngo:
        return False, "No NGO assigned to this user"

    return True, "No error"
