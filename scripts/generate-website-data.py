#!/usr/bin/env python3
"""
Generate Website Data from Linguistic Analysis
Creates JSON files for the Next.js frontend from linguistic pattern analysis.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def load_linguistic_data(patterns_dir: Path) -> Dict:
    """Load all linguistic pattern JSON files."""
    data = {}
    for json_file in patterns_dir.glob("*-linguistic-patterns.json"):
        influencer_name = json_file.stem.replace('-linguistic-patterns', '')
        with open(json_file, 'r', encoding='utf-8') as f:
            data[influencer_name] = json.load(f)
    return data

def load_raw_language_stats(raw_language_dir: Path) -> Dict:
    """Extract statistics from raw language files."""
    stats = {}
    for txt_file in raw_language_dir.glob("*-raw-language.txt"):
        influencer_name = txt_file.stem.replace('-raw-language', '')
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Extract stats from header
            for line in lines[:10]:
                if 'Source Files:' in line:
                    source_files = int(line.split(':')[1].strip().split()[0])
                elif 'Cleaned Word Count:' in line:
                    word_count = int(line.split(':')[1].strip().replace(',', ''))
            stats[influencer_name] = {
                'source_files': source_files,
                'word_count': word_count
            }
    return stats

def create_influencer_profile(name: str, linguistic_data: Dict, raw_stats: Dict) -> Dict:
    """Create an influencer profile for the website."""
    # Format the name for display
    display_name = name.replace('-', ' ').title()
    
    # Extract key insights from linguistic data
    data = linguistic_data[name]
    stats = raw_stats.get(name, {})
    
    # Calculate engagement metrics based on linguistic patterns
    engagement_score = calculate_engagement_score(data)
    
    return {
        "id": name,
        "name": display_name,
        "slug": name,
        "avatar": f"/avatars/{name}.jpg",  # Placeholder avatar path
        "bio": generate_bio(display_name, data),
        "stats": {
            "posts": stats.get('source_files', 0),
            "words": stats.get('word_count', 0),
            "engagement": engagement_score,
            "patterns": len(data['repetition']['signature_phrases'])
        },
        "tags": generate_tags(data),
        "lastAnalyzed": datetime.now().isoformat()
    }

def calculate_engagement_score(data: Dict) -> float:
    """Calculate an engagement score based on linguistic patterns."""
    score = 0
    
    # YOU-focused language increases engagement
    if data['identity_framing']['primary_frame'] == 'YOU':
        score += 30
    
    # High arousal increases engagement
    if data['emotional_valence']['arousal_level'] == 'high':
        score += 20
    
    # Aspiration-based motivation is engaging
    if data['fear_vs_aspiration']['motivation_style'] == 'aspiration-based':
        score += 15
    
    # Questions engage audience
    score += min(data['rhetorical_devices']['rhetorical_questions'] / 10, 15)
    
    # Sensory richness adds engagement
    score += min(data['sensory_anchors']['sensory_richness'] * 10, 20)
    
    return min(round(score), 100)

def generate_bio(name: str, data: Dict) -> str:
    """Generate a bio based on linguistic patterns."""
    frame = data['identity_framing']['primary_frame']
    metaphor = data['metaphors']['dominant_metaphor']
    temporal = data['temporal_anchoring']['temporal_orientation']
    motivation = data['fear_vs_aspiration']['motivation_style']
    
    frame_desc = {
        'YOU': 'direct and personal',
        'I': 'authority-driven',
        'WE': 'community-focused'
    }.get(frame, 'balanced')
    
    return (f"{name} uses {frame_desc} communication with a {metaphor}-based narrative framework. "
            f"Their content is {temporal}-oriented and primarily {motivation.replace('-', ' ')}.")

def generate_tags(data: Dict) -> List[str]:
    """Generate tags based on linguistic patterns."""
    tags = []
    
    # Add frame tag
    tags.append(f"{data['identity_framing']['primary_frame']}-focused")
    
    # Add metaphor tag
    tags.append(f"{data['metaphors']['dominant_metaphor']}-metaphor")
    
    # Add emotional tag
    tags.append(data['emotional_valence']['emotional_tone'])
    
    # Add temporal tag
    tags.append(f"{data['temporal_anchoring']['temporal_orientation']}-oriented")
    
    # Add motivation tag
    if 'aspiration' in data['fear_vs_aspiration']['motivation_style']:
        tags.append('aspirational')
    else:
        tags.append('fear-based')
    
    return tags

def create_analysis(name: str, linguistic_data: Dict, raw_stats: Dict) -> Dict:
    """Create detailed analysis for an influencer."""
    data = linguistic_data[name]
    display_name = name.replace('-', ' ').title()
    
    # Extract top signature phrases
    signature_phrases = [phrase for phrase, count in data['repetition']['signature_phrases']]
    
    # Extract key metrics
    pronoun_data = data['pronouns']
    emotional_data = data['emotional_valence']
    
    # Calculate emotional tone percentages
    pos_ratio = emotional_data['positivity_ratio']
    neg_ratio = 1 - pos_ratio if pos_ratio > 0 else 0.5
    
    # Create psychological triggers list
    psych_triggers = []
    for trigger in extract_emotional_triggers(data):
        psych_triggers.append({
            "trigger": trigger,
            "description": f"Uses {trigger} to drive engagement",
            "frequency": "high",
            "examples": [f"Example of {trigger} usage"]
        })
    
    return {
        "id": name,
        "influencerId": name,
        "influencerName": display_name,
        "date": datetime.now().isoformat(),
        "analyzedAt": datetime.now().isoformat(),
        "posts": [],  # Will be populated with sample posts
        "overallAssessment": generate_overall_assessment(name, data),
        "brandProfile": {
            "positioning": {
                "archetype": get_archetype(data),
                "description": f"Combines {data['identity_framing']['primary_frame']}-focused messaging with {data['metaphors']['dominant_metaphor']} metaphors",
                "authority": min(round(pronoun_data['i_ratio'] * 20 + 30), 95),
                "relatability": min(round(pronoun_data['we_ratio'] * 30 + 40), 90),
                "persuasion": round(pronoun_data['you_ratio'] * 10),
                "expertise": min(round(50 + (pronoun_data['i_ratio'] * 10)), 85),
                "connection": round(pronoun_data['we_ratio'] * 10)
            },
            "tone": {
                "primary": data['emotional_valence']['emotional_tone'].capitalize(),
                "secondary": [data['cadence_pacing']['pacing_style'], data['emotional_valence']['arousal_level']],
                "emotionalRange": f"{data['emotional_valence']['arousal_level'].capitalize()} arousal with {data['emotional_valence']['emotional_tone']} undertones"
            },
            "uniqueValue": generate_unique_value(name, data),
            "voice": {
                "tone": emotional_data['emotional_tone'],
                "arousal": emotional_data['arousal_level'],
                "style": data['cadence_pacing']['pacing_style'],
                "clarity": 85
            },
            "messaging": {
                "core_themes": extract_core_themes(data),
                "value_props": extract_value_props(data),
                "differentiators": extract_differentiators(data)
            }
        },
        "languagePatterns": {
            "vocabularyComplexity": get_vocabulary_complexity(data),
            "sentenceStructure": f"{data['cadence_pacing']['pacing_style'].capitalize()} with average {data['cadence_pacing']['avg_sentence_length']:.0f} words per sentence",
            "emotionalTone": {
                "positive": round(pos_ratio * 100),
                "neutral": 20,  # Placeholder
                "negative": round(neg_ratio * 100)
            },
            "powerWords": extract_power_words(data),
            "rhetoricalDevices": extract_rhetorical_devices(data),
            "signature_phrases": signature_phrases,
            "word_frequency": extract_word_frequency(data),
            "sentence_structure": {
                "avg_length": data['cadence_pacing']['avg_sentence_length'],
                "variety": data['cadence_pacing']['rhythm_changes'],
                "style": data['cadence_pacing']['pacing_style']
            },
            "emotional_valence": emotional_data['positivity_ratio']
        },
        "psychologicalTriggers": psych_triggers,
        "transformationNarrative": {
            "beforeState": generate_before_state(data),
            "afterState": generate_after_state(data),
            "journey": generate_journey_steps(data),
            "promises": generate_promises(data),
            "evidence": generate_evidence(data)
        },
        "missionVision": {
            "mission": generate_mission(name, data),
            "vision": generate_vision(name, data),
            "values": generate_values(data),
            "beliefs": generate_beliefs(data),
            "goals": generate_goals(data)
        },
        "neuropsychAnalysis": {
            "emotional_triggers": extract_emotional_triggers(data),
            "cognitive_biases": extract_cognitive_biases(data),
            "persuasion_tactics": extract_persuasion_tactics(data),
            "psychological_hooks": signature_phrases[:5]
        },
        "recommendations": generate_recommendations(data),
        "insights": generate_insights(data),
        "metrics": {
            "consistency_score": 85,
            "authority_score": round(pronoun_data['i_ratio'] * 20),
            "engagement_score": calculate_engagement_score(data),
            "neuropsych_score": calculate_neuropsych_score(data)
        }
    }

def extract_core_themes(data: Dict) -> List[str]:
    """Extract core themes from linguistic patterns."""
    themes = []
    
    # Based on dominant metaphor
    metaphor_themes = {
        'journey': ['transformation', 'progress', 'growth'],
        'war': ['competition', 'strategy', 'victory'],
        'building': ['creation', 'foundation', 'systems'],
        'game': ['winning', 'rules', 'mastery'],
        'nature': ['organic growth', 'evolution', 'nurturing'],
        'machine': ['optimization', 'efficiency', 'automation']
    }
    
    themes.extend(metaphor_themes.get(data['metaphors']['dominant_metaphor'], []))
    
    # Based on temporal focus
    if data['temporal_anchoring']['temporal_orientation'] == 'future':
        themes.append('vision')
    elif data['temporal_anchoring']['temporal_orientation'] == 'past':
        themes.append('experience')
    else:
        themes.append('action')
    
    return themes[:4]

def extract_value_props(data: Dict) -> List[str]:
    """Extract value propositions from linguistic patterns."""
    props = []
    
    if data['fear_vs_aspiration']['motivation_style'] == 'aspiration-based':
        props.extend(['achieve goals', 'unlock potential', 'maximize success'])
    else:
        props.extend(['avoid mistakes', 'reduce risk', 'protect assets'])
    
    if data['identity_framing']['primary_frame'] == 'YOU':
        props.append('personalized guidance')
    elif data['identity_framing']['primary_frame'] == 'WE':
        props.append('community support')
    else:
        props.append('expert knowledge')
    
    return props[:3]

def extract_differentiators(data: Dict) -> List[str]:
    """Extract differentiators from linguistic patterns."""
    diffs = []
    
    # Unique combination of frame + metaphor
    diffs.append(f"{data['identity_framing']['primary_frame'].lower()}-focused {data['metaphors']['dominant_metaphor']} approach")
    
    # Emotional approach
    if data['emotional_valence']['arousal_level'] == 'high':
        diffs.append('high-energy delivery')
    else:
        diffs.append('calm, methodical approach')
    
    # Sensory preference
    diffs.append(f"{data['sensory_anchors']['dominant_sense'].lower()}-rich communication")
    
    return diffs

def extract_emotional_triggers(data: Dict) -> List[str]:
    """Extract emotional triggers from linguistic patterns."""
    triggers = []
    
    if data['fear_vs_aspiration']['aspiration_percentage'] > 60:
        triggers.extend(['ambition', 'growth mindset', 'success desire'])
    if data['fear_vs_aspiration']['fear_percentage'] > 30:
        triggers.extend(['loss aversion', 'FOMO', 'security needs'])
    
    if data['emotional_valence']['urgency_ratio'] > 0.7:
        triggers.append('urgency')
    
    if data['rhetorical_devices']['rhetorical_questions'] > 20:
        triggers.append('curiosity')
    
    return triggers[:4]

def extract_cognitive_biases(data: Dict) -> List[str]:
    """Extract cognitive biases being leveraged."""
    biases = []
    
    if data['identity_framing']['primary_frame'] == 'YOU':
        biases.append('personalization bias')
    
    if data['temporal_anchoring']['future_percentage'] > 40:
        biases.append('optimism bias')
    elif data['temporal_anchoring']['past_percentage'] > 40:
        biases.append('hindsight bias')
    
    if data['rhetorical_devices']['numbered_lists'] > 50:
        biases.append('clustering illusion')
    
    if data['emotional_valence']['urgency_ratio'] > 0.7:
        biases.append('scarcity effect')
    
    return biases[:3]

def extract_persuasion_tactics(data: Dict) -> List[str]:
    """Extract persuasion tactics from linguistic patterns."""
    tactics = []
    
    if data['rhetorical_devices']['contrast_patterns'] > 10:
        tactics.append('contrast principle')
    
    if data['rhetorical_devices']['rhetorical_questions'] > 20:
        tactics.append('socratic questioning')
    
    if data['pronouns']['you_ratio'] > 3:
        tactics.append('direct address')
    
    if data['pronouns']['we_ratio'] > 1:
        tactics.append('inclusive language')
    
    if data['repetition']['signature_phrases']:
        tactics.append('repetition for emphasis')
    
    return tactics[:4]

def extract_word_frequency(data: Dict) -> Dict[str, int]:
    """Extract word frequency from signature phrases."""
    freq = {}
    for phrase, count in data['repetition']['top_bigrams'][:10]:
        # Skip if contains brackets (censored words)
        if '[' not in phrase:
            freq[phrase] = count
    return freq

def calculate_neuropsych_score(data: Dict) -> int:
    """Calculate a neuropsychological effectiveness score."""
    score = 0
    
    # Consistent framing
    if data['identity_framing']['primary_frame']:
        score += 20
    
    # Clear metaphorical framework
    if data['metaphors']['metaphor_diversity'] >= 2:
        score += 15
    
    # Effective use of rhetorical devices
    if data['rhetorical_devices']['rhetorical_density'] > 0.5:
        score += 15
    
    # Strong sensory anchoring
    if data['sensory_anchors']['sensory_richness'] > 0.5:
        score += 15
    
    # Clear motivation style
    if abs(data['fear_vs_aspiration']['aspiration_percentage'] - 50) > 20:
        score += 15
    
    # Signature phrases established
    if len(data['repetition']['signature_phrases']) >= 5:
        score += 20
    
    return min(score, 100)

def generate_recommendations(data: Dict) -> List[str]:
    """Generate recommendations based on linguistic patterns."""
    recs = []
    
    # Balance recommendations
    if data['pronouns']['i_ratio'] > 5:
        recs.append("Reduce I-focused language to increase relatability")
    elif data['pronouns']['you_ratio'] < 2:
        recs.append("Increase YOU-focused language for better engagement")
    
    if data['emotional_valence']['positivity_ratio'] < 0.3:
        recs.append("Balance negative tone with more positive messaging")
    elif data['emotional_valence']['positivity_ratio'] > 0.7:
        recs.append("Add contrast with realistic challenges for credibility")
    
    if data['sensory_anchors']['sensory_richness'] < 0.5:
        recs.append("Incorporate more sensory language for memorable content")
    
    if data['cadence_pacing']['rhythm_changes'] < 10:
        recs.append("Vary sentence structure for better rhythm and engagement")
    
    return recs[:3]

def generate_insights(data: Dict) -> List[str]:
    """Generate insights from linguistic patterns."""
    insights = []
    
    # Frame insight
    frame = data['identity_framing']['primary_frame']
    insights.append(f"Uses {frame}-centered framing to {get_frame_purpose(frame)}")
    
    # Metaphor insight
    metaphor = data['metaphors']['dominant_metaphor']
    insights.append(f"Leverages {metaphor} metaphors to create {get_metaphor_effect(metaphor)}")
    
    # Emotional insight
    if data['emotional_valence']['urgency_ratio'] > 0.7:
        insights.append("Creates urgency through high-arousal language patterns")
    
    # Signature phrase insight
    if data['repetition']['signature_phrases']:
        top_phrase = data['repetition']['signature_phrases'][0][0]
        insights.append(f'Signature phrase "{top_phrase}" reinforces core messaging')
    
    return insights[:4]

def get_frame_purpose(frame: str) -> str:
    """Get the purpose of a framing style."""
    purposes = {
        'YOU': 'create direct connection and personalization',
        'I': 'establish authority and expertise',
        'WE': 'build community and shared identity'
    }
    return purposes.get(frame, 'engage audience')

def get_metaphor_effect(metaphor: str) -> str:
    """Get the effect of a metaphor type."""
    effects = {
        'journey': 'narrative of transformation',
        'war': 'competitive urgency',
        'building': 'systematic progress',
        'game': 'playful mastery',
        'nature': 'organic development',
        'machine': 'predictable efficiency'
    }
    return effects.get(metaphor, 'conceptual understanding')

def generate_overall_assessment(name: str, data: Dict) -> str:
    """Generate overall assessment of the influencer."""
    display_name = name.replace('-', ' ').title()
    frame = data['identity_framing']['primary_frame']
    metaphor = data['metaphors']['dominant_metaphor']
    temporal = data['temporal_anchoring']['temporal_orientation']
    
    return (f"{display_name} demonstrates a {frame}-centered communication style, "
            f"leveraging {metaphor} metaphors to create {get_metaphor_effect(metaphor)}. "
            f"Their {temporal}-focused approach combined with {data['fear_vs_aspiration']['motivation_style']} "
            f"messaging creates a compelling narrative that resonates with their audience.")

def get_archetype(data: Dict) -> str:
    """Determine archetype based on linguistic patterns."""
    if data['pronouns']['i_ratio'] > 4:
        return "The Expert"
    elif data['pronouns']['we_ratio'] > 2:
        return "The Community Builder"
    elif data['pronouns']['you_ratio'] > 4:
        return "The Coach"
    elif data['metaphors']['dominant_metaphor'] == 'war':
        return "The Warrior"
    elif data['metaphors']['dominant_metaphor'] == 'journey':
        return "The Guide"
    else:
        return "The Teacher"

def generate_unique_value(name: str, data: Dict) -> str:
    """Generate unique value proposition."""
    display_name = name.replace('-', ' ').title()
    return (f"{display_name} provides unique value through their {data['metaphors']['dominant_metaphor']}-based "
            f"framework and {data['identity_framing']['primary_frame']}-focused approach, "
            f"creating a distinctive voice in their niche.")

def get_vocabulary_complexity(data: Dict) -> str:
    """Determine vocabulary complexity."""
    avg_sentence = data['cadence_pacing']['avg_sentence_length']
    if avg_sentence < 12:
        return "simple"
    elif avg_sentence < 18:
        return "moderate"
    else:
        return "complex"

def extract_power_words(data: Dict) -> List[str]:
    """Extract power words from top phrases."""
    power_words = []
    for phrase, _ in data['repetition']['top_bigrams'][:5]:
        if '[' not in phrase:  # Skip censored words
            words = phrase.split()
            for word in words:
                if len(word) > 4 and word not in ['going', 'have', 'want', 'need']:
                    power_words.append(word)
    return list(set(power_words))[:8]

def extract_rhetorical_devices(data: Dict) -> List[str]:
    """Extract rhetorical devices used."""
    devices = []
    if data['rhetorical_devices']['contrast_patterns'] > 10:
        devices.append("Contrast")
    if data['rhetorical_devices']['rhetorical_questions'] > 20:
        devices.append("Questions")
    if data['rhetorical_devices']['numbered_lists'] > 50:
        devices.append("Lists")
    if data['rhetorical_devices']['imperatives'] > 5:
        devices.append("Commands")
    if len(data['repetition']['signature_phrases']) > 3:
        devices.append("Repetition")
    return devices

def generate_before_state(data: Dict) -> str:
    """Generate the 'before' state in transformation narrative."""
    if data['fear_vs_aspiration']['motivation_style'] == 'fear-based':
        return "Struggling with challenges, feeling overwhelmed by obstacles"
    else:
        return "Seeking growth, ready for the next level of success"

def generate_after_state(data: Dict) -> str:
    """Generate the 'after' state in transformation narrative."""
    metaphor = data['metaphors']['dominant_metaphor']
    if metaphor == 'journey':
        return "Arrived at destination, transformed and fulfilled"
    elif metaphor == 'war':
        return "Victorious, conquered challenges and emerged stronger"
    elif metaphor == 'building':
        return "Established, with solid foundations and systems in place"
    elif metaphor == 'game':
        return "Winning, mastered the rules and achieving consistent results"
    else:
        return "Transformed, operating at a higher level of capability"

def generate_journey_steps(data: Dict) -> List[str]:
    """Generate transformation journey steps."""
    steps = []
    if data['temporal_anchoring']['temporal_orientation'] == 'future':
        steps = ["Vision creation", "Goal setting", "Action planning", "Execution", "Achievement"]
    elif data['temporal_anchoring']['temporal_orientation'] == 'present':
        steps = ["Awareness", "Decision", "Action", "Momentum", "Results"]
    else:
        steps = ["Learning from past", "Understanding patterns", "Making changes", "Building new habits", "Creating future"]
    return steps[:4]

def generate_promises(data: Dict) -> List[str]:
    """Generate promises based on motivation style."""
    if data['fear_vs_aspiration']['motivation_style'] == 'aspiration-based':
        return ["Achieve your goals", "Unlock your potential", "Create lasting success"]
    else:
        return ["Avoid costly mistakes", "Protect your progress", "Minimize risks"]

def generate_evidence(data: Dict) -> List[str]:
    """Generate evidence types used."""
    evidence = []
    if data['temporal_anchoring']['past_percentage'] > 20:
        evidence.append("Personal experience")
    if data['pronouns']['i_ratio'] > 3:
        evidence.append("Expert knowledge")
    if data['rhetorical_devices']['numbered_lists'] > 30:
        evidence.append("Systematic frameworks")
    evidence.append("Proven strategies")
    return evidence[:3]

def generate_mission(name: str, data: Dict) -> str:
    """Generate mission statement."""
    display_name = name.replace('-', ' ').title()
    return f"To help people {generate_promises(data)[0].lower()} through {data['metaphors']['dominant_metaphor']}-based strategies"

def generate_vision(name: str, data: Dict) -> str:
    """Generate vision statement."""
    return f"A world where everyone can {generate_after_state(data).lower()}"

def generate_values(data: Dict) -> List[str]:
    """Generate core values."""
    values = []
    if data['emotional_valence']['emotional_tone'] == 'positive':
        values.append("Optimism")
    if data['pronouns']['we_ratio'] > 1:
        values.append("Community")
    if data['pronouns']['i_ratio'] > 3:
        values.append("Expertise")
    if data['fear_vs_aspiration']['motivation_style'] == 'aspiration-based':
        values.append("Growth")
    values.append("Authenticity")
    return values[:4]

def generate_beliefs(data: Dict) -> List[str]:
    """Generate core beliefs."""
    beliefs = []
    metaphor = data['metaphors']['dominant_metaphor']
    
    if metaphor == 'journey':
        beliefs.extend(["Every step forward matters", "The path reveals itself as you walk"])
    elif metaphor == 'building':
        beliefs.extend(["Strong foundations create lasting success", "Systems scale, effort doesn't"])
    elif metaphor == 'game':
        beliefs.extend(["Success has learnable rules", "Practice makes permanent"])
    
    if data['identity_framing']['primary_frame'] == 'YOU':
        beliefs.append("You have untapped potential")
    elif data['identity_framing']['primary_frame'] == 'WE':
        beliefs.append("Together we achieve more")
    
    return beliefs[:5]

def generate_goals(data: Dict) -> List[str]:
    """Generate strategic goals."""
    goals = []
    if data['fear_vs_aspiration']['motivation_style'] == 'aspiration-based':
        goals = ["Inspire transformation", "Enable achievement", "Foster growth"]
    else:
        goals = ["Provide security", "Reduce uncertainty", "Build confidence"]
    return goals

def create_sample_posts(name: str, linguistic_data: Dict) -> List[Dict]:
    """Create sample posts based on linguistic patterns."""
    # For now, create placeholder posts
    # In production, these would come from actual transcript excerpts
    return [
        {
            "id": f"{name}-post-1",
            "title": "Sample Post 1",
            "content": "Content based on linguistic patterns...",
            "date": datetime.now().isoformat(),
            "engagement": 95
        }
    ]

def main():
    """Main function to generate website data."""
    # Set up paths
    base_path = Path('/Users/vincentquarles/Documents/day-4-SubstackAnalysis')
    patterns_dir = base_path / 'influencer-data' / 'linguistic-patterns'
    raw_language_dir = base_path / 'influencer-data' / 'creator-raw-language'
    data_dir = base_path / 'data'
    
    # Create data directories
    data_dir.mkdir(exist_ok=True)
    (data_dir / 'analyses').mkdir(exist_ok=True)
    (data_dir / 'posts').mkdir(exist_ok=True)
    
    print("Loading linguistic data...")
    linguistic_data = load_linguistic_data(patterns_dir)
    raw_stats = load_raw_language_stats(raw_language_dir)
    
    # Create influencers.json
    print("\nGenerating influencers.json...")
    influencers = []
    for name in linguistic_data.keys():
        profile = create_influencer_profile(name, linguistic_data, raw_stats)
        influencers.append(profile)
    
    with open(data_dir / 'influencers.json', 'w', encoding='utf-8') as f:
        json.dump(influencers, f, indent=2)
    print(f"  ✅ Created influencers.json with {len(influencers)} profiles")
    
    # Create individual analysis files
    print("\nGenerating analysis files...")
    for name in linguistic_data.keys():
        analysis = create_analysis(name, linguistic_data, raw_stats)
        
        # Add sample posts
        analysis['posts'] = create_sample_posts(name, linguistic_data)
        
        # Save analysis file
        with open(data_dir / 'analyses' / f'{name}.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
        print(f"  ✅ Created {name}.json")
    
    # Create posts files (placeholder for now)
    print("\nGenerating posts files...")
    for name in linguistic_data.keys():
        posts = {
            "posts": create_sample_posts(name, linguistic_data),
            "totalPosts": 5,
            "influencerId": name
        }
        with open(data_dir / 'posts' / f'{name}-posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2)
        print(f"  ✅ Created {name}-posts.json")
    
    print("\n" + "=" * 60)
    print("WEBSITE DATA GENERATION COMPLETE")
    print("=" * 60)
    print(f"\nGenerated files in: {data_dir}")
    print(f"  • influencers.json")
    print(f"  • {len(linguistic_data)} analysis files")
    print(f"  • {len(linguistic_data)} posts files")
    
    # Print summary of each influencer
    print("\nInfluencer Summaries:")
    for influencer in influencers:
        print(f"\n{influencer['name']}:")
        print(f"  Words analyzed: {influencer['stats']['words']:,}")
        print(f"  Engagement score: {influencer['stats']['engagement']}")
        print(f"  Tags: {', '.join(influencer['tags'][:3])}")

if __name__ == "__main__":
    main()