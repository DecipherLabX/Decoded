# DecipherLabX.py
import os
import random
import tweepy
from datetime import datetime

# Try to import load_dotenv if python-dotenv is installed.
# If it's not installed, we'll still proceed (we rely on os.getenv for GitHub Actions).
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except Exception:
    DOTENV_AVAILABLE = False

# -- Optional: load a specific env file if present (useful for local testing)
# priority order:
# 1) If an environment variable "ENV_FILE" is set, attempt to load it
# 2) Else if a file named ".env" exists in the repo root, load it
# 3) Else, skip and rely on environment variables (GitHub Actions / Render)
env_file = os.getenv("ENV_FILE") or ".env"
if DOTENV_AVAILABLE and os.path.exists(env_file):
    load_dotenv(env_file)
    print(f"Loaded environment from: {env_file}")
elif DOTENV_AVAILABLE:
    # try default but silent if missing
    load_dotenv()
    print("python-dotenv available; attempted load (no explicit file found).")
else:
    print("python-dotenv not available; relying on environment variables.")

# -- Read credentials from environment (works for .env or GitHub Secrets)
CONSUMER_KEY = os.getenv("CONSUMER_KEY") or os.getenv("CONSUMER_API_KEY") or os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET") or os.getenv("CONSUMER_API_KEY_SECRET") or os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET") or os.getenv("ACCESS_TOKEN_KEY_SECRET")

# Basic check to show if keys are loaded (do NOT print secrets)
missing = [k for k, v in [
    ("CONSUMER_KEY", CONSUMER_KEY),
    ("CONSUMER_SECRET", CONSUMER_SECRET),
    ("ACCESS_TOKEN", ACCESS_TOKEN),
    ("ACCESS_TOKEN_SECRET", ACCESS_TOKEN_SECRET),
] if not v]

if missing:
    print("WARNING: Missing environment variables:", missing)
    # Do not exit here automatically — if you want to fail fast uncomment:
    # raise SystemExit("Missing required Twitter credentials. Aborting.")

# Authenticate with OAuth1 (working with Consumer + Access tokens)
try:
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    api.verify_credentials()
    print("✅ Twitter authentication OK")
except Exception as e:
    api = None
    print("❌ Twitter authentication failed:", e)

# --- Simple trending selection (placeholder) ---
# Replace with pytrends or other logic; this example uses a tiny fallback list.
topics_fallback = [
    "AI", "Tech news", "Startups", "Motivation", "Productivity",
    "Memes", "Cars", "Design", "Business", "Innovation"
]

def choose_trending_topic():
    # If you are using pytrends (ensure it's in requirements.txt), you can fetch live trends here.
    # For now, pick from fallback.
    return random.choice(topics_fallback)

# --- Caption generator with category -> hashtags & emoji (from earlier)
def categorize_topic(topic):
    t = topic.lower()
    if any(k in t for k in ["ai", "tech", "robot", "innovation", "startup", "digital"]):
        return {"emoji": "🤖", "hashtags": "#AI #TechTrends #Innovation"}
    if any(k in t for k in ["business", "startup", "growth", "finance", "marketing"]):
        return {"emoji": "💼", "hashtags": "#Growth #Startups #BusinessTips"}
    if any(k in t for k in ["movie", "music", "film", "tv", "entertainment", "celebrity"]):
        return {"emoji": "🎬", "hashtags": "#TrendingNow #Viral #Entertainment"}
    if any(k in t for k in ["travel", "vacation", "lifestyle", "tourism"]):
        return {"emoji": "✈️", "hashtags": "#Travel #Lifestyle #Wanderlust"}
    if any(k in t for k in ["health", "fitness", "workout", "diet"]):
        return {"emoji": "💪", "hashtags": "#Health #Fitness #Wellness"}
    return {"emoji": "🔥", "hashtags": "#Viral #Fun #DecipherLabX"}

# Caption templates
def build_caption(topic):
    cat = categorize_topic(topic)
    templates = [
        f"{cat['emoji']} {topic} is trending! Join the buzz 🚀 {cat['hashtags']}",
        f"💡 Insight: {topic} is catching attention! {cat['emoji']} {cat['hashtags']}",
        f"📈 Trending now: {topic} {cat['emoji']} {cat['hashtags']}",
        f"⚡ Hot topic: {topic}! What’s your take? {cat['emoji']} {cat['hashtags']}"
    ]
    return random.choice(templates)

# Optional: media selection logic
def choose_media():
    media_dir = "media"
    if not os.path.isdir(media_dir):
        return None
    files = [f for f in os.listdir(media_dir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4"))]
    return os.path.join(media_dir, random.choice(files)) if files else None

def post(truthy_post=True):
    if api is None:
        print("No API client available — skip posting.")
        return
    topic = choose_trending_topic()
    caption = build_caption(topic)
    media_path = choose_media()

    try:
        if media_path and media_path.lower().endswith((".mp4",)):
            # For videos, tweepy may require chunked upload - this uses media_upload for simplicity
            uploaded = api.media_upload(media_path)
            api.update_status(status=caption, media_ids=[uploaded.media_id])
            print(f"✅ Posted video/media for topic: {topic}")
        elif media_path:
            uploaded = api.media_upload(media_path)
            api.update_status(status=caption, media_ids=[uploaded.media_id])
            print(f"✅ Posted image/media for topic: {topic}")
        else:
            api.update_status(status=caption)
            print(f"✅ Posted text for topic: {topic}")
    except Exception as e:
        print("❌ Error while posting:", e)

if __name__ == "__main__":
    print(f"Starting DecipherLabX at {datetime.now().isoformat()}")
    post()
