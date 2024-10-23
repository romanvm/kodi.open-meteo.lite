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


class KodiWeatherCode(enum.StrEnum):
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
    OpenMeteoWeatherCode.CLOUDY_2: [KodiWeatherCode.PARTLY_CLOUDY_DAY, KodiWeatherCode.PARTLY_CLOUDY_NIGHT],
    OpenMeteoWeatherCode.CLOUDY_3: [KodiWeatherCode.MOSTLY_CLOUDY_DAY, KodiWeatherCode.MOSTLY_CLOUDY_NIGHT],
    OpenMeteoWeatherCode.FOG: [KodiWeatherCode.FOGGY],
    OpenMeteoWeatherCode.FOG_WITH_RIME: [KodiWeatherCode.FOGGY],
    OpenMeteoWeatherCode.DRIZZLE_1: [KodiWeatherCode.DRIZZLE],
    OpenMeteoWeatherCode.DRIZZLE_2: [KodiWeatherCode.DRIZZLE],
    OpenMeteoWeatherCode.DRIZZLE_3: [KodiWeatherCode.DRIZZLE],
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_1: [KodiWeatherCode.FREEZING_DRIZZLE],
    OpenMeteoWeatherCode.FREEZING_DRIZZLE_2: [KodiWeatherCode.FREEZING_DRIZZLE],
    OpenMeteoWeatherCode.RAIN_1: [KodiWeatherCode.SCATTERED_SHOWERS],
    OpenMeteoWeatherCode.RAIN_2: [KodiWeatherCode.SHOWERS],
    OpenMeteoWeatherCode.RAIN_3: [KodiWeatherCode.SHOWERS],
    OpenMeteoWeatherCode.FREEZING_RAIN_1: [KodiWeatherCode.FREEZING_RAIN],
    OpenMeteoWeatherCode.FREEZING_RAIN_2: [KodiWeatherCode.FREEZING_RAIN],
    OpenMeteoWeatherCode.SNOW_1: [KodiWeatherCode.SNOW],
    OpenMeteoWeatherCode.SNOW_2: [KodiWeatherCode.SNOW],
    OpenMeteoWeatherCode.SNOW_3: [KodiWeatherCode.HEAVY_SNOW],
    OpenMeteoWeatherCode.SNOW_GRAINS: [KodiWeatherCode.SLEET],
    OpenMeteoWeatherCode.RAIN_SHOWERS_1: [KodiWeatherCode.SHOWERS],
    OpenMeteoWeatherCode.RAIN_SHOWERS_2: [KodiWeatherCode.SHOWERS],
    OpenMeteoWeatherCode.RAIN_SHOWERS_3: [KodiWeatherCode.SHOWERS],
    OpenMeteoWeatherCode.SNOW_SHOWERS_1: [KodiWeatherCode.SNOW_SHOWERS],
    OpenMeteoWeatherCode.SNOW_SHOWERS_2: [KodiWeatherCode.SNOW_SHOWERS],
    OpenMeteoWeatherCode.THUNDERSTORM: [KodiWeatherCode.THUNDERSTORMS],
    OpenMeteoWeatherCode.THUNDERSTORM_WITH_HAIL_1: [KodiWeatherCode.HAIL],
    OpenMeteoWeatherCode.THUNDERSTORM_WITH_HAIL_2: [KodiWeatherCode.HAIL],
}


def get_kodi_weather_code(open_meteo_code: int, is_night: bool) -> str:
    kodi_codes = WEATHER_CODES_MAP.get(open_meteo_code)
    if kodi_codes is None:
        return KodiWeatherCode.NA
    if len(kodi_codes) == 1:
        return kodi_codes[0]
    return kodi_codes[1] if is_night else kodi_codes[0]
