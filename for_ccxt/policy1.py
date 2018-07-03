# -*- coding: utf-8 -*-
import ccxt
import time

exchange = ccxt.gateio({"apiKey": "0368E005-8696-4C30-874B-3F8011972BED",
                        "secret": "b48810de25da779a9633815df5bf073acbb7c9ac6bd6afd9f97db21fce425e92"})

listPool = []  # 价格池
LENGTH = 10  # 价格池容量
symbol = "ADA/USDT"
AMOUNT = 6  # 每次买入量，gate.io要求大于1 usdt


def doTicker():
    ticker = exchange.fetch_ticker(symbol=symbol)
    last = ticker["last"]
    if len(listPool) < LENGTH:
        listPool.append(last)
        print("%s 写入价格池" % last)
    else:
        pMax = max(listPool)
        pMin = min(listPool)
        print("Current pMax: %s, pMin: %s, last: %s" %(pMax, pMin, last))
        account = exchange.fetch_balance()
        free_cyocoin = account[symbol.split("/")[0]]["free"]
        total_cyocoin = account[symbol.split("/")[0]]["total"]
        free_unit = account[symbol.split("/")[1]]["free"]
        print("Current Free %s: %s, %s: %s" %(symbol.split("/")[0], free_cyocoin, symbol.split("/")[1], free_unit))
        if last > pMax and free_cyocoin * ():
            if free_cyocoin > last and free_cyocoin:
                id = exchange.create_limit_sell_order(symbol, free_cyocoin, last)
                print("sell id --> " + str(id))
        elif last < pMin:
            if free_unit > 2 and total_cyocoin < 30:
                id = exchange.create_limit_buy_order(symbol, AMOUNT, last)
                print("buy id --> " + str(id))
        listPool.pop(0)
        listPool.append(last)


def get_exchange_fee(amount, price):
    return amount * price * 2 / 1000



def main():
    while (True):
        doTicker()  # 执行策略
        time.sleep(30)  # 休息一段时间


if __name__ == '__main__':
    main()
