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

from .common.kodi_service import GettextEmulator

_ = GettextEmulator.gettext

logger = logging.getLogger(__name__)


def set_location(location_id: str) -> None:
    pass


def populate_weather_info(location_no: str) -> None:
    pass


def main():
    parameter = sys.argv[1]
    if parameter.startswith('location'):
        set_location(parameter)
        return
    populate_weather_info(parameter)
