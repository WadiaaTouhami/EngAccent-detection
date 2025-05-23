import requests
from moviepy.editor import VideoFileClip
import os


def download_video(url: str, output_path: str) -> bool:
    """Download a video from a URL to a local file"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        print(f"Starting download from: {url}")
        resp = requests.get(url, stream=True, timeout=60, headers=headers)
        resp.raise_for_status()

        total_size = 0
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    total_size += len(chunk)

        # Verify file was downloaded
        if os.path.getsize(output_path) == 0:
            print("Downloaded file is empty")
            return False

        print(f"Download completed: {total_size / (1024*1024):.1f} MB")
        return True

    except Exception as e:
        print(f"Download error: {e}")
        return False


def extract_audio(video_path: str, audio_path: str) -> bool:
    """Extract audio track from a video file"""
    clip = None
    try:
        print(f"Loading video: {video_path}")
        clip = VideoFileClip(video_path)

        if clip.audio is None:
            print("No audio track found in video")
            return False

        print(f"Video duration: {clip.duration:.1f} seconds")
        print(f"Audio duration: {clip.audio.duration:.1f} seconds")

        # Extract audio with specific parameters that match Whisper expectations
        print("Extracting audio...")
        clip.audio.write_audiofile(
            audio_path,
            logger=None,
            verbose=False,
            ffmpeg_params=[
                "-ar",
                "16000",  # 16kHz sample rate (Whisper default)
                "-ac",
                "1",  # Mono channel
                "-acodec",
                "pcm_s16le",  # 16-bit PCM
                "-f",
                "wav",  # WAV format
            ],
        )

        # Close the clip to release resources
        clip.close()
        clip = None

        # Add a small delay to ensure file is fully written
        import time

        time.sleep(1.0)

        # Verify the extracted audio file
        if not os.path.exists(audio_path):
            print("Audio file was not created")
            return False

        audio_size = os.path.getsize(audio_path)
        if audio_size < 1000:  # Less than 1KB
            print(f"Audio file too small: {audio_size} bytes")
            return False

        print(f"Audio extracted successfully: {audio_size / 1024:.1f} KB")

        # Test that we can actually read the file
        try:
            with open(audio_path, "rb") as f:
                f.read(100)  # Try to read first 100 bytes
            print("Audio file is readable")
        except Exception as e:
            print(f"Audio file is not readable: {e}")
            return False

        return True

    except Exception as e:
        print(f"Audio extraction error: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        if clip:
            try:
                clip.close()
            except:
                pass
