import requests
from requests.models import Response
from requests.sessions import Request
import base58
import base64
from pprint import pprint
from pprint import pprint
from tronpy import Tron as TRX
from tronpy.keys import PrivateKey
import hashlib


# !pip install requests
import requests

# !pip install base58
import base58

# !pip install ecdsa
import ecdsa

# !pip install pycryptodome
from Crypto.Hash import keccak




class Tron():
    
    def __init__(self , address , key):
        self.ADDRESS = address
        self.PRIV_KEY = key

        self.CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT

        self.API_URL_BASE = 'https://api.trongrid.io/'

        self.METHOD_BALANCE_OF = 'balanceOf(address)'

        self.METHOD_TRANSFER = 'transfer(address,uint256)'

        self.DEFAULT_FEE_LIMIT = 1_000_000

    def usdt_transfer(self, to, amount, memo=''):
        client = TRX()
        contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
        txn = (
            contract.functions.transfer.with_transfer(100_000_000)
            .call(to, 1_000)
            .with_owner(self.ADDRESS)  # address of the private key
            .fee_limit(5_000_000)
            .build()
            .sign(PrivateKey(bytes.fromhex(self.PRIV_KEY)))
        )
        txn.broadcast()

    def transfer(self, to, amount, memo=''):
        client = TRX()
        txn = (
            client.trx.transfer(self.ADDRESS, to, 1_000)
            .build()
            .sign(PrivateKey(bytes.fromhex(self.PRIV_KEY)))
        )
        txn.broadcast()

