import datetime
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
import asyncio
import httpx
from django.utils.timezone import now


def get_today_weather(res):
    if res.status_code == httpx.codes.OK:
        res_js_today = res.json()
        context = {'city': res_js_today['name'],
                   'temp': res_js_today['main']['temp'],
                   'feels_like': res_js_today['main']['feels_like'],
                   'weather_status': res_js_today['weather'][0]['description'],
                   'icon': res_js_today['weather'][0]['icon'],
                   'cur_time': timezone.localtime(timezone.now()).time()
                   }
    else:
        context = {'message': f'Такой город не найден.'}
    return context


def get_5_day_weather(res):
    if res.status_code == httpx.codes.OK:
        res_js_5_day = res.json()
        week_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        week_weather = []
        skip_date = f"{now().date()}"
        weather_on_day = dict()
        for weather in res_js_5_day['list']:
            dt = weather['dt_txt'].split()

            if dt[0] == skip_date:
                continue
            else:
                if dt[1] == '03:00:00':
                    day = dt[0].split('-')
                    date = datetime.date(day=int(day[2]), month=int(day[1]), year=int(day[0]))
                    weather_on_day['date'] = date
                    weather_on_day['temp_night'] = weather['main']['temp']
                    weather_on_day['day_week'] = week_days[date.weekday()]

                elif dt[1] == '15:00:00':
                    weather_on_day['temp_day'] = weather['main']['temp']
                    weather_on_day['weather_status'] = weather['weather'][0]['description']
                    weather_on_day['icon'] = weather['weather'][0]['icon']
                    skip_date = dt[0]
                    week_weather.append(weather_on_day)
                    weather_on_day = {}
        return week_weather
    else:
        return


def main(request):
    return render(request, 'main_app/main.html')


async def weather_view(request):
    city_name = request.GET.get('city_name')
    url_today = f'https://api.openweathermap.org/data/2.5/weather'
    url_5_day = 'http://api.openweathermap.org/data/2.5/forecast'
    get_params = {'q': city_name, 'units': 'metric', 'appid': settings.OWM_API_KEY, 'lang': 'ru'}
    try:
        async with httpx.AsyncClient() as client:
            res_weather_today, res_weather_5_day = await asyncio.gather(*[
                client.get(url_today, params=get_params),
                client.get(url_5_day, params=get_params),
            ])
            context = get_today_weather(res_weather_today)
            context['weather_on_5_day'] = get_5_day_weather(res_weather_5_day)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    return render(request, "main_app/weather_page.html", context)
