import os 
import openai

# Set environment variables
my_api_key = os.getenv('OPENAI_KEY')

openai.api_key = my_api_key

# WRITE YOUR CODE HERE
def get_sentiment(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=60
    )
    sentiment = response.choices[0].text.strip()
    return sentiment

def make_decision(tick_data, sma, rs, rsi, vwap, book_order):

    # task given to openai (system = behavior, user = request)
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a crypto specialist and can make crypto suggestions off data retrieved from Binance"},
            {"role": "user", "content": f"Based off this information provided make a suggested plan of action like selling, holding, or buying:" 
                                        f"tick data: {tick_data}, simple moving average: {sma}, relative strength: {rs}, relative strength index: {rsi},"
                                        f"volume weighted average price: {vwap}, book order: {book_order}"}
        ]
    )

    return completion.choices[0].message.content

