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

from rest_framework.routers import SimpleRouter
from schools import views


router = SimpleRouter()

router.register(r'school', views.SchoolViewSet, 'School')
router.register(r'schoolacademicyear', views.SchoolAcademicYearViewSet, 'SchoolAcademicYear')
router.register(r'schoolcategory', views.SchoolCategoryViewSet, 'SchoolCategory')
router.register(r'schooltype', views.SchoolTypeViewSet, 'SchoolType')
router.register(r'schoolmedium', views.SchoolMediumViewSet, 'SchoolMedium')
router.register(r'standard', views.StandardViewSet, 'Standard')
# router.register(r'schoolfunders', views.SchoolFundersViewSet, 'SchoolFunders')
# router.register(r'classroomfunders', views.ClassroomFundersViewSet, 'ClassroomFunders')

urlpatterns = router.urls
