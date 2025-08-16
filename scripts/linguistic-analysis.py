#!/usr/bin/env python3
"""
Linguistic Pattern Analysis for Creator Profiles
Analyzes raw language files to extract neuropsychological patterns
based on 10 key linguistic measures.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import string

class LinguisticAnalyzer:
    def __init__(self, text: str):
        self.text = text.lower()
        self.sentences = self._split_sentences(text)
        self.words = self.text.split()
        self.word_count = len(self.words)
        
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting (can be improved with NLTK)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def analyze_identity_framing(self) -> Dict:
        """Analyze YOU vs I vs WE positioning."""
        # Count all instances of pronouns, not just specific phrases
        # This gives more accurate representation of communication style
        
        # Count all YOU pronouns and variations
        you_count = len(re.findall(r"\byou\b|\byour\b|\byou're\b|\byou've\b|\byou'll\b|\byou'd\b", self.text))
        
        # Count all I pronouns and variations  
        i_count = len(re.findall(r"\bi\b|\bmy\b|\bme\b|\bi'm\b|\bi've\b|\bi'll\b|\bi'd\b|\bmine\b", self.text))
        
        # Count all WE pronouns and variations
        we_count = len(re.findall(r"\bwe\b|\bour\b|\bus\b|\bwe're\b|\bwe've\b|\bwe'll\b|\bwe'd\b|\bours\b", self.text))
        
        total = you_count + i_count + we_count
        
        return {
            "you_focused": you_count,
            "i_focused": i_count,
            "we_focused": we_count,
            "you_percentage": round((you_count / total * 100), 1) if total > 0 else 0,
            "i_percentage": round((i_count / total * 100), 1) if total > 0 else 0,
            "we_percentage": round((we_count / total * 100), 1) if total > 0 else 0,
            "primary_frame": max(["YOU", "I", "WE"], 
                                key=lambda x: {"YOU": you_count, "I": i_count, "WE": we_count}[x])
        }
    
    def analyze_emotional_valence(self) -> Dict:
        """Analyze positive vs negative emotional charge."""
        positive_words = {
            'amazing', 'awesome', 'beautiful', 'best', 'brilliant', 'excellent',
            'fantastic', 'good', 'great', 'happy', 'love', 'perfect', 'positive',
            'success', 'wonderful', 'win', 'winning', 'opportunity', 'growth',
            'achieve', 'accomplish', 'thrive', 'prosper', 'excel', 'master'
        }
        
        negative_words = {
            'afraid', 'angry', 'bad', 'broken', 'danger', 'dead', 'death',
            'difficult', 'fail', 'failure', 'fear', 'hate', 'horrible', 'hurt',
            'lose', 'loss', 'mistake', 'negative', 'never', 'no', 'not',
            'pain', 'problem', 'sad', 'terrible', 'wrong', 'worst', 'crisis'
        }
        
        urgent_words = {
            'now', 'immediately', 'urgent', 'quick', 'fast', 'hurry',
            'asap', 'today', 'must', 'need', 'critical', 'important'
        }
        
        calm_words = {
            'relax', 'calm', 'peace', 'steady', 'patient', 'gradual',
            'slowly', 'eventually', 'sometime', 'whenever', 'perhaps'
        }
        
        pos_count = sum(1 for word in self.words if word in positive_words)
        neg_count = sum(1 for word in self.words if word in negative_words)
        urgent_count = sum(1 for word in self.words if word in urgent_words)
        calm_count = sum(1 for word in self.words if word in calm_words)
        
        return {
            "positive_count": pos_count,
            "negative_count": neg_count,
            "positivity_ratio": round(pos_count / (pos_count + neg_count), 2) if (pos_count + neg_count) > 0 else 0,
            "urgent_count": urgent_count,
            "calm_count": calm_count,
            "urgency_ratio": round(urgent_count / (urgent_count + calm_count), 2) if (urgent_count + calm_count) > 0 else 0,
            "emotional_tone": "positive" if pos_count > neg_count else "negative",
            "arousal_level": "high" if urgent_count > calm_count else "low"
        }
    
    def analyze_metaphors(self) -> Dict:
        """Identify core metaphorical frames."""
        metaphor_patterns = {
            "journey": ['journey', 'path', 'road', 'destination', 'step', 'milestone', 'progress'],
            "war": ['battle', 'fight', 'attack', 'defend', 'strategy', 'weapon', 'victory', 'defeat'],
            "building": ['build', 'foundation', 'construct', 'structure', 'framework', 'blueprint'],
            "game": ['game', 'play', 'win', 'lose', 'score', 'rules', 'level', 'player'],
            "nature": ['grow', 'seed', 'plant', 'harvest', 'bloom', 'root', 'branch'],
            "machine": ['system', 'process', 'mechanism', 'engine', 'operate', 'function']
        }
        
        metaphor_counts = {}
        for metaphor, words in metaphor_patterns.items():
            count = sum(1 for word in self.words if word in words)
            metaphor_counts[metaphor] = count
        
        dominant_metaphor = max(metaphor_counts, key=metaphor_counts.get)
        
        return {
            "metaphor_counts": metaphor_counts,
            "dominant_metaphor": dominant_metaphor,
            "metaphor_diversity": len([m for m, c in metaphor_counts.items() if c > 0])
        }
    
    def analyze_repetition(self) -> Dict:
        """Extract signature phrases and repetition patterns."""
        # Get 2-grams, 3-grams, 4-grams
        bigrams = []
        trigrams = []
        fourgrams = []
        
        for i in range(len(self.words) - 1):
            bigrams.append(' '.join(self.words[i:i+2]))
        
        for i in range(len(self.words) - 2):
            trigrams.append(' '.join(self.words[i:i+3]))
            
        for i in range(len(self.words) - 3):
            fourgrams.append(' '.join(self.words[i:i+4]))
        
        # Filter out common/boring phrases
        boring_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were'}
        
        filtered_bigrams = [b for b in bigrams if not all(w in boring_words for w in b.split())]
        filtered_trigrams = [t for t in trigrams if not all(w in boring_words for w in t.split())]
        filtered_fourgrams = [f for f in fourgrams if not all(w in boring_words for w in f.split())]
        
        bigram_counts = Counter(filtered_bigrams).most_common(10)
        trigram_counts = Counter(filtered_trigrams).most_common(10)
        fourgram_counts = Counter(filtered_fourgrams).most_common(5)
        
        return {
            "top_bigrams": bigram_counts,
            "top_trigrams": trigram_counts,
            "top_fourgrams": fourgram_counts,
            "signature_phrases": trigram_counts[:5]  # Top 5 3-word phrases as signatures
        }
    
    def analyze_pronouns(self) -> Dict:
        """Analyze pronoun usage ratios."""
        i_pronouns = ['i', "i'm", "i've", "i'll", "i'd", 'me', 'my', 'mine', 'myself']
        you_pronouns = ['you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself']
        we_pronouns = ['we', "we're", "we've", "we'll", "we'd", 'us', 'our', 'ours', 'ourselves']
        they_pronouns = ['they', "they're", "they've", "they'll", "they'd", 'them', 'their', 'theirs']
        
        i_count = sum(1 for word in self.words if word in i_pronouns)
        you_count = sum(1 for word in self.words if word in you_pronouns)
        we_count = sum(1 for word in self.words if word in we_pronouns)
        they_count = sum(1 for word in self.words if word in they_pronouns)
        
        total_pronouns = i_count + you_count + we_count + they_count
        
        return {
            "i_count": i_count,
            "you_count": you_count,
            "we_count": we_count,
            "they_count": they_count,
            "i_ratio": round(i_count / self.word_count * 100, 2),
            "you_ratio": round(you_count / self.word_count * 100, 2),
            "we_ratio": round(we_count / self.word_count * 100, 2),
            "they_ratio": round(they_count / self.word_count * 100, 2),
            "pronoun_profile": self._get_pronoun_profile(i_count, you_count, we_count)
        }
    
    def _get_pronoun_profile(self, i_count: int, you_count: int, we_count: int) -> str:
        """Determine pronoun profile."""
        if i_count > you_count and i_count > we_count:
            return "Authority/Expertise"
        elif you_count > i_count and you_count > we_count:
            return "Persuasion/Personalization"
        elif we_count > i_count and we_count > you_count:
            return "Community/Solidarity"
        else:
            return "Balanced"
    
    def analyze_rhetorical_devices(self) -> Dict:
        """Identify rhetorical patterns."""
        contrasts = len(re.findall(r'\bnot\s+\w+,?\s+but\b', self.text))
        contrasts += len(re.findall(r'\binstead of\b', self.text))
        contrasts += len(re.findall(r'\brather than\b', self.text))
        
        questions = len(re.findall(r'\?', self.text))
        rhetorical_questions = len(re.findall(r'(have you ever|do you think|what if|why do|how can)', self.text))
        
        # Lists (looking for numbered patterns)
        numbered_lists = len(re.findall(r'\b(first|second|third|1\.|2\.|3\.|\bone\b|\btwo\b|\bthree\b)', self.text))
        
        # Commands/imperatives (simplified)
        imperatives = len(re.findall(r'^(do|don\'t|stop|start|think|imagine|remember|consider)', self.text, re.MULTILINE))
        
        return {
            "contrast_patterns": contrasts,
            "questions_total": questions,
            "rhetorical_questions": rhetorical_questions,
            "numbered_lists": numbered_lists,
            "imperatives": imperatives,
            "rhetorical_density": round((contrasts + questions + numbered_lists) / len(self.sentences), 2) if self.sentences else 0
        }
    
    def analyze_temporal_anchoring(self) -> Dict:
        """Analyze temporal focus."""
        past_indicators = ['was', 'were', 'had', 'did', 'used to', 'remember', 'back then', 
                          'previously', 'before', 'yesterday', 'last', 'ago', 'history']
        present_indicators = ['is', 'are', 'now', 'today', 'currently', 'right now', 
                             'at this moment', 'these days', 'nowadays']
        future_indicators = ['will', 'going to', 'gonna', 'shall', 'tomorrow', 'soon', 
                            'eventually', 'later', 'next', 'future', 'upcoming']
        
        past_count = sum(1 for word in self.words if word in past_indicators)
        present_count = sum(1 for word in self.words if word in present_indicators)
        future_count = sum(1 for word in self.words if word in future_indicators)
        
        total_temporal = past_count + present_count + future_count
        
        return {
            "past_focus": past_count,
            "present_focus": present_count,
            "future_focus": future_count,
            "past_percentage": round(past_count / total_temporal * 100, 1) if total_temporal > 0 else 0,
            "present_percentage": round(present_count / total_temporal * 100, 1) if total_temporal > 0 else 0,
            "future_percentage": round(future_count / total_temporal * 100, 1) if total_temporal > 0 else 0,
            "temporal_orientation": max(['past', 'present', 'future'], 
                                      key=lambda x: {'past': past_count, 'present': present_count, 'future': future_count}[x])
        }
    
    def analyze_sensory_anchors(self) -> Dict:
        """Identify sensory language patterns."""
        visual_words = ['see', 'look', 'watch', 'picture', 'imagine', 'visualize', 'appear', 
                       'show', 'view', 'observe', 'notice', 'glimpse', 'vision']
        auditory_words = ['hear', 'listen', 'sound', 'tell', 'say', 'speak', 'voice', 
                         'tone', 'ring', 'echo', 'whisper', 'loud', 'quiet']
        kinesthetic_words = ['feel', 'touch', 'grab', 'hold', 'push', 'pull', 'heavy', 
                           'light', 'smooth', 'rough', 'warm', 'cold', 'pressure']
        
        visual_count = sum(1 for word in self.words if word in visual_words)
        auditory_count = sum(1 for word in self.words if word in auditory_words)
        kinesthetic_count = sum(1 for word in self.words if word in kinesthetic_words)
        
        total_sensory = visual_count + auditory_count + kinesthetic_count
        
        return {
            "visual_count": visual_count,
            "auditory_count": auditory_count,
            "kinesthetic_count": kinesthetic_count,
            "dominant_sense": max(['visual', 'auditory', 'kinesthetic'], 
                                 key=lambda x: {'visual': visual_count, 'auditory': auditory_count, 'kinesthetic': kinesthetic_count}[x]),
            "sensory_richness": round(total_sensory / self.word_count * 100, 2)
        }
    
    def analyze_fear_vs_aspiration(self) -> Dict:
        """Analyze fear-based vs aspiration-based language."""
        fear_words = ['afraid', 'fear', 'danger', 'risk', 'threat', 'avoid', 'escape', 
                     'protect', 'defend', 'lose', 'miss', 'fail', 'mistake', 'regret',
                     'worried', 'anxious', 'scared', 'terrified']
        
        aspiration_words = ['achieve', 'success', 'grow', 'improve', 'goal', 'dream', 
                           'vision', 'opportunity', 'potential', 'possibility', 'win',
                           'gain', 'benefit', 'reward', 'accomplish', 'excel', 'thrive']
        
        fear_count = sum(1 for word in self.words if word in fear_words)
        aspiration_count = sum(1 for word in self.words if word in aspiration_words)
        
        total_motivation = fear_count + aspiration_count
        
        return {
            "fear_count": fear_count,
            "aspiration_count": aspiration_count,
            "fear_percentage": round(fear_count / total_motivation * 100, 1) if total_motivation > 0 else 0,
            "aspiration_percentage": round(aspiration_count / total_motivation * 100, 1) if total_motivation > 0 else 0,
            "motivation_style": "fear-based" if fear_count > aspiration_count else "aspiration-based"
        }
    
    def analyze_cadence_pacing(self) -> Dict:
        """Analyze sentence length and pacing."""
        sentence_lengths = [len(s.split()) for s in self.sentences]
        
        if not sentence_lengths:
            return {"error": "No sentences found"}
        
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        
        short_sentences = sum(1 for l in sentence_lengths if l < 8)
        medium_sentences = sum(1 for l in sentence_lengths if 8 <= l <= 20)
        long_sentences = sum(1 for l in sentence_lengths if l > 20)
        
        # Analyze rhythm changes
        rhythm_changes = 0
        for i in range(1, len(sentence_lengths)):
            diff = abs(sentence_lengths[i] - sentence_lengths[i-1])
            if diff > 10:  # Significant length change
                rhythm_changes += 1
        
        return {
            "avg_sentence_length": round(avg_length, 1),
            "shortest_sentence": min(sentence_lengths),
            "longest_sentence": max(sentence_lengths),
            "short_sentences": short_sentences,
            "medium_sentences": medium_sentences,
            "long_sentences": long_sentences,
            "rhythm_changes": rhythm_changes,
            "pacing_style": "punchy" if avg_length < 12 else "flowing" if avg_length > 18 else "balanced"
        }

def process_influencer_profile(input_file: Path, output_dir: Path) -> Dict:
    """Process a single influencer's raw language file."""
    influencer_name = input_file.stem.replace('-raw-language', '')
    print(f"\nAnalyzing {influencer_name}...")
    
    # Read the raw language file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just the transcript text (skip metadata)
    lines = content.split('\n')
    transcript_start = 0
    for i, line in enumerate(lines):
        if 'CLEANED TRANSCRIPT TEXT:' in line:
            transcript_start = i + 2
            break
    
    text = '\n'.join(lines[transcript_start:])
    
    # Initialize analyzer
    analyzer = LinguisticAnalyzer(text)
    
    # Run all analyses
    results = {
        "influencer": influencer_name,
        "word_count": analyzer.word_count,
        "sentence_count": len(analyzer.sentences),
        "identity_framing": analyzer.analyze_identity_framing(),
        "emotional_valence": analyzer.analyze_emotional_valence(),
        "metaphors": analyzer.analyze_metaphors(),
        "repetition": analyzer.analyze_repetition(),
        "pronouns": analyzer.analyze_pronouns(),
        "rhetorical_devices": analyzer.analyze_rhetorical_devices(),
        "temporal_anchoring": analyzer.analyze_temporal_anchoring(),
        "sensory_anchors": analyzer.analyze_sensory_anchors(),
        "fear_vs_aspiration": analyzer.analyze_fear_vs_aspiration(),
        "cadence_pacing": analyzer.analyze_cadence_pacing()
    }
    
    # Create output filename
    output_file = output_dir / f"{influencer_name}-linguistic-patterns.json"
    
    # Write JSON results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Also create a human-readable report
    report_file = output_dir / f"{influencer_name}-linguistic-report.txt"
    create_readable_report(results, report_file)
    
    print(f"  ✅ Created: {output_file.name}")
    print(f"  ✅ Created: {report_file.name}")
    
    return results

def create_readable_report(results: Dict, output_file: Path):
    """Create a human-readable report of the linguistic analysis."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"LINGUISTIC PATTERN ANALYSIS: {results['influencer'].replace('-', ' ').title()}\n")
        f.write("=" * 70 + "\n\n")
        
        # Identity Framing
        f.write("1. IDENTITY FRAMING\n")
        f.write("-" * 40 + "\n")
        id_frame = results['identity_framing']
        f.write(f"Primary Frame: {id_frame['primary_frame']}\n")
        f.write(f"  YOU-focused: {id_frame['you_percentage']}% ({id_frame['you_focused']} instances)\n")
        f.write(f"  I-focused: {id_frame['i_percentage']}% ({id_frame['i_focused']} instances)\n")
        f.write(f"  WE-focused: {id_frame['we_percentage']}% ({id_frame['we_focused']} instances)\n\n")
        
        # Emotional Valence
        f.write("2. EMOTIONAL VALENCE & AROUSAL\n")
        f.write("-" * 40 + "\n")
        emo = results['emotional_valence']
        f.write(f"Emotional Tone: {emo['emotional_tone'].upper()}\n")
        f.write(f"Arousal Level: {emo['arousal_level'].upper()}\n")
        f.write(f"  Positivity Ratio: {emo['positivity_ratio']}\n")
        f.write(f"  Urgency Ratio: {emo['urgency_ratio']}\n\n")
        
        # Metaphors
        f.write("3. METAPHORICAL FRAMES\n")
        f.write("-" * 40 + "\n")
        meta = results['metaphors']
        f.write(f"Dominant Metaphor: {meta['dominant_metaphor'].upper()}\n")
        f.write("Metaphor Usage:\n")
        for m, count in meta['metaphor_counts'].items():
            if count > 0:
                f.write(f"  {m}: {count} references\n")
        f.write("\n")
        
        # Signature Phrases
        f.write("4. SIGNATURE PHRASES\n")
        f.write("-" * 40 + "\n")
        rep = results['repetition']
        f.write("Top 3-word patterns:\n")
        for phrase, count in rep['signature_phrases']:
            f.write(f"  \"{phrase}\" - {count}x\n")
        f.write("\n")
        
        # Pronouns
        f.write("5. PRONOUN PROFILE\n")
        f.write("-" * 40 + "\n")
        pro = results['pronouns']
        f.write(f"Profile: {pro['pronoun_profile']}\n")
        f.write(f"  I/me/my: {pro['i_ratio']}% of words\n")
        f.write(f"  You/your: {pro['you_ratio']}% of words\n")
        f.write(f"  We/us/our: {pro['we_ratio']}% of words\n\n")
        
        # Rhetorical Devices
        f.write("6. RHETORICAL DEVICES\n")
        f.write("-" * 40 + "\n")
        rhet = results['rhetorical_devices']
        f.write(f"Contrast Patterns: {rhet['contrast_patterns']}\n")
        f.write(f"Questions: {rhet['questions_total']} (Rhetorical: {rhet['rhetorical_questions']})\n")
        f.write(f"Numbered Lists: {rhet['numbered_lists']}\n")
        f.write(f"Imperatives: {rhet['imperatives']}\n")
        f.write(f"Rhetorical Density: {rhet['rhetorical_density']}\n\n")
        
        # Temporal Anchoring
        f.write("7. TEMPORAL ANCHORING\n")
        f.write("-" * 40 + "\n")
        temp = results['temporal_anchoring']
        f.write(f"Primary Orientation: {temp['temporal_orientation'].upper()}\n")
        f.write(f"  Past: {temp['past_percentage']}%\n")
        f.write(f"  Present: {temp['present_percentage']}%\n")
        f.write(f"  Future: {temp['future_percentage']}%\n\n")
        
        # Sensory Anchors
        f.write("8. SENSORY ANCHORS\n")
        f.write("-" * 40 + "\n")
        sens = results['sensory_anchors']
        f.write(f"Dominant Sense: {sens['dominant_sense'].upper()}\n")
        f.write(f"  Visual: {sens['visual_count']} references\n")
        f.write(f"  Auditory: {sens['auditory_count']} references\n")
        f.write(f"  Kinesthetic: {sens['kinesthetic_count']} references\n")
        f.write(f"Sensory Richness: {sens['sensory_richness']}%\n\n")
        
        # Fear vs Aspiration
        f.write("9. FEAR VS ASPIRATION\n")
        f.write("-" * 40 + "\n")
        fear = results['fear_vs_aspiration']
        f.write(f"Motivation Style: {fear['motivation_style'].upper()}\n")
        f.write(f"  Fear-based: {fear['fear_percentage']}%\n")
        f.write(f"  Aspiration-based: {fear['aspiration_percentage']}%\n\n")
        
        # Cadence & Pacing
        f.write("10. CADENCE & PACING\n")
        f.write("-" * 40 + "\n")
        pace = results['cadence_pacing']
        f.write(f"Pacing Style: {pace['pacing_style'].upper()}\n")
        f.write(f"Average Sentence Length: {pace['avg_sentence_length']} words\n")
        f.write(f"  Short (<8 words): {pace['short_sentences']}\n")
        f.write(f"  Medium (8-20 words): {pace['medium_sentences']}\n")
        f.write(f"  Long (>20 words): {pace['long_sentences']}\n")
        f.write(f"Rhythm Changes: {pace['rhythm_changes']}\n")

def main():
    """Main function to process all influencer profiles."""
    # Set up paths
    base_path = Path('/Users/vincentquarles/Documents/day-4-SubstackAnalysis')
    input_dir = base_path / 'influencer-data' / 'creator-raw-language'
    output_dir = base_path / 'influencer-data' / 'linguistic-patterns'
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Process each raw language file
    results = []
    for raw_file in input_dir.glob("*-raw-language.txt"):
        result = process_influencer_profile(raw_file, output_dir)
        results.append(result)
    
    # Print summary
    print("\n" + "=" * 70)
    print("LINGUISTIC ANALYSIS COMPLETE")
    print("=" * 70)
    
    for result in results:
        name = result['influencer'].replace('-', ' ').title()
        print(f"\n{name}:")
        print(f"  Primary Frame: {result['identity_framing']['primary_frame']}")
        print(f"  Pronoun Profile: {result['pronouns']['pronoun_profile']}")
        print(f"  Emotional Tone: {result['emotional_valence']['emotional_tone']}")
        print(f"  Dominant Metaphor: {result['metaphors']['dominant_metaphor']}")
        print(f"  Temporal Focus: {result['temporal_anchoring']['temporal_orientation']}")
        print(f"  Motivation Style: {result['fear_vs_aspiration']['motivation_style']}")
    
    print(f"\nOutput files saved to: {output_dir}")

if __name__ == "__main__":
    main()