from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st
from typing import List, Dict
import time

# Cache the sentiment pipeline to avoid reloading
@st.cache_resource
def load_sentiment_pipeline():
    """Load and cache the sentiment analysis model"""
    return pipeline("sentiment-analysis")

def analyze_sentiment_batch(comments: List[str], batch_size: int = 32) -> List[Dict]:
    """
    Analyze sentiment for comments in batches for better performance
    
    Args:
        comments: List of comment texts
        batch_size: Number of comments to process at once
    
    Returns:
        List of sentiment analysis results
    """
    if not comments:
        return []
    
    # Load the cached pipeline
    sentiment_pipeline = load_sentiment_pipeline()
    
    results = []
    total_batches = (len(comments) + batch_size - 1) // batch_size
    
    # Process comments in batches
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i + batch_size]
        
        try:
            # Analyze batch
            batch_results = sentiment_pipeline(batch)
            
            # Process results
            for j, result in enumerate(batch_results):
                comment_index = i + j
                if comment_index < len(comments):
                    results.append({
                        "text": comments[comment_index],
                        "label": result['label'],
                        "score": round(result['score'], 2)
                    })
                    
        except Exception as e:
            # Handle errors gracefully
            st.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
            # Add placeholder results for failed batch
            for j in range(len(batch)):
                comment_index = i + j
                if comment_index < len(comments):
                    results.append({
                        "text": comments[comment_index],
                        "label": "NEUTRAL",
                        "score": 0.5
                    })
    
    return results

# Keep the original function for backward compatibility
def analyze_sentiment(comments):
    return analyze_sentiment_batch(comments)
