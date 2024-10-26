# Copyright (C] 2024, Roman Miroshnychenko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option] any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import enum

from libs.common.kodi_service import GettextEmulator

_ = GettextEmulator.gettext


class KodiWeatherCode(enum.Enum):
    NA = 'na'
    SUNNY = '32'
    CLEAR_NIGHT = '31'
    FAIR_DAY = '34'
    FAIR_NIGHT = '33'
    PARTLY_CLOUDY_DAY = '30'
    PARTLY_CLOUDY_NIGHT = '31'
    MOSTLY_CLOUDY_DAY = '28'
    MOSTLY_CLOUDY_NIGHT = '27'
    FOGGY = '20'
    DRIZZLE = '9'
    FREEZING_DRIZZLE = '8'
    SCATTERED_SHOWERS = '40'
    FREEZING_RAIN = '10'
    LIGHT_SNOW_SHOWERS = '14'
    SNOW = '16'
    HEAVY_SNOW = '41'
    SLEET = '18'
    SHOWERS = '12'
    SNOW_SHOWERS = '46'
    THUNDERSTORMS = '4'
    HAIL = '17'


class OpenMeteoWeatherCode(enum.IntEnum):
    CLEAR = 0
    CLOUDY_1 = 1
    CLOUDY_2 = 2
    CLOUDY_3 = 3
    FOG = 45
    FOG_WITH_RIME = 48
    DRIZZLE_1 = 51
    DRIZZLE_2 = 53
    DRIZZLE_3 = 55
    FREEZING_DRIZZLE_1 = 56
    FREEZING_DRIZZLE_2 = 57
    RAIN_1 = 61
    RAIN_2 = 62
    RAIN_3 = 63
    FREEZING_RAIN_1 = 56
    FREEZING_RAIN_2 = 57
    SNOW_1 = 71
    SNOW_2 = 73
    SNOW_3 = 75
    SNOW_GRAINS = 77
    RAIN_SHOWERS_1 = 80
    RAIN_SHOWERS_2 = 81
    RAIN_SHOWERS_3 = 82
    SNOW_SHOWERS_1 = 85
    SNOW_SHOWERS_2 = 86
    THUNDERSTORM = 95
    THUNDERSTORM_WITH_HAIL_1 = 96
    THUNDERSTORM_WITH_HAIL_2 = 99


WEATHER_CODES_MAP = {
    OpenMeteoWeatherCode.CLEAR: [KodiWeatherCode.SUNNY, KodiWeatherCode.CLEAR_NIGHT],
    OpenMeteoWeatherCode.CLOUDY_1: [KodiWeatherCode.FAIR_DAY, KodiWeatherCode.FAIR_NIGHT],
    OpenMeteoWeatherCode.CLOUDY_2: [
        KodiWeatherCode.PARTLY_CLOUDY_DAY,
        KodiWeatherCode.PARTLY_CLOUDY_NIGHT,
    ],
    OpenMeteoWeatherCode.CLOUDY_3: [
        KodiWeatherCode.MOSTLY_CLOUDY_DAY,
        KodiWeatherCode.MOSTLY_CLOUDY_NIGHT,
    ],
    OpenMeteoWeatherCode.FOG: KodiWeatherCode.FOGGY,
    OpenMeteoWeatherCode.FOG_WITH_RIME: KodiWeatherCode.FOGGY,
    OpenMeteoWeatherCode.DRIZZLE_1: KodiWeatherCode.DRIZZLE,
    OpenMeteoWeatherCode.DRIZZLE_2: KodiWeatherCode.DRIZZLE,
    OpenMeteoWeatherCode.DRIZZLE_3: KodiWeatherCode.DRIZZLE,
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_1: KodiWeatherCode.FREEZING_DRIZZLE,
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_2: KodiWeatherCode.FREEZING_DRIZZLE,
    OpenMeteoWeatherCode.RAIN_1: KodiWeatherCode.SCATTERED_SHOWERS,
    OpenMeteoWeatherCode.RAIN_2: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.RAIN_3: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.FREEZING_RAIN_1: KodiWeatherCode.FREEZING_RAIN,
    OpenMeteoWeatherCode.FREEZING_RAIN_2: KodiWeatherCode.FREEZING_RAIN,
    OpenMeteoWeatherCode.SNOW_1: KodiWeatherCode.SNOW,
    OpenMeteoWeatherCode.SNOW_2: KodiWeatherCode.SNOW,
    OpenMeteoWeatherCode.SNOW_3: KodiWeatherCode.HEAVY_SNOW,
    OpenMeteoWeatherCode.SNOW_GRAINS: KodiWeatherCode.SLEET,
    OpenMeteoWeatherCode.RAIN_SHOWERS_1: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.RAIN_SHOWERS_2: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.RAIN_SHOWERS_3: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.SNOW_SHOWERS_1: KodiWeatherCode.SNOW_SHOWERS,
    OpenMeteoWeatherCode.SNOW_SHOWERS_2: KodiWeatherCode.SNOW_SHOWERS,
    OpenMeteoWeatherCode.THUNDERSTORM: KodiWeatherCode.THUNDERSTORMS,
    OpenMeteoWeatherCode.THUNDERSTORM_WITH_HAIL_1: KodiWeatherCode.HAIL,
    OpenMeteoWeatherCode.THUNDERSTORM_WITH_HAIL_2: KodiWeatherCode.HAIL,
}


def get_kodi_weather_code(open_meteo_code: int, is_day: bool) -> str:
    kodi_code = WEATHER_CODES_MAP.get(open_meteo_code)
    if kodi_code is None:
        return KodiWeatherCode.NA.value
    if isinstance(kodi_code, list):
        return kodi_code[0].value if is_day else kodi_code[1].value
    return kodi_code.value


WEATHER_CONDITION_LABELS_MAP = {
    OpenMeteoWeatherCode.CLEAR: [_('Sunny'), _('Clear')],
    OpenMeteoWeatherCode.CLOUDY_1: _('Fair'),
    OpenMeteoWeatherCode.CLOUDY_2: _('Cloudy'),
    OpenMeteoWeatherCode.CLOUDY_3: _('Overcast'),
    OpenMeteoWeatherCode.FOG: _('Fog'),
    OpenMeteoWeatherCode.FOG_WITH_RIME: _('Fog with rime'),
    OpenMeteoWeatherCode.DRIZZLE_1: _('Light drizzle'),
    OpenMeteoWeatherCode.DRIZZLE_2: _('Drizzle'),
    OpenMeteoWeatherCode.DRIZZLE_3: _('Heavy drizzle'),
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_1: _('Freezing drizzle'),
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_2: _('Freezing drizzle'),
    OpenMeteoWeatherCode.RAIN_1: _('Light rain'),
    OpenMeteoWeatherCode.RAIN_2: _('Rain'),
    OpenMeteoWeatherCode.RAIN_3: _('Heavy rain'),
    OpenMeteoWeatherCode.FREEZING_RAIN_1: _('Freezing rain'),
    OpenMeteoWeatherCode.FREEZING_RAIN_2: _('Freezing rain'),
    OpenMeteoWeatherCode.SNOW_1: _('Light snow'),
    OpenMeteoWeatherCode.SNOW_2: _('Snow'),
    OpenMeteoWeatherCode.SNOW_3: _('Heavy snow'),
    OpenMeteoWeatherCode.SNOW_GRAINS: _('Snow grains'),
    OpenMeteoWeatherCode.RAIN_SHOWERS_1: _('Rain showers'),
    OpenMeteoWeatherCode.RAIN_SHOWERS_2: _('Rain showers'),
    OpenMeteoWeatherCode.RAIN_SHOWERS_3: _('Rain showers'),
    OpenMeteoWeatherCode.SNOW_SHOWERS_1: _('Snow showers'),
    OpenMeteoWeatherCode.SNOW_SHOWERS_2: _('Snow showers'),
    OpenMeteoWeatherCode.THUNDERSTORM: _('Thunderstorm'),
    OpenMeteoWeatherCode.THUNDERSTORM_WITH_HAIL_1: _('Thunderstorm with hail'),
    OpenMeteoWeatherCode.THUNDERSTORM_WITH_HAIL_2: _('Thunderstorm with hail'),
}


def get_weather_condition_label(open_meteo_code, is_day):
    label = WEATHER_CONDITION_LABELS_MAP.get(open_meteo_code)
    if label is None:
        return 'N/A'
    if isinstance(label, list):
        return label[0] if is_day else label[1]
    return label


WIND_DIRECTION_MAP = {
    0: _('N'),
    1: _('NE'),
    2: _('NE'),
    3: _('E'),
    4: _('E'),
    5: _('SE'),
    6: _('SE'),
    7: _('S'),
    8: _('S'),
    9: _('SW'),
    10: _('SW'),
    11: _('W'),
    12: _('W'),
    13: _('NW'),
    14: _('NW'),
    15: _('N'),
}


def get_wind_direction(direction_degrees: int) -> str:
    direction_code = round(direction_degrees / 22.5)
    return WIND_DIRECTION_MAP[direction_code]
