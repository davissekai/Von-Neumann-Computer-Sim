#!/usr/bin/env python3
"""
Test NVIDIA API Connection
Quick test to verify the correct NVIDIA API endpoint and configuration
"""

import requests
import json

def test_nvidia_endpoints():
    """Test different NVIDIA API endpoints to find the working one"""
    
    api_key = "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"
    
    # Different endpoint configurations to try
    endpoints = [
        {
            "name": "NVIDIA Integrate API",
            "url": "https://integrate.api.nvidia.com/v1/chat/completions",
            "model": "meta/llama-3.1-70b-instruct",
            "format": "openai"
        },
        {
            "name": "NVIDIA NIM Direct", 
            "url": "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/meta/llama-3_1-70b-instruct",
            "model": "meta/llama-3_1-70b-instruct",
            "format": "nvidia"
        },
        {
            "name": "NVIDIA Build API",
            "url": "https://api.nvidia.com/v1/chat/completions", 
            "model": "meta/llama3-70b-instruct",
            "format": "openai"
        }
    ]
    
    test_message = "Hello, this is a test message."
    
    for endpoint in endpoints:
        print(f"\n🧪 Testing {endpoint['name']}")
        print(f"URL: {endpoint['url']}")
        print(f"Model: {endpoint['model']}")
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            if endpoint['format'] == 'openai':
                # OpenAI-compatible format
                payload = {
                    "model": endpoint['model'],
                    "messages": [
                        {"role": "user", "content": test_message}
                    ],
                    "max_tokens": 100,
                    "temperature": 0.7
                }
            else:
                # NVIDIA-specific format
                payload = {
                    "messages": [
                        {"role": "user", "content": test_message}
                    ],
                    "max_tokens": 100,
                    "temperature": 0.7,
                    "stream": False
                }
            
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                endpoint['url'],
                headers=headers,
                json=payload,
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ SUCCESS!")
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                return endpoint  # Return the working endpoint
            else:
                print(f"❌ FAILED")
                print(f"Error Response: {response.text}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: {e}")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout Error")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
    
    print(f"\n❌ All endpoints failed")
    return None

def test_simple_connection():
    """Test basic connectivity to NVIDIA"""
    print("🔗 Testing basic connectivity to NVIDIA...")
    
    try:
        # Test basic connection to nvidia.com
        response = requests.get("https://www.nvidia.com", timeout=5)
        print(f"✅ Basic internet connection works (status: {response.status_code})")
        
        # Test API domain
        response = requests.get("https://integrate.api.nvidia.com", timeout=5)
        print(f"✅ NVIDIA API domain reachable (status: {response.status_code})")
        
    except Exception as e:
        print(f"❌ Connection issue: {e}")

if __name__ == "__main__":
    print("🤖 NVIDIA API CONNECTION TEST")
    print("=" * 50)
    
    # Test basic connectivity first
    test_simple_connection()
    
    # Test API endpoints
    working_endpoint = test_nvidia_endpoints()
    
    if working_endpoint:
        print(f"\n🎉 Found working endpoint: {working_endpoint['name']}")
        print(f"Use this configuration in von_neu_ai.py:")
        print(f"URL: {working_endpoint['url']}")
        print(f"Model: {working_endpoint['model']}")
    else:
        print(f"\n💡 Suggestions:")
        print(f"1. Check if your API key is valid and active")
        print(f"2. Verify you have access to NVIDIA's API services")
        print(f"3. Check your network/firewall settings")
        print(f"4. Try running this from a different network")



'''

        PS C:\Users\P\AAAProjectD24\Python Prgmming\Experiments\von_neumann_computer> python test_nvidia_api.py
🤖 NVIDIA API CONNECTION TEST
==================================================
🔗 Testing basic connectivity to NVIDIA...
✅ Basic internet connection works (status: 200)
✅ NVIDIA API domain reachable (status: 404)

🧪 Testing NVIDIA Integrate API
URL: https://integrate.api.nvidia.com/v1/chat/completions
Model: meta/llama-3.1-70b-instruct
Payload: {
  "model": "meta/llama-3.1-70b-instruct",
  "messages": [
    {
      "role": "user",
      "content": "Hello, this is a test message."
    }
  ],
  "max_tokens": 100,
  "temperature": 0.7
}
Status Code: 200
Response Headers: {'Date': 'Sun, 24 Aug 2025 20:01:40 GMT', 'Content-Type': 'application/json', 'Content-Length': '468', 'Connection': 'keep-alive', 'Access-Control-Expose-Headers': 'nvcf-reqid', 'Nvcf-Reqid': '2be42a61-c725-430a-830b-fdf2a06e00ac', 'Nvcf-Status': 'fulfilled', 'Server': 'uvicorn', 'Vary': 'Origin'}
✅ SUCCESS!
Response: {
  "id": "chat-8ee9a0de1f3e487db9e9e764e8b0560d",
  "object": "chat.completion",
  "created": 1756065698,
  "model": "meta/llama-3.1-70b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! This is a test response. It looks like everything is working properly. Is there anything else I can help with?"
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 18,
    "total_tokens": 43,
    "completion_tokens": 25
  },
  "prompt_logprobs": null
}

🎉 Found working endpoint: NVIDIA Integrate API
Use this configuration in von_neu_ai.py:
URL: https://integrate.api.nvidia.com/v1/chat/completions
Model: meta/llama-3.1-70b-instruct
PS C:\Users\P\AAAProjectD24\Python Prgmming\Experiments\von_neumann_computer> 
'''
