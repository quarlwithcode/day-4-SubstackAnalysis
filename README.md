# Neuropsychological Brand Analysis Platform

A comprehensive platform for analyzing the psychological patterns and communication strategies of top online influencers through linguistic analysis of their content.

## 🎯 Features

- **YouTube Transcript Analysis**: Downloads and processes YouTube video transcripts
- **10-Dimension Linguistic Analysis**: Analyzes pronouns, metaphors, emotional valence, temporal anchoring, and more
- **Unique Psychological Profiles**: Creates differentiated profiles for each creator
- **Interactive Web Interface**: Next.js 14 app with visual comparisons and insights
- **11 Pre-Analyzed Influencers**: Including Dan Koe, Alex Hormozi, Gary Vaynerchuk, and more

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/quarlwithcode/day-4-SubstackAnalysis)

### Deployment Instructions

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Deploy (no configuration required!)
4. Optional: Add `OPENAI_API_KEY` in Vercel dashboard for enhanced analysis features

**Note:** The application works perfectly without the OpenAI API key using pre-generated analysis data.

## 📊 Analyzed Influencers

| Influencer | Words Analyzed | Transcripts | Archetype |
|------------|---------------|-------------|-----------|
| Dan Koe | 27,670 | 6 | The Systems Designer |
| Greg Isenberg | 27,090 | 5 | The Strategic Mentor |
| Alex Hormozi | 53,393 | 5 | The Game Master |
| Gary Vaynerchuk | 545 | 1 | The Urgency Master |
| David Ondrej | 379 | 1 | The Technical Architect |
| Liam Ottley | 478 | 1 | The Opportunity Architect |
| Matthew Lakajev | 487 | 1 | The Viral Engineer |
| Shan Hanif | 1,325 | 1 | The Scale Commander |
| Dan Martell | 529 | 1 | The Brutal Truth Teller |
| Chris Do | 516 | 1 | The Brand Philosopher |
| Ali Abdaal | 539 | 1 | The Evidence Optimizer |

**Total: 112,951 words analyzed across 11 influencers**

## 💻 Local Development

```bash
# Clone the repository
git clone https://github.com/quarlwithcode/day-4-SubstackAnalysis.git
cd day-4-SubstackAnalysis

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Environment Variables (Optional)

Create a `.env.local` file:

```env
# Optional - app works without it
OPENAI_API_KEY=your_openai_api_key_here
```

## 🏗️ Project Structure

```
├── app/                    # Next.js 14 app directory
│   ├── api/               # API routes
│   ├── influencers/       # Dynamic influencer pages
│   └── page.tsx           # Landing page
├── components/            # React components
├── data/                  # Pre-analyzed influencer data
│   ├── influencers.json   # Main influencer profiles
│   ├── analyses/          # Detailed analysis files
│   └── posts/             # Content samples
├── influencer-data/       # Raw transcripts and linguistic patterns
├── lib/                   # Utility functions
│   ├── rss-parser.ts      # RSS feed processing
│   ├── text-cleaner.ts    # Content cleaning
│   └── neuropsych-analyzer.ts # Analysis logic
├── scripts/               # Python analysis scripts
│   ├── generate-creator-profiles.py
│   ├── linguistic-analysis.py
│   └── generate-website-data-v2.py
└── transcript-downloader/ # Flask app for YouTube transcripts
```

## 🧠 Analysis Dimensions

The platform analyzes 10 neuropsychological dimensions:

1. **Identity Framing** - YOU vs I vs WE positioning
2. **Emotional Valence** - Positive vs negative charge & urgency
3. **Metaphorical Frames** - Journey, war, building, game, nature, machine
4. **Repetition Patterns** - Signature phrases and messaging consistency
5. **Pronoun Usage** - Authority, persuasion, or community building
6. **Rhetorical Devices** - Questions, contrasts, lists, imperatives
7. **Temporal Anchoring** - Past, present, or future focus
8. **Sensory Language** - Visual, auditory, or kinesthetic anchors
9. **Fear vs Aspiration** - Motivation through fear or opportunity
10. **Cadence & Pacing** - Sentence rhythm and complexity

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: Python (Flask for transcript downloading)
- **Analysis**: Python linguistic analysis pipeline
- **Data Storage**: JSON files for pre-computed analysis
- **Deployment**: Optimized for Vercel

## 📈 Use Cases

- **Content Creators**: Model successful patterns or find unique positioning
- **Marketing Agencies**: Analyze client brands and competitor strategies
- **Brand Consultants**: Provide data-driven brand voice recommendations
- **AI Companies**: Train models to replicate specific creator styles
- **Investment Firms**: Evaluate creator authenticity and growth potential

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for your own analysis!

## 🙏 Acknowledgments

Built with data from YouTube transcripts of leading online creators. This tool is for educational and research purposes.

---

**Created as an "MRI for personal brands"** - scientifically decoding the psychological DNA of successful online influencers.