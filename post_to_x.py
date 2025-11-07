import tweepy, os, requests

def get_x_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_CLIENT_ID"),
        consumer_secret=os.getenv("X_CLIENT_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET")
    )

def post_to_x(text, media_url=None):
    client = get_x_client()
    try:
        if media_url:
            # Download media temporarily to memory
            r = requests.get(media_url)
            temp_file = "temp_media"
            ext = ".mp4" if "mp4" in media_url else ".jpg"
            with open(temp_file + ext, "wb") as f:
                f.write(r.content)

            # Upload to X
            media = client.media_upload(filename=temp_file + ext)
            client.create_tweet(text=text, media_ids=[media.media_id])
            os.remove(temp_file + ext)
        else:
            client.create_tweet(text=text)

        print("✅ Tweet posted successfully!")
    except Exception as e:
        print("❌ Error posting tweet:", e)
