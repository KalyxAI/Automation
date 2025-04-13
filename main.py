from utils import authenticate_twitter, setup_openai, summarize_text_with_gpt
from config import load_config
import schedule
import time

# --- INIT SETUP ---
config = load_config()
twitter_api = authenticate_twitter()
setup_openai()

ALPHA_ACCOUNTS = ["0xSisyphus", "cygaar", "rektbuilder", "danny_postma", "bankless", "dylancoop"]

def fetch_alpha_tweets():
    tweets = []
    for user in ALPHA_ACCOUNTS:
        try:
            user_tweets = twitter_api.user_timeline(screen_name=user, count=5, tweet_mode='extended')
            for tweet in user_tweets:
                tweets.append(tweet.full_text)
        except Exception as e:
            print(f"Error fetching tweets for {user}: {e}")
    return tweets

def post_to_twitter(summary):
    try:
        twitter_api.update_status(summary)
        print("✅ Posted alpha summary to Twitter.")
    except Exception as e:
        print(f"❌ Failed to post tweet: {e}")

def run_kalyx():
    print("\n🚀 Running KALYX AI...")
    tweets = fetch_alpha_tweets()
    if tweets:
        prompt = "Summarize the following crypto alpha tweets into a concise, actionable report with bullet points:\n\n" + "\n\n".join(tweets[-10:])
        summary = summarize_text_with_gpt(prompt)
        post_to_twitter(summary)
    else:
        print("No tweets to summarize.")

schedule.every().hour.do(run_kalyx)

if __name__ == "__main__":
    print("KALYX Alpha Bot started...")
    while True:
        schedule.run_pending()
        time.sleep(10)