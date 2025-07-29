#!/usr/bin/env python3
"""
Quick Clarifai connection test
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_clarifai_simple():
    """Simple test of Clarifai connection"""
    print("🧪 Testing Clarifai Connection")
    print("=" * 40)
    
    # Check environment
    clarifai_pat = os.getenv('CLARIFAI_PAT')
    print(f"CLARIFAI_PAT present: {bool(clarifai_pat)}")
    print(f"PAT length: {len(clarifai_pat) if clarifai_pat else 0}")
    print(f"PAT starts with: {clarifai_pat[:10] + '...' if clarifai_pat and len(clarifai_pat) > 10 else 'N/A'}")
    
    # Test LiteLLM availability
    try:
        import litellm
        from litellm import completion
        
        # Enable debug mode
        litellm.set_verbose = True
        litellm._turn_on_debug()
        
        print("✅ LiteLLM available (debug mode enabled)")
        
        # Test simple completion
        try:
            from litellm import completion
            
            # Set environment variable for LiteLLM
            if clarifai_pat:
                os.environ['CLARIFAI_PAT'] = clarifai_pat
            
            print("\n🚀 Testing Clarifai API call...")
            
            # Test with different models from Clarifai examples
            models_to_try = [
                "openai/gcp/generate/models/gemini-2_5-flash",
                "openai/openai/chat-completion/models/gpt-4o",
                "openai/deepseek-ai/deepseek-chat/models/DeepSeek-R1-Distill-Qwen-7B"
            ]
            
            for model in models_to_try:
                try:
                    print(f"Trying model: {model}")
                    response = completion(
                        model=model,
                        messages=[{"role": "user", "content": "Say 'Hello!'"}],
                        max_tokens=20,
                        base_url="https://api.clarifai.com/v2/ext/openai/v1",
                        api_key=clarifai_pat,
                        stream=False  # Explicitly disable streaming
                    )
                    print(f"✅ Success with {model}!")
                    print(f"Response: {response.choices[0].message.content}")
                    return True
                except Exception as e:
                    print(f"❌ Failed with {model}: {str(e)}")
                    continue
            
            print("❌ All models failed")
            return False
            
        except Exception as e:
            print(f"❌ API call failed: {str(e)}")
            print("This might be due to:")
            print("- Invalid PAT")
            print("- Network issues")
            print("- Model not available")
            return False
            
    except ImportError:
        print("❌ LiteLLM not available")
        print("Install with: pip install litellm")
        return False

if __name__ == "__main__":
    test_clarifai_simple()
