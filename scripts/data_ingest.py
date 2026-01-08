"""
Script to collect news via RSS and save to JSON.
Respects robots.txt and scraping best practices.

In addition to ingestion, this script generates quality metrics
and saves an external report for auditing and future comparison.
"""

import time
import json
import os
from datetime import datetime

import feedparser
import utils


# Configuration
feeds = {
    "NASA": "https://www.nasa.gov/news-release/feed/"
}

RAW_FOLDER = "data/raw"
REPORTS_FOLDER = "reports"

REQUEST_DELAY = 2  # seconds between requests


# Metrics Initialization
metrics = {
    "timestamp": datetime.utcnow().isoformat(),
    "total_urls": 0,
    "robots_blocked": 0,
    "download_failed": 0,
    "extraction_empty": 0,
    "fallback_used": 0,
    "texts_with_content": 0,
    "text_lengths": []  # used later for statistics
}


# Main Ingestion Loop
for source, feed_url in feeds.items():
    print(f"\nProcessing feed: {source}")

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        metrics["total_urls"] += 1
        news_url = entry.link

        # Robots.txt verification
        if not utils.can_fetch(news_url):
            metrics["robots_blocked"] += 1
            print(f"Blocked by robots.txt: {news_url}")
            continue

        # Page download
        downloaded = utils.download_news(news_url)
        if downloaded is None:
            metrics["download_failed"] += 1
            continue

        # Text extraction
        text = utils.extract_text(downloaded)

        if text is None:
            metrics["extraction_empty"] += 1

            # Fallback: RSS description (if available)
            text = entry.get("description", None)
            if text:
                metrics["fallback_used"] += 1
                print(f"Warning: Using RSS description for '{entry.title}'")

        # Content metrics
        if text:
            metrics["texts_with_content"] += 1
            metrics["text_lengths"].append(len(text))

        # Final data structure
        news_data = {
            "title": entry.title,
            "url": news_url,
            "source": source,
            "date": entry.get("published", ""),
            "context": text
        }

        file_path = utils.save_json(news_data, RAW_FOLDER)
        if file_path:
            print(f"News saved to: {file_path}")

        time.sleep(REQUEST_DELAY)


# Metrics post-processing
if metrics["text_lengths"]:
    metrics["avg_text_length"] = sum(metrics["text_lengths"]) / len(metrics["text_lengths"])
    metrics["min_text_length"] = min(metrics["text_lengths"])
    metrics["max_text_length"] = max(metrics["text_lengths"])
else:
    metrics["avg_text_length"] = 0
    metrics["min_text_length"] = 0
    metrics["max_text_length"] = 0


# Remove raw list to keep the report clean
metrics.pop("text_lengths")


# Terminal Report Output
print("\n===== Ingestion Report =====")
print(f"Total URLs processed: {metrics['total_urls']}")
print(f"Blocked by robots.txt: {metrics['robots_blocked']}")
print(f"Failed downloads: {metrics['download_failed']}")
print(f"Empty extractions: {metrics['extraction_empty']}")
print(f"RSS Fallback used: {metrics['fallback_used']}")
print(f"Texts with content: {metrics['texts_with_content']}")
print(f"Average text length: {metrics['avg_text_length']:.2f}")
print(f"Minimum text length: {metrics['min_text_length']}")
print(f"Maximum text length: {metrics['max_text_length']}")
print("============================\n")


# Saving external report
os.makedirs(REPORTS_FOLDER, exist_ok=True)

report_name = f"ingestion_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
report_path = os.path.join(REPORTS_FOLDER, report_name)

with open(report_path, "w", encoding="utf-8") as f:
    json.dump(metrics, f, ensure_ascii=False, indent=4)

print(f"Report saved to: {report_path}")