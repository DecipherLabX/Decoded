from dotenv import load_dotenv
import os, random, time
from topic_scraper import get_trending_topics
from media_fetcher import get_media_url
from ai_caption import generate_caption
from post_to_x import post_to_x

load_dotenv()

def main():
    print("🚀 DecipherLabX Internet Bot Starting (OAuth 2.0)...")

    while True:
        topics = get_trending_topics()
        topic = random.choice(topics)
        print(f"🎯 Selected topic: {topic}")

        caption = generate_caption(topic)
        print(f"📝 Caption: {caption}")

        media_url = get_media_url(topic)
        print(f"🌐 Media URL: {media_url}")

        post_to_x(caption, media_url)

        print("🕒 Sleeping for 30 minutes...")
        time.sleep(1800)  # 30 minutes

if __name__ == "__main__":
    main()
