# -*- coding: utf-8 -*-
import ccxt
import time
import numpy as np
from logging import Logger

gateio = ccxt.gateio({})

listPool = []  # 价格池
sortPool = []  # 排序后的价格池
LENGTH = 1440  # 价格池容量    12小时的价格
symbol = "EOS/USDT"
AMOUNT = 0.4  # 每次买入量，gate.io要求大于1 usdat
interval = 30  # 30 每次获取价格的时间间隔,单位:秒
avg_short = 51  # 51 短线均值：avg_short * interval (秒)
avg_middle = 101  # 101 中线均值：avg_middle  * interval (秒)
# avg_long = 301 # 长线均值: avg_long * interval (秒)
sell_lmt = 173  # 可卖数量低于该值不卖
buy_lmt = 1  # 可买余额低于该值不买

sell_price = []  # 卖出价列表
buy_price = []  # 买入价列表

avg_diff = [0, 0, 0]  # 短均线值-中均线值的差

logger = Logger(logName='log/avg_strategy', logLevel="INFO", logger="start_avg.py").getlog()


def doTicker():
    ticker = gateio.fetch_ticker(symbol=symbol)
    last = ticker["last"]
    # print(ticker)
    # print("=================")
    # print(last)

    if len(listPool) < avg_middle:
        listPool.append(last)
        logger.info("%s 写入价格池" % last)
        # print("%s 写入价格池" % last)
    else:
        if len(listPool) > LENGTH:
            listPool.pop(0)  # 共取12小时的价格进行
        listPool.append(last)
        sortPool = sorted(list(set(listPool)))
        if len(sortPool) > 4:
            pMax = sortPool[-5]  # 取第五大的
            pMin = sortPool[4]  # 取第五小的
        else:
            pMax = sortPool[-1]
            pMin = sortPool[0]
        # logger.info("sortPool: %s, Max: %s, Min: %s" % (sortPool,pMax,pMin))
        pAvg_short = np.mean(listPool[-avg_short:])
        pAvg_middle = np.mean(listPool[-avg_middle:])
        avg_diff.append(pAvg_short - pAvg_middle)
        if len(avg_diff) > 3:
            avg_diff.pop(0)
        # logger.info("均线差：%s" % (avg_diff))
        # pAvg_long = np.mean(listPool[-avg_long:])
        pInc = 100 * (last - pMin) / pMin
        logger.info("当前价格: %.4f, 最低价格: %.4f, 25分钟 均值: %.4f, 50分钟均值: %.4f, 当前涨幅: %.2f" % (
        last, pMin, pAvg_short, pAvg_middle, pInc) + "%")
        account = gateio.fetch_balance()
        free_cyocoin = account[symbol.split("/")[0]]["free"]
        free_unit = account[symbol.split("/")[1]]["free"]
        logger.info(
            "Current Free %s: %s, %s: %s" % (symbol.split("/")[0], free_cyocoin, symbol.split("/")[1], free_unit))

        # ==================涨幅大于2%，25分钟均线突破50分钟 均线，卖出信号===================#
        if pInc > 2 and avg_diff[-1] < 0 and avg_diff[-2] >= 0 and avg_diff[
            -3] >= 0 and free_cyocoin > sell_lmt and free_cyocoin:
            id = gateio.create_limit_sell_order(symbol, AMOUNT, last)
            logger.info("卖出价格：%s，卖出数量：%s" % (last, AMOUNT))
            sell_price.append(last)
        # ===================================卖出操作结束====================================#

        # ==================存在卖出记录，当前价格低于卖出价2%，准备买入=====================#
        for i in range(len(sell_price)):
            if 100 * (sell_price[i] - last) / sell_price[i] > 2 and avg_diff[-1] > 0 and avg_diff[-2] <= 0 and avg_diff[
                -3] <= 0 and free_unit > buy_lmt:
                id = gateio.create_limit_buy_order(symbol, AMOUNT, last)
                logger.info("买入价格：%s, 买入数量：%s" % (last, AMOUNT))
                free_unit = free_unit - last * AMOUNT
                sell_price.pop(i)
        # ===================================买入操作结束====================================#


def main():
    while (True):
        doTicker()  # 执行策略
        time.sleep(interval)  # 休息一段时间


if __name__ == '__main__':
    main()
