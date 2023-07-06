from exchange.views import currency
from exchange.models import Leverage, Price, General
from django.core.management.base import BaseCommand, CommandError
import requests
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        price = Price.objects.get()
        rial = price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent / 100))
        r = requests.get(url = 'https://api.coinex.com/v1/market/ticker/all')
        list = r.json()['data']['ticker']
        list2 = {}
        i = 0
        while i < 20:
            for item in Leverage.objects.all():
                if item.symbol == 'BTCUSDT':
                    pprice = float(list[item.symbol]['last'])
                    item.volume = float(list[item.symbol]['vol'])
                    item.last = pprice 
                    item.change = (float(list[item.symbol]['last']) - float(list[item.symbol]['open'])) / float(list[item.symbol]['open']) * 100
                    item.rial = pprice * (price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent3 / 100)))
                elif 'USDT' in item.symbol:
                    if item.symbol in list:
                        list2[item.symbol] = list[item.symbol]
                        pprice = float(list[item.symbol]['last'])
                        item.volume = float(list[item.symbol]['vol'])
                        item.last = pprice 
                        item.change = (float(list[item.symbol]['last']) - float(list[item.symbol]['open'])) / float(list[item.symbol]['open']) * 100
                        item.rial = pprice * rial
                item.save()
            print('done')
            time.sleep(3)
            i += 1
            