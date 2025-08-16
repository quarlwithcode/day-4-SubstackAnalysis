#!/usr/bin/env python3
"""Check the actual import structure"""

import youtube_transcript_api
print("Module contents:")
print(dir(youtube_transcript_api))

# Check for the main class
if hasattr(youtube_transcript_api, 'YouTubeTranscriptApi'):
    api = youtube_transcript_api.YouTubeTranscriptApi
    print("\nYouTubeTranscriptApi methods:")
    for method in dir(api):
        if not method.startswith('_'):
            print(f"  - {method}")
            
# Check if it's an instance or needs instantiation
print("\nTrying to use the API...")

video_id = "ZdO00Y-u1y0"

# Try method 1: Direct use
try:
    print("\n1. Direct use of fetch:")
    api_instance = youtube_transcript_api.YouTubeTranscriptApi()
    result = api_instance.fetch(video_id)
    print(f"  Success! Got: {type(result)}")
except Exception as e:
    print(f"  Failed: {e}")

# Try method 2: Class method
try:
    print("\n2. Using as class method:")
    result = youtube_transcript_api.YouTubeTranscriptApi.fetch(video_id)
    print(f"  Success! Got: {type(result)}")
except Exception as e:
    print(f"  Failed: {e}")
    
# Try method 3: Look for other functions
try:
    print("\n3. Looking for standalone functions:")
    if hasattr(youtube_transcript_api, 'get_transcript'):
        print("  Found get_transcript!")
        result = youtube_transcript_api.get_transcript(video_id)
        print(f"  Success! Got: {type(result)}")
except Exception as e:
    print(f"  Failed: {e}")