#!/usr/bin/env python3
"""Direct test of YouTube transcript fetching"""

from youtube_transcript_api import YouTubeTranscriptApi
import json

video_id = "ZdO00Y-u1y0"
print(f"Testing video ID: {video_id}")

try:
    # First, list available transcripts
    print("\n1. Listing available transcripts...")
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    # Get the transcript generator
    transcripts = list(transcript_list)
    print(f"   Found {len(transcripts)} transcript(s)")
    
    # Try to get manually created transcripts first, then auto-generated
    transcript_to_use = None
    
    # First pass: look for manually created English transcripts
    for t in transcripts:
        print(f"   - {t.language} ({t.language_code}) - Generated: {t.is_generated}")
        if t.language_code.startswith('en') and not t.is_generated:
            transcript_to_use = t
            print(f"   ✓ Selected manual transcript: {t.language_code}")
            break
    
    # Second pass: if no manual transcript, use auto-generated
    if not transcript_to_use:
        for t in transcripts:
            if t.language_code.startswith('en'):
                transcript_to_use = t
                print(f"   ✓ Selected auto-generated transcript: {t.language_code}")
                break
    
    if transcript_to_use:
        print("\n2. Fetching transcript...")
        # Use the find_transcript method with the exact language code
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([transcript_to_use.language_code])
        fetched_data = transcript.fetch()
        
        print(f"✅ Success! Fetched {len(fetched_data)} segments")
        print(f"\nFirst 3 segments:")
        for i, segment in enumerate(fetched_data[:3]):
            print(f"   {i+1}. {segment['text'][:100]}...")
        
        # Calculate total duration
        if fetched_data:
            total_duration = fetched_data[-1]['start'] + fetched_data[-1]['duration']
            minutes = int(total_duration // 60)
            seconds = int(total_duration % 60)
            print(f"\nTotal duration: {minutes}:{seconds:02d}")
            
            # Word count
            full_text = ' '.join([s['text'] for s in fetched_data])
            word_count = len(full_text.split())
            print(f"Total words: {word_count}")
    else:
        print("❌ No English transcript found")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"   Error type: {type(e).__name__}")
    
    # Try alternative method
    print("\n3. Trying alternative fetch method...")
    try:
        # Direct fetch without listing
        from youtube_transcript_api._api import TranscriptListFetcher
        fetcher = TranscriptListFetcher(video_id)
        transcript_data = fetcher.fetch()
        print(f"   Raw data keys: {transcript_data.keys() if hasattr(transcript_data, 'keys') else 'Not a dict'}")
    except Exception as e2:
        print(f"   Alternative method also failed: {e2}")