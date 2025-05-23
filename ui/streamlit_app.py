import streamlit as st
import requests
import json
import os

# For Streamlit Cloud deployment, we need to handle the API differently
# Since we can't run the FastAPI server separately on Streamlit Cloud,
# we'll import the pipeline directly

try:
    # Try to use the API if it's available (local development)
    API_URL = "http://localhost:8000"
    health_resp = requests.get(f"{API_URL}/health", timeout=2)
    USE_API = health_resp.status_code == 200
except:
    # Use direct pipeline import for Streamlit Cloud
    USE_API = False

if not USE_API:
    # Import pipeline directly for Streamlit Cloud
    try:
        from app.pipeline import AccentDetectionPipeline

        @st.cache_resource
        def load_pipeline():
            return AccentDetectionPipeline()

        pipeline = load_pipeline()
    except Exception as e:
        st.error(f"Failed to load pipeline: {e}")
        pipeline = None


def process_with_api(video_url):
    """Process using FastAPI (local development)"""
    resp = requests.post(
        f"{API_URL}/process",
        json={"video_url": video_url},
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()


def process_with_pipeline(video_url):
    """Process using direct pipeline (Streamlit Cloud)"""
    if pipeline is None:
        return {"status": "error", "message": "Pipeline not loaded"}
    return pipeline.process(video_url)


def main():
    st.set_page_config(page_title="Accent Detection Demo", page_icon="🎙️", layout="wide")

    st.title("🎙️ Accent Detection Demo")
    st.markdown("**Upload a video URL to detect English accents using AI**")

    # Show deployment info
    if USE_API:
        st.info("🟢 Running in local development mode with API")
    else:
        st.info("☁️ Running on Streamlit Cloud with direct pipeline")

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
            "https://rr5---sn-4g5ednz7.googlevideo.com/videoplayback?expire=1748032642&ei=IogwaK_4Abvz6dsPn7-hkAg&ip=128.79.11.77&id=o-AFisAs-5m_5A5BXF8hrc3BgKtF_ZPq-EbuNlqZ2YZMIj&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ==&gcr=fr&bui=AecWEAZhSSUI7sX9J3cmTkISXI0WQy5EvLeUP5O7eITfsRPXrNdv7dYSOzZcnWyZYlPqKlc-z5kCDTb8&vprv=1&svpuc=1&mime=video/mp4&ns=fK-mXJ7JyoQ76noBgFIrSH4Q&rqh=1&gir=yes&clen=2862944&ratebypass=yes&dur=38.656&lmt=1748007128017237&lmw=1&c=TVHTML5&sefc=1&txp=5430534&n=7q_iuEsLXZ2MFA&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,gcr,bui,vprv,svpuc,mime,ns,rqh,gir,clen,ratebypass,dur,lmt&sig=AJfQdSswRQIgcDxqKDG9Obv0itsyH904K2FV_G9bvXiehDgMIJpGxxsCIQDiJ9V-y_miSlvqI1sayCX_jRdiqt7flOJJVPp4BumXmg==&from_cache=False&title=Australian%20MP%20ends%20final%20day%20speech%20with%20a%20%27shoey%27%20|%20ITV%20News&redirect_counter=1&cm2rm=sn-hgnlr7s&rrc=80&fexp=24350590,24350737,24350827,24350961,24351173,24351177,24351495,24351528,24351594,24351638,24351658,24351661,24351759,24351789,24351864,24351907,24352018,24352019&req_id=2a4608dbfd69a3ee&cms_redirect=yes&cmsv=e&met=1748011050,&mh=Jy&mip=194.214.61.51&mm=34&mn=sn-4g5ednz7&ms=ltu&mt=1748009973&mv=u&mvi=5&pl=22&rms=ltu,au&lsparams=met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=ACuhMU0wRQIgJOwO7hQQgdMvmtGytlJFx26u4sufXuQqu9qtnQVERygCIQCteCWfN_xBerFNJqli_IgzRqi_VMrz3iWcNZRf1Hy_HA%3D%3D",
        ]

        for i, url in enumerate(example_urls):
            if st.button(f"Use Example {i+1}", key=f"example_{i}"):
                st.session_state.video_url = url
                st.rerun()

    with col2:
        st.markdown("### 🚀 Process Video")
        process_btn = st.button(
            "🔍 Analyze Accent", type="primary", use_container_width=True
        )

    # Get URL from session state if set by example button
    if hasattr(st.session_state, "video_url"):
        video_url = st.session_state.video_url

    if process_btn:
        if not video_url:
            st.error("⚠️ Please enter a valid video URL.")
        else:
            with st.spinner("🔄 Processing video... This may take a few minutes."):
                try:
                    # Choose processing method based on environment
                    if USE_API:
                        data = process_with_api(video_url)
                    else:
                        data = process_with_pipeline(video_url)

                    # Display results based on response
                    if data.get("status") == "success":
                        st.success("✅ Processing completed!")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            language = data.get("language", "Unknown")
                            lang_conf = data.get("language_confidence", 0)
                            st.metric(
                                "Language",
                                language.upper() if language else "Unknown",
                                (
                                    f"{lang_conf:.1%} confidence"
                                    if lang_conf
                                    else "No confidence data"
                                ),
                            )

                        with col2:
                            accent = data.get("accent")
                            accent_conf = data.get("accent_confidence_percentage", 0)
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
                            st.metric("Status", "🟢 Success")

                        # Summary
                        summary = data.get("summary", "Processing completed")
                        if summary:
                            st.info(f"**Summary:** {summary}")

                    else:
                        # Handle error status
                        st.error("❌ Processing failed!")
                        error_msg = data.get("message", "Unknown error occurred")
                        st.error(f"**Error:** {error_msg}")

                        # Show status if available
                        status = data.get("status", "error")
                        st.metric("Status", f"🔴 {status.title()}")

                    # Full response details
                    with st.expander("📊 View Full Response"):
                        st.json(data)

                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ Cannot connect to API server. Running in direct mode..."
                    )
                    # Fallback to direct processing
                    try:
                        data = process_with_pipeline(video_url)
                        # Display results (same code as above)
                    except Exception as e:
                        st.error(f"❌ Processing failed: {str(e)}")

                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    st.error("Please check the console logs for more details.")


if __name__ == "__main__":
    main()
