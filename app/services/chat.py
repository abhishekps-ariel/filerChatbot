from openai import OpenAI
from typing import List, Tuple
from app.config import get_settings
from app.models import DocumentChunk

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


class ChatService:
    """Service for generating answers using OpenAI."""
    
    def __init__(self):
        self.model = settings.openai_model
    
    def generate_answer(
        self,
        question: str,
        context_chunks: List[Tuple[DocumentChunk, float]]
    ) -> str:
        """
        Generate answer using retrieved context and OpenAI.
        
        Args:
            question: User's question
            context_chunks: List of (DocumentChunk, similarity_score) tuples
            
        Returns:
            Generated answer
        """
        # Build context from chunks
        context = self._build_context(context_chunks)
        
        # Create system and user messages
        system_message = """You are FILIR Bot, a helpful AI assistant for the Massachusetts foreclosure petition filing system.

Your role:
- Help users understand the petition process, requirements, and system features
- Answer questions clearly and concisely in a friendly, professional tone
- Keep answers brief (2-4 sentences max) - users prefer short, direct answers
- Use bullet points for steps or lists to save space
- Never mention "context", "documents", "provided information", or reveal that you're using retrieved data
- If you don't have enough information to answer, politely say "I don't have information about that specific topic. Could you ask about petition filing, statuses, or system features?"
-You are a conversational assistant.
-Prioritize natural dialogue, continuity, and helpfulness.
-Respond succinctly, but not abruptly.
-Acknowledge user intent before answering.
-Ask clarifying questions only when necessary.
Avoid robotic or enumerated responses unless asked.
- For greetings like "hi" or "hello", respond warmly and offer to help with petition questions"""

        user_message = f"""Use this information to answer:
{context}

User question: {question}

Your response (be natural, helpful, and BRIEF):"""
        
        # Call OpenAI
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
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
