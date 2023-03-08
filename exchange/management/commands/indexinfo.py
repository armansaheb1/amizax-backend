from time import sleep
import requests
from django.core.management.base import BaseCommand, CommandError
import datetime as DT
import json
from exchange.models import Indexprice


class Command(BaseCommand):
    def handle(self, *args, **options):


        end = DT.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
        start = (DT.datetime.now() - DT.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ") 
        print(end)
        print(start)
        r = requests.get(f'https://api.nomics.com/v1/currencies/sparkline?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT&start={start}&end={end}')

        sleep(2)

        response = requests.get('https://api.nomics.com/v1/currencies/ticker?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT')
        for item in Indexprice.objects.all():
            item.delete()
        ind = Indexprice(PriceHistory=r, price = response)
        ind.save()