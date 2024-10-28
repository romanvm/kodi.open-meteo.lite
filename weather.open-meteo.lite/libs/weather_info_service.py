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
# along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
This module includes functions that are responsible for populating various weather-related
properties of the Weather window (id=12600)
"""

import logging
from datetime import datetime, date
from pprint import pformat
from typing import NamedTuple, Dict, List, Any, Optional

import xbmc
from xbmcgui import Window

from libs.common.kodi_service import ADDON, BANNER, ADDON_NAME
from libs.converter_service import (
    get_weather_condition_label,
    get_kodi_weather_code,
    get_wind_direction,
    get_temperature,
    get_wind_speed,
)
from libs.open_meteo_api import get_forecast, OPEN_METEO_DATE_TIME_FORMAT, OPEN_METEO_DATE_FORMAT

logger = logging.getLogger(__name__)

WEATHER_WINDOW = Window(12600)

LONG_DATE_FORMAT = xbmc.getRegion('datelong')
SHORT_DATE_FORMAT = xbmc.getRegion('dateshort')
TIME_FORMAT = xbmc.getRegion('time').replace(':%S', '')
TEMPERATURE_UNIT = xbmc.getRegion('tempunit')
SPEED_UNIT = xbmc.getRegion('speedunit')


class LocationData(NamedTuple):
    name: str
    longitude: float
    latitude: float
    timezone: str


class HourlyWeather(NamedTuple):
    time: datetime
    temperature_2m: int
    relative_humidity_2m: int
    dew_point_2m: int
    apparent_temperature: int
    precipitation_probability: int
    weather_code: int
    surface_pressure: int
    wind_speed_10m: float
    wind_direction_10m: int
    cloud_cover: int
    is_day: bool

    @classmethod
    def from_raw_values(cls, **values):
        return cls(
            time=datetime.strptime(values['time'], OPEN_METEO_DATE_TIME_FORMAT),
            temperature_2m=round(values['temperature_2m']),
            relative_humidity_2m=values['relative_humidity_2m'],
            dew_point_2m=round(values['dew_point_2m']),
            apparent_temperature=round(values['apparent_temperature']),
            precipitation_probability=values['precipitation_probability'],
            weather_code=values['weather_code'],
            surface_pressure=round(values['surface_pressure']),
            wind_speed_10m=values['wind_speed_10m'],
            wind_direction_10m=values['wind_direction_10m'],
            cloud_cover=values['cloud_cover'],
            is_day=bool(values['is_day'])
        )


class DailyWeather(NamedTuple):
    time: date
    weather_code: int
    temperature_2m_max: int
    temperature_2m_min: int
    sunrise: datetime
    sunset: datetime
    precipitation_probability_mean: int
    wind_speed_10m_max: float
    wind_direction_10m_dominant: int
    uv_index_max: float

    @classmethod
    def from_raw_values(cls, **values):
        return cls(
            time=datetime.strptime(values['time'], OPEN_METEO_DATE_FORMAT).date(),
            weather_code=values['weather_code'],
            temperature_2m_max=round(values['temperature_2m_max']),
            temperature_2m_min=round(values['temperature_2m_min']),
            sunrise=datetime.strptime(values['sunrise'], OPEN_METEO_DATE_TIME_FORMAT),
            sunset=datetime.strptime(values['sunset'], OPEN_METEO_DATE_TIME_FORMAT),
            precipitation_probability_mean=values['precipitation_probability_mean'],
            wind_speed_10m_max=values['wind_speed_10m_max'],
            wind_direction_10m_dominant=values['wind_direction_10m_dominant'],
            uv_index_max=values['uv_index_max']
        )


def _get_location_data(location_id: str) -> Optional[LocationData]:
    name = ADDON.getSettingString(f'{location_id}_name')
    latitude = ADDON.getSettingNumber(f'{location_id}_lat')
    longitude = ADDON.getSettingNumber(f'{location_id}_lon')
    timezone = ADDON.getSettingString(f'{location_id}_timezone')
    location_data = LocationData(name, latitude, longitude, timezone)
    if not all(location_data):
        return None
    return location_data


def _populate_current_weather(current_info: Dict[str, Any]) -> None:
    open_meteo_weather_code = current_info['weather_code']
    is_day = bool(current_info['is_day'])
    kodi_weather_code = get_kodi_weather_code(open_meteo_weather_code, is_day)
    window_properties_map = {
        'Current.Condition': get_weather_condition_label(open_meteo_weather_code, is_day),
        'Current.Temperature': str(round(current_info['temperature_2m'])),
        'Current.Wind': str(current_info['wind_speed_10m']),
        'Current.WindDirection': get_wind_direction(current_info['wind_direction_10m']),
        'Current.Humidity': str(round(current_info['relative_humidity_2m'])),
        'Current.FeelsLike': str(round(current_info['apparent_temperature'])),
        'Current.OutlookIcon': f'{kodi_weather_code}.png',
        'Current.FanartCode': kodi_weather_code,
    }
    logger.debug('Populating current weather:\n%s', pformat(window_properties_map))
    for prop, value in window_properties_map.items():
        WEATHER_WINDOW.setProperty(prop, value)


def _populate_hourly_weather(hourly_info: Dict[str, List[Any]]) -> None:
    keys = tuple(hourly_info.keys())
    first_hour = True
    for i, values in enumerate(zip(*hourly_info.values()), 1):
        hourly_weather = HourlyWeather.from_raw_values(**dict(zip(keys, values)))
        if first_hour:
            WEATHER_WINDOW.setProperty('Current.DewPoint', str(hourly_weather.dew_point_2m))
            WEATHER_WINDOW.setProperty('Current.Precipitation',
                                       str(hourly_weather.precipitation_probability) + '%')
            WEATHER_WINDOW.setProperty('Current.Cloudiness', str(hourly_weather.cloud_cover) + '%')
            first_hour = False
        hourly_prefix = f'Hourly.{i}'
        kodi_weather_code = get_kodi_weather_code(hourly_weather.weather_code,
                                                  hourly_weather.is_day)
        window_properties_map = {
            f'{hourly_prefix}.Time': hourly_weather.time.strftime(TIME_FORMAT),
            f'{hourly_prefix}.LongDate': hourly_weather.time.strftime(LONG_DATE_FORMAT),
            f'{hourly_prefix}.ShortDate': hourly_weather.time.strftime(SHORT_DATE_FORMAT),
            f'{hourly_prefix}.Outlook': get_weather_condition_label(hourly_weather.weather_code,
                                                             hourly_weather.is_day),
            f'{hourly_prefix}.OutlookIcon': f'{kodi_weather_code}.png',
            f'{hourly_prefix}.FanartCode': kodi_weather_code,
            f'{hourly_prefix}.WindSpeed': get_wind_speed(hourly_weather.wind_speed_10m, SPEED_UNIT),
            f'{hourly_prefix}.WindDirection': get_wind_direction(hourly_weather.wind_direction_10m),
            f'{hourly_prefix}.Humidity': str(hourly_weather.relative_humidity_2m),
            f'{hourly_prefix}.Temperature': get_temperature(hourly_weather.temperature_2m,
                                                            TEMPERATURE_UNIT),
            f'{hourly_prefix}.DewPoint': str(hourly_weather.dew_point_2m),
            f'{hourly_prefix}.FeelsLike': get_temperature(hourly_weather.apparent_temperature,
                                                          TEMPERATURE_UNIT),
            f'{hourly_prefix}.Pressure': str(hourly_weather.surface_pressure),
            f'{hourly_prefix}.Precipitation': str(hourly_weather.precipitation_probability) + '%',
        }
        logger.debug('Setting hourly weather %s:\n%s', i, pformat(window_properties_map))
        for prop, value in window_properties_map.items():
            WEATHER_WINDOW.setProperty(prop, value)


def _populate_daily_weather(daily_info: Dict[str, List[Any]]) -> None:
    keys = tuple(daily_info.keys())
    first_day = True
    for i, values in enumerate(zip(*daily_info.values()), 1):
        daily_weather = DailyWeather.from_raw_values(**dict(zip(keys, values)))
        if first_day:
            WEATHER_WINDOW.setProperty('Today.Sunrise', daily_weather.sunrise.strftime(TIME_FORMAT))
            WEATHER_WINDOW.setProperty('Today.Sunset', daily_weather.sunset.strftime(TIME_FORMAT))
            WEATHER_WINDOW.setProperty('Current.UVIndex', str(daily_weather.uv_index_max))
            first_day = False
        daily_prefix = f'Daily.{i}'
        kodi_weather_code = get_kodi_weather_code(daily_weather.weather_code, is_day=True)
        window_properties_map = {
            f'{daily_prefix}.ShortDate': daily_weather.time.strftime(SHORT_DATE_FORMAT),
            f'{daily_prefix}.ShortDay': daily_weather.time.strftime('%a'),
            f'{daily_prefix}.HighTemperature': get_temperature(daily_weather.temperature_2m_max,
                                                               TEMPERATURE_UNIT),
            f'{daily_prefix}.LowTemperature': get_temperature(daily_weather.temperature_2m_min,
                                               TEMPERATURE_UNIT),
            f'{daily_prefix}.Outlook': get_weather_condition_label(daily_weather.weather_code,
                                                                   is_day=True),
            f'{daily_prefix}.OutlookIcon': f'{kodi_weather_code}.png',
            f'{daily_prefix}.FanartCode': kodi_weather_code,
            f'{daily_prefix}.WindSpeed': get_wind_speed(daily_weather.wind_speed_10m_max,
                                                        SPEED_UNIT),
            f'{daily_prefix}.WindDirection': get_wind_direction(
                daily_weather.wind_direction_10m_dominant),
            f'{daily_prefix}.Precipitation': (str(daily_weather.precipitation_probability_mean)
                                              + '%'),
        }
        if i <= 7:
            day_prefix = f'Day{i - 1}'
            # These properties are used in some skins, e.g. aeon.nox.silvo
            window_properties_map.update({
                f'{day_prefix}.Title': daily_weather.time.strftime('%A'),
                f'{day_prefix}.Outlook': window_properties_map[f'{daily_prefix}.Outlook'],
                f'{day_prefix}.OutlookIcon': window_properties_map[f'{daily_prefix}.OutlookIcon'],
                f'{day_prefix}.FanartCode': window_properties_map[f'{daily_prefix}.FanartCode'],
                f'{day_prefix}.HighTemp': window_properties_map[f'{daily_prefix}.HighTemperature'],
                f'{day_prefix}.LowTemp': window_properties_map[f'{daily_prefix}.LowTemperature'],
            })
        logger.debug('Setting daily weather %s:\n%s', i, pformat(window_properties_map))
        for prop, value in window_properties_map.items():
            WEATHER_WINDOW.setProperty(prop, value)


def _populate_general_properties(location_name: str) -> None:
    WEATHER_WINDOW.setProperty('Location', location_name)
    WEATHER_WINDOW.setProperty('Current.Location', location_name)
    WEATHER_WINDOW.setProperty('WeatherProvider', ADDON_NAME)
    WEATHER_WINDOW.setProperty('WeatherProviderLogo', str(BANNER))
    is_fetched = 'true' if location_name else ''
    WEATHER_WINDOW.setProperty('Weather.IsFetched', is_fetched)
    WEATHER_WINDOW.setProperty('Current.IsFetched', is_fetched)
    WEATHER_WINDOW.setProperty('Hourly.IsFetched', is_fetched)
    WEATHER_WINDOW.setProperty('Daily.IsFetched', is_fetched)
    locations = 0
    for i in range(1, 4):
        location_name = ADDON.getSettingString(f'location{i}_name')
        if location_name:
            locations += 1
        WEATHER_WINDOW.setProperty(f'Location{i}', location_name)
    WEATHER_WINDOW.setProperty('Locations', str(locations))


def populate_weather_info_for_location(location_id: str) -> None:
    location_data = _get_location_data(location_id)
    if location_data is None:
        logger.error('Location %s is not set', location_id)
        _populate_general_properties('')
        return
    forecast_info = get_forecast(*location_data[1:])
    _populate_current_weather(forecast_info['current'])
    _populate_hourly_weather(forecast_info['hourly'])
    _populate_daily_weather(forecast_info['daily'])
    _populate_general_properties(location_data.name)
