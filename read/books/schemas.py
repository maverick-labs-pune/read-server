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


class BookSchema:
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
                        description="Book's KEY",
                    )
                ),
                coreapi.Field(
                    "name",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        title="Book's name",
                        description="Book's name",
                    )
                ),
                coreapi.Field(
                    "type",
                    required=False,
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
            description="Edit/update book to NGO",
        )
        return schema

    @staticmethod
    def deactivate_book():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    "id",
                    required=True,
                    location="path",
                    schema=coreschema.String(
                        title="KEY",
                        description="Book Key",
                    )
                )
            ],
            description="Deactivate Book",
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
                        title="Books file",
                        description="Contains information of books",
                    )
                )
            ],
            encoding="multipart/form-data",
            description="Import books through file",

        )
        return schema
