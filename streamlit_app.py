import streamlit as st
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

try:
    from app.pipeline import AccentDetectionPipeline

    @st.cache_resource
    def load_pipeline():
        """Load the pipeline once and cache it"""
        return AccentDetectionPipeline()

    # Initialize pipeline
    pipeline = load_pipeline()
    pipeline_available = True

except Exception as e:
    st.error(f"Failed to load AI models: {str(e)}")
    st.error("This might be due to memory limitations on Streamlit Cloud.")
    st.info("Please try running this app locally for full functionality.")
    pipeline = None
    pipeline_available = False


def main():
    st.set_page_config(page_title="Accent Detection Demo", page_icon="🎙️", layout="wide")

    st.title("🎙️ Accent Detection Demo")
    st.markdown("**Upload a video URL to detect English accents using AI**")

    # Show status
    if pipeline_available:
        st.success("🟢 AI models loaded successfully!")
    else:
        st.warning("⚠️ AI models not available - running in demo mode")

    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("This tool analyzes speech in videos to:")
        st.write("• Detect the language being spoken")
        st.write("• Classify English accents")
        st.write("• Provide confidence scores")

        st.header("📝 Supported Formats")
        st.write("• Direct MP4 links")
        st.write("• Loom videos")
        st.write("• YouTube (some)")
        st.write("• Other public video URLs")

        if not pipeline_available:
            st.header("⚠️ Notice")
            st.write(
                "The AI models couldn't load due to Streamlit Cloud memory limits."
            )
            st.write("For full functionality, run this app locally.")

    # Main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        video_url = st.text_input(
            "Video URL",
            placeholder="https://example.com/video.mp4",
            help="Enter a direct link to a video file",
        )

        # Example URLs for testing
        st.markdown("**Example URLs to try:**")
        example_urls = [
            "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4",
            "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        ]

        for i, url in enumerate(example_urls):
            if st.button(f"Use Example {i+1}", key=f"example_{i}"):
                st.session_state.video_url = url
                st.rerun()

    with col2:
        st.markdown("### 🚀 Process Video")
        if pipeline_available:
            process_btn = st.button(
                "🔍 Analyze Accent", type="primary", use_container_width=True
            )
        else:
            process_btn = st.button(
                "🔍 Demo Mode",
                type="secondary",
                use_container_width=True,
                help="AI models not loaded - showing demo results",
            )

    # Get URL from session state if set by example button
    if hasattr(st.session_state, "video_url"):
        video_url = st.session_state.video_url

    if process_btn:
        if not video_url:
            st.error("⚠️ Please enter a valid video URL.")
        else:
            if pipeline_available:
                # Real processing
                with st.spinner("🔄 Processing video... This may take a few minutes."):
                    try:
                        result = pipeline.process(video_url)
                        display_results(result)
                    except Exception as e:
                        st.error(f"❌ Processing failed: {str(e)}")
                        st.error("This might be due to memory or resource limitations.")
            else:
                # Demo mode
                with st.spinner("🔄 Running in demo mode..."):
                    import time

                    time.sleep(2)  # Simulate processing

                    # Show demo results
                    demo_result = {
                        "status": "demo",
                        "language": "en",
                        "language_confidence": 0.95,
                        "accent": "American",
                        "accent_confidence": 0.82,
                        "accent_confidence_percentage": 82.0,
                        "summary": "Demo result - AI models not loaded on Streamlit Cloud",
                    }
                    display_results(demo_result)


def display_results(result):
    """Display processing results"""
    if result.get("status") in ["success", "demo"]:
        if result.get("status") == "demo":
            st.info("🎭 Demo Results (AI models not loaded)")
        else:
            st.success("✅ Processing completed!")

        col1, col2, col3 = st.columns(3)

        with col1:
            language = result.get("language", "Unknown")
            lang_conf = result.get("language_confidence", 0)
            st.metric(
                "Language",
                language.upper() if language else "Unknown",
                f"{lang_conf:.1%} confidence" if lang_conf else "No confidence data",
            )

        with col2:
            accent = result.get("accent")
            accent_conf = result.get("accent_confidence_percentage", 0)
            if accent:
                st.metric(
                    "Accent",
                    accent,
                    (
                        f"{accent_conf:.1f}% confidence"
                        if accent_conf
                        else "No confidence data"
                    ),
                )
            else:
                st.metric("Accent", "Not detected", "N/A")

        with col3:
            status_emoji = "🎭" if result.get("status") == "demo" else "🟢"
            status_text = "Demo" if result.get("status") == "demo" else "Success"
            st.metric("Status", f"{status_emoji} {status_text}")

        # Summary
        summary = result.get("summary", "Processing completed")
        if summary:
            st.info(f"**Summary:** {summary}")

    else:
        # Handle error status
        st.error("❌ Processing failed!")
        error_msg = result.get("message", "Unknown error occurred")
        st.error(f"**Error:** {error_msg}")
        st.metric("Status", "🔴 Error")

    # Full response details
    with st.expander("📊 View Full Response"):
        st.json(result)


if __name__ == "__main__":
    main()
