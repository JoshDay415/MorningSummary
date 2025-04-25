# utils/news.py

import feedparser

def get_rss_headlines(feed_url, limit=25):
    feed = feedparser.parse(feed_url)
    headlines = [entry.title for entry in feed.entries[:limit]]
    return headlines
