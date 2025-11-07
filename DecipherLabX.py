import os, random, time, schedule
from datetime import datetime
import tweepy
from dotenv import load_dotenv
from pytrends.request import TrendReq

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# --------------- AUTH ---------------
# OAuth 2.0 (User Context)
client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)
api_v1 = tweepy.API(
    tweepy.OAuth1UserHandler(
        os.getenv("CONSUMER_KEY"),
        os.getenv("CONSUMER_SECRET"),
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCESS_TOKEN_SECRET")
    )
)

# Initialize Google Trends
pytrends = TrendReq(hl='en-US', tz=360)

caption_templates = [
    "🔥 {topic} is trending right now! #DecipherLabX #{tag}",
    "💡 Everyone’s talking about {topic}! What’s your take? #{tag} #Viral",
    "🚀 {topic} is blowing up online — stay ahead! #{tag} #Growth",
    "⚡ Trend Alert: {topic}! Join the discussion 👇 #{tag}"
]

def get_trending_topics():
    try:
        trending_df = pytrends.trending_searches(pn='global')
        topics = trending_df[0].tolist()
        banned = ['religion', 'faith', 'spiritual', 'war', 'violence']
        clean_topics = [t for t in topics if all(b not in t.lower() for b in banned)]
        return clean_topics[:10]
    except Exception as e:
        print("⚠️ Error fetching trends:", e)
        return ["AI", "Innovation", "Startups"]

def build_caption():
    topic = random.choice(get_trending_topics())
    tag = topic.replace(" ", "")
    return random.choice(caption_templates).format(topic=topic, tag=tag), topic

def select_media(topic):
    media_dir = "media"
    if not os.path.exists(media_dir):
        return None
    files = os.listdir(media_dir)
    for f in files:
        if topic.split()[0].lower() in f.lower():
            return os.path.join(media_dir, f)
    return os.path.join(media_dir, random.choice(files)) if files else None

def post_tweet():
    caption, topic = build_caption()
    media_path = select_media(topic)

    try:
        if media_path and media_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
            uploaded = api_v1.media_upload(media_path)
            client.create_tweet(text=caption, media_ids=[uploaded.media_id])
            print(f"✅ [{datetime.now().strftime('%H:%M')}] Posted: {topic}")
        else:
            client.create_tweet(text=caption)
            print(f"✅ [{datetime.now().strftime('%H:%M')}] Posted text about: {topic}")
    except Exception as e:
        print("❌ Error posting:", e)

# Schedule: every 48 minutes (~30/day)
schedule.every(48).minutes.do(post_tweet)

print("🤖 DecipherLabX OAuth 2.0 bot started...")
post_tweet()  # immediate post

while True:
    schedule.run_pending()
    time.sleep(30)
