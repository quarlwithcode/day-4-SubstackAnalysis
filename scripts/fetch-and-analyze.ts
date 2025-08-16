import { fetchSubstackFeed } from '../lib/rss-parser';
import { cleanSubstackContent } from '../lib/text-cleaner';
import { analyzeNeuropsychology } from '../lib/neuropsych-analyzer';
import { saveInfluencer, saveAnalysis, ensureDataDirectories } from '../lib/data-manager';
import { Influencer } from '../types';

async function analyzeInfluencer(name: string, substackUrl: string, description: string) {
  console.log(`\n📊 Analyzing ${name}...`);
  
  try {
    // Ensure data directories exist
    await ensureDataDirectories();
    
    // Create influencer slug
    const slug = name.toLowerCase().replace(/\s+/g, '-');
    const id = slug;
    
    console.log('📡 Fetching RSS feed...');
    const posts = await fetchSubstackFeed(substackUrl);
    console.log(`✅ Found ${posts.length} posts`);
    
    // Clean content
    console.log('🧹 Cleaning content...');
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
      description,
      lastAnalyzed: new Date().toISOString(),
      postCount: cleanedPosts.length
    };
    
    // Save influencer
    console.log('💾 Saving influencer data...');
    await saveInfluencer(influencer);
    
    // Analyze neuropsychology
    console.log('🧠 Analyzing neuropsychology...');
    const analysis = await analyzeNeuropsychology(id, cleanedPosts.slice(0, 10)); // Analyze first 10 posts for POC
    
    // Save analysis
    console.log('💾 Saving analysis...');
    await saveAnalysis(analysis);
    
    console.log(`✨ Successfully analyzed ${name}!`);
    console.log(`   - ${cleanedPosts.length} posts processed`);
    console.log(`   - Analysis saved to data/analyses/${id}.json`);
    
    return { influencer, analysis };
  } catch (error) {
    console.error(`❌ Error analyzing ${name}:`, error);
    throw error;
  }
}

async function main() {
  console.log('🚀 Starting Neuropsychology Brand Analyzer');
  console.log('==========================================\n');
  
  // Analyze Greg Isenberg
  await analyzeInfluencer(
    'Greg Isenberg',
    'https://latecheckout.substack.com/feed',
    'Founder of Late Checkout, sharing insights on startups, product development, and internet culture'
  );
  
  // Add more influencers here as needed
  // await analyzeInfluencer('Name', 'https://example.substack.com/feed', 'Description');
  
  console.log('\n==========================================');
  console.log('✅ All analyses complete!');
}

// Run the script
main().catch(console.error);