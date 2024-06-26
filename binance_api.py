import asyncio
import numpy as np
import os

from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

'''
Minimum factors required to make a prediction of a coin are : 
- Intraday tick data, Moving Averages, Relative strength data, RSI, VWAP, and Order book snapshots

Other Predictors that can be added later for better predictions: 
- Historical Data, Fundamental Analysis, Sentiment Analysis, and Broader Market Data
'''

binace_api_key = os.getenv('BINANCE_API_KEY')
binance_secret_key = os.getenv('BINANCE_SECRET_KEY')

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
    rsi_values = [float(rsi)]
    rs_values = [float(rs)]

    for i in range(period, len(prices) - 1):

        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss[i]) / period

        if avg_loss != 0:
            rs = avg_gain / avg_loss 
        else:
            rs = 0

        rsi = 100 - (100 / (1 + rs))

        rsi_values.append(float(rsi))
        rs_values.append(float(rs))
    
    return rsi_values, rs_values

def calculate_VolumeWeightedAveragePrice(quote_volume, volume):
    return sum(quote_volume) / sum(volume) 

async def get_info():

    client = await AsyncClient.create(binance_secret_key, binace_api_key, tld='us')

    symbol = str(input("Enter the coin you'd like information for: ")) # Temporary until other API set

    tick_data = await client.get_ticker(symbol=symbol) # 24-hour period
    candlesticks = await client.get_klines(symbol=symbol, interval="1h")
    order_book = await client.get_order_book(symbol=symbol) 

    prices = []
    volume = []
    quote_volume=[]
    for candle in candlesticks:
        prices.append(float(candle[4]))
        volume.append(float(candle[5]))
        quote_volume.append(float(candle[7]))


    sma = calculate_SimpleMovingAverage(prices, 60)
    rsi, rs = calculate_RelativeStrength(prices, 14)
    vwap = calculate_VolumeWeightedAveragePrice(quote_volume, volume)

    print(tick_data)
    print(order_book)
    print(sma)
    print(rsi)
    print(rs)
    print(vwap)

    await client.close_connection()


asyncio.run(get_info())

