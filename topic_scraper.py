import requests, os

def get_trending_topics():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    topics = [a["title"] for a in data.get("articles", []) if a.get("title")]
    return topics[:10] if topics else ["AI", "SpaceX", "Innovation"]