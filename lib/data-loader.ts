// Static data loader for production builds
// This loads JSON data at build time instead of runtime

// Import all data statically at build time
import influencersData from '@/data/influencers.json';
import alexHormoziAnalysis from '@/data/analyses/alex-hormozi.json';
import aliAbdaalAnalysis from '@/data/analyses/ali-abdaal.json';
import chrisDoAnalysis from '@/data/analyses/chris-do.json';
import danKoeAnalysis from '@/data/analyses/dan-koe.json';
import danMartellAnalysis from '@/data/analyses/dan-martell.json';
import davidOndrejAnalysis from '@/data/analyses/david-ondrej.json';
import garyVaynerchukAnalysis from '@/data/analyses/gary-vaynerchuk.json';
import gregIsenbergAnalysis from '@/data/analyses/greg-isenberg.json';
import liamOttleyAnalysis from '@/data/analyses/liam-ottley.json';
import matthewLakajevAnalysis from '@/data/analyses/matthew-lakajev.json';
import shanHanifAnalysis from '@/data/analyses/shan-hanif.json';

// Simplified interfaces that match our actual JSON data
interface SimplifiedInfluencer {
  id: string;
  name: string;
  slug: string;
  avatar?: string;
  bio?: string;
  description?: string;
  stats?: {
    posts: number;
    words: number;
    engagement: number;
    patterns: number;
  };
  tags?: string[];
  lastAnalyzed?: string;
  // Optional fields from Influencer type
  substackUrl?: string;
  rssUrl?: string;
  postCount?: number;
}

// Create a map of all analyses
const analysesMap: Record<string, any> = {
  'alex-hormozi': alexHormoziAnalysis,
  'ali-abdaal': aliAbdaalAnalysis,
  'chris-do': chrisDoAnalysis,
  'dan-koe': danKoeAnalysis,
  'dan-martell': danMartellAnalysis,
  'david-ondrej': davidOndrejAnalysis,
  'gary-vaynerchuk': garyVaynerchukAnalysis,
  'greg-isenberg': gregIsenbergAnalysis,
  'liam-ottley': liamOttleyAnalysis,
  'matthew-lakajev': matthewLakajevAnalysis,
  'shan-hanif': shanHanifAnalysis,
};

export async function getInfluencers(): Promise<SimplifiedInfluencer[]> {
  const influencers = influencersData as SimplifiedInfluencer[];
  // Add default values for required fields if missing
  return influencers.map(inf => ({
    ...inf,
    description: inf.description || inf.bio || `Analysis of ${inf.name}'s content`,
    substackUrl: inf.substackUrl || '#',
    rssUrl: inf.rssUrl || '#',
    postCount: inf.postCount || inf.stats?.posts || 0
  }));
}

export async function getInfluencer(slug: string): Promise<SimplifiedInfluencer | null> {
  const influencers = await getInfluencers();
  return influencers.find(i => i.slug === slug) || null;
}

export async function getAnalysis(influencerId: string): Promise<any | null> {
  const analysis = analysesMap[influencerId];
  if (!analysis) return null;

  // Return the analysis as-is since components expect the actual structure from JSON
  return {
    ...analysis,
    analyzedAt: analysis.analyzedAt || analysis.date || new Date().toISOString(),
    posts: analysis.posts || [],
    brandProfile: analysis.brandProfile || {
      positioning: {
        archetype: 'Creator',
        authority: 75,
        relatability: 80,
        expertise: 85,
        description: 'A thought leader'
      },
      tone: {
        primary: 'Conversational',
        secondary: ['Inspiring'],
        emotionalRange: 'Balanced'
      },
      uniqueValue: 'Unique insights'
    },
    languagePatterns: analysis.languagePatterns || {
      commonPhrases: [],
      vocabularyComplexity: 'moderate',
      sentenceStructure: 'Varied',
      rhetoricalDevices: [],
      powerWords: [],
      emotionalTone: { positive: 60, negative: 10, neutral: 30 }
    },
    psychologicalTriggers: analysis.psychologicalTriggers || [],
    transformationNarrative: analysis.transformationNarrative || {
      beforeState: 'Starting point',
      afterState: 'Success',
      journey: [],
      promises: [],
      evidence: []
    },
    missionVision: analysis.missionVision || {
      mission: 'To inspire',
      vision: 'A better future',
      values: [],
      beliefs: [],
      goals: []
    },
    overallAssessment: analysis.overallAssessment || 'Analysis of content'
  };
}

export async function searchInfluencers(query: string): Promise<SimplifiedInfluencer[]> {
  const influencers = await getInfluencers();
  const searchTerm = query.toLowerCase();
  
  return influencers.filter(i => 
    i.name.toLowerCase().includes(searchTerm) ||
    (i.description && i.description.toLowerCase().includes(searchTerm)) ||
    (i.bio && i.bio.toLowerCase().includes(searchTerm))
  );
}