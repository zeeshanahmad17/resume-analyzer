import requests
import time
BASE_URL = "http://localhost:5000"
JOB_DESCRIPTION = """
Full Stack Developer - 2+ years React and Node.js experience required.
Skills: React, Next.js, TypeScript, REST APIs, Agile/Scrum.
"""
def test_analysis():
    # Upload resume
    files = {"file": open(r"tests\test_data\CV.docx", "rb")}
    upload = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
    resume_id = upload.json()['resume_id']
    print(f"Resume uploaded: {resume_id}")
    
    # Wait for MongoDB Atlas vector index to sync
    print("Waiting 10 seconds for index to sync...")
    time.sleep(10)
    
    # Analyze
    payload = {"resume_id": resume_id, "job_description": JOB_DESCRIPTION}
    analysis = requests.post(f"{BASE_URL}/api/analyze", json=payload)
    
    print(f"\nFull API Response:")
    print(f"Status Code: {analysis.status_code}")
    print(f"Response: {analysis.json()}")
    
    if 'analysis' not in analysis.json():
        print("\n❌ Error: 'analysis' not in response")
        return
    
    result = analysis.json()['analysis']
    
    print(f"\nMatch Score: {result['match_score']}%")
    print(f"ATS Score: {result['ats_score']}%")
    print(f"Matched Skills: {result['matched_skills']}")
    print(f"Missing Skills: {result['missing_skills']}")

if __name__ == "__main__":
    test_analysis()
