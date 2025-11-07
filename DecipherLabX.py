import os
import random
import tweepy
from dotenv import load_dotenv
from pytrends.request import TrendReq

# Load secrets
load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Twitter auth
auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# Google Trends
pytrends = TrendReq(hl="en-US", tz=360)
trending_df = pytrends.trending_searches()
trending_topics = trending_df[0].tolist()

# Exclude sensitive/religious
excluded_keywords = ["god", "religion", "islam", "hindu", "muslim", "church", "temple", "spiritual", "bible"]
filtered_topics = [t for t in trending_topics if all(bad.lower() not in t.lower() for bad in excluded_keywords)]

if not filtered_topics:
    filtered_topics = ["AI innovation", "Startup growth", "Tech trends", "Automobile", "Motivation", "Funny memes"]

# Pick a topic
topic = random.choice(filtered_topics)

# Categorize topic for hashtags & emojis
def categorize_topic(topic):
    topic_lower = topic.lower()
    if any(k in topic_lower for k in ["ai", "tech", "robot", "innovation", "startup", "digital"]):
        return {"emoji": "🤖", "hashtags": "#AI #TechTrends #Innovation"}
    elif any(k in topic_lower for k in ["business", "startup", "growth", "finance", "marketing"]):
        return {"emoji": "💼", "hashtags": "#Growth #Startups #BusinessTips"}
    elif any(k in topic_lower for k in ["movie", "music", "film", "tv", "entertainment", "celebrity"]):
        return {"emoji": "🎬", "hashtags": "#TrendingNow #Viral #Entertainment"}
    elif any(k in topic_lower for k in ["travel", "vacation", "lifestyle", "tourism"]):
        return {"emoji": "✈️", "hashtags": "#Travel #Lifestyle #Wanderlust"}
    elif any(k in topic_lower for k in ["health", "fitness", "workout", "diet"]):
        return {"emoji": "💪", "hashtags": "#Health #Fitness #Wellness"}
    else:
        return {"emoji": "🔥", "hashtags": "#Viral #Fun #DecipherLabX"}

category = categorize_topic(topic)

# Dynamic captions
caption_styles = [
    f"{category['emoji']} {topic} is trending! Join the buzz 🚀 {category['hashtags']}",
    f"💡 Insight: {topic} is catching attention! {category['emoji']} {category['hashtags']}",
    f"📈 Trending now: {topic} {category['emoji']} {category['hashtags']}",
    f"⚡ Hot topic: {topic}! What’s your take? {category['emoji']} {category['hashtags']}"
]

tweet_text = random.choice(caption_styles)

# Optional media
media_folder = "media"
media_files = [os.path.join(media_folder, f) for f in os.listdir(media_folder) if f.endswith((".jpg", ".png", ".mp4"))] if os.path.exists(media_folder) else []

try:
    if media_files and random.random() < 0.4:
        media = random.choice(media_files)
        api.update_status_with_media(status=tweet_text, filename=media)
        print(f"✅ Posted with media: {topic}")
    else:
        api.update_status(tweet_text)
        print(f"✅ Posted text: {topic}")

except Exception as e:
    print("❌ Error posting tweet:", e)
