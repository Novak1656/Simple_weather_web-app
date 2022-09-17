from django.conf import settings
from django.template import Library
import requests
import datetime

from django.utils.timezone import now

register = Library()


@register.filter(name='is_plus_temp')
def is_plus_temp(temp):
    if '-' not in str(temp):
        return f"+{temp}"
    return temp
