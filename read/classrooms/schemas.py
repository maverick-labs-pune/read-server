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


class ClassroomSchema:
    @staticmethod
    def add_students():
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
                        enum=('MALE', 'FEMALE')
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
                coreapi.Field(
                    "academic_year",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="KEY",
                        description="Academic Year KEY"
                    )
                ),
                coreapi.Field(
                    "classroom",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="KEY",
                        description="Classroom's KEY"
                    )
                )
            ],
            description="Add Student to classroom",
        )
        return schema