import Link from 'next/link';
import { getAnalysis } from '@/lib/data-loader';

// Use any type for influencer to handle both formats
interface InfluencerCardProps {
  influencer: any;
  analysis?: any;
  featured?: boolean;
}

export default async function InfluencerCard({ influencer, featured = false }: InfluencerCardProps) {
  const analysis = await getAnalysis(influencer.id);
  
  const archetype = analysis?.brandProfile?.positioning?.archetype || 'Analyst';
  const authority = analysis?.brandProfile?.positioning?.authority || 0;
  const engagement = analysis?.brandProfile?.positioning?.relatability || 0;
  const triggers = analysis?.psychologicalTriggers?.length || 0;
  
  return (
    <Link href={`/influencers/${influencer.slug}`}>
      <div className={`${featured ? 'modern-card' : 'notion-card'} cursor-pointer group animate-fade-in`}>
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-xl font-semibold group-hover:text-modern-blue-600 transition-colors">
            {influencer.name}
          </h3>
          {featured && (
            <span className="stat-badge stat-badge-purple animate-pulse-soft">
              Featured
            </span>
          )}
        </div>
        
        <p className="text-notion-text-secondary mb-4 line-clamp-2">
          {influencer.description}
        </p>
        
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-modern-emerald-50 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-modern-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-xs text-notion-text-tertiary">Authority</p>
              <p className="text-sm font-semibold">{authority}%</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-modern-blue-50 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-modern-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div>
              <p className="text-xs text-notion-text-tertiary">Engagement</p>
              <p className="text-sm font-semibold">{engagement}%</p>
            </div>
          </div>
        </div>
        
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-notion-text-secondary">Archetype</span>
            <span className="stat-badge stat-badge-blue">{archetype}</span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-notion-text-secondary">Posts Analyzed</span>
            <span className="font-medium">{influencer.postCount || 0}</span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-notion-text-secondary">Psych Triggers</span>
            <span className="font-medium">{triggers}</span>
          </div>
        </div>
        
        <div className="pt-3 border-t border-notion-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-modern-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-xs text-notion-text-tertiary">Active</span>
              </div>
              {triggers > 3 && (
                <span className="stat-badge stat-badge-amber">High Impact</span>
              )}
            </div>
            {influencer.lastAnalyzed && (
              <span className="text-xs text-notion-text-tertiary">
                {new Date(influencer.lastAnalyzed).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}