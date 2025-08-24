#!/usr/bin/env python3
"""
Von Neu AI Chat Test
Quick test to verify Von Neu AI functionality with the API key
"""

import sys
import os

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from von_neu_ai import VonNeuAI

def test_von_neu_basic():
    """Basic test of Von Neu functionality"""
    print("🤖 VON NEU AI CHAT TEST")
    print("=" * 40)
    print("Testing Von Neu AI with API key...")
    print()
    
    # Initialize Von Neu
    try:
        von_neu = VonNeuAI()
        print(f"✅ Von Neu initialized successfully")
        
        # Check status
        status = von_neu.get_status()
        print(f"📊 API Connected: {status['api_connected']}")
        print(f"📊 Model: {status['model']}")
        print(f"📊 Rate Limit Remaining: {status['rate_limit_remaining']}")
        print()
        
        # Test greeting
        print("🎬 Von Neu Startup Greeting:")
        print(von_neu.get_startup_greeting())
        print()
        
        # Test a simple chat
        print("💬 Testing chat functionality...")
        test_message = "Hello Von Neu! Who are you?"
        print(f"USER: {test_message}")
        print()
        
        response = von_neu.chat(test_message)
        print("VON NEU:")
        print(response)
        print()
        
        # Test personality consistency
        print("🧪 Testing personality consistency...")
        personality_tests = [
            "Tell me about modern smartphones",
            "Who created you?",
            "What do you know about Python programming?"
        ]
        
        for i, test in enumerate(personality_tests, 1):
            print(f"\nTest {i}: {test}")
            response = von_neu.chat(test)
            
            # Check for key personality elements
            checks = {
                "Mentions Renhuang Dey": "renhuang dey" in response.lower(),
                "Shows confusion about modern tech": any(word in response.lower() 
                    for word in ["confused", "don't understand", "bewildered", "peculiar"]),
                "References vintage era": any(word in response.lower() 
                    for word in ["1970", "1980", "era", "master", "vintage"])
            }
            
            print("Response summary:")
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {check}")
            
            print(f"Response length: {len(response)} characters")
        
        print("\n🎉 Von Neu test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        print("\nTroubleshooting:")
        print("1. Check that your API key is set in .env file")
        print("2. Verify internet connection") 
        print("3. Check API service status")

if __name__ == "__main__":
    test_von_neu_basic()