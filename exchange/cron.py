from exchange.models import General, Indexprice, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import datetime as DT
from time import sleep
import base58


from tronapi import Tron
full_node = 'https://api.trongrid.io'
solidity_node = 'https://api.trongrid.io'
event_server = 'https://api.trongrid.io/'

API_URL_BASE = 'https://api.trongrid.io/'

CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT

API_URL_BASE = 'https://api.trongrid.io/'

METHOD_BALANCE_OF = 'balanceOf(address)'

METHOD_TRANSFER = 'transfer(address,uint256)'

DEFAULT_FEE_LIMIT = 1_000_000  # 1 TRX

def INDEXINFO():
    i = 0
    while i < 20:
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

        sleep(2)
        i = i + 1

def RIALTICKER():
        rial = requests.get(url = 'https://dapi.p3p.repl.co/api/?currency=usd')   
        r = rial.json()
        price = Price.objects.get(id = 1)
        price.rial = int(r['Price']) 
        price.usd = int(r['Price']) 
        price.save()

def USDT():
    for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 4)):
        ADDRESS = item.address
        PRIV_KEY = item.key
        def amount_to_parameter(amount):
                    return '%064x' % amount
        def address_to_parameter(addr):
            return "0" * 24 + base58.b58decode_check(addr)[1:].hex()
        url = 'https://api.trongrid.io/' + 'wallet/triggerconstantcontract'
        payload = {
            'owner_address': base58.b58decode_check(ADDRESS).hex(),
            'contract_address': base58.b58decode_check(CONTRACT).hex(),
            'function_selector': METHOD_BALANCE_OF,
            'parameter': address_to_parameter(ADDRESS),
        }
        resp = requests.post(url, json=payload)
        data = resp.json()

        if data['result'].get('result', None):
            val = data['constant_result'][0]
            balance = int(val, 16)
            print(balance)
            item.amount = balance / 1000000
            item.save()
