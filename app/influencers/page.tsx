import { Suspense } from 'react';
import SearchBar from '@/components/SearchBar';
import InfluencerCard from '@/components/InfluencerCard';
import { getInfluencers, searchInfluencers } from '@/lib/data-loader';

async function InfluencersList({ searchQuery }: { searchQuery?: string }) {
  const influencers = searchQuery 
    ? await searchInfluencers(searchQuery)
    : await getInfluencers();

  if (influencers.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-notion-text-secondary">
          {searchQuery 
            ? `No influencers found for "${searchQuery}"`
            : 'No influencers added yet'}
        </p>
      </div>
    );
  }

  return (
    <div className="grid md:grid-cols-2 gap-6">
      {influencers.map((influencer) => (
        <InfluencerCard key={influencer.id} influencer={influencer} />
      ))}
    </div>
  );
}

export default async function InfluencersPage({
  searchParams,
}: {
  searchParams: { search?: string };
}) {
  return (
    <main className="notion-page">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Influencers</h1>
        <p className="text-notion-text-secondary mb-6">
          Explore neuropsychological analyses of influential content creators
        </p>
        <SearchBar />
      </div>
      
      <Suspense fallback={<div>Loading influencers...</div>}>
        <InfluencersList searchQuery={searchParams.search} />
      </Suspense>
    </main>
  );
}