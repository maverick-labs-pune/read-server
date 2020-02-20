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

from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.generators import is_custom_action, LinkNode, insert_into
from rest_framework.schemas.utils import is_list_view

from books.schemas import BookSchema
from ngos.schemas import NGOSchema
from schools.schemas import SchoolSchema
from students.schemas import StudentSchema
from users.schemas import UserSchema

custom_schemas = {
    ('/ngos/', 'POST'): NGOSchema.create(),
    ('/ngos/{id}/', 'PUT'): NGOSchema.update(),
    ('/books/{id}/', 'PUT'): BookSchema.update(),
    ('/schools/{id}/', 'PUT'): SchoolSchema.update(),
    ('/students/', 'POST'): StudentSchema.create(),
    ('/students/{id}/', 'PUT'): StudentSchema.update(),
    ('/users/{id}/', 'PUT'): UserSchema.update(),

}


class CoreAPISchemaGenerator(SchemaGenerator):

    def get_keys(self, subpath, method, view):
        """
        Return a list of keys that should be used to layout a link within
        the schema document.

        /users/                   ("users", "list"), ("users", "create")
        /users/{pk}/              ("users", "read"), ("users", "update"), ("users", "delete")
        /users/enabled/           ("users", "enabled")  # custom viewset list action
        /users/{pk}/star/         ("users", "star")     # custom viewset detail action
        /users/{pk}/groups/       ("users", "groups", "list"), ("users", "groups", "create")
        /users/{pk}/groups/{pk}/  ("users", "groups", "read"), ("users", "groups", "update"), ("users", "groups", "delete")
        """
        if hasattr(view, 'action'):
            # Viewsets have explicitly named actions.
            action = view.action
        else:
            # Views have no associated action, so we determine one from the method.
            if is_list_view(subpath, method, view):
                action = 'list'
            else:
                action = self.default_mapping[method.lower()]

        named_path_components = [
            component for component
            in subpath.strip('/').split('/')
            if '{' not in component
        ]

        if is_custom_action(action):
            # Custom action, eg "/users/{pk}/activate/", "/users/active/"
            if len(view.action_map) > 1:
                action = self.default_mapping[method.lower()]
                if action in self.coerce_method_names:
                    action = self.coerce_method_names[action]
                return named_path_components + [action]
            else:
                return named_path_components[:-1] + [action]

        if action in self.coerce_method_names:
            action = self.coerce_method_names[action]

        # Default action, eg "/users/", "/users/{pk}/"
        return named_path_components + [action]

    def get_links(self, request=None):
        """
        Return a dictionary containing all the links that should be
        included in the API schema.
        """
        links = LinkNode()

        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue

            schema = custom_schemas.get((path, method))
            if schema:
                link = schema.get_link(path, method, base_url=self.url)
            else:
                link = view.schema.get_link(path, method, base_url=self.url)
            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, link)

        return links
