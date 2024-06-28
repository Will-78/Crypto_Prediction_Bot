import numpy as np
import os

from binance import AsyncClient

"""
Minimum factors required to make a prediction of a coin are :
- Intraday tick data, Moving Averages, Relative strength data, 
    RSI, VWAP, and Order book snapshots

Other Predictors that can be added later for better predictions:
- Historical Data, Fundamental Analysis, Sentiment Analysis, and Broader Market Data
"""

binace_api_key = os.getenv("BINANCE_API_KEY")
binance_secret_key = os.getenv("BINANCE_SECRET_KEY")


def calculate_SimpleMovingAverage(prices, interval):
    # average of candlestick prices over a given interval
    return sum(prices) / interval


def calculate_RelativeStrength(prices, period):

    if len(prices) < period + 1:
        return -1

    # calculate the rs and rsi values for initial and over each period

    differences = np.diff(prices)

    gains = np.where(differences > 0, differences, 0)
    loss = np.where(differences < 0, -differences, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(loss[:period])

    if avg_loss != 0:
        rs = avg_gain / avg_loss
    else:
        rs = 0

    rsi = 100 - (100 / (1 + rs))  # initial RSI value

    # Get rest of RSI values over period
    rsi_values = [float(rsi)]
    rs_values = [float(rs)]

    for i in range(period, len(prices) - 1):

        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss[i]) / period

        if avg_loss != 0:
            rs = avg_gain / avg_loss  # rs formula
        else:
            rs = 0

        rsi = 100 - (100 / (1 + rs))  # rsi formula

        rsi_values.append(float(rsi))
        rs_values.append(float(rs))

    return rsi_values, rs_values


def calculate_VolumeWeightedAveragePrice(quote_volume, volume):
    return sum(quote_volume) / sum(volume)  # quoted volume over overal value


async def get_info(symbol):

    # create an async client to handle calls efficiently via RESTful API

    client = await AsyncClient.create(
        binance_secret_key, binace_api_key, tld="us"
    )  # all async commands require await (must be in async function)

    try:
        tick_data = await client.get_ticker(symbol=symbol)  # 24-hour period
        candlesticks = await client.get_klines(symbol=symbol, interval="1h")
        order_book = await client.get_order_book(symbol=symbol)

    except:

        await client.close_connection()
        return
    else:

        # extract data from the candlesticks
        prices = []
        volume = []
        quote_volume = []
        for candle in candlesticks:
            prices.append(float(candle[4]))
            volume.append(float(candle[5]))
            quote_volume.append(float(candle[7]))

        # calculate necessary factors that cannot be retrieved via API
        sma = calculate_SimpleMovingAverage(prices, 60)
        rsi, rs = calculate_RelativeStrength(prices, 14)
        vwap = calculate_VolumeWeightedAveragePrice(quote_volume, volume)

        await client.close_connection()

        return tick_data, sma, rs, rsi, vwap, order_book
