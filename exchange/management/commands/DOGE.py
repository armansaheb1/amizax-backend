from exchange.views import currency
from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from blockcypher import *
import json
from cryptos import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 6)):
            res = get_address_full(address=item.address, coin_symbol="doge")
            balance = int(res['balance']) / 100000000
            if balance > 0 :
                amount = int(balance * 751.2134)
                ret = simple_spend(from_privkey='QSYhFcBd7WNGreoPokm7T9GZ5D7xPZRJ4eSGGf72UayAgA4FwXBK', to_address='DQdVkyabujfWcVZc3HPZgqXKdrNm2ZYW9W', to_satoshis=amount, coin_symbol='doge', api_key='68356d33c9124e4aa4e305f5953561b5')
                print(ret) 