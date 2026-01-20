import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.chunker import ResumeChunker
# Sample resume text for testing
SAMPLE_RESUME = """
John Doe
Software Engineer
PROFESSIONAL SUMMARY
Experienced software engineer with 5 years of expertise in Python, Flask, and AI/ML. 
Proven track record of building scalable web applications and implementing machine learning solutions.
WORK EXPERIENCE
Senior Software Engineer at Tech Corp (2021-2024)
- Led development of AI-powered analytics platform
- Managed team of 4 engineers
- Implemented microservices architecture
Software Engineer at StartupXYZ (2019-2021)
- Built RESTful APIs using Flask
- Developed data processing pipelines
- Collaborated with cross-functional teams
EDUCATION
Bachelor of Science in Computer Science
University of Technology (2015-2019)
GPA: 3.8/4.0
SKILLS
Programming: Python, JavaScript, SQL, Java
Frameworks: Flask, Django, React, Node.js
Tools: Git, Docker, AWS, MongoDB
AI/ML: TensorFlow, PyTorch, scikit-learn
PROJECTS
AI Resume Analyzer
- Built semantic resume analysis system using RAG architecture
- Implemented vector search with MongoDB Atlas
- Integrated Google Gemini for embeddings and LLM reasoning
CERTIFICATIONS
AWS Certified Solutions Architect
Google Cloud Professional Data Engineer
"""
def test_chunk_detection():
    """Test section detection and chunking"""
    chunker = ResumeChunker(chunk_size=100, overlap=20)
    chunks = chunker.chunk_by_sections(SAMPLE_RESUME)
    
    print("Chunking Test Results\n")
    print("=" * 60)
    print(f"Total chunks created: {len(chunks)}\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk['section']}")
        print(f"  ID: {chunk['chunk_id']}")
        print(f"  Words: {chunk['word_count']}")
        print(f"  Text preview: {chunk['text'][:100]}...")
        print()
    
    # Assertions
    assert len(chunks) > 0, "Should create at least one chunk"
    assert all('text' in chunk for chunk in chunks), "All chunks should have text"
    assert all('section' in chunk for chunk in chunks), "All chunks should have section"
    
    print("=" * 60)
    print("All chunking tests passed!")
    
    return chunks
if __name__ == "__main__":
    test_chunk_detection()
