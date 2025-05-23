# Save this as test_final.py
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.getcwd())

from app.pipeline import AccentDetectionPipeline


def test_pipeline():
    print("=" * 60)
    print("TESTING ACCENT DETECTION PIPELINE")
    print("=" * 60)

    try:
        # Initialize pipeline
        print("1. Initializing pipeline...")
        pipeline = AccentDetectionPipeline(whisper_model_size="base")
        print("✓ Pipeline initialized successfully!")

        # Test with a known working video URL
        test_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"

        print(f"\n2. Testing with URL: {test_url}")
        print("This may take a few minutes...")

        # Process the video
        result = pipeline.process(test_url)

        print("\n" + "=" * 60)
        print("FINAL RESULT:")
        print("=" * 60)

        for key, value in result.items():
            print(f"{key:25}: {value}")

        print("=" * 60)

        # Check if it was successful
        if result.get("status") == "success":
            print("🎉 SUCCESS! The pipeline is working correctly!")
            print(f"✓ Language: {result.get('language')}")
            print(
                f"✓ Accent: {result.get('accent')} ({result.get('accent_confidence_percentage')}% confidence)"
            )
        else:
            print("❌ FAILED!")
            print(f"Error: {result.get('message')}")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_pipeline()
