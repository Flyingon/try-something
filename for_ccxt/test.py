#-*- coding: utf-8 -*-

import ccxt


binance = ccxt.binance()
gateio = ccxt.gateio({"apiKey":"0368E005-8696-4C30-874B-3F8011972BED","secret":"b48810de25da779a9633815df5bf073acbb7c9ac6bd6afd9f97db21fce425e92"})

gateio.load_markets()
# print(gateio.fetch_tickers())
gateio.symbols
print(gateio.account())
print(gateio.fetch_ticker("ADA/USDT"))

print(gateio.create_limit_buy_order("ADA/USDT", 0.0006, 0.0078))
print(gateio.create_limit_sell_order("EOS/USDT", 1, 12))
print(gateio.create_limit_buy_order("EOS/USDT", 1, 10))

print(gateio.fetch_my_trades())
print(gateio.fetch_balance())
print(gateio.fetch_trade(symbol="EOS/USDT"))

print(gateio.create_market_sell_order("EOS/USDT", 1, 10))
print(exchange.create_limit_buy_order(symbol, 1, 0))




