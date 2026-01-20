from typing import List, Dict
import re

class ResumeChunker:
    """Split resume into chunks"""

    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_by_sections(self, text: str) -> List[Dict[str, str]]:
        """
        Chunk by detecting resume sections.
        
        Returns:
            List of chunks with metadata
        """
        sections = self._detect_sections(text)
        chunks = []
        
        for section_name, section_text in sections.items():
            # Further split large sections
            if len(section_text.split()) > self.chunk_size:
                sub_chunks = self._split_text(section_text)
                for i, chunk_text in enumerate(sub_chunks):
                    chunks.append({
                        "text": chunk_text,
                        "section": section_name,
                        "chunk_id": f"{section_name}_{i}",
                        "word_count": len(chunk_text.split())
                    })
            else:
                chunks.append({
                    "text": section_text,
                    "section": section_name,
                    "chunk_id": section_name,
                    "word_count": len(section_text.split())
                })
        
        return chunks
    
    def _detect_sections(self, text: str) -> Dict[str, str]:
        """Detect common resume sections."""
        # More specific patterns that look for section headers followed by content
        section_patterns = {
            "Summary": r"(professional summary|summary|profile|objective|about me)\s*(.*?)(?=(work experience|experience|employment history|education|skills|projects|certifications)|$)",
            "Experience": r"(work experience|experience|employment history|professional experience)\s*(.*?)(?=(education|skills|projects|certifications|awards)|$)",
            "Education": r"(education|academic background|qualifications)\s*(.*?)(?=(skills|projects|certifications|awards|references)|$)",
            "Skills": r"(skills|technical skills|competencies|core competencies)\s*(.*?)(?=(projects|certifications|awards|references|languages)|$)",
            "Projects": r"(projects|key projects|notable projects)\s*(.*?)(?=(certifications|awards|references|languages|education)|$)",
            "Certifications": r"(certifications|certificates|licenses|professional certifications)\s*(.*?)(?=(awards|references|languages|projects)|$)",
            "Awards": r"(awards|achievements|honors|recognitions)\s*(.*?)(?=(references|languages|certifications)|$)",
        }
        
        sections = {}
        matched_positions = []
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                start = match.start()
                content = match.group(2).strip()
                if content and len(content) > 20:  # Minimum content length
                    sections[section_name] = content
                    matched_positions.append((start, match.end(), section_name))
        
        # Sort by position to get sections in order
        matched_positions.sort()
        
        # Extract any remaining text as "Other"
        if matched_positions:
            # Get text before first section
            if matched_positions[0][0] > 0:
                header_text = text[:matched_positions[0][0]].strip()
                if len(header_text) > 20:
                    sections["Header"] = header_text
            
            # Get text after last section
            last_end = matched_positions[-1][1]
            if last_end < len(text):
                remaining = text[last_end:].strip()
                if len(remaining) > 20:
                    sections["Other"] = remaining
        else:
            # No sections detected, treat entire text as one section
            sections["Content"] = text
        
        return sections

    def _split_text(self, text: str) -> List[str]:
        """Split long text into chunks with overlap."""
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            # Get chunk
            chunk_words = words[i:i + self.chunk_size]
            chunk = ' '.join(chunk_words)
            chunks.append(chunk)
            
            # Move forward with overlap
            i += self.chunk_size - self.overlap
        
        return chunks
