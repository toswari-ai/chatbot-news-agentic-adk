"""
Configuration helper for News Chatbot
"""

import os
from typing import Dict, List, Optional

def get_config() -> Dict:
    """Get current configuration"""
    return {
        "clarifai_pat": os.getenv('CLARIFAI_PAT', ''),
        "clarifai_api_base": os.getenv('CLARIFAI_API_BASE', 'https://api.clarifai.com/v2'),
        "streamlit_port": int(os.getenv('STREAMLIT_SERVER_PORT', 8501)),
        "streamlit_host": os.getenv('STREAMLIT_SERVER_ADDRESS', 'localhost'),
    }

def is_clarifai_configured() -> bool:
    """Check if Clarifai is properly configured"""
    pat = os.getenv('CLARIFAI_PAT', '')
    return bool(pat and pat != 'your_clarifai_personal_access_token_here')

def get_available_models() -> List[str]:
    """Get list of available models"""
    return [
        "gpt-4o",
        "gpt-4o-mini", 
        "claude-3-5-sonnet-20241022",
        "meta-llama/Meta-Llama-3.1-8B-Instruct"
    ]

def get_model_info(model_name: str) -> Dict:
    """Get information about a specific model"""
    model_info = {
        "gpt-4o": {
            "provider": "OpenAI",
            "description": "Advanced reasoning and analysis",
            "speed": "Medium",
            "cost": "High"
        },
        "gpt-4o-mini": {
            "provider": "OpenAI", 
            "description": "Fast responses, cost-effective",
            "speed": "Fast",
            "cost": "Low"
        },
        "claude-3-5-sonnet-20241022": {
            "provider": "Anthropic",
            "description": "Detailed analysis and reasoning",
            "speed": "Medium",
            "cost": "Medium"
        },
        "meta-llama/Meta-Llama-3.1-8B-Instruct": {
            "provider": "Meta",
            "description": "Open source, customizable",
            "speed": "Fast", 
            "cost": "Low"
        }
    }
    
    return model_info.get(model_name, {
        "provider": "Unknown",
        "description": "Custom model",
        "speed": "Unknown",
        "cost": "Unknown"
    })

def validate_setup() -> Dict[str, bool]:
    """Validate the current setup"""
    try:
        import streamlit
        streamlit_ok = True
    except ImportError:
        streamlit_ok = False
    
    try:
        import requests
        requests_ok = True
    except ImportError:
        requests_ok = False
    
    try:
        from dotenv import load_dotenv
        dotenv_ok = True
    except ImportError:
        dotenv_ok = False
    
    try:
        import litellm
        litellm_ok = True
    except ImportError:
        litellm_ok = False
    
    try:
        from google import genai
        google_adk_ok = True
    except ImportError:
        google_adk_ok = False
    
    return {
        "streamlit": streamlit_ok,
        "requests": requests_ok,
        "python_dotenv": dotenv_ok,
        "litellm": litellm_ok,
        "google_adk": google_adk_ok,
        "clarifai_configured": is_clarifai_configured()
    }
