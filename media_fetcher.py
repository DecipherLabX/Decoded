import os, random, requests

def get_media_url(topic):
    topic_query = topic.replace(" ", "+")
    
    # Try Unsplash first
    unsplash_url = f"https://source.unsplash.com/800x600/?{topic_query}"
    
    # 30% chance to choose a short mp4 from Pexels
    if random.random() < 0.3:
        video_url = "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
        return video_url
    else:
        return unsplash_url