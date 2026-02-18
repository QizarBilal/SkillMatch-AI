from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import pdfplumber
import docx
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import uuid
import json
import io
import re
from datetime import datetime
from nlp_engine import clean_text, extract_skills, extract_keywords, parse_resume_structured, parse_jd_structured
from nlp_preprocessing import preprocess_text, extract_skills_hybrid, extract_keywords_hybrid, generate_tfidf_vectors
from auth import hash_password, verify_password, create_access_token, verify_token
from comparison_engine import compare_profiles
from mongodb import users_collection, submissions_collection, resumes_collection, job_descriptions_collection, analysis_results_collection, test_connection
import pymongo.errors
import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

# Test MongoDB connection on startup (non-blocking)
@app.on_event("startup")
async def startup_event():
    test_connection()

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

@app.post("/auth/register")
def register(req: RegisterRequest):
    try:
        existing = users_collection.find_one({"email": req.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if len(req.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        hashed = hash_password(req.password)
        
        user_count = users_collection.count_documents({})
        user_id = user_count + 1
        
        user_doc = {
            "user_id": user_id,
            "email": req.email,
            "password_hash": hashed,
            "created_at": datetime.utcnow()
        }
        users_collection.insert_one(user_doc)
        
        token = create_access_token({"user_id": user_id, "email": req.email})
        
        return {
            "user_id": user_id,
            "email": req.email,
            "token": token
        }
    except pymongo.errors.OperationFailure as e:
        raise HTTPException(
            status_code=503,
            detail="Database authentication failed. Please check MongoDB Atlas configuration: ensure user exists, password is correct, and IP is whitelisted."
        )
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")

@app.post("/auth/login")
def login(req: LoginRequest):
    try:
        user = users_collection.find_one({"email": req.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not verify_password(req.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token({"user_id": user["user_id"], "email": user["email"]})
        
        return {
            "user_id": user["user_id"],
            "email": user["email"],
            "token": token
        }
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=503,
            detail="Database authentication failed. Please check MongoDB Atlas configuration."
        )
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")

@app.get("/auth/me")
def get_current_user(user_id: int = Depends(verify_token)):
    try:
        user = users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": user["user_id"],
            "email": user["email"],
            "created_at": user["created_at"].isoformat()
        }
    except pymongo.errors.OperationFailure:
        raise HTTPException(status_code=503, detail="Database authentication failed.")
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")

@app.get("/submissions")
def get_submissions(user_id: int = Depends(verify_token)):
    try:
        submissions = list(submissions_collection.find({"user_id": user_id}).sort("created_at", -1))
        
        result = []
        for sub in submissions:
            parsed_resume = sub.get("parsed_resume_fields", {})
            parsed_jd = sub.get("parsed_jd_fields", {})
            
            if isinstance(parsed_resume, str):
                parsed_resume = json.loads(parsed_resume)
            if isinstance(parsed_jd, str):
                parsed_jd = json.loads(parsed_jd)
            
            resume_text = sub.get("resume_text", "")
            jd_text = sub.get("job_description_text", "")
            
            result.append({
                "submission_id": sub.get("submission_id", ""),
                "resume_text": resume_text[:200] + "..." if len(resume_text) > 200 else resume_text,
                "jd_text": jd_text[:200] + "..." if len(jd_text) > 200 else jd_text,
                "candidate_name": parsed_resume.get("candidate_name", "Unknown"),
                "job_role": parsed_jd.get("job_role", "Not specified"),
                "created_at": sub.get("created_at", datetime.utcnow()).isoformat()
            })
        
        return result
    except pymongo.errors.OperationFailure:
        raise HTTPException(status_code=503, detail="Database authentication failed.")
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")

def preprocess_image_for_ocr(image):
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    if width < 1500:
        scale = 1500 / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.5)
    
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)
    
    from PIL import ImageOps
    image = ImageOps.autocontrast(image, cutoff=2)
    
    image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return image

def is_text_quality_good(text):
    if not text or len(text) < 50:
        return False
    
    total_chars = len(text)
    alpha_chars = sum(c.isalpha() or c.isspace() for c in text)
    alpha_ratio = alpha_chars / total_chars if total_chars > 0 else 0
    
    if alpha_ratio < 0.7:
        return False
    
    words = text.split()
    if len(words) < 10:
        return False
    
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    if avg_word_length < 3 or avg_word_length > 15:
        return False
    
    garbled_patterns = [
        r'[a-z]{15,}',
        r'\b[bcdfghjklmnpqrstvwxyz]{5,}\b',
        r'[wxy]{3,}',
    ]
    
    for pattern in garbled_patterns:
        matches = re.findall(pattern, text.lower())
        if len(matches) > len(words) * 0.1:
            return False
    
    common_words = ['the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'with', 'experience', 'skills', 'education', 'work', 'at', 'by', 'from', 'as', 'about', 'have', 'has', 'had', 'was', 'were', 'been', 'be', 'are', 'am']
    common_word_count = sum(1 for word in words if word.lower() in common_words)
    if len(words) > 30 and common_word_count < 3:
        return False
    
    vowel_count = sum(1 for c in text.lower() if c in 'aeiou')
    consonant_count = sum(1 for c in text.lower() if c.isalpha() and c not in 'aeiou')
    if consonant_count > 0:
        vowel_ratio = vowel_count / consonant_count
        if vowel_ratio < 0.25 or vowel_ratio > 2.0:
            return False
    
    return True

def read_pdf(file):
    text = ""
    file_bytes = file.read()
    file.seek(0)
    
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + " "
    except Exception:
        pass
    
    if is_text_quality_good(text):
        return text
    
    print(f"PDF text quality check failed. Extracted text length: {len(text)}")
    print(f"Sample text: {text[:200] if text else 'No text'}")
    
    try:
        import fitz
        
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        ocr_text = ""
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            
            processed_img = preprocess_image_for_ocr(img)
            
            page_text = pytesseract.image_to_string(
                processed_img,
                lang='eng',
                config='--psm 1 --oem 3'
            )
            ocr_text += page_text + " "
        
        pdf_document.close()
        
        print(f"OCR text length: {len(ocr_text)}")
        print(f"OCR sample: {ocr_text[:200] if ocr_text else 'No OCR text'}")
        
        if is_text_quality_good(ocr_text):
            return ocr_text
        elif len(ocr_text) > len(text) and len(ocr_text) > 100:
            return ocr_text
        else:
            return text if text else ocr_text
    except ImportError as e:
        print(f"PyMuPDF import error: {e}")
        if text:
            return text
        raise Exception("PyMuPDF not installed. Please install: pip install PyMuPDF")
    except Exception as e:
        print(f"OCR error: {str(e)}")
        if text:
            return text
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def read_docx(file):
    d = docx.Document(file)
    return " ".join([p.text for p in d.paragraphs])

def read_txt(file):
    return file.read().decode('utf-8', errors='ignore')

def read_image(file):
    img = Image.open(file)
    img = preprocess_image_for_ocr(img)
    text = pytesseract.image_to_string(img, config='--psm 6 --oem 3')
    return text

@app.post("/analyze")
async def analyze(
    resume: UploadFile, 
    job_description: str = Form(None), 
    jd_file: UploadFile = None,
    user_id: int = Depends(verify_token)
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

    try:
        submission_count = submissions_collection.count_documents({})
        submission_id = submission_count + 1
        
        submission_doc = {
            "submission_id": submission_id,
            "user_id": user_id,
            "resume_text": raw,
            "parsed_resume_fields": resume_structured,
            "job_description_text": jd_text,
            "parsed_jd_fields": jd_structured,
            "resume_clean_text": resume_preprocessed['reconstructed_clean_text'],
            "resume_tokens": resume_preprocessed['clean_tokens'][:100],
            "resume_skills": resume_skills_extracted,
            "jd_clean_text": jd_preprocessed['reconstructed_clean_text'],
            "jd_tokens": jd_preprocessed['clean_tokens'][:100],
            "jd_skills": jd_skills_extracted,
            "created_at": datetime.utcnow()
        }
        submissions_collection.insert_one(submission_doc)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=503,
            detail="Database authentication failed. Please check MongoDB Atlas configuration: ensure user exists, password is correct, and IP is whitelisted."
        )
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB insertion warning: {str(e)}")

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

    resume_profile_obj = {
        'candidate_name': resume_structured['candidate_name'],
        'email': resume_structured['email'],
        'phone': resume_structured['phone'],
        'location': resume_structured['location'],
        'technical_skills': resume_structured['technical_skills'],
        'programming_languages': resume_structured['programming_languages'],
        'frameworks': resume_structured['frameworks'],
        'tools': resume_structured['tools'],
        'databases': resume_structured['databases'],
        'education_degrees': resume_structured['education_degrees'],
        'education_fields': resume_structured['education_fields'],
        'education_institutions': resume_structured['education_institutions'],
        'experience_roles': resume_structured['experience_roles'],
        'experience_companies': resume_structured['experience_companies'],
        'experience_years_estimated': resume_structured['experience_years_estimated'],
        'project_titles': resume_structured['project_titles'],
        'project_technologies': resume_structured['project_technologies'],
        'certifications': resume_structured['certifications']
    }

    job_profile_obj = {
        'job_role': jd_structured['job_role'],
        'required_skills': jd_structured['required_skills'],
        'required_languages': jd_structured['required_languages'],
        'required_frameworks': jd_structured['required_frameworks'],
        'required_tools': jd_structured['required_tools'],
        'required_databases': jd_structured['required_databases'],
        'required_experience_years': jd_structured['required_experience_years'],
        'required_education': jd_structured['required_education']
    }

    comparison_result = compare_profiles(resume_profile_obj, job_profile_obj)

    try:
        resume_doc = {
            'resume_id': rid,
            'user_id': user_id,
            'profile': resume_profile_obj,
            'raw_text': raw,
            'created_at': datetime.utcnow()
        }
        resumes_collection.insert_one(resume_doc)

        jd_doc = {
            'jd_id': rid,
            'user_id': user_id,
            'profile': job_profile_obj,
            'raw_text': jd_text,
            'created_at': datetime.utcnow()
        }
        job_descriptions_collection.insert_one(jd_doc)

        analysis_doc = {
            'analysis_id': rid,
            'user_id': user_id,
            'resume_id': rid,
            'jd_id': rid,
            'comparison': comparison_result,
            'match_percentage': comparison_result['match_percentage'],
            'created_at': datetime.utcnow()
        }
        analysis_results_collection.insert_one(analysis_doc)
    except Exception as e:
        print(f"MongoDB insertion warning: {str(e)}")

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
                "institutions": resume_structured['education_institutions'],
                "entries": resume_structured.get('education_entries', [])
            },
            "experience": {
                "roles": resume_structured['experience_roles'],
                "companies": resume_structured['experience_companies'],
                "date_ranges": resume_structured['experience_date_ranges'],
                "years_estimated": resume_structured['experience_years_estimated'],
                "entries": resume_structured.get('experience_entries', [])
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
        "comparison": comparison_result,
        "dataset_size": 0 if 'submission_count' not in locals() else submissions_collection.count_documents({})
    }
