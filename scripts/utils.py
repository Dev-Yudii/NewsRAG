from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import trafilatura
import json
import os
import re
import time

def can_fetch(url):
    """
    Checks if the URL can be accessed by the bot according to robots.txt.
    """
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch('*', url)
    except Exception as error:
        print(f"Error reading robots.txt from {robots_url}: {error}")
        return False

def download_news(url):
    """
    Downloads the HTML content of the news article.
    Returns None if the download fails.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        return downloaded
    except Exception as error:
        print(f"Error downloading news from {url}: {error}")
        return None

def extract_text(html):
    """
    Parses HTML and returns cleaned text.
    Returns None if extraction fails.
    """
    if not html:
        return None
    
    # Attempt standard extraction
    text = trafilatura.extract(html)
    
    # If standard fails, try a more aggressive extraction (includes tables, ignores some heuristics)
    if not text:
        text = trafilatura.extract(
            html, 
            include_tables=True, 
            include_comments=False, 
            no_fallback=False
        )
        
    return text

def save_json(news_data, folder):
    """
    Saves news data to a JSON file with a sanitized filename.
    Creates the destination folder if it doesn't exist.
    """
    os.makedirs(folder, exist_ok=True)

    # 1. Sanitize title: Remove non-alphanumeric characters (except spaces/hyphens)
    title = news_data.get("title", "no_title")
    clean_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    
    # 2. Set character limit for the filename
    clean_title = clean_title[:50]

    # 3. Add timestamp and ensure .json extension
    timestamp = int(time.time())
    file_name = f"{clean_title}_{timestamp}.json"
    file_path = os.path.join(folder, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
        return file_path
    except Exception as error:
        print(f"Error saving JSON to {file_path}: {error}")
        return None