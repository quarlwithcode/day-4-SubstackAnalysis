import fs from 'fs/promises';
import path from 'path';
import { Influencer, NeuropsychAnalysis } from '@/types';

const DATA_DIR = path.join(process.cwd(), 'data');
const ANALYSES_DIR = path.join(DATA_DIR, 'analyses');
const INFLUENCERS_FILE = path.join(DATA_DIR, 'influencers.json');

export async function ensureDataDirectories(): Promise<void> {
  try {
    await fs.mkdir(DATA_DIR, { recursive: true });
    await fs.mkdir(ANALYSES_DIR, { recursive: true });
  } catch (error) {
    console.error('Error creating data directories:', error);
  }
}

export async function saveInfluencer(influencer: Influencer): Promise<void> {
  await ensureDataDirectories();
  
  const influencers = await getInfluencers();
  const existingIndex = influencers.findIndex(i => i.id === influencer.id);
  
  if (existingIndex >= 0) {
    influencers[existingIndex] = influencer;
  } else {
    influencers.push(influencer);
  }
  
  await fs.writeFile(INFLUENCERS_FILE, JSON.stringify(influencers, null, 2));
}

export async function getInfluencers(): Promise<Influencer[]> {
  try {
    const data = await fs.readFile(INFLUENCERS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

export async function getInfluencer(slug: string): Promise<Influencer | null> {
  const influencers = await getInfluencers();
  return influencers.find(i => i.slug === slug) || null;
}

export async function saveAnalysis(analysis: NeuropsychAnalysis): Promise<void> {
  await ensureDataDirectories();
  
  const filename = `${analysis.influencerId}.json`;
  const filepath = path.join(ANALYSES_DIR, filename);
  
  await fs.writeFile(filepath, JSON.stringify(analysis, null, 2));
}

export async function getAnalysis(influencerId: string): Promise<NeuropsychAnalysis | null> {
  try {
    const filename = `${influencerId}.json`;
    const filepath = path.join(ANALYSES_DIR, filename);
    const data = await fs.readFile(filepath, 'utf-8');
    return JSON.parse(data);
  } catch {
    return null;
  }
}

export async function searchInfluencers(query: string): Promise<Influencer[]> {
  const influencers = await getInfluencers();
  const searchTerm = query.toLowerCase();
  
  return influencers.filter(i => 
    i.name.toLowerCase().includes(searchTerm) ||
    i.description.toLowerCase().includes(searchTerm)
  );
}