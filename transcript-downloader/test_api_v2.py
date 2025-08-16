#!/usr/bin/env python3
"""Test with new API version 1.2.2"""

from youtube_transcript_api import YouTubeTranscriptApi

video_id = "ZdO00Y-u1y0"
print(f"Testing video ID: {video_id}")

try:
    # The new API uses fetch() method
    print("\n1. Trying YouTubeTranscriptApi.fetch()...")
    result = YouTubeTranscriptApi.fetch(video_id)
    print(f"Result type: {type(result)}")
    
    if isinstance(result, dict):
        print(f"Result keys: {result.keys()}")
        for key, value in result.items():
            print(f"  {key}: {type(value)} - {len(value) if hasattr(value, '__len__') else 'N/A'} items")
            if isinstance(value, list) and len(value) > 0:
                print(f"    First item: {value[0]}")
    elif isinstance(result, list):
        print(f"✅ Got {len(result)} segments")
        if len(result) > 0:
            print(f"First segment: {result[0]}")
            
            # Get full text
            full_text = ' '.join([s['text'] for s in result])
            word_count = len(full_text.split())
            print(f"\nTotal words: {word_count}")
            print(f"First 200 chars: {full_text[:200]}...")
    
except Exception as e:
    print(f"❌ fetch() failed: {e}")
    print(f"   Error type: {type(e).__name__}")

# Try list() method
print("\n2. Trying YouTubeTranscriptApi.list()...")
try:
    transcripts = YouTubeTranscriptApi.list(video_id)
    print(f"Result type: {type(transcripts)}")
    
    # Iterate through available transcripts
    for transcript in transcripts:
        print(f"  Found transcript: {transcript}")
        if hasattr(transcript, 'language'):
            print(f"    Language: {transcript.language}")
        if hasattr(transcript, 'language_code'):
            print(f"    Code: {transcript.language_code}")
        if hasattr(transcript, 'is_generated'):
            print(f"    Auto-generated: {transcript.is_generated}")
            
        # Try to fetch this transcript
        if hasattr(transcript, 'fetch'):
            try:
                print(f"    Fetching transcript...")
                data = transcript.fetch()
                print(f"    ✅ Got {len(data)} segments")
                break
            except Exception as fe:
                print(f"    ❌ Fetch failed: {fe}")
                
except Exception as e:
    print(f"❌ list() failed: {e}")