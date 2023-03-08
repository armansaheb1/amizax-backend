from bit import Key


def BTC(key, amount, to):
    my_key = Key(key , amount)
    outputs = [
        (to, amount, 'btc')
    ]
    print(my_key.send(outputs))
    return my_key.send(outputs)