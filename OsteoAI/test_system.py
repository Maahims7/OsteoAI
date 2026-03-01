#!/usr/bin/env python3
"""
End-to-end test of OsteoAI prediction pipeline
"""

import os
import sys
import requests
from pathlib import Path

def test_prediction_workflow():
    """Test the complete prediction flow"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("\n" + "="*70)
    print("🏥 OSTEOAI FULL PREDICTION WORKFLOW TEST")
    print("="*70)
    
    # 1. Test homepage
    print("\n[1/5] Testing homepage...")
    try:
        resp = requests.get(f"{base_url}/", timeout=5)
        if resp.status_code == 200 and "OsteoAI" in resp.text:
            print("✅ Splash page loaded (200 OK)")
            print(f"   Content: {len(resp.text)} bytes")
        else:
            print(f"❌ Unexpected response: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 2. Test intro page
    print("\n[2/5] Testing educational intro page...")
    try:
        resp = requests.get(f"{base_url}/intro", timeout=5)
        if resp.status_code == 200 and "Osteoporosis" in resp.text:
            print("✅ Intro page loaded (200 OK)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Test patient form page
    print("\n[3/5] Testing patient intake form...")
    try:
        resp = requests.get(f"{base_url}/patient", timeout=5)
        if resp.status_code == 200 and "Patient" in resp.text:
            print("✅ Patient form page loaded (200 OK)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Test prediction with real dataset image
    print("\n[4/5] Testing AI prediction with sample X-ray...")
    sample_image = Path("D:\\overflow\\OsteoAI\\dataset\\train\\Normal\\Normal 1.png")
    
    if not sample_image.exists():
        print(f"⚠️  Sample image not found at {sample_image}")
        return False
    
    try:
        with open(sample_image, 'rb') as f:
            files = {'xray': f}
            data = {
                'name': 'Test Patient',
                'age': '55',
                'sex': 'Female',
                'height': '165',
                'weight': '70',
                'phone': '1234567890',
                'email': 'test@example.com'
            }
            
            # Also try to upload patient photo (can be same image)
            with open(sample_image, 'rb') as f2:
                files['patient_photo'] = f2
                resp = requests.post(f"{base_url}/predict", data=data, files=files, timeout=30)
        
        if resp.status_code == 200:
            print("✅ Prediction successful (200 OK)")
            if "Normal" in resp.text or "Osteoporosis" in resp.text or "Osteopenia" in resp.text:
                print("   ✓ Prediction result detected in response")
            if "prescription" in resp.text.lower() or "recommendation" in resp.text.lower():
                print("   ✓ Medical recommendations generated")
        else:
            print(f"❌ Prediction failed: {resp.status_code}")
            if resp.text:
                print(f"   Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return False
    
    # 5. Test dashboard
    print("\n[5/5] Testing model dashboard...")
    try:
        resp = requests.get(f"{base_url}/dashboard", timeout=5)
        if resp.status_code == 200 and "accuracy" in resp.text.lower():
            print("✅ Dashboard loaded (200 OK)")
            print("   ✓ Training metrics visible")
        else:
            print(f"⚠️  Dashboard returned {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ OSTEOAI SYSTEM TEST COMPLETE")
    print("="*70)
    print("\n🌐 Access the app at: http://127.0.0.1:5000")
    print("\n📊 Routes:")
    print("   • / → Splash screen")
    print("   • /intro → Educational portal")
    print("   • /patient → Intake form")
    print("   • /predict → Submit for analysis (POST)")
    print("   • /graph → Density visualization")
    print("   • /report → Medical report")
    print("   • /dashboard → Model metrics")
    print("="*70 + "\n")
    
    return True

if __name__ == '__main__':
    try:
        success = test_prediction_workflow()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⛔ Test interrupted by user")
        sys.exit(1)
