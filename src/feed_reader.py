import feedparser
from typing import List, Dict, Optional
from datetime import datetime

class FeedReader:
    def __init__(self, rss_urls: List[str]):
        self.rss_urls = rss_urls
        
    def fetch_articles(self) -> List[Dict]:
        """Fetch articles from multiple RSS feeds."""
        articles = []
        
        for url in self.rss_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'source': feed.feed.get('title', 'Unknown Source'),
                        'summary': entry.get('summary', '')
                    }
                    articles.append(article)
            except Exception as e:
                print(f"Error fetching from {url}: {str(e)}")
                continue
                
        return articles
    
    def validate_feed(self, url: str) -> bool:
        """Validate if RSS feed is accessible and valid."""
        try:
            feed = feedparser.parse(url)
            return feed.get('version', '') != ''
        except:
            return False
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse publication date to datetime object."""
        try:
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        except:
            try:
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
            except:
                return None