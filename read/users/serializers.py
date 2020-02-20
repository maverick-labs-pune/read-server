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

from rest_framework.fields import BooleanField, SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ngos.models import NGO
from read.constants import GroupType
from users.models import User, MobileAuthToken, SupervisorBookFairy, UserResetPassword


class UserSerializer(ModelSerializer):
    ngo_id = SlugRelatedField(source='ngo', slug_field='id', queryset=NGO.objects.all())
    is_active = BooleanField(default=True)
    reset_password = BooleanField(default=True)
    user_type = SerializerMethodField(read_only=True)

    def get_user_type(self, obj):
        groups = obj.groups.all()
        group_names = [group.name for group in groups]
        if len(group_names) == 0:
            return None
        group_name = group_names[0]
        default_group_names = [group_type.value for group_type in GroupType]
        user_group_name = None
        for default_group_name in default_group_names:
            if group_name.find(default_group_name) != -1:
                user_group_name = default_group_name
                break
        return user_group_name

    class Meta:
        model = User
        depth = 2
        exclude = ('id', 'password')


class MobileAuthTokenSerializer(ModelSerializer):
    class Meta:
        model = MobileAuthToken
        depth = 1
        exclude = ('id',)


class SupervisorBookFairySerializer(ModelSerializer):
    supervisor_id = SlugRelatedField(source='supervisor', slug_field='id', queryset=User.objects.all())
    book_fairy_id = SlugRelatedField(source='book_fairy', slug_field='id', queryset=User.objects.all())

    class Meta:
        model = SupervisorBookFairy
        depth = 1
        exclude = ('id',)


class UserResetPasswordSerializer(ModelSerializer):
    user_id = SlugRelatedField(source='user', slug_field='id', queryset=User.objects.all())

    class Meta:
        model = UserResetPassword
        depth = 1
        exclude = ('id',)