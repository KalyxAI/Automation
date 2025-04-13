import tweepy
import openai
import os

def authenticate_twitter():
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_SECRET")
    )
    return tweepy.API(auth)

def setup_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text_with_gpt(prompt_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an alpha analyst."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response["choices"][0]["message"]["content"]