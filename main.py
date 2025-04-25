from utils.weather import get_weather
from utils.news import get_rss_headlines
from utils.summarizer import summarize_headlines
from utils.calendar import get_today_events
from utils.telegram import send_telegram_message
from utils.youtube import get_latest_video
from utils.user_profile import YOUTUBE_CHANNELS
import re

# --- Markdown escape for Telegram MarkdownV2 ---
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(rf'([{re.escape(escape_chars)}])', r'\\\1', text)

# --- Gather data ---
rss_url = "https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en"
headlines = get_rss_headlines(rss_url, limit=25)
gpt_summary_raw = summarize_headlines(headlines)

# Format summary with blank lines between bullets
gpt_summary_lines = [line.strip() for line in gpt_summary_raw.split("•") if line.strip()]
gpt_summary = "\n\n".join(f"• {line}" for line in gpt_summary_lines)

weather_report = get_weather()
calendar_events = get_today_events()

# --- YouTube updates ---
youtube_updates = []
for name, channel_id in YOUTUBE_CHANNELS.items():
    update = get_latest_video(channel_id)
    if update:
        youtube_updates.append(f"*{name}:*\n{update}")

# --- Escape everything for MarkdownV2 ---
gpt_summary = escape_markdown(gpt_summary)
weather_report = escape_markdown(weather_report)
calendar_events = [escape_markdown(e) for e in calendar_events]
youtube_updates = [escape_markdown(u) for u in youtube_updates]

# --- Print to terminal ---
print("\n🗞️ Top Headlines:")
for headline in headlines:
    print("•", headline)

print("\n🧠 GPT Summary:")
print(gpt_summary)

print("\n🌤 Weather in Perth, Australia:")
print(weather_report)

print("\n📆 Today's Calendar:")
for event in calendar_events:
    print(f"• {event}")

if youtube_updates:
    print("\n🎥 YouTube Updates:")
    for update in youtube_updates:
        print(update)

# --- Compose Telegram message ---
message = f"""
🌤 *Weather:*\n{weather_report}

📰 *News Summary:*\n{gpt_summary}

📆 *Today's Calendar:*
{chr(10).join(f'• {event}' for event in calendar_events)}
"""

if youtube_updates:
    message += f"\n\n🎥 *YouTube Updates:*\n" + "\n\n".join(youtube_updates)

send_telegram_message(message.strip())
