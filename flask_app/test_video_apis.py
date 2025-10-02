#!/usr/bin/env python3
"""
Test script for the new Flask video APIs
Run this after starting the Flask server to test the endpoints
"""

import requests
import json
from pathlib import Path

# Flask server URL
BASE_URL = "http://localhost:5000"

def test_batches_api():
    """Test the /api/batches endpoint"""
    print("Testing /api/batches endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/batches")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} batches:")
            for batch_name, batch_data in data.items():
                print(f"  - {batch_name}: {len(batch_data)} signs")
                for sign_name, sign_data in batch_data.items():
                    review_count = len(sign_data.get('reviews', []))
                    has_reference = sign_data.get('reference') is not None
                    print(f"    - {sign_name}: {review_count} reviews, reference: {has_reference}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server. Make sure it's running on port 5000.")
    except Exception as e:
        print(f"Error: {e}")
    
    print()

def test_video_endpoints():
    """Test video serving endpoints (just check if they respond correctly to HEAD requests)"""
    print("Testing video endpoints...")
    
    # Test reference video endpoint
    test_filename = "test.mp4"  # This will likely return 404, but we can check the endpoint works
    try:
        response = requests.head(f"{BASE_URL}/api/video/reference/{test_filename}")
        print(f"Reference video endpoint status: {response.status_code}")
    except Exception as e:
        print(f"Reference video endpoint error: {e}")
    
    # Test review video endpoint
    try:
        response = requests.head(f"{BASE_URL}/api/video/review/TestBatch/TestSign/{test_filename}")
        print(f"Review video endpoint status: {response.status_code}")
    except Exception as e:
        print(f"Review video endpoint error: {e}")
    
    print()

def check_config_files():
    """Check if required configuration files exist"""
    print("Checking configuration files...")
    
    config_path = Path("../WebAnnotationEngine/src/routes/config/videoConfig.json")
    sign_list_path = Path("../WebAnnotationEngine/src/routes/config/sign_list.txt")
    
    print(f"videoConfig.json exists: {config_path.exists()}")
    print(f"sign_list.txt exists: {sign_list_path.exists()}")
    
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            print("Configuration file is valid JSON")
            print(f"Review source: {config.get('review_source', 'Not specified')}")
            print(f"Reference source: {config.get('reference_source', 'Not specified')}")
            print(f"Batches filter: {config.get('batches', 'All batches')}")
        except Exception as e:
            print(f"Error reading config file: {e}")
    
    print()

if __name__ == "__main__":
    print("Flask Video API Test Script")
    print("=" * 40)
    
    check_config_files()
    test_batches_api()
    test_video_endpoints()
    
    print("Test completed!")
