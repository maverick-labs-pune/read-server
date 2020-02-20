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

import json
import re

from django.core.management.base import BaseCommand


def get_po_path(locale, domain, locale_dir):
    return locale_dir + "/" + locale + "/LC_MESSAGES/" + domain + ".po"


# noinspection SpellCheckingInspection
def extract_from_po_file(po_path):
    with open(po_path, 'r', encoding='utf-8') as f:
        tuples = re.findall(r"msgid \"(.+)\"\nmsgstr \"(.+)\"", f.read())
    return tuples


def po_to_json(locales, domain, locale_dir):
    # create PO-like json data for i18n
    for locale in locales:
        obj = {}
        locale_file_path = 'static/locale_' + locale + '.json'
        # obj[locale] = {}
        tuples = extract_from_po_file(get_po_path(locale, domain, locale_dir))
        for tuple in tuples:
            obj[tuple[0]] = tuple[1]
            # obj[locale][tuple[0]] = tuple[1]

        with open(locale_file_path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False)

    return


class Command(BaseCommand):
    help = 'Create locale json files in static dir'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        locales = ["mr_IN", "en_IN"]
        domain = "django"
        localeDir = "locale"
        po_to_json(locales, domain, localeDir)
        return
