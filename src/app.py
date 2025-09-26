import streamlit as st
from feed_reader import FeedReader
from article_extractor import ArticleExtractor
from summarizer import ArticleSummarizer
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="FinDigest - Financial News Summarizer",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {padding: 2rem;}
    .stTitle {font-size: 2.5rem !important;}
    .article-card {border: 1px solid #e6e6e6; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;}
    .source-tag {background-color: #f0f2f6; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem;}
    .timestamp {color: #666; font-size: 0.8rem;}
    .summary-text {line-height: 1.6;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'summarized_articles' not in st.session_state:
    st.session_state.summarized_articles = []

# Default RSS sources
DEFAULT_SOURCES = [
    "http://feeds.reuters.com/reuters/businessNews",
    "https://www.bankofengland.co.uk/rss/news",
    "https://www.ecb.europa.eu/rss/press.html"
]

def load_cached_summaries():
    """Load cached summaries from file"""
    cache_file = "cached_summaries.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return []

def save_cached_summaries(summaries):
    """Save summaries to cache file"""
    cache_file = "cached_summaries.json"
    with open(cache_file, 'w') as f:
        json.dump(summaries, f)

def main():
    # Header
    st.title("FinDigest 📈")
    st.markdown("### Your AI-Powered Financial News Summarizer")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Settings")
        sources = st.text_area(
            "RSS Feed Sources (one per line)",
            value='\n'.join(DEFAULT_SOURCES),
            height=150
        )
        max_articles = st.slider("Maximum articles to fetch", 5, 20, 10)
        
        if st.button("🔄 Refresh Summaries", type="primary"):
            with st.spinner("Fetching and summarizing articles..."):
                # Initialize components
                feed_reader = FeedReader(sources.split('\n'))
                article_extractor = ArticleExtractor()
                summarizer = ArticleSummarizer()
                
                # Fetch and process articles
                articles = feed_reader.fetch_articles()
                processed_articles = []
                
                for article in articles[:max_articles]:
                    content = article_extractor.extract_content(article['link'])
                    if content:
                        summary = summarizer.summarize(content)
                        if summary:
                            processed_articles.append({
                                **article,
                                'summary': summary,
                                'processed_time': datetime.now().isoformat()
                            })
                
                st.session_state.summarized_articles = processed_articles
                save_cached_summaries(processed_articles)
    
    # Main content area
    if not st.session_state.summarized_articles:
        st.session_state.summarized_articles = load_cached_summaries()
    
    if not st.session_state.summarized_articles:
        st.info("👈 Click 'Refresh Summaries' to fetch the latest financial news")
    else:
        # Display articles in cards
        for article in st.session_state.summarized_articles:
            with st.container():
                st.markdown(f"""
                <div class='article-card'>
                    <span class='source-tag'>{article['source']}</span>
                    <h3>{article['title']}</h3>
                    <p class='timestamp'>{article['published']}</p>
                    <p class='summary-text'>{article['summary']}</p>
                    <a href='{article['link']}' target='_blank'>Read original article →</a>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()