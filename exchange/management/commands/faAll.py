from exchange.views import currency
from exchange.models import Leverage, Price, General
from django.core.management.base import BaseCommand, CommandError
import requests
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(url = 'https://api.wallex.ir/v1/markets')
        list = r.json()['result']['symbols']
        for item in Leverage.objects.all():
            if item.symbol in list:
                item.fa_symbol = list[item.symbol]['faBaseAsset']
                item.save()
            else:
                item.fa_symbol = ''
                item.save()
                