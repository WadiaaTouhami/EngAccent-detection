# Force HF Hub to copy instead of symlinking on Windows
import os

os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
os.environ["HF_HUB_CACHE"] = os.path.abspath("./hf_cache")

import tempfile
import traceback
import whisper
from speechbrain.inference import EncoderClassifier
from .utils import download_video, extract_audio
import shutil
from pathlib import Path


class AccentDetectionPipeline:
    def __init__(
        self, whisper_model_size: str = "base"
    ):  # Changed from "tiny" to "base"
        """Initialize and load models once"""
        # Whisper for language detection
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model(whisper_model_size)
        print("✓ Whisper loaded")

        # SpeechBrain for accent classification
        print("Loading SpeechBrain accent classifier...")
        self._load_accent_classifier()
        print("✓ Accent classifier loaded")

        # Label mapping
        self.accent_mapping = {
            "us": "American",
            "england": "British",
            "australia": "Australian",
            "indian": "Indian",
            "canada": "Canadian",
            "bermuda": "Bermudian",
            "scotland": "Scottish",
            "african": "African",
            "ireland": "Irish",
            "newzealand": "New Zealand",
            "wales": "Welsh",
            "malaysia": "Malaysian",
            "philippines": "Filipino",
            "singapore": "Singaporean",
            "hongkong": "Hong Kong",
            "southatlandtic": "South Atlantic",
        }

    def _load_accent_classifier(self):
        """Load accent classifier with Windows-compatible fallback"""
        model_dir = Path("./pretrained_models/accent_ecapa")

        # Try loading from local directory first (if exists)
        if model_dir.exists() and any(model_dir.iterdir()):
            try:
                print("Loading from existing local directory...")
                self.accent_classifier = EncoderClassifier.from_hparams(
                    source=str(model_dir),
                    savedir=str(model_dir),
                )
                return
            except Exception as e:
                print(f"Local loading failed: {e}")

        # Try direct download with temp directory
        try:
            print("Attempting direct download...")
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_model_dir = Path(temp_dir) / "temp_model"

                # Download to temporary directory
                self.accent_classifier = EncoderClassifier.from_hparams(
                    source="Jzuluaga/accent-id-commonaccent_ecapa",
                    savedir=str(temp_model_dir),
                )

                # Copy from temp to permanent location
                model_dir.parent.mkdir(parents=True, exist_ok=True)
                if model_dir.exists():
                    shutil.rmtree(model_dir)
                shutil.copytree(temp_model_dir, model_dir)

                print("✓ Model downloaded and copied successfully")
                return

        except Exception as e:
            print(f"Direct download failed: {e}")

        # Final fallback: Use HuggingFace Hub directly
        try:
            from huggingface_hub import snapshot_download

            print("Trying HuggingFace Hub direct download...")

            # Download model files manually
            repo_path = snapshot_download(
                repo_id="Jzuluaga/accent-id-commonaccent_ecapa", cache_dir="./hf_cache"
            )

            # Copy to our model directory
            model_dir.parent.mkdir(parents=True, exist_ok=True)
            if model_dir.exists():
                shutil.rmtree(model_dir)
            shutil.copytree(repo_path, model_dir)

            # Load the classifier from copied files
            self.accent_classifier = EncoderClassifier.from_hparams(
                source=str(model_dir),
                savedir=str(model_dir),
            )
            print("✓ Successfully loaded via HuggingFace Hub")

        except Exception as e:
            print(f"HuggingFace Hub download failed: {e}")
            print(f"Full error: {traceback.format_exc()}")

            # Last resort: try simple loading
            try:
                print("Trying simple model loading...")
                self.accent_classifier = EncoderClassifier.from_hparams(
                    source="Jzuluaga/accent-id-commonaccent_ecapa",
                    savedir="./pretrained_models/accent_ecapa",
                )
                print("✓ Simple loading succeeded")
            except Exception as final_e:
                print(f"Simple loading also failed: {final_e}")
                raise RuntimeError(
                    f"Failed to load accent classifier after all attempts. "
                    f"Last error: {final_e}. "
                    f"Try running as administrator or enable Windows Developer Mode."
                )

    def process(self, video_url: str) -> dict:
        """End-to-end processing: download -> extract -> detect -> classify"""
        result = {
            "status": "error",
            "video_url": video_url,
            "language": None,
            "language_confidence": 0.0,
            "accent": None,
            "accent_confidence": 0.0,
            "accent_confidence_percentage": 0.0,
            "message": "",
            "summary": "",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, "video.mp4")
            audio_path = os.path.join(tmpdir, "audio.wav")
            audio_backup_path = os.path.join(tmpdir, "audio_backup.wav")  # Backup copy

            try:
                # Download video
                print(f"Downloading video from: {video_url}")
                if not download_video(video_url, video_path):
                    result.update(
                        message="Video download failed. Check URL or free up disk space."
                    )
                    return result

                # Check video file size
                video_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                print(f"✓ Video downloaded ({video_size:.1f} MB)")

                # Extract audio
                print("Extracting audio...")
                if not extract_audio(video_path, audio_path):
                    result.update(
                        message="Audio extraction failed. Video may be corrupted."
                    )
                    return result

                # Check audio file size and properties
                if not os.path.exists(audio_path):
                    result.update(message="Audio file not created")
                    return result

                audio_size = os.path.getsize(audio_path) / (1024 * 1024)  # MB
                print(f"✓ Audio extracted ({audio_size:.1f} MB)")

                if audio_size < 0.01:  # Less than 10KB
                    result.update(
                        message="Audio file too small - may be silent or corrupted"
                    )
                    return result

                # Language detection with enhanced debugging
                print("Detecting language...")
                lang, lang_prob, all_probs = self._detect_language_detailed(audio_path)
                result["language"], result["language_confidence"] = lang, lang_prob

                print(f"✓ Language detection results:")
                print(f"  - Top language: {lang} ({lang_prob:.3f})")
                print(
                    f"  - All probabilities: {dict(list(all_probs.items())[:5])}"
                )  # Top 5

                # If language detection fails, try to force English detection
                if lang == "unknown" or lang_prob < 0.1:
                    print(
                        "⚠️ Language detection uncertain, trying forced English detection..."
                    )
                    # Try to detect anyway and see if it's reasonable English
                    accent_info = self._detect_accent(audio_path)
                    if accent_info["score"] > 0.3:  # Reasonable confidence
                        print("✓ Accent detection suggests this might be English")
                        result.update(
                            status="success",
                            language="en",
                            language_confidence=0.5,  # Moderate confidence
                            accent=accent_info["name"],
                            accent_confidence=accent_info["score"],
                            accent_confidence_percentage=accent_info["percent"],
                            message="Language detection uncertain, but accent detected",
                            summary=f"Possibly {accent_info['name']} accent ({accent_info['percent']}% confidence) - language detection was uncertain",
                        )
                        return result

                if lang != "en":
                    result.update(
                        status="success",
                        message=f"Non-English audio detected: {lang}",
                        summary="Accent detection only works for English audio.",
                    )
                    return result

                # Accent detection
                print("Detecting accent...")
                accent_info = self._detect_accent(audio_path)
                result.update(
                    status="success",
                    accent=accent_info["name"],
                    accent_confidence=accent_info["score"],
                    accent_confidence_percentage=accent_info["percent"],
                    message="Processing completed successfully",
                    summary=f"Detected {accent_info['name']} accent with {accent_info['percent']}% confidence",
                )
                print(
                    f"✓ Accent detected: {accent_info['name']} ({accent_info['percent']}%)"
                )
                return result

            except Exception as e:
                print(f"Pipeline error: {e}")
                traceback.print_exc()
                result.update(message=f"Processing failed: {str(e)}")
                return result

    def _detect_language_detailed(self, audio_path: str) -> tuple[str, float, dict]:
        """Use Whisper to detect language with detailed output - Windows compatible"""
        try:
            # Windows-specific fix for Whisper audio loading
            import numpy as np
            
            print(f"Loading audio from: {audio_path}")
            print(f"File exists: {os.path.exists(audio_path)}")
            print(f"File size: {os.path.getsize(audio_path)} bytes")
            
            # Method 1: Use librosa instead of whisper.load_audio (more reliable on Windows)
            try:
                import librosa
                print("Trying librosa loading...")
                audio_data, sr = librosa.load(audio_path, sr=16000, mono=True)
                print(f"Librosa loaded: {len(audio_data)} samples at {sr}Hz")
                
                # Convert to the format Whisper expects
                if len(audio_data) == 0:
                    raise ValueError("Audio file is empty")
                    
                audio = audio_data.astype(np.float32)
                
            except Exception as librosa_error:
                print(f"Librosa failed: {librosa_error}")
                
                # Method 2: Copy file to a non-temp location first
                try:
                    print("Trying file copy method...")
                    import shutil
                    
                    # Create a copy in the current working directory
                    temp_audio = os.path.join(os.getcwd(), "temp_audio_whisper.wav")
                    shutil.copy2(audio_path, temp_audio)
                    
                    print(f"Copied to: {temp_audio}")
                    audio = whisper.load_audio(temp_audio)
                    
                    # Clean up
                    try:
                        os.remove(temp_audio)
                    except:
                        pass
                        
                except Exception as copy_error:
                    print(f"Copy method failed: {copy_error}")
                    
                    # Method 3: Use absolute path with forward slashes
                    try:
                        print("Trying absolute path conversion...")
                        abs_path = os.path.abspath(audio_path).replace('\\', '/')
                        print(f"Converted path: {abs_path}")
                        audio = whisper.load_audio(abs_path)
                        
                    except Exception as abs_error:
                        print(f"Absolute path method failed: {abs_error}")
                        raise Exception(f"All audio loading methods failed. Last error: {abs_error}")

            print(f"Audio loaded successfully: {len(audio)} samples = {len(audio)/16000:.1f} seconds")
            
            if len(audio) < 16000:  # Less than 1 second
                raise ValueError("Audio is too short for language detection")

            # Use the EXACT same approach as your working Colab code
            audio = whisper.pad_or_trim(audio)  # This is the default 30 seconds
            mel = whisper.log_mel_spectrogram(
                audio, n_mels=self.whisper_model.dims.n_mels
            ).to(self.whisper_model.device)

            # Get language probabilities
            _, probs = self.whisper_model.detect_language(mel)

            # Sort probabilities
            sorted_probs = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))

            # Get the most likely language
            lang = max(probs, key=probs.get)
            confidence = float(probs[lang])

            print(f"Raw Whisper output - Language: {lang}, Confidence: {confidence:.4f}")

            return lang, confidence, sorted_probs

        except Exception as e:
            print(f"Language detection error: {e}")
            import traceback
            traceback.print_exc()
            return "unknown", 0.0, {}

    def _detect_language(self, audio_path: str) -> tuple[str, float]:
        """Use Whisper to detect language"""
        lang, conf, _ = self._detect_language_detailed(audio_path)
        return lang, conf

    def _detect_accent(self, audio_path: str) -> dict:
        """Classify accent and map label - Windows compatible"""
        try:
            print(f"Detecting accent from: {audio_path}")
            
            # Try multiple approaches for Windows compatibility
            for attempt, path_to_try in enumerate([
                audio_path,  # Original path
                os.path.abspath(audio_path),  # Absolute path
                os.path.abspath(audio_path).replace('\\', '/'),  # Forward slashes
            ]):
                try:
                    print(f"Accent detection attempt {attempt + 1}: {path_to_try}")
                    
                    if not os.path.exists(path_to_try) and attempt == 0:
                        continue
                        
                    out_prob, score, index, labels = self.accent_classifier.classify_file(path_to_try)
                    
                    code = labels[0] if labels else "unknown"
                    score_val = float(score[0]) if score.numel() else 0.0
                    name = self.accent_mapping.get(code, code.title())
                    
                    print(f"✓ Accent detection successful: {name} ({score_val:.3f})")
                    
                    return {
                        "code": code,
                        "name": name,
                        "score": score_val,
                        "percent": round(score_val * 100, 1),
                    }
                    
                except Exception as e:
                    print(f"Accent detection attempt {attempt + 1} failed: {e}")
                    if attempt == 2:  # Last attempt
                        raise e
                    continue
                    
        except Exception as e:
            print(f"Accent detection error: {e}")
            import traceback
            traceback.print_exc()
            return {"code": "unknown", "name": "Unknown", "score": 0.0, "percent": 0.0}