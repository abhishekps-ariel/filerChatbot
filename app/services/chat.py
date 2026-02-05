import google.generativeai as genai
from typing import List, Tuple
from app.config import get_settings
from app.models import DocumentChunk

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)


class ChatService:
    """Service for generating answers using Google Gemini."""
    
    def __init__(self):
        self.model = genai.GenerativeModel(settings.gemini_model)
    
    def generate_answer(
        self,
        question: str,
        context_chunks: List[Tuple[DocumentChunk, float]]
    ) -> str:
        """
        Generate answer using retrieved context and Gemini.
        
        Args:
            question: User's question
            context_chunks: List of (DocumentChunk, similarity_score) tuples
            
        Returns:
            Generated answer
        """
        # Build context from chunks
        context = self._build_context(context_chunks)
        
        # Create prompt for Gemini
        prompt = f"""You are FILIR Bot, a helpful AI assistant for the Massachusetts foreclosure petition filing system.

Your role:
- Help users understand the petition process, requirements, and system features
- Answer questions clearly and concisely in a friendly, professional tone
- Keep answers brief (2-4 sentences max) - users prefer short, direct answers
- Use bullet points for steps or lists to save space
- Never mention "context", "documents", "provided information", or reveal that you're using retrieved data
- If you don't have enough information to answer, politely say "I don't have information about that specific topic. Could you ask about petition filing, statuses, or system features?"
- For greetings like "hi" or "hello", respond warmly and offer to help with petition questions

Use this information to answer:
{context}

User question: {question}

Your response (be natural, helpful, and BRIEF):"""
        
        # Call Gemini
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise ValueError(f"Failed to generate answer: {str(e)}")
    
    def _build_context(self, chunks: List[Tuple[DocumentChunk, float]]) -> str:
        """Build context string from chunks."""
        if not chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, (chunk, score) in enumerate(chunks, 1):
            context_parts.append(
                f"[Source {i} - {chunk.document_name} (Relevance: {score:.2f})]:\n{chunk.chunk_text}"
            )
        
        return "\n\n".join(context_parts)
