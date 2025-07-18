from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from typing import List, Optional
import time

# Cache YouTube service to avoid rebuilding
@st.cache_resource
def get_youtube_service(api_key: str):
    """Get cached YouTube service instance"""
    return build('youtube', 'v3', developerKey=api_key)

def get_comments(video_id: str, api_key: str, max_results: int = 50) -> List[str]:
    """
    Fetch comments from YouTube video with optimized performance
    
    Args:
        video_id: YouTube video ID
        api_key: YouTube Data API key
        max_results: Maximum number of comments to fetch
    
    Returns:
        List of comment texts
    """
    try:
        youtube = get_youtube_service(api_key)
        
        # Optimize request parameters
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_results, 100),  # YouTube API limit is 100
            textFormat="plainText",
            order="relevance"  # Get most relevant comments first
        )
        
        response = request.execute()
        
        comments = []
        for item in response.get('items', []):
            try:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                # Filter out very short or empty comments
                if len(comment.strip()) > 5:
                    comments.append(comment)
            except (KeyError, TypeError):
                # Skip malformed comments
                continue
        
        return comments[:max_results]  # Ensure we don't exceed requested limit
        
    except HttpError as e:
        if e.resp.status == 403:
            st.error("API quota exceeded or invalid API key. Please check your YouTube Data API key and quota.")
        elif e.resp.status == 404:
            st.error("Video not found or comments disabled.")
        else:
            st.error(f"YouTube API error: {e}")
        return []
    except Exception as e:
        st.error(f"Error fetching comments: {e}")
        return []

def get_video_info(video_id: str, api_key: str) -> Optional[dict]:
    """
    Get basic video information for validation
    
    Args:
        video_id: YouTube video ID
        api_key: YouTube Data API key
    
    Returns:
        Video information dict or None if error
    """
    try:
        youtube = get_youtube_service(api_key)
        
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        
        response = request.execute()
        
        if response.get('items'):
            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'view_count': video['statistics'].get('viewCount', 0),
                'comment_count': video['statistics'].get('commentCount', 0)
            }
        return None
        
    except Exception as e:
        st.error(f"Error fetching video info: {e}")
        return None
