import { fetchSubstackFeed } from '../lib/rss-parser';
import { cleanSubstackContent } from '../lib/text-cleaner';
import fs from 'fs/promises';
import path from 'path';

interface FetchConfig {
  name: string;
  slug: string;
  feedUrl: string;
  maxPosts: number;
}

async function ensureDirectories() {
  const postsDir = path.join(process.cwd(), 'data', 'posts');
  await fs.mkdir(postsDir, { recursive: true });
}

async function fetchAndSavePosts(config: FetchConfig) {
  console.log(`\n📡 Fetching posts for ${config.name}...`);
  
  try {
    // Fetch posts from RSS feed
    const posts = await fetchSubstackFeed(config.feedUrl);
    console.log(`✅ Found ${posts.length} posts`);
    
    // Clean content and take desired number of posts
    const processedPosts = posts.slice(0, config.maxPosts).map(post => ({
      ...post,
      cleanContent: cleanSubstackContent(post.content)
    }));
    
    // Save posts to JSON file
    const filename = path.join(process.cwd(), 'data', 'posts', `${config.slug}-posts.json`);
    await fs.writeFile(filename, JSON.stringify(processedPosts, null, 2));
    
    console.log(`💾 Saved ${processedPosts.length} posts to ${config.slug}-posts.json`);
    
    return processedPosts;
  } catch (error) {
    console.error(`❌ Error fetching posts for ${config.name}:`, error);
    return [];
  }
}

async function main() {
  console.log('🚀 Starting RSS Post Fetcher');
  console.log('==========================================\n');
  
  await ensureDirectories();
  
  const influencers: FetchConfig[] = [
    {
      name: 'Greg Isenberg',
      slug: 'greg-isenberg',
      feedUrl: 'https://latecheckout.substack.com/feed',
      maxPosts: 25
    },
    {
      name: 'Dan Koe',
      slug: 'dan-koe',
      feedUrl: 'https://letters.thedankoe.com/feed',
      maxPosts: 25
    },
    {
      name: 'Justin Welsh',
      slug: 'justin-welsh',
      feedUrl: 'https://thejustinwelsh.substack.com/feed',
      maxPosts: 25
    }
  ];
  
  const results = [];
  for (const influencer of influencers) {
    const posts = await fetchAndSavePosts(influencer);
    results.push({
      name: influencer.name,
      slug: influencer.slug,
      postCount: posts.length
    });
  }
  
  console.log('\n==========================================');
  console.log('📊 Summary:');
  results.forEach(r => {
    console.log(`   ${r.name}: ${r.postCount} posts saved`);
  });
  console.log('\n✅ All posts fetched and saved successfully!');
}

main().catch(console.error);