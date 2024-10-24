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

import logging
import sys
from typing import Dict, Any

import xbmc
import xbmcgui

from .common.kodi_service import ADDON, ADDON_ID, GettextEmulator
from .open_meteo_api import search_location

_ = GettextEmulator.gettext

logger = logging.getLogger(__name__)
DIALOG = xbmcgui.Dialog()


def _get_full_location_name(location_info: Dict[str, Any]) -> str:
    name_parts = [location_info['name']]
    admin1 = location_info.get('admin1')
    if admin1:
        name_parts.append(admin1)
    admin2 = location_info.get('admin2')
    if admin2:
        name_parts.append(admin2)
    admin3 = location_info.get('admin3')
    if admin3:
        name_parts.append(admin3)
    name_parts.append(location_info['country'])
    return ', '.join(name_parts)


def _save_location_info(location_id: str,
                        full_location_name: str,
                        location_info: Dict[str, Any]) -> None:
    ADDON.setSettingString(location_id, full_location_name)
    ADDON.setSettingString(f'{location_id}_name', location_info['name'])
    ADDON.setSettingNumber(f'{location_id}_lat', location_info['latitude'])
    ADDON.setSettingNumber(f'{location_id}_lon', location_info['longitude'])
    ADDON.setSettingString(f'{location_id}_timezone', location_info['timezone'])


def set_location(location_id: str) -> None:
    logger.debug('Setting location info for location_id %s', location_id)
    location_name = ADDON.getSettingString(f'{location_id}_name')
    keyboard = xbmc.Keyboard(
        location_name,
        _('Enter location')
    )
    keyboard.doModal()
    location_name = keyboard.getText()
    if not location_name:
        DIALOG.notification(
            ADDON_ID,
            _('Location is not entered'),
            icon=xbmcgui.NOTIFICATION_WARNING
        )
        return
    location_results = search_location(location_name)
    if not location_results:
        DIALOG.notification(
            ADDON_ID,
            _('Location not found'),
            icon=xbmcgui.NOTIFICATION_WARNING
        )
        return
    if len(location_results) == 1:
        location_info = location_results[0]
        full_location_name = _get_full_location_name(location_info)
        _save_location_info(location_id, full_location_name, location_info)
    location_options = []
    for location_info in location_results:
        full_location_name = _get_full_location_name(location_info)
        location_options.append(full_location_name)
    selection = DIALOG.select(_('Select location'), location_options)
    if selection == -1:
        DIALOG.notification(
            ADDON_ID,
            _('No location selected'),
            icon=xbmcgui.NOTIFICATION_WARNING
        )
        return
    full_location_name = location_options[selection]
    location_info = location_results[selection]
    _save_location_info(location_id, full_location_name, location_info)
    logger.debug('Location "%s" was set for %s', full_location_name, location_id)


def populate_weather_info(location_no: str) -> None:
    logger.debug('Populating weather info for location_%s...', location_no)


def main() -> None:
    parameter = sys.argv[1]
    if parameter.startswith('location'):
        set_location(parameter)
        return
    populate_weather_info(parameter)
