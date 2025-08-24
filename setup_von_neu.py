#!/usr/bin/env python3
"""
Von Neu Setup Script
Configures and tests Von Neu AI with the API key
"""

import os
import sys

def setup_environment():
    """Set up environment variables for Von Neu"""
    print("🔧 SETTING UP VON NEU AI")
    print("=" * 40)
    
    # Set the API key directly in the environment
    api_key = "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"
    os.environ['LLAMA_API_KEY'] = api_key
    
    print("✅ API key configured in environment")
    print(f"🔑 Key starts with: {api_key[:10]}...")
    
    # Verify environment is set
    env_key = os.getenv('LLAMA_API_KEY')
    if env_key:
        print("✅ Environment variable confirmed")
    else:
        print("❌ Environment variable not set properly")
        return False
    
    return True

def test_von_neu():
    """Test Von Neu with the configured API"""
    print("\n🤖 TESTING VON NEU AI")
    print("=" * 40)
    
    try:
        # Import and initialize Von Neu
        from von_neu_ai import VonNeuAI
        
        von_neu = VonNeuAI()
        
        # Check status
        status = von_neu.get_status()
        print(f"📊 API Connected: {status['api_connected']}")
        print(f"📊 Model: {status['model']}")
        
        if status['api_connected']:
            print("\n💬 Testing API chat...")
            test_message = "Hello Von Neu! Tell me who created you."
            print(f"USER: {test_message}")
            print()
            
            response = von_neu.chat(test_message)
            print("VON NEU:")
            print(response)
            
            # Check if response shows proper personality
            if "renhuang dey" in response.lower():
                print("\n✅ Personality test PASSED - Mentions creator")
            else:
                print("\n⚠️ Personality test - Creator mention not detected")
                
            if len(response) > 50:
                print("✅ Response length test PASSED")
            else:
                print("❌ Response seems too short")
                
        else:
            print("❌ API not connected - using offline mode")
            print("💡 This is normal if API key is invalid or service is down")
            print("📝 Von Neu will still work with offline responses")
            
    except Exception as e:
        print(f"❌ Error testing Von Neu: {e}")
        return False
        
    return True

def show_usage_instructions():
    """Show how to use Von Neu"""
    print("\n📋 HOW TO USE VON NEU")
    print("=" * 40)
    print("1. Run the simulator:")
    print("   python main_interface.py")
    print()
    print("2. Use these commands:")
    print("   chat <message>        - Chat with Von Neu")
    print("   von-neu-status        - Check AI status")
    print("   von-neu-greeting      - Show Von Neu's greeting")
    print("   von-neu-clear         - Clear conversation history")
    print()
    print("3. Example commands:")
    print("   chat Hello Von Neu!")
    print("   chat Who are you?")
    print("   chat Tell me about computers in your era")
    print()
    print("4. Web version:")
    print("   Open computer.html in your browser")
    print("   Click 'Chat with Von Neu' button")

def main():
    """Main setup function"""
    print("🚀 VON NEU AI SETUP & TEST")
    print("=" * 50)
    
    # Step 1: Setup environment
    if not setup_environment():
        print("❌ Setup failed")
        return
    
    # Step 2: Test Von Neu
    if not test_von_neu():
        print("❌ Testing failed")
        return
    
    # Step 3: Show usage
    show_usage_instructions()
    
    print("\n🎉 VON NEU SETUP COMPLETE!")
    print("🤖 Your retro AI companion is ready to chat!")

if __name__ == "__main__":
    main()