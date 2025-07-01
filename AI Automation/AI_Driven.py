# This Python script automates the creation and posting of tweets using:

# AI (OpenAI GPT-4) to generate tweet content

# Twitter API to post automatically

# Scheduling to post at optimal times

# Think of it as a virtual social media manager that creates and shares tech-related tweets 


import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import tweepy
from openai import OpenAI

# Load environment variables
load_dotenv()

class TwitterAIBot:
    def __init__(self):
        # Initialize APIs
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Twitter API v2 authentication
        self.twitter_client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        
        # For media uploads (if needed)
        self.twitter_auth_v1 = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        self.twitter_api_v1 = tweepy.API(self.twitter_auth_v1)

        # Configuration
        self.posting_times = ["09:00", "12:00", "15:00"]  # 24-hour format
        self.content_themes = {
            "tech news": 0.3,
            "AI developments": 0.3,
            "coding tips": 0.2,
            "fun tech facts": 0.2
        }

    def generate_tweet(self, theme: str) -> str:
        """Generate tweet content using OpenAI"""
        prompt = f"""
        Create a engaging tweet about {theme} for a tech-savvy audience.
        - Maximum 280 characters
        - Include 1-2 relevant hashtags
        - Use an informal but professional tone
        - Add emoji if appropriate
        """
        
        response = self.openai_client.chat.completions.create(
           model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a social media manager for a tech company."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    def post_tweet(self, text: str, image_path: str = None) -> bool:
        """Post text + optional image to Twitter"""
        try:
            if image_path:
                # Upload image
                media = self.twitter_api_v1.media_upload(filename=image_path)
                self.twitter_client.create_tweet(text=text, media_ids=[media.media_id])
            else:
                self.twitter_client.create_tweet(text=text)
            print(f"Posted at {datetime.now()}: {text[:50]}...")
            return True
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return False

    def select_theme(self) -> str:
        """Randomly select content theme based on weights"""
        import random
        return random.choices(
            list(self.content_themes.keys()),
            weights=list(self.content_themes.values()),
            k=1
        )[0]

    def run_scheduled_posts(self):
        """Schedule and run automated posting"""
        for post_time in self.posting_times:
            schedule.every().day.at(post_time).do(self.post_new_tweet)

        print(f"Bot started. Will post at {', '.join(self.posting_times)}")
        while True:
            schedule.run_pending()
            time.sleep(60)

    def post_new_tweet(self):
        """Generate and post one tweet"""
        theme = self.select_theme()
        tweet_text = self.generate_tweet(theme)
        self.post_tweet(tweet_text)

if __name__ == "__main__":
    bot = TwitterAIBot()
    
    # For testing (post once immediately)
    bot.post_new_tweet()
    
    # For production (scheduled posting)
    # bot.run_scheduled_posts()