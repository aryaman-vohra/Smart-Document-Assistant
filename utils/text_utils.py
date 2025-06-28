import re
from typing import List

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    return text

def chunk_text(text: str, max_chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks for better processing."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_chunk_size - overlap):
        chunk = ' '.join(words[i:i + max_chunk_size])
        chunks.append(chunk)
        
        if i + max_chunk_size >= len(words):
            break
    
    return chunks

def extract_key_sentences(text: str, num_sentences: int = 5) -> List[str]:
    """Extract key sentences for summary generation."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Simple heuristic: prefer sentences with common important words
    important_words = ['conclusion', 'result', 'finding', 'important', 'significant', 'main', 'key']
    
    scored_sentences = []
    for sentence in sentences:
        score = sum(1 for word in important_words if word.lower() in sentence.lower())
        scored_sentences.append((score, sentence))
    
    # Sort by score and length, return top sentences
    scored_sentences.sort(key=lambda x: (x[0], len(x[1])), reverse=True)
    return [sent[1] for sent in scored_sentences[:num_sentences]]