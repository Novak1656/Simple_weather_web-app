from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now


class TemplatesTestCase(TestCase):
    def test_main_view_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/main.html')

    def test_weather_view_template(self):
        response = self.client.get(reverse('weather_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/weather_page.html')


class OverloadResponseTestCase(TestCase):
    def test_main_view_overload(self):
        time_start = now()
        for _ in range(100):
            response = self.client.get(reverse('main'))
            print(f"TEST MainView {_}| Time: {now() - time_start}")
            self.assertEqual(response.status_code, 200)
            time_start = now()

    def test_weather_view_overload(self):
        time_start = now()
        for _ in range(100):
            response = self.client.get(f"{reverse('weather_view')}?city_name=Орёл")
            print(f"TEST MainView {_}| Time: {now() - time_start}")
            self.assertEqual(response.status_code, 200)
            time_start = now()
