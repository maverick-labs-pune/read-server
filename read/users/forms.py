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

from django import forms

from users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'groups',
                  'first_name',
                  'last_name',
                  'email',
                  'ngo',
                  'is_staff',
                  'user_permissions',
                  )
        # help_texts = {
        #     'mac_address': 'AA:BB:CC:DD:EE:FF'
        # }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data['password']
        if len(password) < 22:
            user.set_password(password)
        if commit:
            user.save()
        return user
