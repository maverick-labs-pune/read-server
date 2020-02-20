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

from rest_framework import permissions

# NGOS
from read.constants import GroupType

PERMISSION_CAN_ADD_NGO = ('add_ngo', 'Can add ngo', 'ngos.add_ngo')
PERMISSION_CAN_CHANGE_NGO = ('change_ngo', 'Can change ngo', 'ngos.change_ngo')
PERMISSION_CAN_DESTROY_NGO = ('delete_ngo', 'Can delete ngo', 'ngos.delete_ngo')
PERMISSION_CAN_VIEW_NGO = ('view_ngo', 'Can view ngo', 'ngos.view_ngo')
PERMISSIONS_NGO = [PERMISSION_CAN_ADD_NGO, PERMISSION_CAN_CHANGE_NGO, PERMISSION_CAN_DESTROY_NGO,
                   PERMISSION_CAN_VIEW_NGO]

# LEVEL
PERMISSION_CAN_ADD_LEVEL = ('add_level', 'Can add level', 'ngos.add_level')
PERMISSION_CAN_CHANGE_LEVEL = ('change_level', 'Can change level', 'ngos.change_level')
PERMISSION_CAN_DESTROY_LEVEL = ('delete_level', 'Can delete level', 'ngos.delete_level')
PERMISSIONS_LEVEL = [PERMISSION_CAN_ADD_LEVEL, PERMISSION_CAN_CHANGE_LEVEL, PERMISSION_CAN_DESTROY_LEVEL]

# USERS
PERMISSION_CAN_ADD_USER = ('add_user', 'Can add user', 'users.add_user')
PERMISSION_CAN_CHANGE_USER = ('change_user', 'Can change user', 'users.change_user')
PERMISSION_CAN_DESTROY_USER = ('delete_user', 'Can delete user', 'users.delete_user')
PERMISSION_CAN_VIEW_USER = ('view_user', 'Can view user', 'users.view_user')
PERMISSION_CAN_IMPORT_USERS = ('can_import', 'Can import user through excel file', 'users.can_import')
PERMISSION_CAN_EXPORT_USERS = ('can_export', 'Can export user through excel file', 'users.can_export')
PERMISSIONS_USER = [PERMISSION_CAN_ADD_USER, PERMISSION_CAN_CHANGE_USER, PERMISSION_CAN_DESTROY_USER,
                    PERMISSION_CAN_VIEW_USER, PERMISSION_CAN_IMPORT_USERS, PERMISSION_CAN_EXPORT_USERS, ]

# SCHOOLS

PERMISSION_CAN_ADD_SCHOOL = ('add_school', 'Can add school', 'schools.add_school')
PERMISSION_CAN_CHANGE_SCHOOL = ('change_school', 'Can change school', 'schools.change_school')
PERMISSION_CAN_DESTROY_SCHOOL = ('delete_school', 'Can delete school', 'schools.delete_school')
PERMISSION_CAN_VIEW_SCHOOL = ('view_school', 'Can view school', 'schools.view_school')
PERMISSION_CAN_IMPORT_SCHOOLS = ('can_import', 'Can import school through excel file', 'schools.can_import')
PERMISSION_CAN_EXPORT_SCHOOLS = ('can_export', 'Can export school through excel file', 'schools.can_export')
PERMISSIONS_SCHOOL = [PERMISSION_CAN_ADD_SCHOOL, PERMISSION_CAN_CHANGE_SCHOOL, PERMISSION_CAN_DESTROY_SCHOOL,
                      PERMISSION_CAN_VIEW_SCHOOL, PERMISSION_CAN_IMPORT_SCHOOLS, PERMISSION_CAN_EXPORT_SCHOOLS]

# BOOKS

PERMISSION_CAN_ADD_BOOK = ('add_book', 'Can add book', 'books.add_book')
PERMISSION_CAN_CHANGE_BOOK = ('change_book', 'Can change book', 'books.change_book')
PERMISSION_CAN_DESTROY_BOOK = ('delete_book', 'Can delete book', 'books.delete_book')
PERMISSION_CAN_VIEW_BOOK = ('view_book', 'Can view book', 'books.view_book')
PERMISSION_CAN_IMPORT_BOOKS = ('can_import', 'Can import book through excel file', 'books.can_import')
PERMISSION_CAN_EXPORT_BOOKS = ('can_export', 'Can export book through excel file', 'books.can_export')
PERMISSIONS_BOOK = [PERMISSION_CAN_ADD_BOOK, PERMISSION_CAN_CHANGE_BOOK, PERMISSION_CAN_DESTROY_BOOK,
                    PERMISSION_CAN_VIEW_BOOK, PERMISSION_CAN_IMPORT_BOOKS, PERMISSION_CAN_EXPORT_BOOKS]

# INVENTORY

PERMISSION_CAN_ADD_INVENTORY = ('add_inventory', 'Can add inventory', 'books.add_inventory')
PERMISSION_CAN_CHANGE_INVENTORY = ('change_inventory', 'Can change inventory', 'books.change_inventory')
PERMISSION_CAN_DESTROY_INVENTORY = ('delete_inventory', 'Can delete inventory', 'books.delete_inventory')
PERMISSION_CAN_VIEW_INVENTORY = ('view_inventory', 'Can view inventory', 'books.view_inventory')
PERMISSIONS_INVENTORY = [PERMISSION_CAN_ADD_INVENTORY, PERMISSION_CAN_CHANGE_INVENTORY,
                         PERMISSION_CAN_DESTROY_INVENTORY,
                         PERMISSION_CAN_VIEW_INVENTORY, ]

# CLASSROOMS

PERMISSION_CAN_ADD_CLASSROOM = ('add_classroom', 'Can add classroom', 'classrooms.add_classroom')
PERMISSION_CAN_CHANGE_CLASSROOM = ('change_classroom', 'Can change classroom', 'classrooms.change_classroom')
PERMISSION_CAN_DESTROY_CLASSROOM = ('delete_classroom', 'Can delete classroom', 'classrooms.delete_classroom')
PERMISSION_CAN_VIEW_CLASSROOM = ('view_classroom', 'Can view classroom', 'classrooms.view_classroom')
PERMISSIONS_CLASSROOM = [PERMISSION_CAN_ADD_CLASSROOM, PERMISSION_CAN_CHANGE_CLASSROOM,
                         PERMISSION_CAN_DESTROY_CLASSROOM,
                         PERMISSION_CAN_VIEW_CLASSROOM, ]

# STUDENTS

PERMISSION_CAN_ADD_STUDENT = ('add_student', 'Can add student', 'students.add_student')
PERMISSION_CAN_CHANGE_STUDENT = ('change_student', 'Can change student', 'students.change_student')
PERMISSION_CAN_DESTROY_STUDENT = ('delete_student', 'Can delete student', 'students.delete_student')
PERMISSION_CAN_VIEW_STUDENT = ('view_student', 'Can view student', 'students.view_student')
PERMISSION_CAN_IMPORT_STUDENTS = ('can_import', 'Can import students through excel file', 'students.can_import')
PERMISSION_CAN_EXPORT_STUDENTS = ('can_export', 'Can export students through excel file', 'students.can_export')

PERMISSIONS_STUDENT = [PERMISSION_CAN_ADD_STUDENT, PERMISSION_CAN_CHANGE_STUDENT, PERMISSION_CAN_DESTROY_STUDENT,
                       PERMISSION_CAN_VIEW_STUDENT, PERMISSION_CAN_IMPORT_STUDENTS, PERMISSION_CAN_EXPORT_STUDENTS]

# SESSIONS

PERMISSION_CAN_ADD_READ_SESSION = ('add_readsession', 'Can add read session', 'read_sessions.add_readsession')
PERMISSION_CAN_CHANGE_READ_SESSION = (
    'change_readsession', 'Can change read session', 'read_sessions.change_readsession')
PERMISSION_CAN_DESTROY_READ_SESSION = (
    'delete_readsession', 'Can delete read session', 'read_sessions.delete_readsession')
PERMISSION_CAN_VIEW_READ_SESSION = ('view_readsession', 'Can view read session', 'read_sessions.view_readsession')
PERMISSIONS_SESSION = [PERMISSION_CAN_ADD_READ_SESSION, PERMISSION_CAN_CHANGE_READ_SESSION,
                       PERMISSION_CAN_DESTROY_READ_SESSION,
                       PERMISSION_CAN_VIEW_READ_SESSION]

PERMISSION_CAN_ADD_READ_SESSION_CLASSROOM = (
    'add_readsessionclassroom', 'Can add read session classroom', 'readsessionclassrooms.add_readsessionclassroom')
PERMISSION_CAN_CHANGE_READ_SESSION_CLASSROOM = (
    'change_readsessionclassroom', 'Can change read session classroom',
    'readsessionclassrooms.change_readsessionclassroom')
PERMISSION_CAN_DESTROY_READ_SESSION_CLASSROOM = ('delete_readsessionclassroom', 'Can delete read session classroom',
                                                 'readsessionclassrooms.delete_readsessionclassroom')
PERMISSION_CAN_VIEW_READ_SESSION_CLASSROOM = (
    'view_readsessionclassroom', 'Can view read session classroom', 'readsessionclassrooms.view_readsessionclassroom')
PERMISSIONS_READ_SESSION_CLASSROOM = [PERMISSION_CAN_ADD_READ_SESSION_CLASSROOM,
                                      PERMISSION_CAN_CHANGE_READ_SESSION_CLASSROOM,
                                      PERMISSION_CAN_DESTROY_READ_SESSION_CLASSROOM,
                                      PERMISSION_CAN_VIEW_READ_SESSION_CLASSROOM]

PERMISSION_CAN_ADD_READ_SESSION_BOOK_FAIRY = (
    'add_readsessionbookfairy', 'Can add read session book fairy', 'readsessionbookfairys.add_readsessionbookfairy')
PERMISSION_CAN_CHANGE_READ_SESSION_BOOK_FAIRY = ('change_readsessionbookfairy', 'Can change read session book fairy',
                                                 'readsessionbookfairys.change_readsessionbookfairy')
PERMISSION_CAN_DESTROY_READ_SESSION_BOOK_FAIRY = ('delete_readsessionbookfairy', 'Can delete read session book fairy',
                                                  'readsessionbookfairys.delete_readsessionbookfairy')
PERMISSION_CAN_VIEW_READ_SESSION_BOOK_FAIRY = (
    'view_readsessionbookfairy', 'Can view read session book fairy', 'readsessionbookfairys.view_readsessionbookfairy')
PERMISSIONS_READ_SESSION_BOOK_FAIRY = [PERMISSION_CAN_ADD_READ_SESSION_BOOK_FAIRY,
                                       PERMISSION_CAN_CHANGE_READ_SESSION_BOOK_FAIRY,
                                       PERMISSION_CAN_DESTROY_READ_SESSION_BOOK_FAIRY,
                                       PERMISSION_CAN_VIEW_READ_SESSION_BOOK_FAIRY]

PERMISSIONS_READ_ADMIN = PERMISSIONS_NGO + [PERMISSION_CAN_ADD_USER, PERMISSION_CAN_CHANGE_USER,
                                            PERMISSION_CAN_VIEW_USER]

PERMISSIONS_NGO_ADMIN = PERMISSIONS_BOOK + PERMISSIONS_SESSION + PERMISSIONS_SCHOOL + PERMISSIONS_USER + \
                        PERMISSIONS_STUDENT + PERMISSIONS_READ_SESSION_BOOK_FAIRY + PERMISSIONS_READ_SESSION_CLASSROOM + \
                        [PERMISSION_CAN_CHANGE_NGO,
                         PERMISSION_CAN_VIEW_NGO,PERMISSION_CAN_CHANGE_USER] + PERMISSIONS_LEVEL + PERMISSIONS_INVENTORY + \
                        PERMISSIONS_CLASSROOM
PERMISSIONS_NGO_BOOK_FAIRY = PERMISSIONS_SESSION + [PERMISSION_CAN_VIEW_INVENTORY, PERMISSION_CAN_VIEW_USER, PERMISSION_CAN_CHANGE_USER]
PERMISSION_NGO_SUPERVISIOR = PERMISSIONS_SESSION + [PERMISSION_CAN_VIEW_USER, PERMISSION_CAN_CHANGE_USER]


def has_permission(request, permission):
    if request.user and request.user.has_perm(permission[2]):
        return True
    return False


class IsSuperUser(permissions.BasePermission):
    """
    Allow if user is a SuperUser
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False


class IsBookFairy(permissions.BasePermission):
    """
    Allow if user is a Book Fairy
    """

    def has_permission(self, request, view):
        if request.user:
            groups = request.user.groups.all()
            if groups.count() == 1 and groups[0].name.find(GroupType.BOOK_FAIRY.value) != -1:
                return True
        return False


class CanAddUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_USER)


class CanChangeUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_USER)


class CanDeleteUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_USER)


class CanViewUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_USER)


class CanImportUsers(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_IMPORT_USERS)


class CanExportUsers(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_EXPORT_USERS)


class CanAddNGO(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_NGO)


class CanChangeNGO(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_NGO)


class CanDeleteNGO(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_NGO)


class CanViewNGO(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_NGO)


class CanAddBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_BOOK)


class CanChangeBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_BOOK)


class CanDeleteBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_BOOK)


class CanViewBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_BOOK)


class CanImportBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_IMPORT_BOOKS)


class CanExportBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_EXPORT_BOOKS)


class CanImportSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_IMPORT_SCHOOLS)


class CanExportSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_EXPORT_SCHOOLS)


class CanAddInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_INVENTORY)


class CanChangeInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_INVENTORY)


class CanDeleteInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_INVENTORY)


class CanViewInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_INVENTORY)


class CanAddStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_STUDENT)


class CanChangeStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_STUDENT)


class CanDeleteStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_STUDENT)


class CanViewStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_STUDENT)


class CanImportStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_IMPORT_STUDENTS)


class CanExportStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_EXPORT_STUDENTS)


class CanAddReadSession(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_READ_SESSION)


class CanChangeReadSession(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_READ_SESSION)


class CanDeleteReadSession(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_READ_SESSION)


class CanViewReadSession(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_READ_SESSION)


class CanAddSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_SCHOOL)


class CanChangeSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_SCHOOL)


class CanDeleteSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_SCHOOL)


class CanViewSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_SCHOOL)


class CanAddLevel(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_LEVEL)


class CanChangeLevel(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_LEVEL)


class CanDeleteLevel(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user.get_all_permissions())
        return has_permission(request, PERMISSION_CAN_DESTROY_LEVEL)


class CanAddClassroom(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_CLASSROOM)


class CanChangeClassroom(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_CLASSROOM)


class CanDeleteClassroom(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_CLASSROOM)


class CanViewClassroom(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_CLASSROOM)


class CanAddInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_ADD_INVENTORY)


class CanChangeInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_CHANGE_INVENTORY)


class CanDeleteInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_DESTROY_INVENTORY)


class CanViewInventory(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_permission(request, PERMISSION_CAN_VIEW_INVENTORY)
