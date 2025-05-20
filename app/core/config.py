import os
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum

# Load environment variables from .env file
load_dotenv()

class AzureOpenAIModelEnum(str, Enum):
    """Enum for Azure OpenAI models."""
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"

class AzureOpenAIEmbeddingModelEnum(str, Enum):
    """Enum for Azure OpenAI embedding models."""
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"

class Settings(BaseModel):
    """Application settings."""
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./documents.db")
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    APP_NAME: str = os.getenv("APP_NAME", "Document API")
    API_VERSION: str = "v1"
    
    # Security settings
    API_KEY: str = os.getenv("API_KEY", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    
    # Azure OpenAI settings
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_EMBEDDINGS_API_KEY: str = os.getenv("AZURE_OPENAI_EMBEDDINGS_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_EMBEDDING_ENDPOINT: str = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    
    # Azure OpenAI model settings
    AZURE_OPENAI_MODEL: AzureOpenAIModelEnum = AzureOpenAIModelEnum(
        os.getenv("AZURE_OPENAI_MODEL", AzureOpenAIModelEnum.GPT_4O_MINI)
    )
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")  # If specified, overrides the model
    
    # Azure OpenAI embedding model settings
    AZURE_OPENAI_EMBEDDING_MODEL: AzureOpenAIEmbeddingModelEnum = AzureOpenAIEmbeddingModelEnum(
        os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", AzureOpenAIEmbeddingModelEnum.TEXT_EMBEDDING_3_LARGE)
    )
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "")  # If specified, overrides the model

# Create settings instance
settings = Settings() 