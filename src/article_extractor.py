import requests
from bs4 import BeautifulSoup
from typing import Optional
import re
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

class ArticleExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FinDigest/1.0 (Financial News Summarizer; respectful bot)'
        })
        self.robot_parsers = {}

    def can_fetch(self, url: str) -> bool:
        """Check if scraping is allowed by robots.txt"""
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        if base_url not in self.robot_parsers:
            rp = RobotFileParser()
            rp.set_url(f"{base_url}/robots.txt")
            try:
                rp.read()
                self.robot_parsers[base_url] = rp
            except:
                return False
        
        return self.robot_parsers[base_url].can_fetch('FinDigest', url)

    def extract_content(self, url: str) -> Optional[str]:
        """Extract main article content from URL."""
        if not self.can_fetch(url):
            return None

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'iframe']):
                element.decompose()
            
            # Find main article content
            article = soup.find('article') or soup.find(class_=re.compile(r'article|post|content|story'))
            if not article:
                paragraphs = soup.find_all('p')
                content = ' '.join(p.get_text().strip() for p in paragraphs)
            else:
                content = article.get_text().strip()
            
            # Clean the content
            content = re.sub(r'\s+', ' ', content)  # Remove extra whitespace
            content = re.sub(r'\n+', '\n', content)  # Remove extra newlines
            
            return content if content else None
            
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None