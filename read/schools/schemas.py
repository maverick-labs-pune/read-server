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


class SchoolSchema:

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
                        description="NGO's KEY",
                    )
                ),
                coreapi.Field(
                    "name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="School name",
                        description="School name",
                    )
                ),
                coreapi.Field(
                    "address",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="School address",
                        description="School address"
                    )
                ),
                coreapi.Field(
                    "pincode",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="School pincode",
                        description="School pincode"
                    )
                ),
                coreapi.Field(
                    "ward_number",
                    required=False,
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
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="School category KEY",
                        description="School category KEY"
                    )
                ),
                coreapi.Field(
                    "school_type",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="School type KEY",
                        description="School type KEY"
                    )
                ),
                coreapi.Field(
                    "organization_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Organization name",
                        description="Organization name"
                    )
                ),
                coreapi.Field(
                    "year_of_intervention",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Year of intervention date",
                        description='Year of intervention date "YYYY-MM-DD" format'
                    )
                ),
                coreapi.Field(
                    "medium",
                    required=False,
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
    def deactivate_school():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="School Key",
                    )
                )
            ],
            description="Deactivate School",
        )
        return schema
