import SearchBar from '@/components/SearchBar';
import InfluencerCard from '@/components/InfluencerCard';
import { getInfluencers } from '@/lib/data-manager';

export default async function Home() {
  const influencers = await getInfluencers();
  const featuredInfluencers = influencers.slice(0, 3);
  
  return (
    <main className="min-h-screen">
      <section className="notion-page pt-20 pb-16">
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-notion-text to-notion-text-secondary bg-clip-text text-transparent">
            Decode the Psychology Behind Influential Brands
          </h1>
          <p className="text-xl text-notion-text-secondary max-w-3xl mx-auto">
            Analyze the neuropsychological patterns in influencer content to understand 
            their brand positioning, transformation narratives, and persuasion techniques.
          </p>
        </div>
        
        <div className="flex justify-center mb-12">
          <SearchBar />
        </div>
        
        {featuredInfluencers.length > 0 && (
          <div className="mb-16 animate-slide-up">
            <h2 className="text-2xl font-semibold mb-6 text-center">Featured Influencers</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {featuredInfluencers.map((influencer) => (
                <InfluencerCard key={influencer.id} influencer={influencer} featured={true} />
              ))}
            </div>
          </div>
        )}
        
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-gradient-to-br from-modern-emerald-50 to-modern-emerald-100 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-modern group-hover:shadow-modern-lg transition-shadow">
              <svg className="w-8 h-8 text-modern-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Language Analysis</h3>
            <p className="text-notion-text-secondary">
              Deep dive into word choice, sentence structure, and rhetorical devices
            </p>
          </div>
          
          <div className="text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-gradient-to-br from-modern-amber-50 to-modern-amber-100 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-modern group-hover:shadow-modern-lg transition-shadow">
              <svg className="w-8 h-8 text-modern-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Psychological Triggers</h3>
            <p className="text-notion-text-secondary">
              Identify FOMO, social proof, authority, and other persuasion techniques
            </p>
          </div>
          
          <div className="text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-gradient-to-br from-modern-blue-50 to-modern-blue-100 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-modern group-hover:shadow-modern-lg transition-shadow">
              <svg className="w-8 h-8 text-modern-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Brand Positioning</h3>
            <p className="text-notion-text-secondary">
              Understand archetype, authority level, and unique value proposition
            </p>
          </div>
        </div>
      </section>
      
      <section className="bg-gradient-to-br from-notion-surface to-white py-16">
        <div className="notion-page">
          <h2 className="text-3xl font-semibold mb-8 text-center">How It Works</h2>
          <div className="max-w-3xl mx-auto space-y-6">
            <div className="flex items-start space-x-4 group">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-notion-accent to-gray-700 text-white rounded-xl flex items-center justify-center text-sm font-semibold shadow-modern group-hover:scale-110 transition-transform">
                1
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-1">Feed Processing</h3>
                <p className="text-notion-text-secondary">
                  We fetch and parse RSS feeds from Substack publications, cleaning the content 
                  to focus purely on the author&apos;s voice and message.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4 group">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-notion-accent to-gray-700 text-white rounded-xl flex items-center justify-center text-sm font-semibold shadow-modern group-hover:scale-110 transition-transform">
                2
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-1">Neuropsychological Analysis</h3>
                <p className="text-notion-text-secondary">
                  Advanced language processing identifies patterns in word choice, emotional triggers, 
                  and persuasion techniques used throughout the content.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4 group">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-notion-accent to-gray-700 text-white rounded-xl flex items-center justify-center text-sm font-semibold shadow-modern group-hover:scale-110 transition-transform">
                3
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-1">Comprehensive Report</h3>
                <p className="text-notion-text-secondary">
                  Get detailed insights into brand positioning, transformation narratives, 
                  mission/vision alignment, and the psychological framework behind their influence.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="py-16">
        <div className="notion-page text-center">
          <h2 className="text-3xl font-semibold mb-4">Ready to Analyze?</h2>
          <p className="text-notion-text-secondary mb-8 max-w-2xl mx-auto">
            Start by searching for an influencer or explore our pre-analyzed profiles 
            to understand the neuropsychology behind successful personal brands.
          </p>
          <a href="/influencers" className="modern-button inline-block">
            Explore All Influencers
          </a>
        </div>
      </section>
    </main>
  );
}