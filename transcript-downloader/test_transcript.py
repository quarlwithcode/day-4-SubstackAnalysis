#!/usr/bin/env python3
"""Test script to verify YouTube transcript API is working"""

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("✅ youtube-transcript-api is installed")
    
    # Test with the video ID from the URL you provided
    video_id = "ZdO00Y-u1y0"
    print(f"\nTesting with video ID: {video_id}")
    
    try:
        # Try to get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"✅ Successfully fetched transcript!")
        print(f"   Transcript has {len(transcript)} segments")
        print(f"   First segment: {transcript[0]['text'][:100]}...")
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        
        # Try with language codes
        print("\nTrying with language codes...")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
            print(f"✅ Successfully fetched with language codes!")
            print(f"   Transcript has {len(transcript)} segments")
        except Exception as e2:
            print(f"❌ Still failed: {e2}")
            
            # List available transcripts
            print("\nListing available transcripts...")
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                for transcript in transcript_list:
                    print(f"   Available: {transcript.language} - {transcript.language_code}")
                
                # Now try to fetch using the transcript object
                print("\nTrying to fetch using transcript object...")
                available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                for transcript in available_transcripts:
                    if transcript.language_code.startswith('en'):
                        print(f"   Fetching: {transcript.language_code}")
                        fetched = transcript.fetch()
                        print(f"✅ Successfully fetched {len(fetched)} segments!")
                        print(f"   First segment: {fetched[0]['text'][:100]}...")
                        break
                        
            except Exception as e3:
                print(f"❌ Could not list transcripts: {e3}")
                
except ImportError:
    print("❌ youtube-transcript-api is NOT installed")
    print("   Run: pip install youtube-transcript-api")