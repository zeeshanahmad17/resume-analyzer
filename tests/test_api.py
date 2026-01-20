import requests
import os

BASE_URL = "http://localhost:5000"
RESUME_PATH = r"V:\Assignment\my docs\CV.docx"  # Change as needed

def test_upload_resume():
    """Test resume upload"""
    url = f"{BASE_URL}/api/upload-resume"
    
    with open(RESUME_PATH, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    print("Resume Upload Test:")
    print(response.json())
    print(f"Status Code: {response.status_code}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Test passed!")

def test_no_file():
    """Test error when no file provided"""
    url = f"{BASE_URL}/api/upload-resume"
    response = requests.post(url)
    
    print("\nNo File Test:")
    print(response.json())
    
    assert response.status_code == 400
    print("Test passed!")

def test_invalid_format():
    """Test error for invalid file format"""
    url = f"{BASE_URL}/api/upload-resume"
    
    # Create temporary invalid file
    invalid_file = "temp_test.jpg"
    with open(invalid_file, "wb") as f:
        f.write(b"fake image")
    
    with open(invalid_file, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    print("\nInvalid Format Test:")
    print(response.json())
    
    assert response.status_code == 400
    assert "Invalid file format" in response.json()["error"]
    
    # Cleanup
    os.remove(invalid_file)
    print("Test passed!")

if __name__ == "__main__":
    print("Running API Tests for Resume Analyzer\n")
    print("=" * 50)
    
    try:
        test_upload_resume()
        test_no_file()
        test_invalid_format()
        
        print("\n" + "=" * 50)
        print("All tests passed!")
        
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nError: {e}")