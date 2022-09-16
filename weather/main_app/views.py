from django.conf import settings
from django.shortcuts import render
import requests
from django.utils import timezone


def main(request):
    return render(request, 'main_app/main.html')


def weather_view(request):
    city_name = request.GET.get('city_name')
    url = f'https://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url, params={'q': city_name, 'units': 'metric', 'appid': settings.OWM_API_KEY, 'lang': 'ru'}
                            ).json()
    if response['cod'] == 200:
        context = {'city': response['name'],
                   'temp': response['main']['temp'],
                   'feels_like': response['main']['feels_like'],
                   'weather_status': response['weather'][0]['description'],
                   'icon': response['weather'][0]['icon'],
                   'cur_time': timezone.localtime(timezone.now()).time()
                   }
    else:
        context = {'message': f'Город {city_name} не найден'}
    return render(request, 'main_app/weather_page.html', context)
