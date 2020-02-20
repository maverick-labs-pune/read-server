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

# Generated by Django 2.1.5 on 2019-05-06 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_sessions', '0002_auto_20190502_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readsession',
            name='type',
            field=models.CharField(choices=[('READ_SESSION_REGULAR', 'Regular'), ('READ_SESSION_EVALUATION', 'Evaluation'), ('READ_SESSION_BOOK_LENDING', 'READ_SESSION_BOOK_LENDING')], max_length=30),
        ),
    ]
