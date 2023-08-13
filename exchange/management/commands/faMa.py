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
            if not item.fa_symbol:
                sym = item.symbol.replace('USDT', '')
                name = str(input(f'{sym} name: '))
                item.fa_symbol = name
                item.save()
                print()
                print(item.fa_symbol)
                