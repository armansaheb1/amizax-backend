from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from bit import Key
from django.core.management.base import BaseCommand, CommandError
from cryptos import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 2)):
            r = requests.get(url = 'https://testnet-api.smartbit.com.au/v1/blockchain/address/' + item.address)
            data = r.json()
            balance = float(data['address']['confirmed']['balance'])
            if balance > 0 :
                print(balance)
                c = Bitcoin(testnet=True)
                print(c.send(item.key, "tb1q2wmp8d0a3gfxn7vgtmk6s7fmxuhtghjzkyqrdp", 2000))
                item.amount += balance
                item.save()