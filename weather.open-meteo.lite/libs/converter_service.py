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
"""Functions that convert various weather parameters"""

import enum

from libs.common.kodi_service import GettextEmulator

_ = GettextEmulator.gettext


class KodiWeatherCode(enum.Enum):
    NA = 'na'
    SUNNY = '32'
    CLEAR_NIGHT = '31'
    FAIR_DAY = '34'
    FAIR_NIGHT = '33'
    PARTLY_CLOUDY_DAY = '28'
    PARTLY_CLOUDY_NIGHT = '27'
    MOSTLY_CLOUDY = '26'
    FOGGY = '20'
    DRIZZLE = '9'
    FREEZING_DRIZZLE = '8'
    SCATTERED_SHOWERS = '40'
    FREEZING_RAIN = '10'
    LIGHT_SNOW_SHOWERS = '14'
    SNOW = '16'
    HEAVY_SNOW = '15'
    SLEET = '18'
    LIGHT_SHOWERS = '11'
    SHOWERS = '12'
    HEAVY_RAIN = '1'
    SNOW_SHOWERS = '46'
    THUNDERSTORMS = '3'
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
    FREEZING_RAIN_1 = 66
    FREEZING_RAIN_2 = 67
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
    OpenMeteoWeatherCode.CLOUDY_3: KodiWeatherCode.MOSTLY_CLOUDY,
    OpenMeteoWeatherCode.FOG: KodiWeatherCode.FOGGY,
    OpenMeteoWeatherCode.FOG_WITH_RIME: KodiWeatherCode.FOGGY,
    OpenMeteoWeatherCode.DRIZZLE_1: KodiWeatherCode.DRIZZLE,
    OpenMeteoWeatherCode.DRIZZLE_2: KodiWeatherCode.DRIZZLE,
    OpenMeteoWeatherCode.DRIZZLE_3: KodiWeatherCode.DRIZZLE,
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_1: KodiWeatherCode.FREEZING_DRIZZLE,
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_2: KodiWeatherCode.FREEZING_DRIZZLE,
    OpenMeteoWeatherCode.RAIN_1: KodiWeatherCode.LIGHT_SHOWERS,
    OpenMeteoWeatherCode.RAIN_2: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.RAIN_3: KodiWeatherCode.HEAVY_RAIN,
    OpenMeteoWeatherCode.FREEZING_RAIN_1: KodiWeatherCode.FREEZING_RAIN,
    OpenMeteoWeatherCode.FREEZING_RAIN_2: KodiWeatherCode.FREEZING_RAIN,
    OpenMeteoWeatherCode.SNOW_1: KodiWeatherCode.SNOW,
    OpenMeteoWeatherCode.SNOW_2: KodiWeatherCode.SNOW,
    OpenMeteoWeatherCode.SNOW_3: KodiWeatherCode.HEAVY_SNOW,
    OpenMeteoWeatherCode.SNOW_GRAINS: KodiWeatherCode.SLEET,
    OpenMeteoWeatherCode.RAIN_SHOWERS_1: KodiWeatherCode.LIGHT_SHOWERS,
    OpenMeteoWeatherCode.RAIN_SHOWERS_2: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.RAIN_SHOWERS_3: KodiWeatherCode.SHOWERS,
    OpenMeteoWeatherCode.SNOW_SHOWERS_1: KodiWeatherCode.LIGHT_SNOW_SHOWERS,
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


# Weather labels are limited mostly to 2-word phrases because of UI space considerations
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
    16: _('N'),
}


def get_wind_direction(direction_degrees: int) -> str:
    direction_code = round(direction_degrees / 22.5)
    return WIND_DIRECTION_MAP[direction_code]


def get_temperature(temperature_celc: int, temperature_unit: str) -> str:
    if temperature_unit == '°F':
        return str(round((temperature_celc * 9 / 5) + 32)) + temperature_unit
    return str(temperature_celc) + '°C'


def _wind_speed_to_beaufort(wind_speed_kmh: float) -> int:
    if wind_speed_kmh < 1:
        return 0  # Calm
    elif wind_speed_kmh <= 5:
        return 1  # Light air
    elif wind_speed_kmh <= 11:
        return 2  # Light breeze
    elif wind_speed_kmh <= 19:
        return 3  # Gentle breeze
    elif wind_speed_kmh <= 28:
        return 4  # Moderate breeze
    elif wind_speed_kmh <= 38:
        return 5  # Fresh breeze
    elif wind_speed_kmh <= 49:
        return 6  # Strong breeze
    elif wind_speed_kmh <= 61:
        return 7  # High wind, moderate gale, near gale
    elif wind_speed_kmh <= 74:
        return 8  # Gale, fresh gale
    elif wind_speed_kmh <= 88:
        return 9  # Strong/severe gale
    elif wind_speed_kmh <= 102:
        return 10  # Storm, whole gale
    elif wind_speed_kmh <= 117:
        return 11  # Violent storm
    return 12  # Hurricane force


def get_wind_speed(wind_speed_kmh: float, speed_unit: str) -> str:
    if speed_unit == 'm/s':
        return str(round(wind_speed_kmh / 3.6)) + _('m/s')
    if speed_unit == 'mph':
        return str(round(wind_speed_kmh * 0.621, 1)) + _('mph')
    if speed_unit == 'Beaufort':
        return f'{_wind_speed_to_beaufort(wind_speed_kmh)} {_("Beaufort")}'
    return str(wind_speed_kmh) + _('km/h')
