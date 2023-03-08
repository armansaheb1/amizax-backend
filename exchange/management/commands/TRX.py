from exchange.views import currency
from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from bit import Key
import json
import logging

from tronapi import Tron
full_node = 'https://api.trongrid.io'
solidity_node = 'https://api.trongrid.io'
event_server = 'https://api.trongrid.io/'
private_key = 'da146374a75310b9666e834ee4ad0866d6f4035967bfc76217c5a495fff9f0d0'

tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 5)):
            trx_kwargs = dict()
            trx_kwargs["private_key"] = item.key
            trx_kwargs["default_address"] = item.address

            tron = Tron(**trx_kwargs)

            balance = tron.trx.get_balance()
            
            if balance > 0 :
                send = tron.trx.send_transaction('TJ8d1N7DjmxRbKRyEwNcYszAinAPACyH4W', balance)
                item.amount += balance
                item.save()
                print(send)