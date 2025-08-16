export function cleanSubstackContent(content: string): string {
  // Remove HTML tags
  let cleaned = content.replace(/<[^>]*>/g, '');
  
  // Remove Substack-specific elements
  cleaned = cleaned.replace(/Subscribe now|View in browser|Share this post|Leave a comment/gi, '');
  cleaned = cleaned.replace(/Paid subscribers only/gi, '');
  cleaned = cleaned.replace(/This is a subscriber-only post/gi, '');
  
  // Remove common footer/header content
  cleaned = cleaned.replace(/^.*?Newsletter by.*?\n/gm, '');
  cleaned = cleaned.replace(/Subscribe to.*?$/gm, '');
  cleaned = cleaned.replace(/Unsubscribe.*?$/gm, '');
  
  // Remove URLs
  cleaned = cleaned.replace(/https?:\/\/[^\s]+/g, '');
  
  // Remove excessive whitespace
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n');
  cleaned = cleaned.replace(/\s{2,}/g, ' ');
  
  // Remove common Substack CTAs
  cleaned = cleaned.replace(/Sign up now|Start your free trial|Upgrade to paid/gi, '');
  cleaned = cleaned.replace(/Share|Comment|Like/gi, '');
  
  // Trim
  cleaned = cleaned.trim();
  
  return cleaned;
}

export function extractKeyPhrases(text: string): string[] {
  // Simple key phrase extraction
  const sentences = text.split(/[.!?]+/);
  const phrases: string[] = [];
  
  sentences.forEach(sentence => {
    // Extract phrases between 3-8 words that might be significant
    const words = sentence.trim().split(/\s+/);
    if (words.length >= 3 && words.length <= 8) {
      // Check if it contains power words or important concepts
      const powerWords = ['transform', 'success', 'growth', 'achieve', 'master', 'learn', 'build', 'create', 'improve'];
      if (powerWords.some(word => sentence.toLowerCase().includes(word))) {
        phrases.push(sentence.trim());
      }
    }
  });
  
  return phrases.slice(0, 10); // Return top 10 phrases
}