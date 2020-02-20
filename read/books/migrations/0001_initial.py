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

# Generated by Django 2.1.5 on 2019-05-02 05:08

import books.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ngos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=books.models.generate_book_key, max_length=4, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('publisher', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_modification_time', models.DateTimeField(auto_now=True)),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ngos.NGO')),
            ],
            options={
                'db_table': 'books',
                'permissions': (('can_import', 'Can import book through excel file'), ('can_export', 'Can export book through excel file')),
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=books.models.generate_book_key, max_length=4, unique=True)),
                ('serial_number', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('go', 'Good'), ('da', 'Damaged'), ('lo', 'Lost')], max_length=2)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='books.Book')),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('book', 'serial_number')},
        ),
    ]
