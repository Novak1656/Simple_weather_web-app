from django.conf import settings
from django.template import Library
import requests
import datetime

from django.utils.timezone import now

register = Library()


@register.inclusion_tag('main_app/weather_on_5_day.html')
def get_weather_5_day(city_name):
    week_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    response = requests.get(url,
                            params={'q': city_name, 'units': 'metric', 'appid': settings.OWM_API_KEY, 'lang': 'ru'}
                            ).json()
    week_weather = []
    skip_date = f"{now().date()}"

    for weather in response['list']:
        dt = weather['dt_txt'].split()
        if dt[0] == skip_date:
            continue
        else:
            if dt[1] == '15:00:00':
                day = dt[0].split('-')
                date = datetime.date(day=int(day[2]), month=int(day[1]), year=int(day[0]))
                weather_on_day = {'date': date,
                                  'day_week': week_days[date.weekday()],
                                  'temp_day': weather['main']['temp'],
                                  'weather_status': weather['weather'][0]['description'],
                                  'icon': weather['weather'][0]['icon']
                                  }
            elif dt[1] == '21:00:00':
                weather_on_day['temp_eve'] = weather['main']['temp']
                skip_date = dt[0]
                week_weather.append(weather_on_day)
    return {'week_weather': week_weather}


@register.filter(name='is_plus_temp')
def is_plus_temp(temp):
    if '-' not in str(temp):
        return f"+{temp}"
    return temp
