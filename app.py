import streamlit as st
from youtube_utils import get_comments
from sentiment_model import analyze_sentiment_batch
import time

# Page configuration
st.set_page_config(
    page_title="YouTube Sentiment Analyzer",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube Sentiment Analyzer")
st.markdown("Analyze the sentiment of YouTube video comments efficiently!")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    max_comments = st.slider("Maximum Comments to Analyze", 10, 200, 50, help="More comments = longer processing time")
    batch_size = st.slider("Batch Size", 8, 64, 32, help="Larger batches = faster processing but more memory usage")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    api_key = st.text_input("Enter your YouTube Data API Key", type="password", help="Get your API key from Google Cloud Console")
    video_url = st.text_input("Paste the YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

with col2:
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Get your YouTube API key from [Google Cloud Console](https://console.cloud.google.com/)
    2. Paste a YouTube video URL
    3. Click 'Analyze Comments'
    4. Wait for results (processing time depends on comment count)
    """)

# Cache API key validation
@st.cache_data(ttl=3600)  # Cache for 1 hour
def validate_api_key(api_key):
    """Validate the API key by making a test request"""
    if not api_key:
        return False
    try:
        from youtube_utils import get_comments
        # Try to get a single comment from a popular video
        test_comments = get_comments("dQw4w9WgXcQ", api_key, max_results=1)
        return len(test_comments) >= 0
    except Exception:
        return False

if st.button("🚀 Analyze Comments", type="primary", use_container_width=True):
    if not api_key or not video_url:
        st.error("Please provide both API key and video URL.")
    elif "v=" not in video_url:
        st.error("Please provide a valid YouTube video URL.")
    else:
        # Validate API key
        with st.spinner("Validating API key..."):
            if not validate_api_key(api_key):
                st.error("Invalid API key. Please check your YouTube Data API key.")
                st.stop()
        
        # Extract video ID
        video_id = video_url.split("v=")[-1].split("&")[0]
        
        # Fetch comments with progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("📥 Fetching comments from YouTube...")
            start_time = time.time()
            
            comments = get_comments(video_id, api_key, max_results=max_comments)
            
            if not comments:
                st.warning("No comments found for this video.")
                st.stop()
            
            fetch_time = time.time() - start_time
            progress_bar.progress(50)
            status_text.text(f"✅ Fetched {len(comments)} comments in {fetch_time:.1f}s")
            
            # Analyze sentiment with progress
            status_text.text("🧠 Analyzing sentiment...")
            start_time = time.time()
            
            sentiments = analyze_sentiment_batch(comments, batch_size=batch_size)
            
            analysis_time = time.time() - start_time
            progress_bar.progress(100)
            status_text.text(f"✅ Analysis complete in {analysis_time:.1f}s")
            
            # Display results
            st.success(f"Analysis completed! Processed {len(sentiments)} comments in {fetch_time + analysis_time:.1f} seconds.")
            
            # Summary statistics
            positive_count = sum(1 for s in sentiments if s["label"] == "POSITIVE")
            negative_count = sum(1 for s in sentiments if s["label"] == "NEGATIVE")
            neutral_count = len(sentiments) - positive_count - negative_count
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positive", positive_count, f"{positive_count/len(sentiments)*100:.1f}%")
            with col2:
                st.metric("Negative", negative_count, f"{negative_count/len(sentiments)*100:.1f}%")
            with col3:
                st.metric("Neutral", neutral_count, f"{neutral_count/len(sentiments)*100:.1f}%")
            
            # Display detailed results
            st.subheader("📊 Detailed Results")
            
            # Filter options
            filter_option = st.selectbox("Filter by sentiment:", ["All", "Positive", "Negative", "Neutral"])
            
            filtered_sentiments = sentiments
            if filter_option != "All":
                filtered_sentiments = [s for s in sentiments if s["label"] == filter_option.upper()]
            
            # Display comments with better formatting
            for i, item in enumerate(filtered_sentiments):
                # Determine color based on sentiment
                if item["label"] == "POSITIVE":
                    color = "#28a745"
                    icon = "😊"
                elif item["label"] == "NEGATIVE":
                    color = "#dc3545"
                    icon = "😞"
                else:
                    color = "#6c757d"
                    icon = "😐"
                
                # Create a card-like display with colored comment text
                with st.container():
                    st.markdown(f"""
                    <div style="
                        border-left: 4px solid {color};
                        padding: 10px;
                        margin: 5px 0;
                        background-color: #f8f9fa;
                        border-radius: 5px;
                    ">
                        <div style="font-weight: bold; color: {color};">
                            {icon} {item['label']} ({item['score']:.2f})
                        </div>
                        <div style="margin-top: 5px; color: {color}; font-size: 1.1em;">
                            {item['text'][:200]}{'...' if len(item['text']) > 200 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your API key and video URL, or try with fewer comments.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Built with Streamlit • Uses YouTube Data API v3 • Powered by Transformers</p>
</div>
""", unsafe_allow_html=True)
