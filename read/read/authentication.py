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

from datetime import datetime
from django.utils.timezone import make_aware

from rest_framework import authentication

from users.models import MobileAuthToken


class MobileAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for validating tokens sent from android apps.
    Check http://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
    for details
    """

    def authenticate(self, request):
        token_header = request.META.get('HTTP_AUTHORIZATION', None)
        try:
            token = token_header.split(' ')[1]
        except Exception:
            return None, None

        if token:
            auth_token = MobileAuthToken.objects.filter(token=token, expiry_date__gt=make_aware(datetime.now())).first()
            if auth_token:
                # print("Token exists")
                return auth_token.user, None
            # else:
                # print("Auth Token not found")
        # else:
        #     print("Token in header missing")
        return None, None
