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


class StudentSchema:

    @staticmethod
    def create():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "first_name",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="First name",
                        description="Student's first name"
                    )
                ),
                coreapi.Field(
                    "middle_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Middle name",
                        description="Student's middle name"
                    )
                ),
                coreapi.Field(
                    "last_name",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Last name",
                        description="Student's last name"
                    )
                ),
                coreapi.Field(
                    "address",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Address",
                        description="Student's address"
                    )
                ),
                coreapi.Field(
                    "gender",
                    required=True,
                    location="form",
                    schema=coreschema.Enum(
                        enum=('M', 'F')
                    )
                ),
                coreapi.Field(
                    "mother_tongue",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Mother's tongue",
                        description="Student's mother's tongue"
                    )
                ),
                coreapi.Field(
                    "birth_date",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Birth date",
                        description="Student's birth date"
                    )
                ),
                coreapi.Field(
                    "is_dropout",
                    required=True,
                    location="form",
                    schema=coreschema.Boolean(default=False)
                ),
                coreapi.Field(
                    "has_attended_preschool",
                    required=False,
                    location="form",
                    schema=coreschema.Boolean()
                ),


            ]
        )
        return schema

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
                        description="Students's Key",
                    )
                ),
                coreapi.Field(
                    "first_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="First name",
                        description="Student's first name"
                    )
                ),
                coreapi.Field(
                    "middle_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Middle name",
                        description="Student's middle name"
                    )
                ),
                coreapi.Field(
                    "last_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Last name",
                        description="Student's last name"
                    )
                ),
                coreapi.Field(
                    "address",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Address",
                        description="Student's address"
                    )
                ),
                coreapi.Field(
                    "gender",
                    required=False,
                    location="form",
                    schema=coreschema.Enum(
                        enum=('M', 'F')
                    )
                ),
                coreapi.Field(
                    "mother_tongue",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Mother's tongue",
                        description="Student's mother's tongue"
                    )
                ),
                coreapi.Field(
                    "birth_date",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Birth date",
                        description="Student's birth date"
                    )
                ),
                coreapi.Field(
                    "is_dropout",
                    required=False,
                    location="form",
                    schema=coreschema.Boolean(default=False)
                ),
                coreapi.Field(
                    "has_attended_preschool",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Has attended preschool?",
                        description="Has attended preschool?"
                    )
                )
            ]
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
                        title="Students file",
                        description="Contains information of students",
                    )
                )
            ],
            encoding="multipart/form-data",
            description="Import users through file",

        )
        return schema
