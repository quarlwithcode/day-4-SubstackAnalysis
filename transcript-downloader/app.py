from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
from datetime import datetime
import json

app = Flask(__name__)

# Ensure the influencer-data directory exists
os.makedirs('influencer-data', exist_ok=True)

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]+)',
        r'(?:youtu\.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)',
        r'(?:youtube\.com\/v\/)([\w-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    # Replace spaces with underscores and remove special characters
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.lower()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/download_transcript', methods=['POST'])
def download_transcript():
    """Download YouTube transcript and save as text file"""
    try:
        data = request.json
        youtube_url = data.get('url')
        influencer_name = data.get('influencer')
        video_title = data.get('title')
        
        print(f"Received request - URL: {youtube_url}, Influencer: {influencer_name}, Title: {video_title}")
        
        # Validate inputs
        if not all([youtube_url, influencer_name, video_title]):
            print(f"Missing fields - URL: {youtube_url}, Influencer: {influencer_name}, Title: {video_title}")
            return jsonify({'error': 'All fields are required'}), 400
        
        # Extract video ID
        video_id = extract_video_id(youtube_url)
        print(f"Extracted video ID: {video_id}")
        
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        # Get transcript using new API (v1.2.2)
        transcript_segments = None
        
        try:
            print(f"Listing available transcripts for video ID: {video_id}")
            
            # Create API instance
            api = YouTubeTranscriptApi()
            
            # List available transcripts
            transcript_list = api.list(video_id)
            
            # Find best English transcript (prefer manual over auto-generated)
            selected_transcript = None
            
            # First pass: look for manually created English transcripts
            for transcript in transcript_list:
                print(f"Found transcript: {transcript.language} ({transcript.language_code}) - Generated: {transcript.is_generated}")
                if transcript.language_code.startswith('en') and not transcript.is_generated:
                    selected_transcript = transcript
                    print(f"Selected manual transcript: {transcript.language_code}")
                    break
            
            # Second pass: if no manual transcript, use auto-generated
            if not selected_transcript:
                for transcript in transcript_list:
                    if transcript.language_code.startswith('en'):
                        selected_transcript = transcript
                        print(f"Selected auto-generated transcript: {transcript.language_code}")
                        break
            
            if selected_transcript:
                print(f"Fetching transcript...")
                fetched_data = selected_transcript.fetch()
                print(f"Successfully fetched {len(fetched_data)} segments")
                
                # Convert to list of dicts
                transcript_segments = []
                for segment in fetched_data:
                    if hasattr(segment, 'text'):
                        transcript_segments.append({'text': segment.text})
                    elif isinstance(segment, dict):
                        transcript_segments.append(segment)
            else:
                return jsonify({'error': 'No English transcript available for this video'}), 400
                
        except Exception as e:
            print(f"Error getting transcript: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': f'Could not fetch transcript. Make sure the video has captions enabled. Error: {str(e)}'}), 400
        
        if not transcript_segments:
            return jsonify({'error': 'No transcript segments found'}), 400
        
        # Format transcript text
        transcript_text = ' '.join([entry['text'] for entry in transcript_segments])
        
        # Create folder structure
        safe_influencer = sanitize_filename(influencer_name)
        influencer_folder = os.path.join('influencer-data', safe_influencer)
        
        # Create influencer folder if it doesn't exist
        os.makedirs(influencer_folder, exist_ok=True)
        print(f"Using folder: {influencer_folder}")
        
        # Create filename (without influencer prefix since it's in the folder)
        safe_title = sanitize_filename(video_title)
        filename = f"{safe_title}.txt"
        filepath = os.path.join(influencer_folder, filename)
        
        # Create file content
        content = f"""Video Title: {video_title}
Influencer: {influencer_name}
URL: {youtube_url}
Date Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

========================================
TRANSCRIPT
========================================

{transcript_text}
"""
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': f'Transcript saved to {safe_influencer}/{filename}',
            'filename': f'{safe_influencer}/{filename}',
            'word_count': len(transcript_text.split())
        })
        
    except Exception as e:
        print(f"Unexpected error in download_transcript: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/list_transcripts')
def list_transcripts():
    """List all downloaded transcripts"""
    try:
        files = []
        if os.path.exists('influencer-data'):
            # Walk through all subdirectories
            for root, dirs, filenames in os.walk('influencer-data'):
                for filename in filenames:
                    if filename.endswith('.txt'):
                        filepath = os.path.join(root, filename)
                        # Get relative path from influencer-data
                        relative_path = os.path.relpath(filepath, 'influencer-data')
                        # Get file stats
                        stats = os.stat(filepath)
                        files.append({
                            'name': relative_path,
                            'size': f"{stats.st_size / 1024:.1f} KB",
                            'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                        })
        
        # Sort by modified date (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return jsonify(files)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_influencers')
def get_influencers():
    """Get list of unique influencers from existing folders"""
    try:
        influencers = set()
        if os.path.exists('influencer-data'):
            # Get all subdirectories (these are influencer folders)
            for item in os.listdir('influencer-data'):
                item_path = os.path.join('influencer-data', item)
                if os.path.isdir(item_path):
                    influencers.add(item)
        
        # Add default influencers
        default_influencers = ['greg-isenberg', 'dan-koe', 'justin-welsh']
        influencers.update(default_influencers)
        
        return jsonify(sorted(list(influencers)))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("YouTube Transcript Downloader")
    print("="*50)
    print("\n✅ Server starting...")
    print("📍 Access the app at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000)