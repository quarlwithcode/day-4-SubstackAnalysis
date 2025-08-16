# YouTube Transcript Downloader

A simple local web application to download YouTube video transcripts for influencer language analysis.

## Features

- 🎥 Download transcripts from any YouTube video with captions
- 📝 Save transcripts as organized text files
- 👤 Track multiple influencers
- 🗂️ Auto-organize files by influencer and video title
- 💾 Local storage - all data stays on your machine
- 🎨 Clean, modern web interface

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Navigate to the transcript-downloader directory:
```bash
cd transcript-downloader
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

3. To download a transcript:
   - Paste a YouTube URL (e.g., `https://www.youtube.com/watch?v=ABC123`)
   - Enter the influencer's name (e.g., "Greg Isenberg")
   - Enter a descriptive title for the video
   - Click "Download Transcript"

4. Transcripts are saved in the `influencer-data/` folder as `.txt` files

## File Format

Transcripts are saved with the naming pattern:
```
[influencer-name]-[video-title].txt
```

Example: `greg-isenberg-how-to-build-systems.txt`

Each file contains:
- Video metadata (title, influencer, URL, download date)
- Full transcript text

## Supported YouTube URLs

The app supports various YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Features in Detail

### Influencer Dropdown
- Automatically suggests previously used influencer names
- Can also enter new influencer names

### Transcript List
- Shows all downloaded transcripts
- Displays file size and modification date
- Auto-refreshes every 30 seconds
- Manual refresh button available

### Error Handling
- Clear error messages for:
  - Invalid YouTube URLs
  - Videos without captions
  - Network issues

## Troubleshooting

### "Could not fetch transcript" error
- Make sure the video has captions/subtitles available
- Some videos may have restricted transcripts
- Try videos with auto-generated or manual captions

### Server won't start
- Make sure port 5000 is not in use
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Try running with: `python3 app.py` if you have multiple Python versions

### Can't access the web interface
- Ensure the server is running (you should see "Server starting..." message)
- Try opening `http://127.0.0.1:5000` instead of localhost
- Check your firewall settings

## Tips

- Videos with manually added captions typically have better transcript quality
- Longer videos may take a few seconds to download
- The app works best with educational/talking head content
- Transcripts are saved locally - back them up if needed

## File Structure

```
transcript-downloader/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── influencer-data/      # Downloaded transcripts
│   └── example.txt       # Example transcript format
└── README.md            # This file
```

## Privacy

- All transcripts are stored locally on your machine
- No data is sent to external servers (except YouTube for fetching)
- The app runs entirely on localhost

## Support

For issues or questions, check the troubleshooting section above or review the error messages in the web interface.