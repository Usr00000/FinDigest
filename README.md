# FinDigest - Financial News Summarizer 📈

FinDigest is an AI-powered web application that automatically collects and summarizes financial news articles from reliable sources. It's designed to help beginner investors and finance students stay informed by providing concise, accessible summaries of important financial news.

## Features

- Automatic fetching of financial news from trusted RSS feeds
- AI-powered article summarization using state-of-the-art language models
- Clean, modern web interface for easy reading
- Source attribution and links to original articles
- Configurable news sources and summary settings
- Temporary caching of summaries for quick access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd findigest
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
cd src
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Configure RSS sources in the sidebar or use the default sources

4. Click "Refresh Summaries" to fetch and summarize the latest news

## Default News Sources

- Reuters Business News
- Bank of England News
- European Central Bank Press Releases

You can add or modify sources in the application's sidebar.

## Technical Details

- **Feed Reader**: Uses `feedparser` to fetch and parse RSS feeds
- **Article Extractor**: Implements respectful web scraping with `beautifulsoup4`
- **Summarizer**: Utilizes the BART model from Hugging Face's `transformers` library
- **Web Interface**: Built with `streamlit` for a responsive user experience

## Ethical Considerations

- Respects `robots.txt` directives
- Implements reasonable request delays
- Properly attributes all content sources
- Avoids paywalled content

## Requirements

- Python 3.7+
- See `requirements.txt` for package dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.