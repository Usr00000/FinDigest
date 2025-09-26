import schedule
import time
from datetime import datetime
import json
import os
from feed_reader import FeedReader
from article_extractor import ArticleExtractor
from summarizer import ArticleSummarizer
from dotenv import load_dotenv

load_dotenv()

class NewsUpdateScheduler:
    def __init__(self):
        self.feed_reader = FeedReader(self._get_default_feeds())
        self.article_extractor = ArticleExtractor()
        self.summarizer = ArticleSummarizer()
        self.max_articles = int(os.getenv('MAX_ARTICLES', 20))
        self.cache_file = 'cached_summaries.json'

    def _get_default_feeds(self):
        """Get default RSS feeds from environment variables"""
        feeds_str = os.getenv('DEFAULT_RSS_FEEDS', '')
        return feeds_str.split(',') if feeds_str else []

    def update_summaries(self):
        """Fetch and summarize new articles"""
        print(f"[{datetime.now()}] Starting scheduled update...")
        
        try:
            # Fetch articles
            articles = self.feed_reader.fetch_articles()
            processed_articles = []
            
            for article in articles[:self.max_articles]:
                content = self.article_extractor.extract_content(article['link'])
                if content:
                    summary = self.summarizer.summarize(content)
                    if summary:
                        processed_articles.append({
                            **article,
                            'summary': summary,
                            'processed_time': datetime.now().isoformat()
                        })
            
            # Save to cache file
            with open(self.cache_file, 'w') as f:
                json.dump(processed_articles, f)
                
            print(f"[{datetime.now()}] Successfully updated {len(processed_articles)} articles")
            
        except Exception as e:
            print(f"[{datetime.now()}] Error during update: {str(e)}")

def main():
    scheduler = NewsUpdateScheduler()
    
    # Schedule updates
    schedule.every().day.at("06:00").do(scheduler.update_summaries)  # Morning update
    schedule.every().day.at("12:00").do(scheduler.update_summaries)  # Noon update
    schedule.every().day.at("18:00").do(scheduler.update_summaries)  # Evening update
    
    # Initial update
    scheduler.update_summaries()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()