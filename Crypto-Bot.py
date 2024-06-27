'''
This is the layout for the complete script for this project as of now. This does not necessarily
need to be used, but provides a helpful mental map for how everything should work together.
None of the values for the variables have been plugged in yet.
'''
import asyncio
from binance_api import get_info
from database import *
from gptapi import make_decision

async def getPrediction():
    symbol = str(input("Enter the currency symbol you would like an opinion on: ")) + 'USDT' # assuming USDT pair for simplicity
    
    crypto_id = await fetch_currency(symbol)
    if not crypto_id:
        await insert_currency(symbol)
        crypto_id = await fetch_currency(symbol)

    tick_data, sma, rs, rsi, vwap, book_order = await get_info(symbol) 
    decision = make_decision(tick_data, sma, rs, rsi, vwap, book_order)

    await cache_prediction(crypto_id, decision)

    print(f"{decision}\n")

async def retrieve_predictions():
    symbol = str(input("Enter the currency symbol you would like an opinion on: ")) + 'USDT' # assuming USDT pair for simplicity

    crypto_id = await fetch_currency(symbol)

    if crypto_id:
        timestamps, responses = await fetch_prediction(crypto_id)

        if timestamps != None and responses != None:
            for time, response in zip(timestamps, responses):
                print(f"On {time} the prediction was {response} for {symbol}")
            
        else:
            print(f"Error fetching prior predictions for {symbol}")
        
    else:
        print("There are no records of this crypto item in the database")




def print_user_operations():
    print("1) Request a prediction")
    print("2) View prior predictions")   
    print("3) Exit")
    

# Main function
def main():
    asyncio.run(create_db()) 
    
    print_user_operations()

    user_choice = input("Enter your choice of operation 1-3: ")
    while user_choice != "3":

        if user_choice == "1":
            asyncio.run(getPrediction())

        elif user_choice == "2":
            asyncio.run(retrieve_predictions())
        
        else:
            print("Invalid input please try again")
        
        print_user_operations()
        user_choice = input("Enter your choice of operation 1-3: ")

        

if __name__ == '__main__':
    main()
