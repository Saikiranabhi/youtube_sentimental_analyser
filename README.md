# YouTube Sentiment Analyzer

Analyze the sentiment of YouTube video comments using state-of-the-art NLP models. This interactive web app fetches comments from any public YouTube video and provides a detailed sentiment breakdown (positive, negative, neutral) using Hugging Face Transformers.

---

## 🚀 Features
- Analyze sentiment of YouTube comments in bulk
- Interactive Streamlit web interface
- Batch processing for speed and efficiency
- Visual summary of sentiment distribution
- Filter and view individual comments by sentiment
- Secure API key handling

---

## 🗂️ Project Structure
```
Youtube_sentiment_analyser/
├── app.py                # Streamlit web app
├── sentiment_model.py    # Sentiment analysis logic (Transformers)
├── youtube_utils.py      # YouTube API utilities
├── requirements.txt      # Python dependencies
```

---

## 🛠️ Technologies Used
- **Python**: Core programming language
- **Streamlit**: Web app framework for interactive UI
- **Google API Python Client**: Fetch YouTube comments via Data API v3
- **Transformers (Hugging Face)**: State-of-the-art sentiment analysis
- **Torch**: Deep learning backend for Transformers
- **Pandas & Numpy**: Data handling and manipulation

### Technology Descriptions
- **Streamlit**: Instantly turns Python scripts into shareable web apps
- **Transformers**: Pretrained NLP models for sentiment analysis
- **Google API Python Client**: Access YouTube Data API for comment retrieval

---

## 📦 Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd Youtube_sentiment_analyser
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. **Open in browser:**
   - Go to the local URL provided by Streamlit (usually http://localhost:8501)

---

## 📝 Usage
- Get a YouTube Data API key from Google Cloud Console
- Paste a YouTube video URL and your API key
- Set the number of comments and batch size
- Click **Analyze Comments**
- View sentiment metrics and detailed comment breakdown

---
```mermaid
flowchart TD
    A["User"] -->|"Enter API Key & Video URL"| B["Streamlit Web App"]
    B -->|"Extract Video ID"| C["YouTube Utils"]
    C -->|"Fetch Comments"| D["YouTube Data API"]
    D -->|"Return Comments"| C
    C -->|"Send Comments"| E["Sentiment Model"]
    E -->|"Analyze Sentiment"| F["Results"]
    F -->|"Display Metrics & Comments"| B
---

## 🔗 GitHub Repository
[https://github.com/Saikiranabhi/youtube_sentimental_analyser.git](#) <!-- Replace with your actual repo URL -->

---

## 📚 Important Notes
- Requires a valid YouTube Data API key (see Google Cloud Console)
- Only public videos with enabled comments are supported
- For best results, deploy using Streamlit Cloud or similar services

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
 
