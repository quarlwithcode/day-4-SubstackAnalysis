import { NextRequest, NextResponse } from 'next/server';
import { fetchSubstackFeed } from '@/lib/rss-parser';
import { cleanSubstackContent } from '@/lib/text-cleaner';
import { analyzeNeuropsychology } from '@/lib/neuropsych-analyzer';
import { saveInfluencer, saveAnalysis } from '@/lib/data-manager';
import { Influencer } from '@/types';

export async function POST(request: NextRequest) {
  try {
    const { name, substackUrl, description } = await request.json();
    
    if (!name || !substackUrl) {
      return NextResponse.json(
        { error: 'Name and Substack URL are required' },
        { status: 400 }
      );
    }
    
    // Create influencer slug
    const slug = name.toLowerCase().replace(/\s+/g, '-');
    const id = slug;
    
    // Fetch RSS feed
    const posts = await fetchSubstackFeed(substackUrl);
    
    // Clean content
    const cleanedPosts = posts.map(post => ({
      ...post,
      cleanContent: cleanSubstackContent(post.content)
    }));
    
    // Create influencer record
    const influencer: Influencer = {
      id,
      name,
      slug,
      substackUrl,
      rssUrl: substackUrl.endsWith('/feed') ? substackUrl : `${substackUrl}/feed`,
      description: description || `Analysis of ${name}'s content`,
      lastAnalyzed: new Date().toISOString(),
      postCount: cleanedPosts.length
    };
    
    // Save influencer
    await saveInfluencer(influencer);
    
    // Analyze neuropsychology
    const analysis = await analyzeNeuropsychology(id, cleanedPosts);
    
    // Save analysis
    await saveAnalysis(analysis);
    
    return NextResponse.json({
      success: true,
      influencer,
      analysisId: id
    });
    
  } catch (error) {
    console.error('Error analyzing influencer:', error);
    return NextResponse.json(
      { error: 'Failed to analyze influencer' },
      { status: 500 }
    );
  }
}