import { notFound } from 'next/navigation';
import AnalysisSection from '@/components/AnalysisSection';
import { getInfluencer, getAnalysis } from '@/lib/data-manager';

export default async function InfluencerAnalysisPage({
  params,
}: {
  params: { slug: string };
}) {
  const influencer = await getInfluencer(params.slug);
  
  if (!influencer) {
    notFound();
  }
  
  const analysis = await getAnalysis(influencer.id);
  
  if (!analysis) {
    return (
      <main className="notion-page">
        <h1 className="text-4xl font-bold mb-4">{influencer.name}</h1>
        <p className="text-notion-text-secondary">
          Analysis not yet available. Please check back later.
        </p>
      </main>
    );
  }

  return (
    <main className="notion-page">
      <header className="mb-12 animate-fade-in">
        <h1 className="text-4xl font-bold mb-4">{influencer.name}</h1>
        <p className="text-notion-text-secondary mb-4">{influencer.description}</p>
        
        {/* Key Metrics Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
          <div className="metric-card text-center">
            <div className="text-3xl font-bold text-modern-emerald-600">
              {analysis.brandProfile.positioning.authority}%
            </div>
            <div className="text-sm text-notion-text-secondary mt-1">Authority</div>
          </div>
          <div className="metric-card text-center">
            <div className="text-3xl font-bold text-modern-blue-600">
              {analysis.brandProfile.positioning.relatability}%
            </div>
            <div className="text-sm text-notion-text-secondary mt-1">Relatability</div>
          </div>
          <div className="metric-card text-center">
            <div className="text-3xl font-bold text-modern-purple-600">
              {analysis.posts.length}
            </div>
            <div className="text-sm text-notion-text-secondary mt-1">Posts Analyzed</div>
          </div>
          <div className="metric-card text-center">
            <div className="text-3xl font-bold text-modern-amber-600">
              {analysis.psychologicalTriggers.length}
            </div>
            <div className="text-sm text-notion-text-secondary mt-1">Psych Triggers</div>
          </div>
        </div>
      </header>

      {/* Overall Assessment - Now at the top for better context */}
      <div className="mb-12 animate-slide-up">
        <div className="insight-card insight-info">
          <h2 className="text-xl font-semibold mb-3 flex items-center">
            <span className="w-8 h-8 bg-modern-blue-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-modern-blue-600">✨</span>
            </span>
            Executive Summary
          </h2>
          <p className="text-notion-text leading-relaxed">{analysis.overallAssessment}</p>
        </div>
      </div>

      {/* 1. Brand Profile */}
      <AnalysisSection title="1. Brand Profile & Positioning">
        <div className="grid md:grid-cols-2 gap-6">
          <div className="modern-card">
            <h3 className="font-semibold mb-4 flex items-center">
              <span className="stat-badge stat-badge-emerald mr-2">Core</span>
              Positioning Analysis
            </h3>
            <div className="space-y-3">
              <div className="insight-card insight-success">
                <span className="text-sm text-modern-emerald-700 font-medium">Archetype</span>
                <p className="font-semibold text-lg mt-1">{analysis.brandProfile.positioning.archetype}</p>
              </div>
              <p className="text-notion-text-secondary text-sm">
                {analysis.brandProfile.positioning.description}
              </p>
              
              <div className="space-y-3 mt-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Authority Level</span>
                    <span className="font-medium">{analysis.brandProfile.positioning.authority}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill bg-gradient-to-r from-modern-emerald-500 to-modern-emerald-600" 
                      style={{ width: `${analysis.brandProfile.positioning.authority}%` }}
                    />
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Relatability Score</span>
                    <span className="font-medium">{analysis.brandProfile.positioning.relatability}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill bg-gradient-to-r from-modern-blue-500 to-modern-blue-600" 
                      style={{ width: `${analysis.brandProfile.positioning.relatability}%` }}
                    />
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Expertise Demonstration</span>
                    <span className="font-medium">{analysis.brandProfile.positioning.expertise}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill bg-gradient-to-r from-modern-purple-500 to-modern-purple-600" 
                      style={{ width: `${analysis.brandProfile.positioning.expertise}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="modern-card">
            <h3 className="font-semibold mb-4 flex items-center">
              <span className="stat-badge stat-badge-blue mr-2">Style</span>
              Tone & Communication
            </h3>
            <div className="space-y-4">
              <div className="insight-card insight-info">
                <span className="text-sm text-modern-blue-600 font-medium">Primary Tone</span>
                <p className="font-semibold mt-1">{analysis.brandProfile.tone.primary}</p>
              </div>
              
              <div>
                <span className="text-sm text-notion-text-secondary">Secondary Tones</span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {analysis.brandProfile.tone.secondary.map((tone: string, index: number) => (
                    <span key={index} className="stat-badge stat-badge-blue">
                      {tone}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <span className="text-sm text-notion-text-secondary">Emotional Range</span>
                <p className="text-notion-text mt-1">{analysis.brandProfile.tone.emotionalRange}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="modern-card mt-6">
          <h3 className="font-semibold mb-3 flex items-center">
            <span className="stat-badge stat-badge-purple mr-2">UVP</span>
            Unique Value Proposition
          </h3>
          <p className="text-notion-text leading-relaxed">{analysis.brandProfile.uniqueValue}</p>
        </div>
      </AnalysisSection>

      {/* 2. Language Patterns */}
      <AnalysisSection title="2. Language & Communication Patterns">
        <div className="grid md:grid-cols-2 gap-6">
          <div className="modern-card">
            <h3 className="font-semibold mb-4">Structure Analysis</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-notion-surface rounded-lg">
                <span className="text-notion-text-secondary">Complexity</span>
                <span className={`stat-badge ${
                  analysis.languagePatterns.vocabularyComplexity === 'complex' ? 'stat-badge-purple' :
                  analysis.languagePatterns.vocabularyComplexity === 'moderate' ? 'stat-badge-blue' :
                  'stat-badge-emerald'
                }`}>
                  {analysis.languagePatterns.vocabularyComplexity}
                </span>
              </div>
              <div className="p-3 bg-notion-surface rounded-lg">
                <span className="text-sm text-notion-text-secondary">Sentence Structure</span>
                <p className="text-notion-text mt-1">{analysis.languagePatterns.sentenceStructure}</p>
              </div>
            </div>
          </div>
          
          <div className="modern-card">
            <h3 className="font-semibold mb-4">Emotional Tone Distribution</h3>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="flex items-center">
                    <span className="w-2 h-2 bg-modern-emerald-500 rounded-full mr-2"></span>
                    Positive
                  </span>
                  <span className="font-medium">{analysis.languagePatterns.emotionalTone.positive}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill bg-modern-emerald-500" 
                    style={{ width: `${analysis.languagePatterns.emotionalTone.positive}%` }}
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="flex items-center">
                    <span className="w-2 h-2 bg-gray-400 rounded-full mr-2"></span>
                    Neutral
                  </span>
                  <span className="font-medium">{analysis.languagePatterns.emotionalTone.neutral}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill bg-gray-400" 
                    style={{ width: `${analysis.languagePatterns.emotionalTone.neutral}%` }}
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="flex items-center">
                    <span className="w-2 h-2 bg-modern-amber-500 rounded-full mr-2"></span>
                    Negative
                  </span>
                  <span className="font-medium">{analysis.languagePatterns.emotionalTone.negative}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill bg-modern-amber-500" 
                    style={{ width: `${analysis.languagePatterns.emotionalTone.negative}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {analysis.languagePatterns.powerWords.length > 0 && (
          <div className="modern-card mt-6">
            <h3 className="font-semibold mb-3">Power Words & Triggers</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.languagePatterns.powerWords.map((word: string, index: number) => (
                <span key={index} className="px-4 py-2 bg-gradient-to-r from-modern-purple-50 to-modern-blue-50 text-modern-purple-600 rounded-lg text-sm font-medium">
                  {word}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {analysis.languagePatterns.rhetoricalDevices.length > 0 && (
          <div className="modern-card mt-6">
            <h3 className="font-semibold mb-3">Rhetorical Techniques</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {analysis.languagePatterns.rhetoricalDevices.map((device: string, index: number) => (
                <div key={index} className="text-center p-3 bg-notion-surface rounded-lg">
                  <span className="text-sm text-notion-text">{device}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </AnalysisSection>

      {/* 3. Psychological Triggers */}
      {analysis.psychologicalTriggers.length > 0 && (
        <AnalysisSection title="3. Psychological Triggers & Persuasion">
          <div className="grid md:grid-cols-2 gap-4">
            {analysis.psychologicalTriggers.map((trigger: any, index: number) => (
              <div key={index} className="modern-card">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-lg">{trigger.type}</h3>
                    <p className="text-sm text-notion-text-secondary mt-1">
                      Used {trigger.frequency} times across content
                    </p>
                  </div>
                  <span className={`stat-badge ${
                    trigger.impact === 'high' ? 'stat-badge-amber' :
                    trigger.impact === 'medium' ? 'stat-badge-blue' :
                    'stat-badge-emerald'
                  }`}>
                    {trigger.impact} impact
                  </span>
                </div>
                
                {trigger.examples.length > 0 && (
                  <div className={`mt-4 p-3 rounded-lg ${
                    trigger.impact === 'high' ? 'bg-modern-amber-50/50' :
                    trigger.impact === 'medium' ? 'bg-modern-blue-50/50' :
                    'bg-modern-emerald-50/50'
                  }`}>
                    <p className="text-xs text-notion-text-tertiary mb-2 font-medium">Example Usage:</p>
                    <ul className="space-y-1">
                      {trigger.examples.map((example: string, i: number) => (
                        <li key={i} className="text-sm text-notion-text-secondary italic">
                          &quot;{example}&quot;
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </AnalysisSection>
      )}

      {/* 4. Transformation Narrative */}
      <AnalysisSection title="4. Transformation Narrative">
        <div className="modern-card">
          <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="insight-card insight-warning">
                <h3 className="font-semibold mb-2 text-modern-amber-700">📍 Before State</h3>
                <p className="text-notion-text">{analysis.transformationNarrative.beforeState}</p>
              </div>
              <div className="insight-card insight-success">
                <h3 className="font-semibold mb-2 text-modern-emerald-700">🎯 After State</h3>
                <p className="text-notion-text">{analysis.transformationNarrative.afterState}</p>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-3 flex items-center">
                <span className="stat-badge stat-badge-blue mr-2">Journey</span>
                Transformation Steps
              </h3>
              <div className="space-y-2">
                {analysis.transformationNarrative.journey.map((step: string, index: number) => (
                  <div key={index} className="flex items-start space-x-3">
                    <span className="flex-shrink-0 w-6 h-6 bg-modern-blue-100 text-modern-blue-600 rounded-full flex items-center justify-center text-xs font-semibold">
                      {index + 1}
                    </span>
                    <span className="text-notion-text">{step}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold mb-3">Promises Made</h3>
                <ul className="space-y-2">
                  {analysis.transformationNarrative.promises.map((promise: string, index: number) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-modern-emerald-500 mt-1">✓</span>
                      <span className="text-notion-text-secondary">{promise}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h3 className="font-semibold mb-3">Evidence Provided</h3>
                <ul className="space-y-2">
                  {analysis.transformationNarrative.evidence.map((evidence: string, index: number) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-modern-blue-500 mt-1">→</span>
                      <span className="text-notion-text-secondary">{evidence}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </AnalysisSection>

      {/* 5. Mission & Vision */}
      <AnalysisSection title="5. Mission, Vision & Values">
        <div className="grid md:grid-cols-2 gap-6">
          <div className="modern-card">
            <div className="w-12 h-12 bg-gradient-to-br from-modern-emerald-100 to-modern-emerald-200 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">🎯</span>
            </div>
            <h3 className="font-semibold mb-3">Mission</h3>
            <p className="text-notion-text-secondary">{analysis.missionVision.mission}</p>
          </div>
          
          <div className="modern-card">
            <div className="w-12 h-12 bg-gradient-to-br from-modern-purple-100 to-modern-purple-200 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">🔮</span>
            </div>
            <h3 className="font-semibold mb-3">Vision</h3>
            <p className="text-notion-text-secondary">{analysis.missionVision.vision}</p>
          </div>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6 mt-6">
          <div className="modern-card">
            <h3 className="font-semibold mb-4">Core Values</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.missionVision.values.map((value: string, index: number) => (
                <span key={index} className="stat-badge stat-badge-emerald">
                  {value}
                </span>
              ))}
            </div>
          </div>
          
          <div className="modern-card">
            <h3 className="font-semibold mb-4">Key Beliefs</h3>
            <ul className="space-y-2">
              {analysis.missionVision.beliefs.slice(0, 4).map((belief: string, index: number) => (
                <li key={index} className="text-sm text-notion-text-secondary">
                  • {belief}
                </li>
              ))}
            </ul>
          </div>
        </div>
        
        <div className="modern-card mt-6">
          <h3 className="font-semibold mb-4">Strategic Goals</h3>
          <div className="grid md:grid-cols-2 gap-3">
            {analysis.missionVision.goals.map((goal: string, index: number) => (
              <div key={index} className="flex items-start space-x-2">
                <span className="text-modern-blue-500 mt-1">🎯</span>
                <span className="text-sm text-notion-text">{goal}</span>
              </div>
            ))}
          </div>
        </div>
      </AnalysisSection>

      {/* Analysis Metadata */}
      <div className="mt-12 pt-8 border-t border-notion-border text-center text-sm text-notion-text-tertiary">
        <p>Analysis generated on {new Date(analysis.analyzedAt).toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })}</p>
        <p className="mt-1">Based on {analysis.posts.length} posts from {influencer.name}&apos;s Substack</p>
      </div>
    </main>
  );
}