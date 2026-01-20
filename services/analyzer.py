import google.generativeai as genai
import json
from typing import List, Dict
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

class ResumeAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.prompt_template = self._load_prompt()
    
    def analyze(self, resume_chunks: List[Dict], job_description: str) -> Dict:
        chunks_text = "\n\n".join([
            f"[Section: {chunk['metadata']['section']}]\n{chunk['text']}"
            for chunk in resume_chunks
        ])

        prompt = self.prompt_template.format(
            resume_chunks=chunks_text,
            job_description=job_description
        )

        try:
            response = self.model.generate_content(
                prompt,
                generation_config = {
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 4096  # Increased from 2048
                }
            )
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if "```json" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                response_text = response_text[json_start:json_end]
            elif response_text.startswith("```"):
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                response_text = response_text[json_start:json_end]
            
            result = json.loads(response_text)
            return result

        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response: {e}")
            return {
                "error": "Failed to parse LLM response",
                "raw_response": response.text[:500]
            }

        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return {"error": str(e)}

    def _load_prompt(self) -> str:
        try:
            with open("prompts/resume_analysis.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return """Analyze the resume chunks against the job description and return JSON with: match_score, ats_score, matched_skills, missing_skills, strengths, weaknesses, improvements, reasoning."""
