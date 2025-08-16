export interface Influencer {
  id: string;
  name: string;
  slug: string;
  substackUrl: string;
  rssUrl: string;
  description: string;
  lastAnalyzed?: string;
  postCount?: number;
}

export interface Post {
  id: string;
  title: string;
  content: string;
  cleanContent: string;
  pubDate: string;
  link: string;
  author?: string;
  categories?: string[];
}

export interface NeuropsychAnalysis {
  influencerId: string;
  analyzedAt: string;
  posts: Post[];
  brandProfile: BrandProfile;
  languagePatterns: LanguagePatterns;
  psychologicalTriggers: PsychologicalTrigger[];
  transformationNarrative: TransformationNarrative;
  missionVision: MissionVision;
  overallAssessment: string;
}

export interface BrandProfile {
  positioning: {
    archetype: string;
    authority: number;
    relatability: number;
    expertise: number;
    description: string;
  };
  tone: {
    primary: string;
    secondary: string[];
    emotionalRange: string;
  };
  uniqueValue: string;
}

export interface LanguagePatterns {
  commonPhrases: string[];
  vocabularyComplexity: 'simple' | 'moderate' | 'complex';
  sentenceStructure: string;
  rhetoricalDevices: string[];
  powerWords: string[];
  emotionalTone: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

export interface PsychologicalTrigger {
  type: string;
  frequency: number;
  examples: string[];
  impact: 'low' | 'medium' | 'high';
}

export interface TransformationNarrative {
  beforeState: string;
  afterState: string;
  journey: string[];
  promises: string[];
  evidence: string[];
}

export interface MissionVision {
  mission: string;
  vision: string;
  values: string[];
  beliefs: string[];
  goals: string[];
}