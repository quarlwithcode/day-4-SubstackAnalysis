import Parser from 'rss-parser';
import { Post } from '@/types';

const parser = new Parser();

export async function fetchRSSFeed(feedUrl: string): Promise<Post[]> {
  try {
    const feed = await parser.parseURL(feedUrl);
    
    return feed.items.map((item, index) => ({
      id: `${feed.title?.toLowerCase().replace(/\s+/g, '-')}-${index}`,
      title: item.title || '',
      content: item.content || item.contentSnippet || '',
      cleanContent: '', // Will be processed by text cleaner
      pubDate: item.pubDate || new Date().toISOString(),
      link: item.link || '',
      author: item.creator || feed.title,
      categories: item.categories || [],
    }));
  } catch (error) {
    console.error('Error fetching RSS feed:', error);
    throw new Error('Failed to fetch RSS feed');
  }
}

export async function fetchSubstackFeed(substackUrl: string): Promise<Post[]> {
  const feedUrl = substackUrl.endsWith('/feed') 
    ? substackUrl 
    : `${substackUrl.replace(/\/$/, '')}/feed`;
  
  return fetchRSSFeed(feedUrl);
}