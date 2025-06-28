import os
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from typing import Dict, Optional, Any
from config.settings import settings
from utils.text_utils import chunk_text, extract_key_sentences
# pyright: reportPrivateImportUsage=false
import google.generativeai as genai


class AIAssistant:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key not found")
        
        self.conversation_history = []
        self._initialize_model()
    
    def _initialize_model(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def update_api_key(self, new_api_key: str):
        self.api_key = new_api_key
        self._initialize_model()
    
    def generate_summary(self, document_text: str) -> str:
        try:
            key_sentences = extract_key_sentences(document_text, 8)
            key_content = ' '.join(key_sentences)
            
            prompt = f"""
            Summarize the following document in exactly 150 words or less. Focus on:
            1. Main purpose/objective
            2. Key findings or points
            3. Important conclusions
            
            Document content: {key_content}
            """
            generation_config = GenerationConfig(
                max_output_tokens=200,
                temperature=0.3,
            )
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            content = response.text or ""
            words = content.strip().split()
            return ' '.join(words[:150]) + ("..." if len(words) > 150 else "")
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def answer_question(self, question: str, document_text: str) -> Dict[str, Any]:
        try:
            chunks = chunk_text(document_text, 1500, 150)
            best_chunk = self._find_relevant_chunk(question, chunks)
            
            prompt = f"""
            Based ONLY on the following document content, answer the user's question.

            Document content: {best_chunk}

            Question: {question}

            Instructions:
            1. Answer only based on the provided document content
            2. If the answer isn't in the document, say "The document doesn't contain information to answer this question"
            3. Provide the specific section/paragraph reference that supports your answer
            4. Be accurate and don't make assumptions beyond what's stated

            Format your response as:
            Answer: [Your answer]
            Reference: [Specific location in document that supports this answer]
            """
            generation_config = GenerationConfig(
                max_output_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
            )
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            parsed = self._parse_answer(response.text or "")
            self.conversation_history.append({
                "question": question,
                "answer": parsed["answer"],
                "reference": parsed["reference"]
            })
            return parsed
        
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "reference": "System error",
                "confidence": 0
            }

    def _find_relevant_chunk(self, question: str, chunks: list) -> str:
        question_words = set(question.lower().split())
        best_chunk, best_score = chunks[0], 0
        for chunk in chunks:
            overlap = len(question_words.intersection(set(chunk.lower().split())))
            if overlap > best_score:
                best_score, best_chunk = overlap, chunk
        return best_chunk

    def _parse_answer(self, answer_text: str) -> Dict[str, Any]:
        result = {"answer": "", "reference": "", "confidence": 0.8}
        for line in answer_text.splitlines():
            if line.startswith("Answer:"):
                result["answer"] = line.split(":", 1)[1].strip()
            elif line.startswith("Reference:"):
                result["reference"] = line.split(":", 1)[1].strip()
        if not result["answer"]:
            result["answer"] = answer_text.strip()
            result["reference"] = "General document content"
        return result

    def get_conversation_context(self) -> str:
        context = "Recent conversation:\n"
        for item in self.conversation_history[-3:]:
            context += f"Q: {item['question']}\nA: {item['answer']}\n\n"
        return context if self.conversation_history else ""

    def clear_history(self):
        self.conversation_history = []

    def validate_api_key(self) -> bool:
        try:
            self.model.generate_content("Hello, this is a test.")
            return True
        except Exception as e:
            print(f"Gemini API key validation failed: {str(e)}")
            return False
