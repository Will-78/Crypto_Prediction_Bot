import asyncio
import json
import numpy as np
import os

from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

'''
Minimum factors required to make a prediction of a coin are : 
- Intraday tick data, Moving Averages, Relative strength data, RSI, VWAP, and Order book snapshots

Other Predictors that can be added later for better predictions: 
- Historical Data, Fundamental Analysis, Sentiment Analysis, and Broader Market Data
'''

binace_api_key = os.getenv('BINANCE_KEY')

def calculate_SimpleMovingAverage(prices, interval):
    return sum(prices) / interval

def calculate_RelativeStrength(prices, period):

    if len(prices) < period + 1:
        return -1
    
    differences = np.diff(prices)

    gains = np.where(differences > 0, differences, 0)
    loss  = np.where(differences < 0, -differences, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(loss[:period])

    if avg_loss != 0:
        rs = avg_gain / avg_loss 
    else:
        rs = 0
    
    rsi = 100 - (100 / (1 + rs)) #initial RSI value

    # Get rest of RSI values
    rsi_values = [rsi]
    rs_values = [rs]

    for i in range(period, len(prices) - 1):

        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss[i]) / period

        if avg_loss != 0:
            rs = avg_gain / avg_loss 
        else:
            rs = 0

        rsi = 100 - (100 / (1 + rs))

        rsi_values.append(rsi)
        rs_values.append(rs)
    
    return rsi_values, rs_values

def calculate_VolumeWeightedAveragePrice(quote_volume, volume):
    return quote_volume / volume 

async def main():

    client = AsyncClient.create()

    symbol = input("Enter the coin you'd like information for: ") # Temporary until other API set

    tick_data = await client.get_ticker(symbol) # 24-hour period
    latest_price = await client.get_symbol_ticker(symbol)
    candlesticks = await client.get_klines(symbol, "1h")
    order_book = await client.get_order_book(symbol)

    sma = calculate_SimpleMovingAverage(candlesticks['close', 60])
    rsi, rs = calculate_RelativeStrength(candlesticks['close'], 14)
    vwap = calculate_VolumeWeightedAveragePrice(tick_data['quote_volume'], tick_data['volume'])

    print(tick_data, latest_price, candlesticks, order_book, sma, rsi, rs, vwap)


