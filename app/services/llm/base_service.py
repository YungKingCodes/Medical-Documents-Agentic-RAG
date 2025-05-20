from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class LLMServiceError(Exception):
    """Base exception for LLM service errors."""
    pass

class LLMServiceUnavailableError(LLMServiceError):
    """Exception raised when a requested LLM service is unavailable."""
    pass

class BaseLLMService(ABC):
    """Abstract base class for LLM services."""
    
    @abstractmethod
    def generate_text(
        self, 
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text based on the provided prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Dict containing the generated text and metadata
        """
        pass

class BaseEmbeddingService(ABC):
    """Abstract base class for embedding services."""
    
    @abstractmethod
    def generate_embeddings(
        self,
        texts: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate embeddings for the provided texts.
        
        Args:
            texts: List of texts to generate embeddings for
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Dict containing the embeddings and metadata
        """
        pass 