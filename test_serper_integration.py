#!/usr/bin/env python3
"""
Test script for Serper API integration with MCP News Agent
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_serper_tool():
    """Test the Serper search tool directly"""
    print("🔍 Testing Serper Search Tool...")
    print("=" * 50)
    
    try:
        from serper_search_tool import SerperSearchTool
        
        # Create tool instance
        tool = SerperSearchTool()
        
        # Test connection
        print("📡 Testing API connection...")
        if tool.test_connection():
            print("✅ Serper API connection successful!")
        else:
            print("❌ Serper API connection failed!")
            return False
        
        # Test general search
        print("\n🔍 Testing general search...")
        results = tool.search("latest AI technology news 2024", num_results=3)
        formatted = tool.format_search_results(results)
        print(formatted[:800] + "..." if len(formatted) > 800 else formatted)
        
        # Test news search
        print("\n📰 Testing news search...")
        news_results = tool.search_news("artificial intelligence breakthrough", num_results=3)
        news_formatted = tool.format_search_results(news_results)
        print(news_formatted[:800] + "..." if len(news_formatted) > 800 else news_formatted)
        
        return True
        
    except Exception as e:
        print(f"❌ Serper tool test failed: {str(e)}")
        return False

def test_news_agent_integration():
    """Test Serper integration with NewsAgent"""
    print("\n🤖 Testing NewsAgent with Serper Integration...")
    print("=" * 50)
    
    try:
        from news_agent_clarifai import NewsAgent
        
        # Create agent
        agent = NewsAgent(model_name="gpt-4o")
        
        # Test search functionality
        print("🔍 Testing news search with agent...")
        results = agent.search_news("technology innovation 2024", num_results=3)
        
        print(f"✅ Found {len(results)} search results")
        for i, result in enumerate(results[:2], 1):
            print(f"\n{i}. {result.get('title', 'No title')}")
            print(f"   Source: {result.get('source', 'Unknown')}")
            print(f"   Engine: {result.get('search_engine', 'Unknown')}")
        
        # Test full search and analyze if Clarifai is configured
        if agent.clarifai_pat and agent.clarifai_pat != 'your_clarifai_personal_access_token_here':
            print("\n🧠 Testing full search and analysis...")
            analysis = agent.search_and_analyze("What are the latest developments in AI technology?")
            print("✅ Analysis completed successfully!")
            print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        else:
            print("\n⚠️ Skipping AI analysis test (CLARIFAI_PAT not configured)")
        
        return True
        
    except Exception as e:
        print(f"❌ NewsAgent integration test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Serper API Integration Tests")
    print("=" * 60)
    
    # Check environment variables
    serper_key = os.getenv('SERPER_API_KEY')
    clarifai_pat = os.getenv('CLARIFAI_PAT')
    
    print(f"🔑 SERPER_API_KEY: {'✅ Set' if serper_key else '❌ Not set'}")
    print(f"🔑 CLARIFAI_PAT: {'✅ Set' if clarifai_pat and clarifai_pat != 'your_clarifai_personal_access_token_here' else '❌ Not set'}")
    print()
    
    if not serper_key:
        print("❌ SERPER_API_KEY is required for testing. Please set it in .env file.")
        return False
    
    # Run tests
    success = True
    
    # Test 1: Direct Serper tool
    if not test_serper_tool():
        success = False
    
    # Test 2: NewsAgent integration
    if not test_news_agent_integration():
        success = False
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Serper API integration is working correctly.")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
