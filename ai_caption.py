import os, openai

def generate_caption(topic):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Write a short, catchy tweet under 250 characters about '{topic}' with 2 trending hashtags."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()