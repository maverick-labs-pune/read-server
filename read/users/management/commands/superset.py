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

from django.core.management import BaseCommand
from django.db import connection

from ngos.models import NGO
from read.create_table_as import create_table_as
from read_sessions.models import ReadSession
from django.db.models import F, CharField
from django.db.models import Value
from django.db.models.functions import Concat


def _superset_init():
    with connection.cursor() as cursor:
        ngos = NGO.objects.all().values_list("name", flat=True)

        # /Drop temporary tables in case the process got cut off before
        for ngo in ngos:
            drop_table_str = "DROP TABLE IF EXISTS %s_sessions_feedback_master_details" % ngo
            cursor.execute(
                drop_table_str
            )
            # Create the new table from the summary query
            ngo_filter = {
                'readsessionclassroom__classroom__school__ngo__name': ngo,
                'readsessionclassroom__classroom__school__ngo__is_active': True
            }
            feedback_sessions = ReadSession.objects.filter(**ngo_filter).annotate(
                session_id=F('id'),
                session_type=F('type'),
                session_academic_year=F('academic_year__name'),
                session_start_date_time=F('start_date_time'),
                session_end_date_time=F('end_date_time'),
                session_is_evaluated=F('is_evaluated'),
                session_is_verified=F('is_verified'),
                session_is_cancelled=F('is_cancelled'),
                session_level=F('studentfeedback__level__en_in'),
                session_feedback_comments=F('studentfeedback__comments'),
                school_name=F('readsessionclassroom__classroom__school__name'),
                school_ngo=F('readsessionclassroom__classroom__school__ngo__name'),
                school_category=F('readsessionclassroom__classroom__school__school_category__name'),
                school_type=F('readsessionclassroom__classroom__school__school_type__name'),
                school_medium=F('readsessionclassroom__classroom__school__medium__name'),
                school_is_active=F('readsessionclassroom__classroom__school__is_active'),
                classroom=Concat('readsessionclassroom__classroom__school__name',
                                 Value(' '),
                                 'readsessionclassroom__classroom__standard',
                                 Value(' '),
                                 'readsessionclassroom__classroom__division', output_field=CharField()),
                student_name=Concat('readsessionclassroom__classroom__classroomacademicyear__student__first_name',
                                    Value(' '),
                                    'readsessionclassroom__classroom__classroomacademicyear__student__last_name'),
                student_gender=F('readsessionclassroom__classroom__classroomacademicyear__student__gender'),
                student_is_dropout=F('readsessionclassroom__classroom__classroomacademicyear__student__is_dropout'),
                student_has_attended_preschool=F(
                    'readsessionclassroom__classroom__classroomacademicyear__student__has_attended_preschool'),
                student_is_active=F('readsessionclassroom__classroom__classroomacademicyear__student__is_active'),
                student_attendance=F('studentfeedback__attendance')
            ).values_list(
                'session_id',
                'session_type',
                'session_academic_year',
                'session_start_date_time',
                'session_end_date_time',
                'session_is_evaluated',
                'session_is_verified',
                'session_is_cancelled',
                'session_level',
                'session_feedback_comments',
                'school_name',
                'school_ngo',
                'school_category',
                'school_type',
                'school_medium',
                'school_is_active',
                'classroom',
                'student_name',
                'student_gender',
                'student_is_dropout',
                'student_has_attended_preschool',
                'student_is_active',
                'student_attendance'
            )
            create_table_str = "%s_sessions_feedback_master_details" % ngo
            create_table_as(
                create_table_str,
                feedback_sessions,
            )


class Command(BaseCommand):
    help = 'Create tables for superset'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        _superset_init()
        print("Finished")
        return
