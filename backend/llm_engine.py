import os
import json
from groq import Groq

def analyze_with_llm(resume_text, jd_text):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
        
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        You are an advanced Applicant Tracking System. I will provide a Candidate's Resume and a Job Description.
        You must analyze them and extract all relevant technical, soft, and domain-specific skills, regardless of the industry (Healthcare, Tech, Marketing, etc.).
        
        Return ONLY a valid JSON object matching this schema exactly. DO NOT wrap it in markdown block quotes (```json).
        
        {{
            "job_role": "Detected Job Role from JD",
            "resume_skills": ["List", "Of", "All", "Skills", "From", "Resume"],
            "job_skills": ["List", "Of", "Required", "Skills", "From", "JD"],
            "comparison": {{
                "match_percentage": 85.5,
                "matched_skills": ["Matched", "Skills"],
                "missing_skills": ["Missing", "Required", "Skills"],
                "additional_skills": ["Bonus", "Resume", "Skills"],
                "experience_gap_warning": "Warning about experience gaps, or empty string",
                "recommendation": "Short hiring verdict (e.g. Strong Fit, Moderate Fit)"
            }},
            "skill_suggestions": {{
                "suggested_skills": [
                    {{
                        "skill": "Suggested Skill Name",
                        "priority": "high",
                        "reason": "Short reason why",
                        "explanation": "Detailed explanation on how it helps"
                    }}
                ],
                "missing_skills_explained": [],
                "total_suggestions": 1,
                "suggestion_categories": {{ "co_occurrence": 1, "domain_based": 0 }}
            }}
        }}
        
        Resume:
        {resume_text[:4000]}
        
        Job Description:
        {jd_text[:4000]}
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a JSON API. You MUST return valid JSON matching the exact schema provided. Do not include any tags or conversational text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return None
