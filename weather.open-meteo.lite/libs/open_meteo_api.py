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
from pprint import pformat
from typing import Dict, List, Any

import simple_requests as requests

from .common.kodi_service import VERSION

logger = logging.getLogger(__name__)

GEOCODING_API_URL = 'https://geocoding-api.open-meteo.com/v1/search'
FORECAST_API_URL = 'https://api.open-meteo.com/v1/forecast'
FORECAST_API_BASE_PARAMS = {
    'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,'
               'weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,is_day',
    'hourly': 'temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,'
              'precipitation_probability,weather_code,surface_pressure,'
              'wind_speed_10m,wind_direction_10m,is_day',
    'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,'
             'wind_speed_10m_max,wind_direction_10m_dominant',
    'format': 'json',
    'timeformat': 'iso8601',
}

HEADERS = {
    'User-Agent': f'Open-Meteo Lite for Kodi v.{VERSION}',
    'Accept': 'application/json',
}


def _call_api(url: str, params: Dict[str, str]) -> Dict[str, Any]:
    response = requests.get(url, params=params, headers=HEADERS.copy())
    if not response.ok:
        logger.error('Open-Meteo returned error %s: %s', response.status_code, response.text)
        response.raise_for_status()
    response_data = response.json()
    logger.debug('Open-Meteo response:\n%s', pformat(response_data))
    return response_data


def search_location(name_query: str) -> List[Dict[str, Any]]:
    result = _call_api(GEOCODING_API_URL, params={'name': name_query})
    return result.get('results')


def get_forecast(latitude: float, longitude: float, timezone: str) -> Dict[str, Any]:
    params = FORECAST_API_BASE_PARAMS.copy()
    params['latitude'] = latitude
    params['longitude'] = longitude
    params['timezone'] = timezone
    return _call_api(FORECAST_API_URL, params=params)
