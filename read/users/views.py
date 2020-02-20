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

from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from read.constants import GroupType, ERROR_LOGIN_1_JSON, \
    ERROR_LOGIN_2_JSON, ERROR_LOGIN_3_JSON, ERROR_LOGIN_4_JSON, ERROR_LOGIN_5_JSON, \
    SUCCESS_LOGOUT_1_JSON, ERROR_LOGOUT_1_JSON, ERROR_403_JSON, SUCCESS_LANGUAGE_CHANGE_JSON, ERROR_400_JSON, \
    ERROR_500_JSON, API_URL
from read.utils import get_ngo_specific_group_name, create_serializer_error, \
 create_response_error, request_user_belongs_to_users_ngo, request_user_belongs_to_user_ngo

from read.validators import validate_user_type
from users.models import User, MobileAuthToken, UserResetPassword
from users.permissions import has_permission, PERMISSION_CAN_VIEW_USER, \
    PERMISSION_CAN_CHANGE_USER, IsBookFairy, CanDeleteUser, CanChangeUser
from users.serializers import UserSerializer, UserResetPasswordSerializer


class UserViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_VIEW_USER):
            return Response(status=403, data=ERROR_403_JSON())
        try:
            user = User.objects.get(key=pk)
        except User.DoesNotExist:
            return Response(status=404)

        if not request_user_belongs_to_user_ngo(request, user):
            return Response(status=403, data=ERROR_403_JSON())

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        if not has_permission(request, PERMISSION_CAN_CHANGE_USER):
            return Response(status=403, data=ERROR_403_JSON())
        try:
            user = User.objects.get(key=pk)
        except User.DoesNotExist:
            return Response(status=404)

        if not request_user_belongs_to_user_ngo(request, user):
            return Response(status=403, data=ERROR_403_JSON())

        # If new user's type update user with new user type
        user_type = request.data.get('user_type')
        is_valid, error = validate_user_type(user_type)
        if not is_valid:
            return Response(status=400, data={'message': {'user_type': [error]}})

        data = request.data.copy()
        if data.get('email') == "" or data.get('email') is None:
            data['email'] = None

        password = data.get('password')
        if password == "" or password is None:
            password = None
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            ngo_admin_group_name = get_ngo_specific_group_name(GroupType(user_type), user.ngo.key)
            group = Group.objects.get(name=ngo_admin_group_name)
            user = serializer.save()
            if password is not None:
                user.set_password(password)
                user.reset_password = True
                user.save()
            # Remove user from previous group
            user.groups.clear()
            user.groups.add(group)
            return Response(serializer.data)
        return Response(status=400, data=create_serializer_error(serializer))

    @action(methods=['POST'], detail=False, permission_classes=[CanDeleteUser])
    def deactivate_user(self, request, pk=None):
        keys = request.data.get('keys')
        user_keys = json.loads(keys)

        if not request_user_belongs_to_users_ngo(request, user_keys):
            return Response(status=403, data=ERROR_403_JSON())

        users = User.objects.filter(key__in=user_keys)
        for user in users:
            user.is_active = False
            user.save()
        return Response(status=204)

    @action(methods=['POST'], detail=True, permission_classes=[CanChangeUser])
    def set_language(self, request, pk=None):
        language = request.data.get('selected_language')
        if language != "en_IN" and language != "mr_IN":
            return Response(status=400, data=ERROR_400_JSON())
        # TODO error
        if request.user and request.user.is_authenticated:
            request.user.language = language
            request.user.save()
            return Response(status=200, data=SUCCESS_LANGUAGE_CHANGE_JSON())
        return Response(status=500, data=ERROR_500_JSON())

    @action(methods=['POST'], detail=True)
    def reset_password(self, request, pk):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(key=pk)
        except User.DoesNotExist as e:
            return Response(status=404, data=create_response_error(e))
        if user.check_password(old_password):
            user.set_password(new_password)
            user.reset_password = False
            user.save()
            update_session_auth_hash(request, user)
            return Response(status=201)
        else:
            return Response(status=400, data=create_response_error("Old password is wrong."))


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    if username is None:
        return Response(data=ERROR_LOGIN_1_JSON(), status=400)
    if password is None:
        return Response(data=ERROR_LOGIN_2_JSON(), status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        # A backend authenticated the credentials
        try:
            login(request._request, user)
        except:
            return Response(data=ERROR_LOGIN_5_JSON(), status=500)

        # TODO do not allow super user to log in
        groups = user.groups.all()
        group_names = [group.name for group in groups]
        if len(group_names) == 1:
            group_name = group_names[0]
            default_group_names = [group_type.value for group_type in GroupType]
            user_group_name = None
            for default_group_name in default_group_names:
                if group_name.find(default_group_name) != -1:
                    user_group_name = default_group_name
                    break

            if user_group_name is None:
                return Response(data=ERROR_LOGIN_4_JSON(), status=500)

            data = {'username': user.username,
                    'key': user.key,
                    'ngo': user.ngo.key if user.ngo else None,
                    'ngo_name': user.ngo.name if user.ngo else None,
                    'permissions': user.get_all_permissions(),
                    'group': user_group_name,
                    'language': user.language,
                    'first_name': user.first_name,
                    'is_reset_password': user.reset_password
                    }
            # .update(SUCCESS_LOGIN_1_JSON)
            return Response(data=data, status=200)
        else:
            return Response(data=ERROR_LOGIN_4_JSON(), status=500)

    else:
        # No backend authenticated the credentials
        return Response(data=ERROR_LOGIN_3_JSON(), status=403)


@api_view(['POST'])
def logout_view(request):
    if request.user and request.user.is_authenticated:
        logout(request)
        return Response(data=SUCCESS_LOGOUT_1_JSON(), status=200)
    else:
        return Response(data=ERROR_LOGOUT_1_JSON, status=403)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_mobile_view(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    if username is None:
        print("yolo")
        return Response(data=ERROR_LOGIN_1_JSON(), status=400)
    if password is None:
        return Response(data=ERROR_LOGIN_2_JSON(), status=400)
    user = authenticate(username=username, password=password)
    if user:
        # A backend authenticated the credentials
        groups = user.groups.all()
        if groups.count() == 1 and groups[0].name.find(GroupType.BOOK_FAIRY.value) != -1:
            expiry_date = datetime.now(tz=timezone.utc) + timedelta(days=30)
            auth_token = MobileAuthToken.objects.create(user=user, expiry_date=expiry_date)
            data = {'username': user.username,
                    'key': user.key,
                    'ngo': user.ngo.key if user.ngo else None,
                    'permissions': user.get_all_permissions(),
                    'group': GroupType.BOOK_FAIRY.value,
                    'language': user.language,
                    'token': auth_token.token,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'expiry_date': auth_token.expiry_date
                    }
            return Response(data=data, status=200)
        else:
            return Response(data=ERROR_LOGIN_4_JSON(), status=500)
    else:
        # No backend authenticated the credentials
        return Response(data=ERROR_LOGIN_3_JSON(), status=403)


@api_view(['POST'])
def logout_mobile_view(request):
    if request.user and request.user.is_authenticated:
        logout(request)
        return Response(data=SUCCESS_LOGOUT_1_JSON(), status=200)
    else:
        return Response(data=ERROR_LOGOUT_1_JSON, status=403)


@api_view(['POST'])
@permission_classes([IsBookFairy])
def refresh_mobile_token_view(request):
    if request.user and request.user.is_authenticated:
        expiry_date = datetime.now(tz=timezone.utc) + timedelta(days=30)
        auth_token = MobileAuthToken.objects.create(user=request.user, expiry_date=expiry_date)
        return Response(status=200, data={
            'token': auth_token.token,
            'expiry_date': auth_token.expiry_date,
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def get_forgot_password_token(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as e:
        return Response(status=404, data=create_response_error("Email does not exist"))

    expiry_date = datetime.now(tz=timezone.utc) + timedelta(hours=24)
    data = {"user_id": user.id, "expiry_date": expiry_date}
    serializer = UserResetPasswordSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # token = serializer.data.get('reset_password_token')
        # link = API_URL + token
        # # TODO Change from and to emails and configure mailgun in settings
        # subject, from_email, to = 'Reset password request', 'from@example.com', 'to@example.com'
        # html_content = '<p>Hi,<br/><br/> ' \
        #                'We\'ve received a request to reset your password.<br/>' \
        #                'Ignore this email if you did not request it.<br/><br/>' \
        #                'To complete this process, visit the following link. <br/>' \
        #                '%s</p>', link
        # msg = EmailMultiAlternatives(subject, '', from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        return Response(status=204)
    else:
        return Response(status=400, data=create_serializer_error(serializer))


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    token = request.data.get('token')
    password = request.data.get('password')
    try:
        queryset = UserResetPassword.objects.get(reset_password_token=token,
                                                 expiry_date__gte=datetime.now(tz=timezone.utc),
                                                 is_used=False)
        user = User.objects.get(key=queryset.user.key)
    except UserResetPassword.DoesNotExist as e:
        return Response(status=404, data=create_response_error(e))

    user.set_password(password)
    user.save()
    queryset.is_used = True
    queryset.save()
    return Response(status=204)


@api_view(['POST'])
@permission_classes([AllowAny])
def book_fairy_forgot_password(request):
    username = request.data.get('username').strip() if request.data.get('username') else None
    print(username)
    if not username:
        return Response(status=400,data=create_response_error(ERROR_400_JSON()))

    try:
        book_fairy = User.objects.get(username=username)
    except User.DoesNotExist as e:
        return Response(status=404, data=create_response_error(e))

    groups = book_fairy.groups.all()
    group_names = [group.name for group in groups]
    if len(group_names) == 1:
        group_name = group_names[0]
        if group_name.find(GroupType.BOOK_FAIRY.value) != -1:
            # TODO send email to ngo admin of the book fairy
            return Response(status=204)

        else:
            return Response(data=ERROR_LOGIN_4_JSON(), status=500)
    else:
        return Response(data=ERROR_LOGIN_4_JSON(), status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def is_authenticated(request):
    if request.user and request.user.is_authenticated:
        return Response(status=200, data={"is_authenticated": True})
    else:
        return Response(status=200, data={"is_authenticated": False})


@api_view(['GET'])
@permission_classes([AllowAny])
def translations(request):
    response = {}
    with open('static/locale_en_IN.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
        data_file.close()
        response.update({'en_IN': data})
    with open('static/locale_mr_IN.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
        data_file.close()
        response.update({'mr_IN': data})

    return Response(status=200, data=response)


@api_view(['GET'])
@permission_classes([AllowAny])
def is_forgot_password_token_valid(request):
    token = request.GET.get('token')
    if not token:
        return Response(status=400, data=create_response_error("Token is invalid"))

    try:
        UserResetPassword.objects.get(reset_password_token=token, expiry_date__gte=datetime.now(tz=timezone.utc), is_used=False)
    except UserResetPassword.DoesNotExist as e:
        return Response(status=404, data=create_response_error("Token does not exist/expired..."))
    return Response(status=204)