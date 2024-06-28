'''
This is the layout for the complete script for this project as of now. This does not necessarily
need to be used, but provides a helpful mental map for how everything should work together.
None of the values for the variables have been plugged in yet.
'''
import asyncio # to make api calls more efficent and not slow down on time
from binance_api import get_info
from database import *
from gptapi import make_decision

async def getPrediction():
    symbol = str(input("\nEnter the currency symbol you would like an opinion on: ")) + 'USDT' # assuming USDT pair for simplicity
    
    # obtain the id associated with the coin else create a record of it
    crypto_id = await fetch_currency(symbol)
    if not crypto_id:
        await insert_currency(symbol)
        crypto_id = await fetch_currency(symbol)

    # Make call to binacne for relevant information to then make a decision with openai
    tick_data, sma, rs, rsi, vwap, book_order = await get_info(symbol) 
    decision = make_decision(tick_data, sma, rs, rsi, vwap, book_order)

    # store a record of this prediction
    await cache_prediction(crypto_id, decision)

    print(f"\n{decision}\n")

async def retrieve_predictions():
    symbol = str(input("\nEnter the currency symbol you would like an opinion on: ")) + 'USDT' # assuming USDT pair for simplicity

    # attempt to get coin id else is has not beeen recorded yet
    crypto_id = await fetch_currency(symbol) 

    if crypto_id:

        # pull information from the database to print out if there is none throw error
        timestamps, responses = await fetch_prediction(crypto_id)

        if len(timestamps) and len(responses):
            for time, response in zip(timestamps, responses):
                print(f"\nOn {time} the prediction was {response} for {symbol}")
            
        else:
            print(f"\nError fetching prior predictions for {symbol}")
        
    else:
        print("\nThere are no records of this crypto item in the database")




def print_user_operations():
    print("\n===========================")
    print("1) Request a prediction")
    print("2) View prior predictions")   
    print("3) Exit\n")
    print("===========================\n")
    

# Main function
def main():
    asyncio.run(create_db()) 

    print("\nWelcome to the cryptocurrency market analysis program")
    print("To use this program select your action below and enter the Cryptocurrency you would to analize")
    
    print_user_operations()

    # set up loop for consistent I/O

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
