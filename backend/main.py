from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import docx
import pytesseract
from PIL import Image
import pandas as pd
import uuid
from nlp_engine import clean_text, extract_skills, extract_keywords, parse_resume_structured, parse_jd_structured

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dataset_path = "dataset_store.csv"

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + " "
    return text

def read_docx(file):
    d = docx.Document(file)
    return " ".join([p.text for p in d.paragraphs])

def read_image(file):
    img = Image.open(file)
    return pytesseract.image_to_string(img)

@app.post("/analyze")
async def analyze(resume: UploadFile, job_description: str = Form(...)):
    ext = resume.filename.split(".")[-1].lower()

    if ext == "pdf":
        raw = read_pdf(resume.file)
    elif ext == "docx":
        raw = read_docx(resume.file)
    else:
        raw = read_image(resume.file)

    cleaned_resume = clean_text(raw)
    resume_structured = parse_resume_structured(raw)

    cleaned_jd = clean_text(job_description)
    jd_structured = parse_jd_structured(job_description)

    rid = str(uuid.uuid4())[:8]

    row = {
        "resume_id": rid,
        "candidate_name": resume_structured['candidate_name'],
        "email": resume_structured['email'],
        "phone": resume_structured['phone'],
        "location": resume_structured['location'],
        "technical_skills": ",".join(resume_structured['technical_skills']),
        "programming_languages": ",".join(resume_structured['programming_languages']),
        "frameworks": ",".join(resume_structured['frameworks']),
        "tools": ",".join(resume_structured['tools']),
        "databases": ",".join(resume_structured['databases']),
        "education_degrees": ",".join(resume_structured['education_degrees']),
        "education_fields": ",".join(resume_structured['education_fields']),
        "experience_roles": ",".join(resume_structured['experience_roles']),
        "experience_years_estimated": resume_structured['experience_years_estimated'],
        "project_technologies": ",".join(resume_structured['project_technologies']),
        "job_role": jd_structured['job_role'],
        "required_skills": ",".join(jd_structured['required_skills']),
        "required_languages": ",".join(jd_structured['required_languages']),
        "required_frameworks": ",".join(jd_structured['required_frameworks']),
        "required_tools": ",".join(jd_structured['required_tools']),
        "required_experience_years": jd_structured['required_experience_years']
    }

    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        df = pd.DataFrame()
    except Exception:
        df = pd.DataFrame()
    
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    try:
        df.to_csv(dataset_path, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write dataset: {str(e)}")

    all_resume_skills = (
        resume_structured['technical_skills'] + 
        resume_structured['tools'] + 
        resume_structured['frameworks'] + 
        resume_structured['programming_languages'] +
        resume_structured['databases']
    )
    
    all_jd_keywords = (
        jd_structured['required_skills'] + 
        jd_structured['required_frameworks'] + 
        jd_structured['required_tools'] + 
        jd_structured['required_languages'] +
        jd_structured['required_databases']
    )

    return {
        "resume_id": rid,
        "cleaned_resume_text": cleaned_resume,
        "cleaned_job_description_text": cleaned_jd,
        "resume_profile": {
            "candidate_name": resume_structured['candidate_name'],
            "contact": {
                "email": resume_structured['email'],
                "phone": resume_structured['phone'],
                "location": resume_structured['location']
            },
            "technical_expertise": {
                "skills": resume_structured['technical_skills'],
                "languages": resume_structured['programming_languages'],
                "frameworks": resume_structured['frameworks'],
                "tools": resume_structured['tools'],
                "databases": resume_structured['databases']
            },
            "soft_skills": resume_structured['soft_skills'],
            "education": {
                "degrees": resume_structured['education_degrees'],
                "fields": resume_structured['education_fields'],
                "institutions": resume_structured['education_institutions']
            },
            "experience": {
                "roles": resume_structured['experience_roles'],
                "companies": resume_structured['experience_companies'],
                "date_ranges": resume_structured['experience_date_ranges'],
                "years_estimated": resume_structured['experience_years_estimated']
            },
            "projects": {
                "titles": resume_structured['project_titles'],
                "technologies": resume_structured['project_technologies']
            },
            "certifications": resume_structured['certifications']
        },
        "job_profile": {
            "role": jd_structured['job_role'],
            "required_technical": {
                "skills": jd_structured['required_skills'],
                "languages": jd_structured['required_languages'],
                "frameworks": jd_structured['required_frameworks'],
                "tools": jd_structured['required_tools'],
                "databases": jd_structured['required_databases']
            },
            "requirements": {
                "experience_years": jd_structured['required_experience_years'],
                "education": jd_structured['required_education']
            },
            "additional": {
                "nice_to_have": jd_structured['nice_to_have_skills'],
                "responsibility_terms": jd_structured['responsibility_tech_terms']
            }
        },
        "resume_skills": all_resume_skills,
        "job_keywords": all_jd_keywords,
        "dataset_size": len(df)
    }
