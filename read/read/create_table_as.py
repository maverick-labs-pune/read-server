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

from django.db import DEFAULT_DB_ALIAS, connections


def create_table_as(table_name, queryset, using=DEFAULT_DB_ALIAS):
    compiler = queryset.query.get_compiler(using=using)
    sql, params = compiler.as_sql()
    connection = connections[DEFAULT_DB_ALIAS]
    sql = "CREATE TABLE " + connection.ops.quote_name(table_name) + " AS " + sql
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
