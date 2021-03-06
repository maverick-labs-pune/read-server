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

# Generated by Django 2.1.5 on 2019-05-14 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20190503_1242'),
        ('books', '0005_auto_20190514_0913'),
        ('read_sessions', '0003_auto_20190506_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadSessionHomeLendingBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('le', 'Lend'), ('co', 'Collect')], max_length=2)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_modification_time', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='books.Book')),
                ('inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='books.Inventory')),
                ('read_session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='read_sessions.ReadSession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.Student')),
            ],
            options={
                'db_table': 'read_session_home_lending_books',
            },
        ),
    ]
