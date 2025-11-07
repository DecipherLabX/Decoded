from openai import OpenAI
client = OpenAI()

def generate_caption(topic):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative AI bot."},
            {"role": "user", "content": f"Write a catchy tweet caption about {topic}."}
        ]
    )
    return completion.choices[0].message.content
