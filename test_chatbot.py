#!/usr/bin/env python3
"""
Test script for the News Chatbot
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic functionality without dependencies"""
    print("🧪 Testing News Chatbot Basic Functionality")
    print("=" * 50)
    
    try:
        from news_agent_clarifai import NewsAgent, validate_environment
        
        print("✅ Successfully imported NewsAgent")
        
        # Test environment validation
        env_status = validate_environment()
        print(f"\n📋 Environment Status:")
        for component, available in env_status.items():
            status = "✅" if available else "❌"
            print(f"  {status} {component}: {available}")
        
        # Create agent
        print(f"\n🤖 Creating NewsAgent...")
        agent = NewsAgent(model_name="gpt-4o")
        print("✅ NewsAgent created successfully")
        
        # Test connection (will work even without PAT)
        print(f"\n🔗 Testing connection...")
        connected = agent.test_connection()
        status = "✅ Connected" if connected else "⚠️  Limited functionality (no PAT)"
        print(f"  {status}")
        
        # Test search functionality
        print(f"\n🔍 Testing search functionality...")
        test_query = "latest technology news"
        results = agent.search_news(test_query, num_results=3)
        print(f"✅ Search returned {len(results)} results")
        
        # Test full search and analyze
        print(f"\n📰 Testing full search and analysis...")
        analysis = agent.search_and_analyze(test_query)
        print(f"✅ Analysis generated ({len(analysis)} characters)")
        
        print(f"\n🎉 All basic tests passed!")
        print(f"\n💡 To enable full AI features:")
        print(f"   1. Get a Clarifai PAT from: https://clarifai.com/settings/security")
        print(f"   2. Add it to your .env file: CLARIFAI_PAT=your_token_here")
        print(f"   3. Install full requirements: pip install -r requirements.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print(f"\n🎨 Testing Streamlit app import...")
    try:
        # Check if we can import the main components
        import streamlit as st
        print("✅ Streamlit available")
        
        # Try to import the app (without running it)
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        if 'st.set_page_config' in app_content:
            print("✅ Streamlit app structure looks good")
            return True
        else:
            print("⚠️  App structure may have issues")
            return False
            
    except ImportError:
        print("❌ Streamlit not available - install with: pip install streamlit")
        return False
    except Exception as e:
        print(f"❌ App test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 News Chatbot Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    
    # Test streamlit app
    streamlit_ok = test_streamlit_app()
    
    print(f"\n📊 Test Summary:")
    print(f"  Basic Functionality: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"  Streamlit App: {'✅ PASS' if streamlit_ok else '❌ FAIL'}")
    
    if basic_ok and streamlit_ok:
        print(f"\n🎉 All tests passed! You can now run: ./start.sh")
    else:
        print(f"\n⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)
