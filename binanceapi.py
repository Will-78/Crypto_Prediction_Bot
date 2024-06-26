from binance.client import Client

client = Client(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')

def place_order(symbol, side, quantity):
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=quantity
    )
    return order
