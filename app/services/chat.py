from openai import OpenAI, AzureOpenAI
from typing import List, Tuple
from app.config import get_settings
from app.models import DocumentChunk

settings = get_settings()


class ChatService:
    """Service for generating answers using GPT-4o-mini or Azure OpenAI."""
    
    def __init__(self):
        if settings.use_azure:
            self.client = AzureOpenAI(
                api_key=settings.openai_api_key,
                azure_endpoint=settings.azure_endpoint,
                api_version=settings.azure_api_version
            )
            self.model = settings.azure_chat_deployment
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
    
    def generate_answer(
        self,
        question: str,
        context_chunks: List[Tuple[DocumentChunk, float]]
    ) -> str:
        """
        Generate answer using retrieved context and GPT-4o-mini.
        
        Args:
            question: User's question
            context_chunks: List of (DocumentChunk, similarity_score) tuples
            
        Returns:
            Generated answer
        """
        # Build context from chunks
        context = self._build_context(context_chunks)
        
        # Create prompt
        system_prompt = """You are a helpful assistant for the FILIR petition system. 
Answer questions based on the provided context from petition documents.
If the context doesn't contain enough information to answer the question, say so clearly.
Be concise and accurate."""
        
        user_prompt = f"""Context from petition documents:
{context}

Question: {question}

Answer based on the context above:"""
        
        # Call GPT-4o-mini
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            return answer.strip()
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
