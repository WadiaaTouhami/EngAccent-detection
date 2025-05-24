import streamlit as st
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# Global variables to store the pipeline loading result
pipeline = None
pipeline_available = False
pipeline_error = None

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
    # Store the error but don't display it yet - wait for main()
    pipeline_error = str(e)
    pipeline = None
    pipeline_available = False


def main():
    # This MUST be the first Streamlit command
    st.set_page_config(page_title="Accent Detection Demo", page_icon="🎙️", layout="wide")

    st.title("🎙️ Accent Detection Demo")
    st.markdown("**Upload a video URL to detect English accents using AI**")

    # Now handle the pipeline loading status
    if pipeline_available:
        st.success("🟢 AI models loaded successfully!")
    else:
        st.error(f"Failed to load AI models: {pipeline_error}")
        st.error("This might be due to memory limitations on Streamlit Cloud.")
        st.info("Please try running this app locally for full functionality.")

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
            "https://rr7---sn-n4g-jqbe6.googlevideo.com/videoplayback?expire=1748105856&ei=IKYxaLrPArr4xN8P18HLuQg&ip=88.167.83.136&id=o-AEBvcxPBenUVwbyT7S72CH9EzbFOrRsyhw-ABzXnDbq8&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ==&rms=au,au&bui=AecWEAZ0OaGgAF5MxE7jAwNqL9kY0nCxFeapMPKO1oq3h6E9xXz2dveX7N9nNomfDgIZeIkzcAfr4LQW&vprv=1&svpuc=1&mime=video/mp4&ns=9zGDYZkvzUx5kYAa8N_8cIAQ&rqh=1&gir=yes&clen=1714582&ratebypass=yes&dur=45.139&lmt=1747060668915302&lmw=1&c=TVHTML5&sefc=1&txp=6300224&n=m89ssEsh_rwCbw&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,bui,vprv,svpuc,mime,ns,rqh,gir,clen,ratebypass,dur,lmt&sig=AJfQdSswRAIgAJinNQpTDUZqRVGMPekMmLNd8_uo6eI7zrxLci7ESRgCIDLqmiiXTqZ2-9odbukpAnR9vb45vBolhUXS7G-u4_mc&from_cache=False&title=Why%20we%20need%20to%20take%20back%20control%20of%20our%20borders:%20Prime%20Minister%20Keir%20Starmer%20explains&redirect_counter=1&rm=sn-25gkz76&rrc=104&fexp=24350590,24350737,24350827,24350961,24351173,24351177,24351495,24351528,24351594,24351638,24351658,24351662,24351759,24351790,24351864,24351907,24352018,24352020&req_id=5010a7dd14eba3ee&cms_redirect=yes&cmsv=e&ipbypass=yes&met=1748084264,&mh=Ah&mip=78.122.101.79&mm=31&mn=sn-n4g-jqbe6&ms=au&mt=1748083997&mv=m&mvi=7&pl=22&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=ACuhMU0wRgIhAK4nsY2Kha5TBulunM6i_JE8js22VOcePttS96U2-32eAiEAqO8G90SDrZovg21syNfNUxoOBeHHxh1fJp59sXieFqs%3D",
            "https://rr1---sn-25ge7nz6.googlevideo.com/videoplayback?expire=1748104701&ei=naExaNjEEqaJvdIP1JfKuAs&ip=2a01:e0a:2bf:24a0:2215:deff:fe87:a84c&id=o-ANfNELlaSQVwY3GSsGJBiTy9Bs5ZkkuZM8lV5trLJBgd&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ==&rms=au,au&gcr=fr&bui=AecWEAa2RX93ap-5GS6kaxejUu746R0IwMBj8zW9IBcELYMC4xSiQUMlX26ekBgEG-B1fvork-3XAvNh&vprv=1&svpuc=1&mime=video/mp4&ns=_hiL9sldH7KGrif_R5HckxgQ&rqh=1&gir=yes&clen=2862944&ratebypass=yes&dur=38.656&lmt=1748007128017237&lmw=1&c=TVHTML5&sefc=1&txp=5430534&n=p8kYtLOYt97SmA&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,gcr,bui,vprv,svpuc,mime,ns,rqh,gir,clen,ratebypass,dur,lmt&sig=AJfQdSswRQIhAMDad8pkcvG5zC9p_Rxbn_IQgRMzSV986sbWEeU6nvQQAiADozOV0HfDXxd13RGOHF-xIjSPaxyNHpGJAMKOwxqm-w==&from_cache=True&title=Australian%20MP%20ends%20final%20day%20speech%20with%20a%20%27shoey%27%20|%20ITV%20News&redirect_counter=1&rm=sn-25grk7e&rrc=104&fexp=24350590,24350737,24350827,24350961,24351173,24351177,24351495,24351528,24351594,24351638,24351658,24351662,24351759,24351789,24351864,24351907,24352011,24352018,24352019,24352021&req_id=cde353b8b922a3ee&cms_redirect=yes&cmsv=e&ipbypass=yes&met=1748083159,&mh=Jy&mip=78.122.101.79&mm=31&mn=sn-25ge7nz6&ms=au&mt=1748082796&mv=m&mvi=1&pl=22&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=ACuhMU0wRQIgMf7CrMQQnDg-13ONHt0fCBVfCmrlr6VW8WnG0EjbzdECIQDJFUSL1vV-0KBPvubTi7spzAkD46PsIfpBIk_BaMT5iw%3D%3D",
            "https://rr1---sn-25ge7nzs.googlevideo.com/videoplayback?expire=1748105229&ei=raMxaLS5NLaIvdIPnp_1-Ao&ip=176.165.28.99&id=o-ALN_86rmK0j-x-WQfXWJEkNZ0vOsMq0nG_GlJlI-lfJ7&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ==&bui=AecWEAbl02pwi_52YxaGdv1OEugQooqJbniQVrb30uZzZKl7cNx5cSmVmy2CPijfQ7Um2jVA35bP2azv&vprv=1&svpuc=1&mime=video/mp4&ns=LQcfmM8W15INFOnNpGC8RtgQ&rqh=1&gir=yes&clen=2041990&ratebypass=yes&dur=27.477&lmt=1747315492792182&lmw=1&c=TVHTML5&sefc=1&txp=5430534&n=KveOTRec6HqH2w&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,bui,vprv,svpuc,mime,ns,rqh,gir,clen,ratebypass,dur,lmt&sig=AJfQdSswRAIgHUGPsc4PHkI0RNFNowP10glJfxtRukHHWPOijUvB5BwCIGUgtVMMfo_P7iw3F2DVv7QN4O-tfY1x_m8c7LLoK32a&from_cache=True&title=Trump%20says%20US-Iran%20%27very%20close%27%20to%20nuclear%20deal&rm=sn-cv0tb0xn-jqbr7e,sn-25gkr7e&rrc=79,104,80&fexp=24350590,24350737,24350827,24350961,24351173,24351177,24351495,24351528,24351594,24351638,24351658,24351661,24351662,24351759,24351789,24351864,24351907,24352015,24352018,24352019&req_id=5e4b7d9b23d1a3ee&ipbypass=yes&redirect_counter=3&cm2rm=sn-n4g-jqber7l&cms_redirect=yes&cmsv=e&met=1748083763,&mh=FO&mip=78.122.101.79&mm=30&mn=sn-25ge7nzs&ms=nxu&mt=1748083474&mv=m&mvi=1&pl=22&rms=nxu,au&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=ACuhMU0wRQIgVsU1iNL9hq4kIxh9VpUxEMW9HcPyzzibXAHYfy8M3J8CIQDdS4dE0zSIXRTdj9-Wjjuqvcvo30CmRWy-28mo-4Tf7Q%3D%3D",
            "https://rr2---sn-25ge7nzr.googlevideo.com/videoplayback?expire=1748106887&ei=J6oxaNG8Ie74xN8PpdTJyQQ&ip=37.65.50.6&id=o-AOkqlFjNzgLMod5kMPZDpw6qcPckk9-Jhft9YUQHHX1p&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ==&bui=AecWEAb-vm9NFa092YZgQxQIpM5QIJXf7AbtdaVouKUN9a5sxHch9njk-fFDh-Zp4KQ0IM9DAydMRVLo&vprv=1&svpuc=1&mime=video/mp4&ns=G6ASvYFYaesLSI_6G_L4Rc0Q&rqh=1&gir=yes&clen=4009337&ratebypass=yes&dur=53.717&lmt=1747883482056817&lmw=1&fexp=24350590,24350737,24350827,24350961,24351173,24351177,24351495,24351528,24351594,24351598,24351638,24351658,24351661,24351662,24351759,24351789,24351864,24351907,24352018,24352020,51466643&c=TVHTML5&sefc=1&txp=5430534&n=wJGabqOzkvZ-dQ&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,bui,vprv,svpuc,mime,ns,rqh,gir,clen,ratebypass,dur,lmt&sig=AJfQdSswRAIgRLxSiPlgZR05Ctyat46P0LgcBlmdWXGTcQ_AYaUAzGUCIDlaJSmz4CmM_OeWgTe1idRDy1OGU2xCU5wNM22pQotG&from_cache=True&title=South%20Africa%20President%20Calls%20Meeting%20With%20Trump%20%27A%20Great%20Success%27&rm=sn-n4g-nmcd7s,sn-25gr67l&rrc=79,80,104&req_id=8fd8f8f15fbaa3ee&cm2rm=sn-n4g-jqber7s&rms=nxu,au&redirect_counter=3&cms_redirect=yes&cmsv=e&ipbypass=yes&met=1748085327,&mh=3X&mip=78.122.101.79&mm=30&mn=sn-25ge7nzr&ms=nxu&mt=1748084915&mv=m&mvi=2&pl=22&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=ACuhMU0wRQIhANIIyBrYcMSa1VFHJBon7zw31nv3TQXsE-5xGU2za8pdAiBvogLNEZ6iFblT57Rw44uL9w7vKN_qP3xhIcL4LNnYFw%3D%3D",
            "https://rr5---sn-n4g-jqbe6.googlevideo.com/videoplayback?expire=1748107276&ei=rKsxaNfrK-rZxN8Pmva_8AU&ip=86.235.220.209&id=o-APkAmHdsNoOwBLTV_iFytf8ij0LUDNFfKtGKRnu5gb2A&itag=18&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ==&rms=au,au&bui=AecWEAZT3YCN0lmczoVE8CUYeifCN1KvzUlUrYJvUWirICTkKdNdV79ygcwf4VAs5O5cjkibthClPqM5&vprv=1&svpuc=1&mime=video/mp4&ns=rJy1p0ZRZh5falRvzaYAGSsQ&rqh=1&gir=yes&clen=3694190&ratebypass=yes&dur=49.408&lmt=1747517926224429&lmw=1&fexp=24350590,24350737,24350827,24350961,24351064,24351173,24351177,24351495,24351528,24351594,24351638,24351658,24351661,24351759,24351790,24351864,24351907,24352018,24352020,24352099,51466642&c=TVHTML5&sefc=1&txp=5430534&n=HNlOyJkfGFixyw&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,bui,vprv,svpuc,mime,ns,rqh,gir,clen,ratebypass,dur,lmt&sig=AJfQdSswRQIgOu-apT2tmlQKLi2lAtls5N1Lm3YDeVS9TZtjWLG_cHoCIQCAGgcS29pXz8rPBC4zUpDE-YozQGYgTKkrlCxO3n5fIA==&from_cache=True&title=French%20President%20Macron%20calls%20Israeli%20PM%27s%20Gaza%20measures%20a%20%22disgrace%22%20|%20DW%20News&redirect_counter=1&rm=sn-25grl76&rrc=104&req_id=688ac9535ddfa3ee&cms_redirect=yes&cmsv=e&ipbypass=yes&met=1748085725,&mh=cg&mip=78.122.101.79&mm=31&mn=sn-n4g-jqbe6&ms=au&mt=1748085443&mv=m&mvi=5&pl=22&lsparams=ipbypass,met,mh,mip,mm,mn,ms,mv,mvi,pl,rms&lsig=ACuhMU0wRQIgOlGmqMzv9wLArH2wjpdM13-mpX1_JdDfh4xVdwi1fiICIQDtb7henUIxR5toWUuAA4Raqlw6nAo1reyi5W3znTKUbw%3D%3D",
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
