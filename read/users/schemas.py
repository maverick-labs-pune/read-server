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

import coreapi
import coreschema
from rest_framework.schemas import ManualSchema


class UserSchema:

    @staticmethod
    def update():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="User's Key",
                    )
                ),
                coreapi.Field(
                    "first_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="First Name",
                        description="User's first name",
                    )
                ), coreapi.Field(
                    "middle_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Middle name",
                        description="User's middle name",
                    )
                ), coreapi.Field(
                    "last_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Last name",
                        description="User's last name",
                    )
                ), coreapi.Field(
                    "email",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="email address",
                        description="User's ",
                    )
                ), coreapi.Field(
                    "username",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Username",
                        description="User's username",
                    )
                ),
                coreapi.Field(
                    "password",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Password",
                        description="User's password",
                    )
                ),
                coreapi.Field(
                    "user_type",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Type",
                        description="User's Type"
                    )
                )
            ],
            description="Enter User Details",
        )
        return schema

    @staticmethod
    def deactivate_user():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="User's Key",
                    )
                )
            ],
            description="Deactivate User",
        )
        return schema

    @staticmethod
    def file_import():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "file",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="User file",
                        description="Contains information of users",
                    )
                )
            ],
            encoding="multipart/form-data",
            description="Import users through file",

        )
        return schema
