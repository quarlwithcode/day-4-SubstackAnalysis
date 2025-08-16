#!/usr/bin/env python3
"""Final working test with correct segment access"""

from youtube_transcript_api import YouTubeTranscriptApi

video_id = "ZdO00Y-u1y0"
print(f"Testing Dan Koe video: https://www.youtube.com/watch?v={video_id}")

try:
    # Create API instance
    api = YouTubeTranscriptApi()
    
    # List available transcripts
    print("\nListing available transcripts...")
    transcript_list = api.list(video_id)
    
    # Find English transcript (prefer manually created over auto-generated)
    selected_transcript = None
    for transcript in transcript_list:
        if transcript.language_code == 'en-US' and not transcript.is_generated:
            selected_transcript = transcript
            print(f"✓ Selected: {transcript.language} (manual)")
            break
        elif transcript.language_code.startswith('en'):
            selected_transcript = transcript
            print(f"✓ Selected: {transcript.language} (auto-generated)")
    
    if selected_transcript:
        # Fetch the transcript
        print("\nFetching transcript...")
        data = selected_transcript.fetch()
        print(f"✅ Successfully fetched {len(data)} segments")
        
        # Process segments
        segments = []
        for segment in data:
            # Check if it's a dict-like object with text
            if hasattr(segment, 'text'):
                segments.append({'text': segment.text, 'start': segment.start, 'duration': segment.duration})
            elif isinstance(segment, dict):
                segments.append(segment)
            else:
                print(f"   Unknown segment type: {type(segment)}")
        
        print(f"   Processed {len(segments)} segments")
        
        if segments:
            # Show first few segments
            print(f"\nFirst 3 segments:")
            for i, seg in enumerate(segments[:3]):
                print(f"   {i+1}. [{seg['start']:.1f}s] {seg['text'][:80]}...")
            
            # Get full text and stats
            full_text = ' '.join([seg['text'] for seg in segments])
            word_count = len(full_text.split())
            
            # Calculate duration
            last_segment = segments[-1]
            total_duration = last_segment['start'] + last_segment['duration']
            minutes = int(total_duration // 60)
            seconds = int(total_duration % 60)
            
            print(f"\nVideo Stats:")
            print(f"   Duration: {minutes}:{seconds:02d}")
            print(f"   Total words: {word_count:,}")
            print(f"   Avg words/minute: {word_count / (total_duration/60):.0f}")
            
            print(f"\nFirst 500 characters of transcript:")
            print(f"   {full_text[:500]}...")
            
            # Save to file
            filename = 'influencer-data/dan-koe-test-transcript.txt'
            print(f"\nSaving to {filename}...")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Video Title: Testing Dan Koe Video\n")
                f.write(f"Influencer: Dan Koe\n")
                f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                f.write(f"Duration: {minutes}:{seconds:02d}\n")
                f.write(f"Words: {word_count:,}\n")
                f.write("\n" + "="*50 + "\n")
                f.write("TRANSCRIPT\n")
                f.write("="*50 + "\n\n")
                f.write(full_text)
            print(f"✅ Saved successfully!")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()