import os 
import openai
from openai import OpenAI

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

def make_decision(sentiment):
    if 'positive' in sentiment.lower():
        return 'BUY'
    elif 'negative' in sentiment.lower():
        return 'SELL'
    else:
        return 'HOLD'

# Create an OpenAPI client using the key from our environment variable
client = OpenAI(
    api_key=my_api_key,
)

# Specify the model to use and the messages to send
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a university instructor and can explain programming concepts clearly in a few words."},
        {"role": "user", "content": "What are the advantages of pair programming?"}
    ]
)
print(completion.choices[0].message.content) 