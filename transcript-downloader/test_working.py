#!/usr/bin/env python3
"""Working test with new API"""

from youtube_transcript_api import YouTubeTranscriptApi

video_id = "ZdO00Y-u1y0"
print(f"Testing video ID: {video_id}")
print(f"URL: https://www.youtube.com/watch?v={video_id}")

try:
    # Create API instance
    api = YouTubeTranscriptApi()
    
    # Fetch transcript
    print("\nFetching transcript...")
    transcript = api.fetch(video_id)
    
    print(f"✅ Success!")
    print(f"   Type: {type(transcript)}")
    print(f"   Transcript segments: {len(transcript)}")
    
    # Get the actual text
    if len(transcript) > 0:
        print(f"\nFirst 3 segments:")
        for i, segment in enumerate(transcript[:3]):
            print(f"   {i+1}. {segment['text'][:100]}...")
        
        # Full text stats
        full_text = ' '.join([s['text'] for s in transcript])
        word_count = len(full_text.split())
        print(f"\nStats:")
        print(f"   Total segments: {len(transcript)}")
        print(f"   Total words: {word_count:,}")
        print(f"   First 300 chars: {full_text[:300]}...")
        
        # Save to test file
        print("\nSaving to test file...")
        with open('influencer-data/dan-koe-test.txt', 'w', encoding='utf-8') as f:
            f.write(f"Video: https://www.youtube.com/watch?v={video_id}\n")
            f.write(f"Words: {word_count}\n")
            f.write(f"Segments: {len(transcript)}\n")
            f.write("\n" + "="*50 + "\n\n")
            f.write(full_text)
        print("   Saved to influencer-data/dan-koe-test.txt")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Type: {type(e).__name__}")
    
    # Try listing transcripts
    print("\nTrying to list available transcripts...")
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        print(f"   Found transcripts: {transcript_list}")
        
        for transcript in transcript_list:
            print(f"\n   Transcript info:")
            print(f"     Language: {transcript.language if hasattr(transcript, 'language') else 'Unknown'}")
            print(f"     Code: {transcript.language_code if hasattr(transcript, 'language_code') else 'Unknown'}")
            print(f"     Generated: {transcript.is_generated if hasattr(transcript, 'is_generated') else 'Unknown'}")
            
            if transcript.language_code.startswith('en'):
                print(f"     Fetching English transcript...")
                data = transcript.fetch()
                print(f"     ✅ Got {len(data)} segments!")
                break
                
    except Exception as e2:
        print(f"   List also failed: {e2}")