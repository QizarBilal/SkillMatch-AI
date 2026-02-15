from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import pdfplumber
import docx
import pytesseract
from PIL import Image
import pandas as pd
import uuid
import json
from nlp_engine import clean_text, extract_skills, extract_keywords, parse_resume_structured, parse_jd_structured
from nlp_preprocessing import preprocess_text, extract_skills_hybrid, extract_keywords_hybrid, generate_tfidf_vectors
from auth import hash_password, verify_password, create_access_token, verify_token
from database import get_db, User, Submission
import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

dataset_path = "dataset_store.csv"

@app.post("/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    hashed = hash_password(req.password)
    user = User(email=req.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"user_id": user.user_id, "email": user.email})
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "token": token
    }

@app.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": user.user_id, "email": user.email})
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "token": token
    }

@app.get("/auth/me")
def get_current_user(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }

@app.get("/submissions")
def get_submissions(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    submissions = db.query(Submission).filter(Submission.user_id == user_id).order_by(Submission.created_at.desc()).all()
    
    result = []
    for sub in submissions:
        parsed_resume = json.loads(sub.parsed_resume_fields) if sub.parsed_resume_fields else {}
        parsed_jd = json.loads(sub.parsed_jd_fields) if sub.parsed_jd_fields else {}
        
        result.append({
            "submission_id": sub.submission_id,
            "resume_text": sub.resume_text[:200] + "..." if len(sub.resume_text) > 200 else sub.resume_text,
            "jd_text": sub.job_description_text[:200] + "..." if len(sub.job_description_text) > 200 else sub.job_description_text,
            "candidate_name": parsed_resume.get("candidate_name", "Unknown"),
            "job_role": parsed_jd.get("job_role", "Not specified"),
            "created_at": sub.created_at.isoformat()
        })
    
    return result

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

def read_txt(file):
    return file.read().decode('utf-8', errors='ignore')

def read_image(file):
    img = Image.open(file)
    return pytesseract.image_to_string(img)

@app.post("/analyze")
async def analyze(
    resume: UploadFile, 
    job_description: str = Form(None), 
    jd_file: UploadFile = None,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    ext = resume.filename.split(".")[-1].lower()

    if ext == "pdf":
        raw = read_pdf(resume.file)
    elif ext == "docx":
        raw = read_docx(resume.file)
    else:
        raw = read_image(resume.file)

    cleaned_resume = clean_text(raw)
    resume_structured = parse_resume_structured(raw)

    if jd_file:
        jd_ext = jd_file.filename.split(".")[-1].lower()
        if jd_ext == "pdf":
            jd_text = read_pdf(jd_file.file)
        elif jd_ext == "docx":
            jd_text = read_docx(jd_file.file)
        elif jd_ext == "txt":
            jd_text = read_txt(jd_file.file)
        else:
            jd_text = read_image(jd_file.file)
    elif job_description:
        jd_text = job_description
    else:
        raise HTTPException(status_code=400, detail="Either job_description text or jd_file must be provided")

    cleaned_jd = clean_text(jd_text)
    jd_structured = parse_jd_structured(jd_text)

    resume_preprocessed = preprocess_text(raw)
    jd_preprocessed = preprocess_text(jd_text)
    
    resume_skills_extracted = extract_skills_hybrid(raw)
    jd_skills_extracted = extract_keywords_hybrid(jd_text)
    
    tfidf_data = generate_tfidf_vectors(raw, jd_text)

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
        "required_experience_years": jd_structured['required_experience_years'],
        "resume_clean_text": resume_preprocessed['reconstructed_clean_text'],
        "resume_tokens": ",".join(resume_preprocessed['clean_tokens'][:100]),
        "resume_extracted_skills": ",".join(resume_skills_extracted),
        "jd_clean_text": jd_preprocessed['reconstructed_clean_text'],
        "jd_tokens": ",".join(jd_preprocessed['clean_tokens'][:100]),
        "jd_extracted_skills": ",".join(jd_skills_extracted)
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
    
    submission = Submission(
        user_id=user_id,
        resume_text=raw,
        parsed_resume_fields=json.dumps(resume_structured),
        job_description_text=jd_text,
        parsed_jd_fields=json.dumps(jd_structured),
        resume_clean_text=resume_preprocessed['reconstructed_clean_text'],
        resume_tokens=json.dumps(resume_preprocessed['clean_tokens']),
        resume_skills=json.dumps(resume_skills_extracted),
        jd_clean_text=jd_preprocessed['reconstructed_clean_text'],
        jd_tokens=json.dumps(jd_preprocessed['clean_tokens']),
        jd_skills=json.dumps(jd_skills_extracted)
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

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
        "resume_preprocessed": {
            "clean_text": resume_preprocessed['reconstructed_clean_text'],
            "tokens": resume_preprocessed['clean_tokens'][:100],
            "lemmatized_tokens": resume_preprocessed['lemmatized_tokens'][:100]
        },
        "jd_preprocessed": {
            "clean_text": jd_preprocessed['reconstructed_clean_text'],
            "tokens": jd_preprocessed['clean_tokens'][:100],
            "lemmatized_tokens": jd_preprocessed['lemmatized_tokens'][:100]
        },
        "resume_skills_extracted": resume_skills_extracted,
        "jd_skills_extracted": jd_skills_extracted,
        "tfidf_vectors": {
            "resume_vector_length": len(tfidf_data['resume_tfidf_vector']),
            "jd_vector_length": len(tfidf_data['jd_tfidf_vector']),
            "feature_count": len(tfidf_data['feature_names'])
        },
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
