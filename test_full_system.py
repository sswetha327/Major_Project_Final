#!/usr/bin/env python3
"""
Full System Test Script
Tests both frontend and backend integration
"""
import requests
import json
import time

def test_backend():
    print("🔧 Testing Backend...")
    
    # Test backend health
    try:
        response = requests.get("http://localhost:5001/")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False
    
    # Test database status
    try:
        response = requests.get("http://localhost:5001/database-status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Database status: {status['database_connected']}")
            print(f"   Products stored: {status.get('products_stored', 0)}")
        else:
            print(f"❌ Database status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database status check failed: {e}")
        return False
    
    # Test analyze endpoint
    try:
        test_data = {"url": "https://example.com/test"}
        response = requests.post(
            "http://localhost:5001/analyze-product",
            json=test_data,
            headers={"Origin": "http://localhost:3004"}
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Product analysis working")
            print(f"   Reviews: {len(result.get('reviews', []))}")
            print(f"   Summary: {result.get('summary', {})}")
            return True
        else:
            print(f"❌ Product analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Product analysis failed: {e}")
        return False

def test_frontend():
    print("\n🎨 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:3000/")
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def test_cors():
    print("\n🌐 Testing CORS...")
    
    try:
        # Test OPTIONS request (preflight) for port 3000
        response = requests.options(
            "http://localhost:5001/analyze-product",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        if response.status_code == 200:
            print("✅ CORS preflight successful")
            print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
            return True
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def main():
    print("🚀 Full System Integration Test")
    print("=" * 50)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    cors_ok = test_cors()
    
    print("\n📊 Test Results:")
    print("=" * 30)
    print(f"Backend: {'✅ OK' if backend_ok else '❌ FAILED'}")
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ FAILED'}")
    print(f"CORS: {'✅ OK' if cors_ok else '❌ FAILED'}")
    
    if backend_ok and frontend_ok and cors_ok:
        print("\n🎉 All systems are working!")
        print("\n📝 Next steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Enter any product URL to test sentiment analysis")
        print("3. Check that results are displayed correctly")
        print("4. Verify data is being stored in MongoDB")
    else:
        print("\n⚠️  Some issues detected. Please check the failed components above.")
    
    return backend_ok and frontend_ok and cors_ok

if __name__ == "__main__":
    main()
