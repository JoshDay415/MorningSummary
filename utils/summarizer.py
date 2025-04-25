# utils/summarizer.py

import openai
import os
from dotenv import load_dotenv
from utils.user_profile import INTERESTS, IGNORE

load_dotenv()
interest_str = ", ".join(INTERESTS)
ignore_str = ", ".join(IGNORE)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_headlines(headlines):
    if not headlines:
        return "No headlines to summarize today."

    prompt = "\n".join(f"- {title}" for title in headlines)

    full_prompt = f"""
You're my personal news assistant. You know I care about:
{interest_str}

Please summarize only the most relevant stories (5–10 max) from the following headlines. 

Ignore topics like:
{ignore_str}

Only return the most interesting and relevant headlines in a casual, morning-style summary. Skip anything unrelated.

Headlines:

{prompt}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ GPT Error: {str(e)}"
