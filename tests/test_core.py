import unittest
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from feed_reader import FeedReader
from article_extractor import ArticleExtractor
from summarizer import ArticleSummarizer

class TestFeedReader(unittest.TestCase):
    def setUp(self):
        self.test_feeds = [
            "http://feeds.reuters.com/reuters/businessNews",
            "https://www.bankofengland.co.uk/rss/news"
        ]
        self.reader = FeedReader(self.test_feeds)

    def test_feed_validation(self):
        """Test RSS feed validation"""
        self.assertTrue(self.reader.validate_feed(self.test_feeds[0]))
        self.assertFalse(self.reader.validate_feed("http://invalid.feed.url/rss"))

    def test_article_fetching(self):
        """Test article fetching from RSS feeds"""
        articles = self.reader.fetch_articles()
        self.assertIsInstance(articles, list)
        if articles:
            self.assertIn('title', articles[0])
            self.assertIn('link', articles[0])
            self.assertIn('published', articles[0])

class TestArticleExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = ArticleExtractor()

    def test_robots_txt_check(self):
        """Test robots.txt compliance check"""
        self.assertTrue(self.extractor.can_fetch("https://www.reuters.com/business"))

    def test_content_extraction(self):
        """Test article content extraction"""
        test_url = "https://www.reuters.com/business/finance"
        content = self.extractor.extract_content(test_url)
        self.assertIsNotNone(content)

class TestSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = ArticleSummarizer()

    def test_summarization(self):
        """Test article summarization"""
        test_text = "" * 5  # Long test article text
        summary = self.summarizer.summarize(test_text)
        self.assertIsNotNone(summary)

    def test_empty_input(self):
        """Test summarizer behavior with empty input"""
        self.assertIsNone(self.summarizer.summarize(""))

if __name__ == '__main__':
    unittest.main()