"""
QuestionGenerator class with proper imports and type handling.
"""
import random
from typing import List, Dict, Optional, Any, Union
from config.settings import settings

# Import with proper error handling and type ignoring for Pylance
try:
    import google.generativeai as genai  # type: ignore[import]
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None


class QuestionGenerator:
    """Generate and evaluate questions based on document content using Google's Gemini AI."""
    
    def __init__(self):
        if not GENAI_AVAILABLE:
            raise ImportError("google.generativeai package is not installed. Please install it with: pip install google-generativeai")
        
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file")
        
        # Configure and initialize with proper type handling
        genai.configure(api_key=settings.GEMINI_API_KEY)  # type: ignore[attr-defined]
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)  # type: ignore[attr-defined]
        
        self.question_types = [
            "comprehension", "inference", "analysis", "evaluation"
        ]
    
    def generate_challenge_questions(self, document_text: str) -> List[Dict[str, Any]]:
        """Generate 3 challenging questions based on document content."""
        try:
            prompt = self._create_question_prompt(document_text)
            
            # Dictionary approach works better with current package versions
            generation_config: Any = {
                'max_output_tokens': 800,
                'temperature': 0.5,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config  # type: ignore[arg-type]
            )
            
            questions_text = response.text if response.text else ""
            questions = self._parse_questions(questions_text)
            return questions
            
        except Exception as e:
            print(f"Error generating questions: {e}")  # For debugging
            # Fallback questions if API fails
            return self._generate_fallback_questions(document_text)
    
    def evaluate_answer(self, question: str, user_answer: str, 
                       document_text: str, correct_answer: str) -> Dict[str, Union[int, str]]:
        """Evaluate user's answer and provide feedback."""
        try:
            prompt = f"""
            Document excerpt: {document_text[:1000]}...
            
            Question: {question}
            Expected answer: {correct_answer}
            User's answer: {user_answer}
            
            Evaluate the user's answer on a scale of 1-5 and provide constructive feedback.
            Consider:
            1. Accuracy compared to document content
            2. Completeness of the response
            3. Understanding demonstrated
            
            Format your response as:
            Score: [1-5]
            Feedback: [Your detailed feedback]
            Justification: [Reference to specific document content]
            """
            
            generation_config: Any = {
                'max_output_tokens': 400,
                'temperature': 0.3,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config  # type: ignore[arg-type]
            )
            
            evaluation = response.text if response.text else ""
            return self._parse_evaluation(evaluation)
            
        except Exception as e:
            print(f"Error evaluating answer: {e}")  # For debugging
            return {
                "score": 3,
                "feedback": "Unable to evaluate answer at this time.",
                "justification": "System error occurred during evaluation."
            }
    
    def _create_question_prompt(self, document_text: str) -> str:
        """Create prompt for question generation."""
        text_excerpt = document_text[:2000]  # Limit for token efficiency
        
        return f"""
        Based on the following document, generate exactly 3 challenging questions that test comprehension, inference, and analysis.
        
        Document: {text_excerpt}
        
        Create questions that:
        1. Require understanding of key concepts
        2. Test ability to make inferences
        3. Analyze relationships between ideas
        
        Format each question as:
        Q1: [Question]
        A1: [Expected answer based on document]
        
        Q2: [Question]
        A2: [Expected answer based on document]
        
        Q3: [Question]
        A3: [Expected answer based on document]
        """
    
    def _parse_questions(self, questions_text: str) -> List[Dict[str, Any]]:
        """Parse generated questions into structured format."""
        questions: List[Dict[str, Any]] = []
        lines = questions_text.strip().split('\n')
        
        current_q: Optional[str] = None
        current_a: Optional[str] = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q') and ':' in line:
                if current_q and current_a:
                    questions.append({
                        "question": current_q,
                        "expected_answer": current_a,
                        "type": random.choice(self.question_types)
                    })
                current_q = line.split(':', 1)[1].strip()
                current_a = None
            elif line.startswith('A') and ':' in line and current_q:
                current_a = line.split(':', 1)[1].strip()
        
        # Add the last question if exists
        if current_q and current_a:
            questions.append({
                "question": current_q,
                "expected_answer": current_a,
                "type": random.choice(self.question_types)
            })
        
        return questions[:3]  # Ensure only 3 questions
    
    def _parse_evaluation(self, evaluation_text: str) -> Dict[str, Union[int, str]]:
        """Parse evaluation response into structured format."""
        result: Dict[str, Union[int, str]] = {"score": 3, "feedback": "", "justification": ""}
        
        for line in evaluation_text.split('\n'):
            line = line.strip()
            if line.startswith('Score:'):
                try:
                    score_text = line.split(':')[1].strip()
                    # Handle cases like "Score: 4/5" or "Score: 4"
                    score = int(score_text.split('/')[0])
                    result["score"] = max(1, min(5, score))
                except (ValueError, IndexError):
                    pass
            elif line.startswith('Feedback:'):
                result["feedback"] = line.split(':', 1)[1].strip()
            elif line.startswith('Justification:'):
                result["justification"] = line.split(':', 1)[1].strip()
        
        return result
    
    def _generate_fallback_questions(self, document_text: str) -> List[Dict[str, Any]]:
        """Generate simple fallback questions if API fails."""
        return [
            {
                "question": "What are the main topics discussed in this document?",
                "expected_answer": "Based on the document content, identify key themes and subjects.",
                "type": "comprehension"
            },
            {
                "question": "What conclusions can be drawn from the information presented?",
                "expected_answer": "Analyze the evidence and reasoning to identify logical conclusions.",
                "type": "inference"
            },
            {
                "question": "How do the different sections of this document relate to each other?",
                "expected_answer": "Examine the structure and connections between different parts.",
                "type": "analysis"
            }
        ]
    
    def validate_api_key(self) -> bool:
        """Validate if the Gemini API key is working."""
        try:
            # Test with a simple prompt
            response = self.model.generate_content("Hello, this is a test.")
            return response is not None and hasattr(response, 'text')
        except Exception as e:
            print(f"Gemini API key validation failed: {str(e)}")
            return False
    
    def get_question_statistics(self, questions: List[Dict[str, Any]]) -> Dict[str, Union[int, Dict[str, int], float]]:
        """Get statistics about generated questions."""
        if not questions:
            return {"total": 0, "types": {}}
        
        type_counts: Dict[str, int] = {}
        for question in questions:
            q_type = question.get("type", "unknown")
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
        
        total_length = sum(len(str(q["question"])) for q in questions)
        avg_length = total_length / len(questions) if questions else 0
        
        return {
            "total": len(questions),
            "types": type_counts,
            "average_question_length": avg_length
        }