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


class NGOSchema:
    @staticmethod
    def create():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "name",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Name",
                        description="Name of the NGO",
                    )
                ),coreapi.Field(
                    "address",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Address",
                        description="Address of the NGO",
                    )
                ),coreapi.Field(
                    "logo",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Logo",
                        description="Logo of the NGO",
                    )
                ),coreapi.Field(
                    "description",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Description",
                        description="Description of the NGO",
                    )
                ),
            ],
            description="Enter NGO Details",
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
                        title="ID",
                        description="NGO's ID",
                    )
                ),
                coreapi.Field(
                    "name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Name",
                        description="Name of the NGO",
                    )
                ), coreapi.Field(
                    "address",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Address",
                        description="Address of the NGO",
                    )
                ), coreapi.Field(
                    "logo",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Logo",
                        description="Logo of the NGO",
                    )
                ), coreapi.Field(
                    "description",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Description",
                        description="Description of the NGO",
                    )
                ),
            ],
            description="Enter NGO Details",
        )
        return schema

    @staticmethod
    def add_ngo_user():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="NGO's Key",
                    )
                ),
                coreapi.Field(
                    "first_name",
                    required=True,
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
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Last name",
                        description="User's last name",
                    )
                ), coreapi.Field(
                    "email",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="email address",
                        description="User's ",
                    )
                ),coreapi.Field(
                    "username",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Username",
                        description="User's username",
                    )
                ),
                coreapi.Field(
                    "password",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Password",
                        description="User's password",
                    )
                ),
                coreapi.Field(
                    "user_type",
                    required=True,
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
    def deactivate_ngo_admin():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="ID",
                        description="NGO's ID",
                    )
                ),
                coreapi.Field(
                    "user_key",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Admin's key",
                        description="Admin's Key",
                    )
                )
            ],
            description="Deactivate a NGO Admin",
        )
        return schema

    @staticmethod
    def add_book():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="NGO's KEY",
                    )
                ),
                coreapi.Field(
                    "name",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Book's name",
                        description="Book's name",
                    )
                ),
                coreapi.Field(
                    "type",
                    required=True,
                    location="form",
                    schema=coreschema.Enum(
                        enum=('li', 're')
                    )
                ),
                coreapi.Field(
                    "publisher",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Book's description",
                        description="Book's description"
                    )
                ),
                coreapi.Field(
                    "price",
                    required=False,
                    location="form",
                    schema=coreschema.Integer(
                        minimum=0
                    )
                ),
                coreapi.Field(
                    "is_active",
                    required=False,
                    location="form",
                    schema=coreschema.Boolean(default=True)
                )
            ],
            description="Add book to NGO",
        )
        return schema

    @staticmethod
    def add_school():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="NGO's KEY",
                    )
                ),
                coreapi.Field(
                    "name",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School name",
                        description="School name",
                    )
                ),
                coreapi.Field(
                    "address",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School address",
                        description="School address"
                    )
                ),
                coreapi.Field(
                    "pincode",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School pincode",
                        description="School pincode"
                    )
                ),
                coreapi.Field(
                    "ward_number",
                    required=True,
                    location="form",
                    schema=coreschema.Integer(
                        minimum=0
                    )
                ),
                coreapi.Field(
                    "latitude",
                    required=False,
                    location="form",
                    schema=coreschema.Number(
                        title="Latitude",
                        description="Latitude"
                    )
                ),
                coreapi.Field(
                    "longitude",
                    required=False,
                    location="form",
                    schema=coreschema.Number(
                        title="Longitude",
                        description="Longitude"
                    )
                ),
                coreapi.Field(
                    "school_number",
                    required=False,
                    location="form",
                    schema=coreschema.Integer(
                        title="School number",
                        description="School number"
                    )
                ),
                coreapi.Field(
                    "school_category",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School category KEY",
                        description="School category KEY"
                    )
                ),
                coreapi.Field(
                    "school_type",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School type KEY",
                        description="School type KEY"
                    )
                ),
                coreapi.Field(
                    "organization_name",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Organization name",
                        description="Organization name"
                    )
                ),
                coreapi.Field(
                    "year_of_intervention",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Year of intervention date",
                        description='Year of intervention date "YYYY-MM-DD" format'
                    )
                ),
                coreapi.Field(
                    "medium",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School medium",
                        description="Medium KEY"
                    )
                ),

            ],
            description="Add School to NGO",
        )
        return schema

    @staticmethod
    def add_classroom():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="NGO's KEY",
                    )
                ),
                coreapi.Field(
                    "school_id",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="School's key",
                        description="KEY",
                    )
                ),
                coreapi.Field(
                    "standard_id",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Standard's key",
                        description="KEY"
                    )
                ),
                coreapi.Field(
                    "division",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Division",
                        description="Classroom division"
                    )
                ),
                coreapi.Field(
                    "notes",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Notes",
                        description="Notes"
                    )
                )
            ],
            description="Add Classroom to NGO",
        )
        return schema




