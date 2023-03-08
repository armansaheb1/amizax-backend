from exchange.views import currency
from exchange.models import Price, PriceHistory , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(url = 'https://api.nomics.com/v1/currencies/ticker?key=5f176269caf5ea0dfab684904f9316bf1f4f2bc6&ids=BTC,ETH,TRX,DOGE,USDT')
        r = r.json()
        price = PriceHistory(btc = float(r[0]['price']) * 1.07,eth = float(r[1]['price']) * 1.07,usdt = float(r[2]['price']) * 1.07,doge = float(r[3]['price']) * 1.07,trx = float(r[4]['price']) * 1.07,usd = 250000)
        price.save()
