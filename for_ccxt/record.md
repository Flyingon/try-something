
```
>>> print(gateio.create_limit_sell_order("EOS/USDT", 12, 1))
{'info': {'result': 'true', 'message': 'Success', 'code': 0, 'orderNumber': 888447609, 'rate': '1', 'leftAmount': '0.00000000', 'filledAmount': '12', 'filledRate': 10.802}, 'id': 888447609}
>>> print(gateio.create_limit_buy_order("EOS/USDT", 1, 10))
{'info': {'result': 'true', 'message': 'Success', 'code': 0, 'orderNumber': 888535919, 'rate': '10', 'leftAmount': '1.00000000', 'filledAmount': '0', 'filledRate': '10'}, 'id': 888535919}
>>> print(gateio.create_limit_sell_order("EOS/USDT", 1, 13))
{'info': {'result': 'true', 'message': 'Success', 'code': 0, 'orderNumber': 888543698, 'rate': '13', 'leftAmount': '1.00000000', 'filledAmount': '0', 'filledRate': '13'}, 'id': 888543698}
```