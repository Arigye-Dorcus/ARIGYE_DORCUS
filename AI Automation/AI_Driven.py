import tweepy
import schedule
import time
import random
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize Twitter API v2 Client
client = tweepy.Client(
    bearer_token=os.getenv('BEARER_TOKEN'),
    consumer_key=os.getenv('API_KEY'),
    consumer_secret=os.getenv('API_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)

# List of motivational posts
posts = [
    "🌅 Start your day with a positive mindset! #Motivation",
    "💪 Move forward no matter the hardships! #NeverGiveUp",
    "🤔 Take time for reflection today. #Reflection",
    "🚀 Keep going! Your breakthrough is coming! #Persistence",
    "✨ Don't give up on your dreams! #Dreams",
    "🔥 Consistency beats perfection! #Progress",
    "🎯 Focus on progress, not perfection! #Growth",
    "🌱 Growth happens outside your comfort zone! #Challenge",
    "💡 Your potential is limitless! #Potential",
    "🏆 Celebrate small wins! #Gratitude"
]

def post_tweet():
    """Post a random tweet with timestamp"""
    try:
        tweet_text = f"{random.choice(posts)} | {datetime.now().strftime('%H:%M')}"
        response = client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
        print(f"   Tweet ID: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"Failed to post: {e}")

# Verify authentication
try:
    print("...Testing authentication...")
    test_response = client.create_tweet(text="Authentication test tweet - will be deleted")
    client.delete_tweet(test_response.data['id'])
    print("Authentication successful!")
except Exception as e:
    print(f"Auth failed: {e}")
    exit()

# Immediate first tweet
print("\n...Posting first tweet now...")
post_tweet()

# Schedule future tweets
schedule.every().day.at("09:00").do(post_tweet)  # 9 AM
schedule.every().day.at("17:30").do(post_tweet)  # 5:30 PM
schedule.every().day.at("20:00").do(post_tweet)  # 8 PM

print("\n🤖 Twitter Bot Active (API v2)")
print("Next scheduled tweets:")
print("- 9:00 AM")
print("- 5:30 PM")
print("- 8:00 PM")
print("Press Ctrl+C to stop")

# Main loop
try:
    while True:
        #is there any job that is due
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    print("\nBot stopped gracefully.")