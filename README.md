# 🎙️ English Accent Detection App

An AI-powered application that detects English accents from video URLs using AI models. The app analyzes speech in videos to identify the language being spoken and classify different English accents with confidence scores.


## 🎬 Demo Video

**Watch the app in action!** 

[![Demo Video](https://img.shields.io/badge/🎥_Watch_Demo-Google_Drive-blue?style=for-the-badge)](https://drive.google.com/file/d/1n6836Z5zWEICZcGJ_2VzowaOzjviUz0O/view?usp=sharing)

See how the app processes videos and identifies different English accents with confidence scores.


## 🌟 Features

- **Language Detection**: Automatically detects the language being spoken using OpenAI Whisper
- **Accent Classification**: Identifies English accents using SpeechBrain models
- **Multiple Interfaces**: Both web interface (Streamlit) and REST API (FastAPI)
- **Video Processing**: Downloads and processes videos from direct URLs
- **Confidence Scores**: Provides detailed confidence percentages for predictions

## 🎯 Supported Accents

The app can detect the following English accents:

- American
- British
- Australian
- Indian
- Canadian
- Bermudian
- Scottish
- African
- Irish
- New Zealand
- Welsh
- Malaysian
- Filipino
- Singaporean
- Hong Kong
- South Atlantic

## 📁 Project Structure

```
accent_app/
├── app/
│   ├── __init__.py
│   ├── api.py              # FastAPI REST API
│   ├── pipeline.py         # Core AI processing pipeline
│   └── utils.py            # Video download and audio extraction utilities
├── pretrained_models/      # Downloaded AI models (auto-created)
├── hf_cache/              # Hugging Face model cache (auto-created)
├── .devcontainer/         # Development container configuration
├── .gitignore
├── requirements.txt       # Python dependencies
├── streamlit_app.py       # Streamlit web interface
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11
- FFmpeg (for audio processing)
- At least 8GB RAM (recommended)
- Good internet connection (for model downloads)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WadiaaTouhami/EngAccent-detection.git
   cd EngAccent-detection
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

### Running the Application

#### Option 1: Streamlit Web Interface (Recommended)

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

#### Option 2: FastAPI REST API

```bash
# Install uvicorn if not already installed
pip install uvicorn

# Run the API server
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- API schema: `http://localhost:8000/redoc`

## 💻 Usage

### Web Interface

1. Open the Streamlit app in your browser
2. Enter a video URL in the input field
3. Click "🔍 Analyze Accent"
4. Wait for processing (may take 1-3 minutes)
5. View the results with confidence scores

### API Usage

**Process a video:**
```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"video_url": "https://example.com/video.mp4"}'
```

**Response format:**
```json
{
  "status": "success",
  "video_url": "https://example.com/video.mp4",
  "language": "en",
  "language_confidence": 0.94,
  "accent": "British",
  "accent_confidence": 0.78,
  "accent_confidence_percentage": 78.0,
  "summary": "Detected British accent with 78% confidence"
}
```


### Example URLs

The app includes several example URLs for testing:
- Example 1 (British accent)
- Example 2 (American accent)
- Example 3 (African accent)
- Example 4 (French language)

## 🔧 Configuration

### Model Configuration

You can customize the models used in `app/pipeline.py`:

```python
# Change Whisper model size (tiny, base, small, medium, large)
pipeline = AccentDetectionPipeline(whisper_model_size="base")
```

Available Whisper models:
- `tiny`: Fastest, least accurate
- `base`: Good balance (default)
- `small`: Better accuracy
- `medium`: Higher accuracy
- `large`: Best accuracy, slowest

## 🛠️ Technical Details

### AI Models Used

1. **OpenAI Whisper**: Language detection and speech recognition
   - Model: Configurable (tiny to large)
   - Purpose: Detects if audio is English
   - Accuracy: Very high for language detection

2. **SpeechBrain Accent Classifier**: English accent classification
   - Model: `Jzuluaga/accent-id-commonaccent_ecapa`
   - Training: CommonAccent dataset

### Processing Pipeline

1. **Video Download**: Downloads video from URL using `requests`
2. **Audio Extraction**: Extracts audio using `moviepy` and `ffmpeg`
3. **Language Detection**: Uses Whisper to confirm English speech
4. **Accent Classification**: Uses SpeechBrain to classify English accent
5. **Result Formatting**: Returns structured JSON response

### Performance

- **Processing Time**: 1-3 minutes per video (depending on length)
- **Memory Usage**: 2-4GB RAM during processing
- **Accuracy**: ~80-90% for clear speech samples
- **Supported Duration**: Works best with 10 seconds to 3 minutes of speech

## 🚀 Deployment

### Streamlit Cloud

The app is configured for Streamlit Cloud deployment:

1. Fork this repository
2. Connect your GitHub account to [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from your repository

**Note**: Streamlit Cloud has resource limitations that may cause some videos to fail processing.

### Local Deployment

For full functionality, run locally:

```bash
# Install and run
pip install -r requirements.txt
streamlit run streamlit_app.py
```


## 🐛 Troubleshooting

### Common Issues

**1. "Video download failed"**
- Check if the URL is publicly accessible
- Ensure stable internet connection
- Try a different video URL

**2. "Audio extraction failed"**
- Verify FFmpeg is installed correctly
- Check if video contains audio track
- Ensure sufficient disk space

**3. "Models failed to load"**
- Verify internet connection for model downloads
- Check available RAM (needs 2GB+)
- Clear model cache: delete `pretrained_models/` and `hf_cache/` folders

**4. Windows-specific issues**
- Run as administrator if getting permission errors
- Enable Windows Developer Mode for symlinks
- Use forward slashes in file paths

### Performance Tips

- **Use shorter videos** (< 2 minutes) for faster processing
- **Ensure clear audio** for better accuracy
- **Run locally** for best performance vs. cloud deployment
- **Use base or tiny Whisper model** for faster processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.


## 📄 License

This project is open source. Please check individual model licenses:
- OpenAI Whisper: MIT License
- SpeechBrain models: Apache 2.0 License

## 🙏 Acknowledgments

- **OpenAI Whisper**: For excellent speech recognition and language detection
- **SpeechBrain**: For the accent classification model
- **Hugging Face**: For model hosting and easy access
- **Streamlit**: For the simple web interface framework
- **FastAPI**: For the REST API framework

---