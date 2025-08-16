# Neuropsychology Brand Analyzer

A Next.js application that analyzes influencer RSS feeds to dissect the neuropsychology behind their brand through language patterns, positioning, and persuasion techniques.

## Features

- **RSS Feed Processing**: Automatically fetches and processes Substack RSS feeds
- **Neuropsychological Analysis**: Analyzes language patterns, psychological triggers, and brand positioning
- **Clean Notion-Style UI**: Minimalist black and white design inspired by Notion
- **Fast Loading**: Pre-processed JSON data for instant access
- **SEO Optimized**: Built with Next.js for server-side rendering

## Tech Stack

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- RSS Parser
- OpenAI API for analysis

## Getting Started

### Prerequisites

- Node.js 18+ installed
- OpenAI API key (optional for advanced analysis)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/substack-analysis.git
cd substack-analysis
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
```

Edit `.env.local` and add your OpenAI API key (optional):
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## Adding New Influencers

### Method 1: Using the Analysis Script

Run the analysis script to fetch and analyze a new influencer:

```bash
npm run analyze
```

Edit `scripts/fetch-and-analyze.ts` to add new influencers.

### Method 2: Manual Addition

1. Add influencer data to `data/influencers.json`
2. Run analysis to generate insights
3. View results at `/influencers/[slug]`

## Project Structure

```
/
├── app/                  # Next.js app directory
│   ├── api/             # API routes
│   ├── influencers/     # Influencer pages
│   └── page.tsx         # Landing page
├── components/          # React components
├── lib/                 # Utility functions
│   ├── rss-parser.ts   # RSS feed processing
│   ├── text-cleaner.ts # Content cleaning
│   └── neuropsych-analyzer.ts # Analysis logic
├── data/               # JSON data storage
│   ├── influencers.json
│   └── analyses/       # Analysis results
├── scripts/            # CLI tools
└── types/              # TypeScript definitions
```

## Deployment on Vercel

1. Push your code to GitHub

2. Connect your GitHub repository to Vercel:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository

3. Configure environment variables in Vercel:
   - Add `OPENAI_API_KEY` if using AI analysis

4. Deploy:
   - Vercel will automatically build and deploy your application
   - Your app will be available at `https://your-project.vercel.app`

## Features Breakdown

### Neuropsychological Analysis

The platform analyzes:
- **Brand Positioning**: Archetype, authority, relatability, and expertise levels
- **Language Patterns**: Vocabulary complexity, sentence structure, rhetorical devices
- **Psychological Triggers**: FOMO, social proof, authority, reciprocity
- **Transformation Narrative**: Before/after states and journey
- **Mission & Vision**: Core values, beliefs, and goals

### Data Storage

- Uses JSON files for POC-level simplicity
- Pre-processed data for fast loading
- No database required

## Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Analyze an influencer
npm run analyze
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT