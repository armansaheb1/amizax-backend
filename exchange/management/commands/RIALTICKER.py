from exchange.views import currency
from exchange.models import Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        rial = requests.get(url = 'http://api.navasan.tech/latest/?api_key=freeKLG7y5B7iUgVQl4JFjIE7WTXUV6n')   
        r = rial.json()
        price = Price.objects.get(id = 1)
        price.rial = float(r['usd_buy']['value']) * 10
        price.usd = float(r['usd_buy']['value']) * 10
        print(float(r['usd_buy']['value']) * 10)
        price.save()
