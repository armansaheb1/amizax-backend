from exchange.views import currency
from exchange.models import Leverage, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from .lib.coinex import CoinEx

class Command(BaseCommand):
    def handle(self, *args, **options):
        for itemm in Leverage.objects.all():
            itemm.delete()
        r = requests.get(url = 'https://api.coinex.com/v1/margin/market')
        list = r.json()['data'].keys()
        for item in list :
            if ('USDT' in item) :
                lev = Leverage(symbol=item)
                lev.save()
            elif ('BTC' in item) :
                lev = Leverage(symbol=item)
                lev.save()