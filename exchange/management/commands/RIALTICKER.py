from exchange.views import currency
from exchange.models import Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        rial = requests.get(url = 'http://api.navasan.tech/latest/?api_key=1oFGrKOHDblbSXNvErx6Y2XIqMghp2h9')   
        r = rial.json()
        price = Price.objects.get(id = 1)
        price.rial = r['usd_buy']['value'] * 10
        price.usd = r['usd_buy']['value'] * 10
        price.save()
