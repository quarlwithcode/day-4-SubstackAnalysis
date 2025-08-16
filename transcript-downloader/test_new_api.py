#!/usr/bin/env python3
"""Test with new API version"""

from youtube_transcript_api import YouTubeTranscriptApi
import json

video_id = "ZdO00Y-u1y0"
print(f"Testing video ID: {video_id}")
print(f"youtube-transcript-api version: {YouTubeTranscriptApi.__version__ if hasattr(YouTubeTranscriptApi, '__version__') else 'Unknown'}")

# Check available methods
print("\nAvailable methods in YouTubeTranscriptApi:")
for method in dir(YouTubeTranscriptApi):
    if not method.startswith('_'):
        print(f"  - {method}")

try:
    # Try the simple get_transcript method
    print("\n1. Trying get_transcript()...")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(f"✅ Success! Got {len(transcript)} segments")
    print(f"First segment: {transcript[0]['text'][:100]}...")
    
except Exception as e:
    print(f"❌ Failed: {e}")
    
    # Try with language codes
    print("\n2. Trying with language codes...")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        print(f"✅ Success! Got {len(transcript)} segments")
        print(f"First segment: {transcript[0]['text'][:100]}...")
    except Exception as e2:
        print(f"❌ Failed: {e2}")
        
        # Check if there's a get_transcripts method
        if hasattr(YouTubeTranscriptApi, 'get_transcripts'):
            print("\n3. Trying get_transcripts()...")
            try:
                transcripts = YouTubeTranscriptApi.get_transcripts([video_id])
                print(f"✅ Got transcripts: {transcripts}")
            except Exception as e3:
                print(f"❌ Failed: {e3}")