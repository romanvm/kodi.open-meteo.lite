# Copyright (C) 2024, Roman Miroshnychenko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib
import json
import logging
import re
from pathlib import Path

import xbmc
from xbmcaddon import Addon
from xbmcvfs import translatePath

ADDON = Addon()
ADDON_ID = ADDON.getAddonInfo('id')
VERSION = ADDON.getAddonInfo('version')

PATH = Path(translatePath(ADDON.getAddonInfo('path')))
PROFILE = Path(translatePath(ADDON.getAddonInfo('profile')))
ICON = str(PATH / 'icon.png')

LOG_FORMAT = '[{addon_id} v.{addon_version}] {filename}:{lineno} - {message}'


class KodiLogHandler(logging.Handler):
    """
    Logging handler that writes to the Kodi log with correct levels

    It also adds {addon_id} and {addon_version} variables available to log format.
    """
    LEVEL_MAP = {
        logging.NOTSET: xbmc.LOGNONE,
        logging.DEBUG: xbmc.LOGDEBUG,
        logging.INFO: xbmc.LOGINFO,
        logging.WARN: xbmc.LOGWARNING,
        logging.WARNING: xbmc.LOGWARNING,
        logging.ERROR: xbmc.LOGERROR,
        logging.CRITICAL: xbmc.LOGFATAL,
    }

    def emit(self, record):
        record.addon_id = ADDON_ID
        record.addon_version = VERSION
        message = self.format(record)
        kodi_log_level = self.LEVEL_MAP.get(record.levelno, xbmc.LOGDEBUG)
        xbmc.log(message, level=kodi_log_level)


def initialize_logging():
    """
    Initialize the root logger that writes to the Kodi log

    After initialization, you can use Python logging facilities as usual.
    """
    logging.basicConfig(
        format=LOG_FORMAT,
        style='{',
        level=logging.DEBUG,
        handlers=[KodiLogHandler()],
        force=True
    )


class GettextEmulator:
    """
    Emulate GNU Gettext by mapping resource.language.en_gb UI strings to their numeric string IDs
    """
    _instance = None

    class LocalizationError(Exception):  # pylint: disable=missing-docstring
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._en_gb_string_po_path = (PATH / 'resources' / 'language' /
                                      'resource.language.en_gb' / 'strings.po')
        if not self._en_gb_string_po_path.exists():
            raise self.LocalizationError(
                'Missing resource.language.en_gb strings.po localization file')
        if not PROFILE.exists():
            PROFILE.mkdir()
        self._string_mapping_path = PROFILE / 'strings-map.json'
        self.strings_mapping = self._load_strings_mapping()

    def _load_strings_po(self):  # pylint: disable=missing-docstring
        with self._en_gb_string_po_path.open('r', encoding='utf-8') as fo:
            return fo.read()

    def _load_strings_mapping(self):
        """
        Load mapping of resource.language.en_gb UI strings to their IDs

        If a mapping file is missing or resource.language.en_gb strins.po file has been updated,
        a new mapping file is created.

        :return: UI strings mapping
        """
        strings_po = self._load_strings_po()
        strings_po_md5 = hashlib.md5(strings_po.encode('utf-8')).hexdigest()
        try:
            with self._string_mapping_path.open('r', encoding='utf-8') as fo:
                mapping = json.load(fo)
            if mapping['md5'] != strings_po_md5:
                raise IOError('resource.language.en_gb strings.po has been updated')
        except (IOError, ValueError):
            strings_mapping = self._parse_strings_po(strings_po)
            mapping = {
                'strings': strings_mapping,
                'md5': strings_po_md5,
            }
            with self._string_mapping_path.open('w', encoding='utf-8') as fo:
                json.dump(mapping, fo)
        return mapping['strings']

    @staticmethod
    def _parse_strings_po(strings_po):
        """
        Parse resource.language.en_gb strings.po file contents into a mapping of UI strings
        to their numeric IDs.

        :param strings_po: the content of strings.po file as a text string
        :return: UI strings mapping
        """
        id_string_pairs = re.findall(r'^msgctxt "#(\d+?)"\r?\nmsgid "(.*)"\r?$', strings_po, re.M)
        return {string: int(string_id) for string_id, string in id_string_pairs if string}

    @classmethod
    def gettext(cls, en_string: str) -> str:
        """
        Return a localized UI string by a resource.language.en_gb source string

        :param en_string: resource.language.en_gb UI string
        :return: localized UI string
        """
        emulator = cls()
        try:
            string_id = emulator.strings_mapping[en_string]
        except KeyError as exc:
            raise cls.LocalizationError(
                f'Unable to find "{en_string}" string in resource.language.en_gb/strings.po'
            ) from exc
        return ADDON.getLocalizedString(string_id)
