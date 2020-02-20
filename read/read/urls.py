"""read URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from academic_years import views as academic_year_views
from books import views as book_views
from classrooms import views as classroom_views
from ngos import views as ngo_views
from read.schemas import CoreAPISchemaGenerator
from read_sessions import views as read_session_views
from schools import views as school_views
from students import views as student_views
from users import views as user_views
from users.permissions import IsSuperUser

router = routers.SimpleRouter()
router.register(r'books', book_views.BookViewSet, base_name='books')
router.register(r'book_levels', book_views.BookLevelViewSet, base_name='book_levels')
router.register(r'inventory', book_views.InventoryViewSet, base_name='inventory')
router.register(r'classrooms', classroom_views.ClassroomViewSet, base_name='classrooms')
router.register(r'ngos', ngo_views.NGOViewSet, base_name='ngos')
router.register(r'levels', ngo_views.LevelViewSet, base_name='levels')
router.register(r'read_sessions', read_session_views.ReadSessionViewSet, base_name='read')
router.register(r'schools', school_views.SchoolViewSet, base_name='schools')
router.register(r'students', student_views.StudentViewSet, base_name='students')
router.register(r'users', user_views.UserViewSet, base_name='users')
router.register(r'standards', school_views.StandardViewSet, base_name='standards')
router.register(r'academic_years', academic_year_views.AcademicYearViewSet, base_name="academic_years")

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^docs/', include_docs_urls(title='The Read Project API Documentation',
    #                                  permission_classes=[IsSuperUser],
    #                                  generator_class=CoreAPISchemaGenerator)),
    # path('admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^login', user_views.login_view, name='login'),
    url(r'^logout', user_views.logout_view, name='logout'),
    url(r'^forgot_password', user_views.forgot_password, name='forgot_password'),
    url(r'^get_forgot_password_token', user_views.get_forgot_password_token, name='get_forgot_password_token'),
    url(r'^is_forgot_password_token_valid', user_views.is_forgot_password_token_valid,
        name='is_forgot_password_token_valid'),
    url(r'^book_fairy_forgot_password', user_views.book_fairy_forgot_password, name='book_fairy_forgot_password'),
    url(r'^mobile_login', user_views.login_mobile_view, name='login_mobile'),
    url(r'^mobile_logout', user_views.logout_mobile_view, name='logout_mobile'),
    url(r'^refresh_mobile_token', user_views.refresh_mobile_token_view, name='refresh_mobile_token'),
    url(r'^is_authenticated', user_views.is_authenticated, name='is_user_authenticated'),
    url(r'^translations', user_views.translations, name='translations'),
]

