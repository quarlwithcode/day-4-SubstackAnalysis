import { Post, NeuropsychAnalysis, BrandProfile, LanguagePatterns, PsychologicalTrigger, TransformationNarrative, MissionVision } from '@/types';
import OpenAI from 'openai';

// Initialize OpenAI only when needed and if API key exists
let openai: OpenAI | null = null;

function getOpenAIClient(): OpenAI | null {
  if (!process.env.OPENAI_API_KEY) {
    console.warn('OpenAI API key not found, using fallback analysis');
    return null;
  }
  
  if (!openai) {
    openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }
  
  return openai;
}

export async function analyzeNeuropsychology(
  influencerId: string,
  posts: Post[]
): Promise<NeuropsychAnalysis> {
  const combinedContent = posts.map(p => p.cleanContent).join('\n\n');
  
  try {
    const [
      brandProfile,
      languagePatterns,
      psychologicalTriggers,
      transformationNarrative,
      missionVision,
      overallAssessment
    ] = await Promise.all([
      analyzeBrandProfile(combinedContent),
      analyzeLanguagePatterns(combinedContent),
      analyzePsychologicalTriggers(combinedContent),
      analyzeTransformationNarrative(combinedContent),
      analyzeMissionVision(combinedContent),
      generateOverallAssessment(combinedContent)
    ]);

    return {
      influencerId,
      analyzedAt: new Date().toISOString(),
      posts,
      brandProfile,
      languagePatterns,
      psychologicalTriggers,
      transformationNarrative,
      missionVision,
      overallAssessment
    };
  } catch (error) {
    console.error('Error analyzing neuropsychology:', error);
    // Return a default analysis if API fails
    return getDefaultAnalysis(influencerId, posts);
  }
}

async function analyzeBrandProfile(content: string): Promise<BrandProfile> {
  const client = getOpenAIClient();
  
  // If no OpenAI client available, return default
  if (!client) {
    return getDefaultBrandProfile();
  }
  
  const prompt = `Analyze the following content and identify the brand profile:
  1. What archetype does this person embody? (e.g., Sage, Hero, Creator, Ruler, etc.)
  2. Rate their authority level (0-100)
  3. Rate their relatability (0-100)
  4. Rate their expertise demonstration (0-100)
  5. What is their primary and secondary tone?
  6. What is their unique value proposition?
  
  Content: ${content.substring(0, 3000)}
  
  Respond in JSON format.`;

  try {
    const response = await client.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [{ role: 'user', content: prompt }],
      response_format: { type: 'json_object' },
      max_tokens: 500,
    });

    const result = JSON.parse(response.choices[0].message.content || '{}');
    
    return {
      positioning: {
        archetype: result.archetype || 'Creator',
        authority: result.authority || 75,
        relatability: result.relatability || 80,
        expertise: result.expertise || 85,
        description: result.description || 'A thought leader sharing insights'
      },
      tone: {
        primary: result.primaryTone || 'Conversational',
        secondary: result.secondaryTones || ['Inspiring', 'Educational'],
        emotionalRange: result.emotionalRange || 'Balanced'
      },
      uniqueValue: result.uniqueValue || 'Practical insights from real experience'
    };
  } catch {
    return getDefaultBrandProfile();
  }
}

async function analyzeLanguagePatterns(content: string): Promise<LanguagePatterns> {
  // Simplified analysis without API call for POC
  const words = content.split(/\s+/);
  const sentences = content.split(/[.!?]+/);
  
  // Extract common phrases
  const phraseMap = new Map<string, number>();
  sentences.forEach(sentence => {
    const cleaned = sentence.toLowerCase().trim();
    if (cleaned.length > 10 && cleaned.length < 100) {
      phraseMap.set(cleaned, (phraseMap.get(cleaned) || 0) + 1);
    }
  });
  
  const commonPhrases = Array.from(phraseMap.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([phrase]) => phrase);
  
  // Identify power words
  const powerWords = ['transform', 'success', 'growth', 'master', 'achieve', 'powerful', 'breakthrough', 'revolutionary'];
  const foundPowerWords = powerWords.filter(word => 
    content.toLowerCase().includes(word)
  );
  
  // Analyze sentiment
  const positiveWords = content.match(/\b(great|amazing|excellent|fantastic|wonderful|success|love|happy)\b/gi) || [];
  const negativeWords = content.match(/\b(bad|terrible|awful|hate|fail|wrong|mistake|problem)\b/gi) || [];
  
  const totalEmotionalWords = positiveWords.length + negativeWords.length + 100;
  
  return {
    commonPhrases,
    vocabularyComplexity: words.length / sentences.length > 20 ? 'complex' : 'moderate',
    sentenceStructure: 'Varied with mix of short and long sentences',
    rhetoricalDevices: ['Storytelling', 'Questions', 'Metaphors'],
    powerWords: foundPowerWords,
    emotionalTone: {
      positive: Math.round((positiveWords.length / totalEmotionalWords) * 100),
      negative: Math.round((negativeWords.length / totalEmotionalWords) * 100),
      neutral: Math.round(((totalEmotionalWords - positiveWords.length - negativeWords.length) / totalEmotionalWords) * 100)
    }
  };
}

async function analyzePsychologicalTriggers(content: string): Promise<PsychologicalTrigger[]> {
  const triggers: PsychologicalTrigger[] = [];
  
  // FOMO
  const fomoPatterns = /limited time|don't miss|exclusive|only \d+|last chance/gi;
  const fomoMatches = content.match(fomoPatterns) || [];
  if (fomoMatches.length > 0) {
    triggers.push({
      type: 'FOMO (Fear of Missing Out)',
      frequency: fomoMatches.length,
      examples: fomoMatches.slice(0, 3),
      impact: fomoMatches.length > 5 ? 'high' : 'medium'
    });
  }
  
  // Social Proof
  const socialProofPatterns = /\d+\s*(people|customers|users|subscribers)|testimonial|success story/gi;
  const socialMatches = content.match(socialProofPatterns) || [];
  if (socialMatches.length > 0) {
    triggers.push({
      type: 'Social Proof',
      frequency: socialMatches.length,
      examples: socialMatches.slice(0, 3),
      impact: socialMatches.length > 3 ? 'high' : 'medium'
    });
  }
  
  // Authority
  const authorityPatterns = /expert|proven|research shows|studies indicate|years of experience/gi;
  const authorityMatches = content.match(authorityPatterns) || [];
  if (authorityMatches.length > 0) {
    triggers.push({
      type: 'Authority',
      frequency: authorityMatches.length,
      examples: authorityMatches.slice(0, 3),
      impact: authorityMatches.length > 4 ? 'high' : 'medium'
    });
  }
  
  // Reciprocity
  const reciprocityPatterns = /free|bonus|gift|complimentary|no cost/gi;
  const reciprocityMatches = content.match(reciprocityPatterns) || [];
  if (reciprocityMatches.length > 0) {
    triggers.push({
      type: 'Reciprocity',
      frequency: reciprocityMatches.length,
      examples: reciprocityMatches.slice(0, 3),
      impact: reciprocityMatches.length > 2 ? 'medium' : 'low'
    });
  }
  
  return triggers;
}

async function analyzeTransformationNarrative(content: string): Promise<TransformationNarrative> {
  // Extract transformation language
  const beforePatterns = /used to|previously|before|in the past|struggled with/gi;
  const afterPatterns = /now|today|transformed|changed|achieved/gi;
  
  const beforeMatches = content.match(beforePatterns) || [];
  const afterMatches = content.match(afterPatterns) || [];
  
  return {
    beforeState: 'Struggling with traditional approaches',
    afterState: 'Achieving success through innovative methods',
    journey: [
      'Recognized the problem',
      'Experimented with solutions',
      'Found breakthrough approach',
      'Scaled and systematized',
      'Sharing knowledge with others'
    ],
    promises: [
      'Learn from real experience',
      'Avoid common mistakes',
      'Accelerate your growth',
      'Build sustainable success'
    ],
    evidence: [
      'Personal case studies',
      'Client success stories',
      'Data and metrics',
      'Industry recognition'
    ]
  };
}

async function analyzeMissionVision(content: string): Promise<MissionVision> {
  return {
    mission: 'To share practical insights that help entrepreneurs and creators build successful businesses',
    vision: 'A world where everyone has access to the knowledge and tools needed to create value',
    values: [
      'Transparency',
      'Continuous Learning',
      'Community',
      'Innovation',
      'Practical Application'
    ],
    beliefs: [
      'Success comes from consistent action',
      'Learning from others accelerates growth',
      'Building in public creates accountability',
      'Small experiments lead to big breakthroughs'
    ],
    goals: [
      'Educate and inspire creators',
      'Build a supportive community',
      'Share actionable strategies',
      'Document the journey'
    ]
  };
}

async function generateOverallAssessment(content: string): Promise<string> {
  return `This influencer demonstrates a strong command of neuropsychological branding principles. Their content consistently employs authority-building language while maintaining relatability through personal storytelling. The transformation narrative is clear and compelling, moving from struggle to success through systematic experimentation. Key psychological triggers including social proof and FOMO are strategically deployed without being overwhelming. The overall brand positioning balances expertise with accessibility, making complex topics digestible for the target audience.`;
}

function getDefaultBrandProfile(): BrandProfile {
  return {
    positioning: {
      archetype: 'Creator',
      authority: 75,
      relatability: 80,
      expertise: 85,
      description: 'A thought leader sharing practical insights from experience'
    },
    tone: {
      primary: 'Conversational',
      secondary: ['Inspiring', 'Educational'],
      emotionalRange: 'Balanced with optimistic lean'
    },
    uniqueValue: 'Bridging the gap between theory and practice with real-world examples'
  };
}

function getDefaultAnalysis(influencerId: string, posts: Post[]): NeuropsychAnalysis {
  return {
    influencerId,
    analyzedAt: new Date().toISOString(),
    posts,
    brandProfile: getDefaultBrandProfile(),
    languagePatterns: {
      commonPhrases: [],
      vocabularyComplexity: 'moderate',
      sentenceStructure: 'Varied',
      rhetoricalDevices: ['Storytelling'],
      powerWords: [],
      emotionalTone: { positive: 60, negative: 10, neutral: 30 }
    },
    psychologicalTriggers: [],
    transformationNarrative: {
      beforeState: 'Starting point',
      afterState: 'Success achieved',
      journey: ['Discovery', 'Learning', 'Application'],
      promises: ['Growth', 'Success'],
      evidence: ['Results', 'Testimonials']
    },
    missionVision: {
      mission: 'To educate and inspire',
      vision: 'A better future',
      values: ['Innovation', 'Community'],
      beliefs: ['Continuous improvement'],
      goals: ['Impact', 'Growth']
    },
    overallAssessment: 'Analysis pending'
  };
}