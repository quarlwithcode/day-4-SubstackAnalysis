#!/usr/bin/env python3
"""
Generate Creator Language Profiles
Combines all transcripts for each influencer, removes filler words,
and creates clean language files for pattern analysis.
"""

import os
import re
from pathlib import Path
from typing import List, Set
from collections import Counter

# Common filler words to remove
FILLER_WORDS = {
    'um', 'uh', 'er', 'ah', 'like', 'you know', 'I mean', 'actually', 
    'basically', 'literally', 'honestly', 'right', 'so', 'well', 'okay',
    'just', 'really', 'very', 'quite', 'pretty', 'kind of', 'sort of',
    'you see', 'you know what', 'let me tell you', 'to be honest',
    'at the end of the day', 'the thing is', 'I guess', 'I suppose',
    'you know what I mean', 'and stuff', 'and things', 'whatever',
    'anyway', 'anyhow', 'I think', 'I feel', 'I believe'
}

# Additional stop words for cleaner analysis
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'can', 'shall'
}

def clean_text(text: str, remove_stop_words: bool = False) -> str:
    """
    Clean text by removing filler words and optionally stop words.
    """
    # Convert to lowercase for processing
    text_lower = text.lower()
    
    # Remove filler phrases (multi-word)
    for filler in FILLER_WORDS:
        if ' ' in filler:  # Multi-word filler
            text_lower = re.sub(r'\b' + re.escape(filler) + r'\b', '', text_lower, flags=re.IGNORECASE)
    
    # Split into words
    words = text_lower.split()
    
    # Remove single-word fillers
    single_fillers = {f.lower() for f in FILLER_WORDS if ' ' not in f}
    words = [w for w in words if w not in single_fillers]
    
    # Optionally remove stop words
    if remove_stop_words:
        words = [w for w in words if w not in STOP_WORDS]
    
    # Clean up extra spaces and punctuation
    text = ' '.join(words)
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)  # Remove space before punctuation
    
    return text.strip()

def extract_key_phrases(text: str, min_length: int = 3, top_n: int = 50) -> List[tuple]:
    """
    Extract key phrases (n-grams) from text.
    """
    # Clean the text first
    text = clean_text(text)
    words = text.lower().split()
    
    # Generate n-grams (phrases of min_length words)
    phrases = []
    for i in range(len(words) - min_length + 1):
        phrase = ' '.join(words[i:i + min_length])
        # Skip if contains only stop words
        phrase_words = set(phrase.split())
        if not phrase_words.issubset(STOP_WORDS):
            phrases.append(phrase)
    
    # Count frequency
    phrase_counts = Counter(phrases)
    
    # Return top phrases
    return phrase_counts.most_common(top_n)

def process_influencer_transcripts(influencer_path: Path, output_path: Path) -> dict:
    """
    Process all transcripts for a single influencer.
    """
    influencer_name = influencer_path.name
    print(f"\nProcessing {influencer_name}...")
    
    # Collect all transcript text
    all_text = []
    file_count = 0
    
    for transcript_file in influencer_path.glob("*.txt"):
        print(f"  Reading: {transcript_file.name}")
        with open(transcript_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Skip metadata lines (first few lines typically contain metadata)
            lines = content.split('\n')
            # Find where transcript actually starts (after separator)
            transcript_start = 0
            for i, line in enumerate(lines):
                if 'TRANSCRIPT' in line or '========' in line:
                    transcript_start = i + 1
                    break
            
            # Get just the transcript content
            transcript_text = '\n'.join(lines[transcript_start:])
            all_text.append(transcript_text)
            file_count += 1
    
    if not all_text:
        print(f"  No transcripts found for {influencer_name}")
        return None
    
    # Combine all text
    combined_text = '\n\n'.join(all_text)
    
    # Clean the text
    cleaned_text = clean_text(combined_text)
    
    # Calculate statistics
    original_words = len(combined_text.split())
    cleaned_words = len(cleaned_text.split())
    reduction_percent = ((original_words - cleaned_words) / original_words) * 100
    
    # Extract key phrases
    key_phrases = extract_key_phrases(cleaned_text)
    
    # Create output filename
    output_file = output_path / f"{influencer_name}-raw-language.txt"
    
    # Write cleaned text to file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Add metadata header
        f.write(f"CREATOR LANGUAGE PROFILE: {influencer_name.replace('-', ' ').title()}\n")
        f.write("=" * 60 + "\n")
        f.write(f"Source Files: {file_count} transcripts\n")
        f.write(f"Original Word Count: {original_words:,}\n")
        f.write(f"Cleaned Word Count: {cleaned_words:,}\n")
        f.write(f"Reduction: {reduction_percent:.1f}%\n")
        f.write("=" * 60 + "\n\n")
        
        # Add top key phrases
        f.write("TOP KEY PHRASES (3-word patterns):\n")
        f.write("-" * 40 + "\n")
        for phrase, count in key_phrases[:20]:
            f.write(f"{phrase}: {count} occurrences\n")
        f.write("\n" + "=" * 60 + "\n\n")
        
        # Add cleaned text
        f.write("CLEANED TRANSCRIPT TEXT:\n")
        f.write("=" * 60 + "\n\n")
        f.write(cleaned_text)
    
    print(f"  ✅ Created: {output_file.name}")
    print(f"     Original: {original_words:,} words")
    print(f"     Cleaned: {cleaned_words:,} words")
    print(f"     Reduction: {reduction_percent:.1f}%")
    
    return {
        'influencer': influencer_name,
        'file_count': file_count,
        'original_words': original_words,
        'cleaned_words': cleaned_words,
        'reduction_percent': reduction_percent,
        'top_phrases': key_phrases[:10],
        'output_file': str(output_file)
    }

def main():
    """
    Main function to process all influencer transcripts.
    """
    # Set up paths
    base_path = Path('/Users/vincentquarles/Documents/day-4-SubstackAnalysis')
    influencer_data_path = base_path / 'influencer-data'
    output_path = influencer_data_path / 'creator-raw-language'
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    print(f"Created output directory: {output_path}")
    
    # Process each influencer
    results = []
    influencers = [
        'dan-koe', 'greg-isenberg', 'alex-hormozi', 'gary-vaynerchuk',
        'david-ondrej', 'liam-ottley', 'matthew-lakajev', 'shan-hanif',
        'dan-martell', 'chris-do', 'ali-abdaal'
    ]
    
    for influencer_name in influencers:
        influencer_path = influencer_data_path / influencer_name
        if influencer_path.exists() and influencer_path.is_dir():
            result = process_influencer_transcripts(influencer_path, output_path)
            if result:
                results.append(result)
        else:
            print(f"⚠️  Skipping {influencer_name}: directory not found")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    
    total_original = sum(r['original_words'] for r in results)
    total_cleaned = sum(r['cleaned_words'] for r in results)
    total_reduction = ((total_original - total_cleaned) / total_original) * 100
    
    print(f"\nProcessed {len(results)} influencers:")
    for result in results:
        print(f"  • {result['influencer']}: {result['file_count']} files → {result['cleaned_words']:,} words")
    
    print(f"\nTotal Statistics:")
    print(f"  Original: {total_original:,} words")
    print(f"  Cleaned: {total_cleaned:,} words")
    print(f"  Overall Reduction: {total_reduction:.1f}%")
    
    print(f"\nOutput files saved to: {output_path}")
    
    # Print sample key phrases from each influencer
    print("\n" + "=" * 60)
    print("KEY PHRASE SAMPLES")
    print("=" * 60)
    
    for result in results:
        print(f"\n{result['influencer'].replace('-', ' ').title()}:")
        for phrase, count in result['top_phrases'][:5]:
            print(f"  • '{phrase}' ({count}x)")

if __name__ == "__main__":
    main()