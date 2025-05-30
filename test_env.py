#!/usr/bin/env python3
"""
Test script to verify environment variable loading for OpenAI API.
Run this to check if your setup is correct before running the main generator.
"""

import os
from dotenv import load_dotenv

def test_openai_setup():
    """Test if OpenAI API key is properly configured."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("\nSetup instructions:")
        print("1. Copy env.example to .env: cp env.example .env")
        print("2. Edit .env and add your OpenAI API key")
        print("3. Or export it: export OPENAI_API_KEY='your-key-here'")
        return False
    
    if api_key.startswith("sk-"):
        print(f"✅ OpenAI API key found: {api_key[:15]}...")
        print("✅ Environment setup looks correct!")
        return True
    else:
        print("❌ Invalid OpenAI API key format (should start with 'sk-')")
        return False

if __name__ == "__main__":
    print("Testing environment setup...")
    test_openai_setup() 