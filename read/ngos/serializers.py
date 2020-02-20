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

from rest_framework.fields import BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from ngos.models import NGO, Level


class NGOSerializer(ModelSerializer):
    lookup_field = 'key'
    pk_field = 'key'
    is_active = BooleanField(default=True)

    class Meta:
        model = NGO
        exclude = ('id',)


class LevelSerializer(ModelSerializer):
    lookup_field = 'key'
    pk_field = 'key'
    ngo_id = SlugRelatedField(source='ngo', slug_field='id', queryset=NGO.objects.all())

    class Meta:
        model = Level
        depth = 2
        exclude = ('id',)
