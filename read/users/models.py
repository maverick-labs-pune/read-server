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

from datetime import timedelta

from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from read.constants import PUBLIC_KEY_LENGTH_USER, LENGTH_TOKEN, LENGTH_RESET_PASSWORD_TOKEN
from users.permissions import PERMISSION_CAN_IMPORT_USERS, PERMISSION_CAN_EXPORT_USERS
from django.utils.translation import gettext as _


def generate_user_key():
    return get_random_string(PUBLIC_KEY_LENGTH_USER)


def generate_user_auth_token():
    return get_random_string(LENGTH_TOKEN)


def generate_user_reset_token():
    return get_random_string(LENGTH_RESET_PASSWORD_TOKEN)


class User(AbstractUser):
    ENGLISH = 'en_IN'
    MARATHI = 'mr_IN'
    LANGUAGES = (
        (ENGLISH, 'English'),
        (MARATHI, 'Marathi')
    )

    key = models.CharField(max_length=PUBLIC_KEY_LENGTH_USER, default=generate_user_key, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    ngo = models.ForeignKey('ngos.NGO', null=True, blank=True, on_delete=models.PROTECT)
    email = models.CharField(max_length=255,
                             unique=True,
                             null=True,
                             blank=True,
                             error_messages={
                                 'unique': _("user with this email already exists."),
                             })
    password = models.CharField(max_length=1024, null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    language = models.CharField(max_length=5, choices=LANGUAGES, default=ENGLISH, null=False, blank=True)
    reset_password = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return ''.join(
            [self.first_name, ' ', self.middle_name, ' ', self.last_name])

    class Meta:
        db_table = 'users'
        permissions = (
            PERMISSION_CAN_IMPORT_USERS[0:2],
            PERMISSION_CAN_EXPORT_USERS[0:2],
        )


class MobileAuthToken(models.Model):
    token = models.CharField(max_length=LENGTH_TOKEN, default=generate_user_auth_token, unique=True)
    user = models.ForeignKey('users.User', null=True, blank=False, on_delete=models.PROTECT)
    expiry_date = models.DateTimeField(null=False, blank=False)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mobile_auth_tokens'


class SupervisorBookFairy(models.Model):
    supervisor = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.PROTECT)
    book_fairy = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.PROTECT,
                                   related_name="book_fairies")
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supervisor_book_fairies'


class UserResetPassword(models.Model):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.PROTECT)
    reset_password_token = models.CharField(max_length=LENGTH_RESET_PASSWORD_TOKEN, default=generate_user_reset_token,
                                            unique=True)
    is_used = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    expiry_date = models.DateTimeField(null=False)
    last_modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_reset_password'
