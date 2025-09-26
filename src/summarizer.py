from transformers import pipeline
from typing import Optional
import torch

class ArticleSummarizer:
    def __init__(self):
        # Use BART model fine-tuned for summarization
        self.model_name = "facebook/bart-large-cnn"
        self.device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline(
            "summarization",
            model=self.model_name,
            device=self.device,
            framework="pt"
        )
        
    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> Optional[str]:
        """Generate a concise summary of the article text."""
        if not text or len(text.split()) < min_length:
            return None
            
        try:
            # Split long articles into chunks if needed
            chunks = self._split_into_chunks(text)
            summaries = []
            
            for chunk in chunks:
                summary = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                if summary and len(summary) > 0:
                    summaries.append(summary[0]['summary_text'])
            
            # Combine summaries if multiple chunks were processed
            final_summary = ' '.join(summaries)
            return final_summary if final_summary else None
            
        except Exception as e:
            print(f"Error during summarization: {str(e)}")
            return None
    
    def _split_into_chunks(self, text: str, max_chunk_size: int = 1024) -> list:
        """Split long text into smaller chunks for processing."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_size += len(word) + 1  # +1 for space
            if current_size > max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks