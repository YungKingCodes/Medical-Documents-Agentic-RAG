import os
from typing import Dict, Any, List, Optional
import openai
from app.core.config import settings
from app.services.llm.base_service import BaseLLMService, BaseEmbeddingService, LLMServiceError

class AzureOpenAIService(BaseLLMService):
    """Service for interacting with Azure OpenAI's API."""
    
    DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
    
    def __init__(self):
        self._setup_azure_openai()
        self.client = openai.AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        # Use deployment name if provided, otherwise use the model value
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT or settings.AZURE_OPENAI_MODEL.value
    
    def _setup_azure_openai(self):
        """Configure the Azure OpenAI with settings."""
        if not settings.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY environment variable is not set")
        if not settings.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is not set")
    
    def generate_text(
        self, 
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using Azure OpenAI.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt to override default
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Dict containing the generated text and metadata
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt or self.DEFAULT_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Extract text from response
            text = response.choices[0].message.content
            
            return {
                "text": text,
                "processed_successfully": True,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            # Handle any errors from the API
            raise LLMServiceError(f"Azure OpenAI service error: {str(e)}")

class AzureOpenAIEmbeddingService(BaseEmbeddingService):
    """Service for generating embeddings with Azure OpenAI."""
    
    def __init__(self):
        self._setup_azure_openai()
        # Use a dedicated embedding API key if available, otherwise fall back to the main API key
        api_key = settings.AZURE_OPENAI_EMBEDDINGS_API_KEY or settings.AZURE_OPENAI_API_KEY
        
        # Use a dedicated embedding endpoint if available, otherwise fall back to the main endpoint
        endpoint = settings.AZURE_OPENAI_EMBEDDING_ENDPOINT or settings.AZURE_OPENAI_ENDPOINT
        
        self.client = openai.AzureOpenAI(
            api_key=api_key,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=endpoint
        )
        # Use deployment name if provided, otherwise use the model value
        self.deployment_name = settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT or settings.AZURE_OPENAI_EMBEDDING_MODEL.value
    
    def _setup_azure_openai(self):
        """Configure the Azure OpenAI with settings."""
        # Check if either the embedding-specific API key or the main API key is set
        if not (settings.AZURE_OPENAI_EMBEDDINGS_API_KEY or settings.AZURE_OPENAI_API_KEY):
            raise ValueError("Neither AZURE_OPENAI_EMBEDDINGS_API_KEY nor AZURE_OPENAI_API_KEY environment variable is set")
            
        # Check if either the embedding-specific endpoint or the main endpoint is set
        if not (settings.AZURE_OPENAI_EMBEDDING_ENDPOINT or settings.AZURE_OPENAI_ENDPOINT):
            raise ValueError("Neither AZURE_OPENAI_EMBEDDING_ENDPOINT nor AZURE_OPENAI_ENDPOINT environment variable is set")
    
    def generate_embeddings(
        self,
        texts: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate embeddings for the provided texts.
        
        Args:
            texts: List of texts to generate embeddings for
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Dict containing the embeddings and metadata
        """
        try:
            response = self.client.embeddings.create(
                model=self.deployment_name,
                input=texts,
                **kwargs
            )
            
            # Extract embeddings from response
            embeddings = [item.embedding for item in response.data]
            
            return {
                "embeddings": embeddings,
                "processed_successfully": True,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            # Handle any errors from the API
            raise LLMServiceError(f"Azure OpenAI embedding service error: {str(e)}") 