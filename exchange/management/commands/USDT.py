from exchange.views import currency
from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from bit import Key
import json
import logging
import requests
import base58
import base64
from pprint import pprint


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


tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Wallet.objects.filter(currency = Currencies.objects.get(id = 4)):
            ADDRESS = item.address
            PRIV_KEY = item.key
            def amount_to_parameter(amount):
                return '%064x' % amount
            def address_to_parameter(addr):
                return "0" * 24 + base58.b58decode_check(addr)[1:].hex()

            def sign_transaction(transaction, private_key=PRIV_KEY):
                url = API_URL_BASE + 'wallet/addtransactionsign'
                payload = {'transaction': transaction, 'privateKey': private_key}
                resp = requests.post(url, json=payload)

                data = resp.json()

                if 'Error' in data:
                    print('error:', data)
                    raise RuntimeError
                return data

            def get_trc20_transaction(to, amount, memo=''):
                url = API_URL_BASE + 'wallet/triggersmartcontract'
                payload = {
                    'owner_address': base58.b58decode_check(ADDRESS).hex(),
                    'contract_address': base58.b58decode_check(CONTRACT).hex(),
                    'function_selector': METHOD_TRANSFER,
                    'parameter': address_to_parameter(to) + amount_to_parameter(amount),
                    "fee_limit": DEFAULT_FEE_LIMIT,
                    'extra_data': base64.b64encode(memo.encode()).decode(),  # TODO: not supported yet
                }
                resp = requests.post(url, json=payload)
                data = resp.json()

                if data['result'].get('result', None):
                    transaction = data['transaction']
                    return transaction

                else:
                    print('error:', bytes.fromhex(data['result']['message']).decode())
                    raise RuntimeError

            def broadcast_transaction(transaction):
                url = API_URL_BASE + 'wallet/broadcasttransaction'
                resp = requests.post(url, json=transaction)

                data = resp.json()
                print(data)

            def transfer(to, amount, memo=''):
                transaction = get_trc20_transaction(to, amount, memo)
                pprint(transaction)
                transaction = sign_transaction(transaction)
                broadcast_transaction(transaction)
                

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
                if balance > 0:
                    transfer('TV8Y12Fciai1wnK5ZZzNGkMPqg3sksidn3', balance)
            else:
                print('error:', bytes.fromhex(data['result']['message']).decode())
