from dotenv import load_dotenv
import os, random, time
from topic_scraper import get_trending_topics
from media_fetcher import get_media_url
from ai_caption import generate_caption
from post_to_x import post_to_x
import openai  # for exception handling

# Load environment variables once
load_dotenv()

def main():
    print("🚀 DecipherLabX Internet Bot Starting (OAuth 2.0)...")

    while True:
        try:
            # Get trending topics and select one randomly
            topics = get_trending_topics()
            topic = random.choice(topics)
            print(f"🎯 Selected topic: {topic}")

            # Generate caption using OpenAI with error handling
            try:
                caption = generate_caption(topic)
            except openai.error.RateLimitError:
                print("⚠️ OpenAI quota exceeded or rate limited. Skipping this post.")
                caption = f"Trending topic: {topic}"  # fallback caption
            except Exception as e:
                print(f"⚠️ OpenAI error: {e}. Skipping this post.")
                caption = f"Trending topic: {topic}"

            print(f"📝 Caption: {caption}")

            # Fetch media URL (image/video) for the topic
            media_url = get_media_url(topic)
            print(f"🌐 Media URL: {media_url}")

            # Post to X/Twitter
            try:
                post_to_x(caption, media_url)
            except Exception as e:
                print(f"⚠️ Failed to post to X: {e}")

            # Wait 30 minutes before next post
            print("🕒 Sleeping for 30 minutes...")
            time.sleep(1800)  # 30 minutes

        except Exception as e:
            # Catch any unexpected errors so the bot keeps running
            print(f"⚠️ Unexpected error in bot loop: {e}")
            time.sleep(300)  # wait 5 minutes before retrying

if __name__ == "__main__":
    main()
