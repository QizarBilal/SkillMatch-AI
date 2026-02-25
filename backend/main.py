from fastapi import FastAPI, UploadFile, Form, File, HTTPException, Depends, BackgroundTasks
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
import pdfplumber
import docx

def set_pytesseract_path():
    import pytesseract
    import platform
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import uuid
import json
import io
import re
import os
import gc
import platform
import asyncio
import warnings
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import socket
import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Monkey patch socket to force IPv4, as HF spaces block IPv6 SMTP heavily causing Network is unreachable
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_getaddrinfo(*args, **kwargs):
    responses = _orig_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]
socket.getaddrinfo = _ipv4_getaddrinfo
import pytesseract
try:
    import fitz # PyMuPDF
except ImportError:
    fitz = None

from .nlp_engine import clean_text, extract_skills, extract_keywords, parse_resume_structured, parse_jd_structured
from .nlp_preprocessing import preprocess_text, extract_skills_hybrid, extract_keywords_hybrid, generate_tfidf_vectors
from .auth import hash_password, verify_password, create_access_token, verify_token
from .comparison_engine import compare_profiles
from .suggestion_engine import generate_skill_suggestions, get_skill_explanation
from .admin import (
    get_analytics_summary, get_top_missing_skills, get_top_job_roles,
    get_skill_category_distribution, get_recommendation_distribution,
    get_recent_analyses, validate_admin_role
)
from .mongodb import users_collection, submissions_collection, resumes_collection, job_descriptions_collection, analysis_results_collection, test_connection, quick_health_check, otp_collection

# Database collection getters are imported from .mongodb

import pymongo.errors

warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")




app = FastAPI()

# Static file serving is handled at the bottom of the file to prevent catching API routes


# Global state for application readiness
app_ready = False

@app.on_event("startup")

async def startup_event():
    global app_ready
    # Run DB test asynchronously without blocking startup
    asyncio.create_task(async_db_test())

async def async_db_test():
    global app_ready
    try:
        await asyncio.sleep(0.1)  # Brief delay to allow app to start serving
        loop = asyncio.get_event_loop()
        # Run blocking DB test in thread pool
        result = await loop.run_in_executor(None, test_connection)
        app_ready = result
    except Exception as e:
        print(f"Startup DB test failed: {e}")
        app_ready = False

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
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResendOTPRequest(BaseModel):
    email: EmailStr

def send_otp_email(to_email: str, otp: str):
    brevo_api_key = os.getenv("BREVO_API_KEY")
    if not brevo_api_key:
        print("BREVO_API_KEY missing, skipping OTP email.")
        return

    from_email = os.getenv("EMAIL_FROM", "bilalqizar@gmail.com")

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f4f5; color: #18181b; margin: 0; padding: 40px 20px;">
        <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 12px; border: 1px solid #e4e4e7; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #6366f1; font-size: 24px; margin: 0; font-weight: 700; letter-spacing: -0.5px;">SkillMatch</h1>
            </div>
            <h2 style="font-size: 18px; font-weight: 600; text-align: center; color: #0f172a; margin-bottom: 20px;">Verify your identity</h2>
            <p style="font-size: 15px; line-height: 1.6; text-align: center; color: #475569; margin-bottom: 30px;">
                Please enter the following verification code to complete your registration. This code is valid for <strong>5 minutes</strong>.
            </p>
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 30px;">
                <span style="font-size: 32px; font-weight: 700; letter-spacing: 8px; color: #334155;">{otp}</span>
            </div>
            <p style="font-size: 13px; text-align: center; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 20px;">
                If you did not request this email, please ignore it or contact support if you have concerns.
            </p>
        </div>
    </body>
    </html>
    """

    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept": "application/json",
                "api-key": brevo_api_key,
                "content-type": "application/json"
            },
            json={
                "sender": {"name": "SkillMatch", "email": from_email},
                "to": [{"email": to_email}],
                "subject": "SkillMatch - Verify your email (OTP)",
                "htmlContent": html
            },
            timeout=10
        )
        if response.status_code in [200, 201, 202]:
            print(f"Successfully sent OTP email to {to_email} via Brevo")
        else:
            print(f"Failed to send OTP email via Brevo: {response.text}")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

def send_welcome_email(to_email: str, user_name: str):
    brevo_api_key = os.getenv("BREVO_API_KEY")
    if not brevo_api_key:
        print("BREVO_API_KEY missing for WELCOME email.")
        return

    from_email = os.getenv("EMAIL_FROM", "bilalqizar@gmail.com")

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #0f1629; color: #f8fafc; margin: 0; padding: 40px 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%); padding: 40px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.3); box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
            <div style="text-align: center; margin-bottom: 32px;">
                <h1 style="color: #8b5cf6; font-size: 28px; margin: 0; letter-spacing: -0.5px; font-weight: 700;">SkillMatch</h1>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 8px;">AI Resume Intelligence Platform</p>
            </div>
            <h2 style="color: #e2e8f0; font-size: 22px; font-weight: 600; margin-bottom: 24px;">Welcome aboard, {user_name}! 🚀</h2>
            <div style="color: #cbd5e1; font-size: 16px; line-height: 1.7;">
                <p style="margin-bottom: 16px;">We're thrilled to have you join our cutting-edge AI ecosystem.</p>
                <p style="margin-bottom: 16px;">SkillMatch's advanced NLP engine is now fully at your disposal. We're here to deeply analyze your resumes, extract core technical competencies, and powerfully benchmark them against any job description.</p>
                <p>No more guessing—just clear, actionable intelligence bridging the gap between talent and opportunity.</p>
            </div>
            <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
                <a href="https://qizarbilal-skillmatch-ai.hf.space/dashboard" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: #ffffff !important; padding: 14px 32px; text-decoration: none; font-size: 16px; font-weight: 600; border-radius: 8px; display: inline-block; box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);">Access Your Dashboard</a>
            </div>
            <p style="color: #64748b; font-size: 14px; text-align: center; margin-top: 40px; border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 24px;">
                Ready to elevate your career? Let's get started.
            </p>
        </div>
    </body>
    </html>
    """
    
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept": "application/json",
                "api-key": brevo_api_key,
                "content-type": "application/json"
            },
            json={
                "sender": {"name": "SkillMatch", "email": from_email},
                "to": [{"email": to_email}],
                "subject": "Welcome to SkillMatch!",
                "htmlContent": html
            },
            timeout=10
        )
        if response.status_code in [200, 201, 202]:
            print(f"Successfully sent Welcome email to {to_email} via Brevo")
        else:
            print(f"Failed to send Welcome email via Brevo: {response.text}")
    except Exception as e:
        print(f"Failed to send welcome email: {e}")

@app.post("/auth/register")
def register(req: RegisterRequest, background_tasks: BackgroundTasks):
    try:
        existing = users_collection().find_one({"email": req.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if len(req.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        hashed = hash_password(req.password)
        
        # Generate 6-digit OTP
        otp_code = "".join([str(secrets.randbelow(10)) for _ in range(6)])
        
        
        # Upsert OTP record
        otp_doc = {
            "email": req.email,
            "otp": otp_code,
            "expiry": datetime.utcnow() + timedelta(minutes=5),
            "verified": False,
            "password_hash": hashed
        }
        

        
        otp_collection().update_one(
            {"email": req.email},
            {"$set": otp_doc},
            upsert=True
        )
        
        background_tasks.add_task(send_otp_email, req.email, otp_code)
        
        return {"message": "OTP sent to email", "email": req.email, "requires_otp": True}
    except pymongo.errors.OperationFailure as e:
        print(f"Registration OperationFailure: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Database operation failed: {str(e)}"
        )
    except pymongo.errors.PyMongoError as e:
        print(f"Registration PyMongoError: {e}")
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")

@app.post("/auth/verify-otp")
def verify_otp(req: VerifyOTPRequest, background_tasks: BackgroundTasks):
    try:
        otp_record = otp_collection().find_one({"email": req.email})
        
        if not otp_record:
            raise HTTPException(status_code=400, detail="No pending registration found for this email")
            
        if otp_record["verified"]:
            raise HTTPException(status_code=400, detail="User is already verified")
            
        if datetime.utcnow() > otp_record["expiry"]:
            raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")
            
        if otp_record["otp"] != req.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
            
        # OTP is valid, mark as verified and create user
        otp_collection().update_one({"email": req.email}, {"$set": {"verified": True}})
        
        # Check if user somehow was created
        existing = users_collection().find_one({"email": req.email})
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
            
        user_count = users_collection().count_documents({})
        user_id = user_count + 1
        
        user_doc = {
            "user_id": user_id,
            "email": req.email,
            "password_hash": otp_record["password_hash"],
            "created_at": datetime.utcnow()
        }
        users_collection().insert_one(user_doc)
        
        # Clean up OTP record
        otp_collection().delete_one({"email": req.email})
        
        # Generate token
        token = create_access_token({"user_id": user_id, "email": req.email})
        
        # Get username prefix from email for welcome
        user_name = req.email.split("@")[0].capitalize()
        background_tasks.add_task(send_welcome_email, req.email, user_name)
        
        return {
            "user_id": user_id,
            "email": req.email,
            "token": token
        }
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

@app.post("/auth/resend-otp")
def resend_otp(req: ResendOTPRequest, background_tasks: BackgroundTasks):
    try:
        otp_record = otp_collection().find_one({"email": req.email})
        if not otp_record:
            raise HTTPException(status_code=400, detail="No pending signup found")
            
        # Optional basic rate-limiting (only resend if within 4 mins to expiry, or just 1 min has passed)
        if otp_record["expiry"] > datetime.utcnow() + timedelta(minutes=4):
            raise HTTPException(status_code=429, detail="Please wait a minute before requesting a new OTP")
            
        otp_code = "".join([str(secrets.randbelow(10)) for _ in range(6)])
        
        otp_collection().update_one(
            {"email": req.email},
            {"$set": {
                "otp": otp_code,
                "expiry": datetime.utcnow() + timedelta(minutes=5)
            }}
        )
        

        
        background_tasks.add_task(send_otp_email, req.email, otp_code)
        
        return {"message": "OTP resent"}
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")


@app.post("/auth/login")
def login(req: LoginRequest):
    try:
        user = users_collection().find_one({"email": req.email})
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
    except pymongo.errors.OperationFailure as e:
        print(f"Login OperationFailure: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Database authentication failed: {str(e)}"
        )
    except pymongo.errors.PyMongoError as e:
        print(f"Login PyMongoError: {e}")
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")


@app.get("/auth/me")
def get_current_user(user_id: int = Depends(verify_token)):
    try:
        user = users_collection().find_one({"user_id": user_id})
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
        submissions = list(submissions_collection().find({"user_id": user_id}).sort("created_at", -1))
        
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
    
    import numpy as np
    img_array = np.array(image)
    
    try:
        import cv2
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_array = clahe.apply(img_array)
        
        img_array = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
        
        img_array = cv2.adaptiveThreshold(
            img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        image = Image.fromarray(img_array)
    except ImportError:
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
        r'\b[a-z]{2,3}[wxy]{2,}[a-z]{2,3}\b',
    ]
    
    garbled_count = 0
    for pattern in garbled_patterns:
        matches = re.findall(pattern, text.lower())
        garbled_count += len(matches)
    
    if len(words) > 0 and garbled_count > len(words) * 0.15:
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
        if not fitz:
            raise ImportError("PyMuPDF (fitz) not installed")
        
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
                config='--psm 6 --oem 3 -c preserve_interword_spaces=1'
            )
            ocr_text += page_text + " "
        
        pdf_document.close()
        
        print(f"OCR text length: {len(ocr_text)}")
        print(f"OCR sample: {ocr_text[:200] if ocr_text else 'No OCR text'}")
        
        ocr_quality_ok = is_text_quality_good(ocr_text)
        original_quality_ok = is_text_quality_good(text)
        
        if not ocr_quality_ok and not original_quality_ok:
            raise Exception(
                "Unable to extract readable text from PDF. This may be due to:\n"
                "1. Poor scan quality (try rescanning at higher resolution)\n"
                "2. Image-based PDF without proper text layer\n"
                "3. Unusual fonts or encoding\n"
                "Please provide a text-based PDF or higher quality scan."
            )
        
        if ocr_quality_ok and not original_quality_ok:
            return ocr_text
        elif original_quality_ok and not ocr_quality_ok:
            return text
        elif ocr_quality_ok and original_quality_ok:
            return ocr_text if len(ocr_text) > len(text) else text
        elif len(ocr_text) > len(text) and len(ocr_text) > 100:
            print("⚠️ WARNING: OCR text quality is poor but using it anyway (better than extracted text)")
            return ocr_text
        else:
            print("⚠️ WARNING: Using extracted text despite poor quality")
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



# Global runtime cache for NLP/ML objects
_nlp_cache = {}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...), 
    job_description: Optional[str] = Form(None), 
    jd_file: Optional[UploadFile] = File(None),
    user_id: int = Depends(verify_token)
):
    # Stage 1: Text Extraction
    def extract_text(file, ext):
        if ext == "pdf":
            return read_pdf(file)
        elif ext == "docx":
            return read_docx(file)
        else:
            set_pytesseract_path()
            return read_image(file)

    ext = resume.filename.split(".")[-1].lower()
    raw = extract_text(resume.file, ext)
    del ext
    gc.collect()

    # Stage 2: Preprocessing
    if "clean_text" not in _nlp_cache:
        from backend.nlp_engine import clean_text
        _nlp_cache["clean_text"] = clean_text
    cleaned_resume = _nlp_cache["clean_text"](raw)
    del _nlp_cache["clean_text"]
    gc.collect()

    # Stage 3: Structured Parsing
    if "parse_resume_structured" not in _nlp_cache:
        from backend.nlp_engine import parse_resume_structured
        _nlp_cache["parse_resume_structured"] = parse_resume_structured
    resume_structured = _nlp_cache["parse_resume_structured"](raw)
    del _nlp_cache["parse_resume_structured"]
    gc.collect()

    # Stage 4: JD Extraction
    if jd_file:
        jd_ext = jd_file.filename.split(".")[-1].lower()
        jd_text = extract_text(jd_file.file, jd_ext)
        del jd_ext
    elif job_description:
        jd_text = job_description
    else:
        raise HTTPException(status_code=400, detail="Either job_description text or jd_file must be provided")
    gc.collect()

    # Stage 5: JD Preprocessing
    if "clean_text" not in _nlp_cache:
        from backend.nlp_engine import clean_text
        _nlp_cache["clean_text"] = clean_text
    cleaned_jd = _nlp_cache["clean_text"](jd_text)
    del _nlp_cache["clean_text"]
    gc.collect()

    # Stage 6: JD Structured Parsing
    if "parse_jd_structured" not in _nlp_cache:
        from backend.nlp_engine import parse_jd_structured
        _nlp_cache["parse_jd_structured"] = parse_jd_structured
    jd_structured = _nlp_cache["parse_jd_structured"](jd_text)
    del _nlp_cache["parse_jd_structured"]
    gc.collect()

    # Stage 7: Preprocessing tokens
    if "preprocess_text" not in _nlp_cache:
        from backend.nlp_preprocessing import preprocess_text
        _nlp_cache["preprocess_text"] = preprocess_text
    resume_preprocessed = _nlp_cache["preprocess_text"](raw)
    jd_preprocessed = _nlp_cache["preprocess_text"](jd_text)
    del _nlp_cache["preprocess_text"]
    gc.collect()

    # Stage 8: Skill Extraction
    if "extract_skills_hybrid" not in _nlp_cache:
        from backend.nlp_preprocessing import extract_skills_hybrid
        _nlp_cache["extract_skills_hybrid"] = extract_skills_hybrid
    resume_skills_extracted = _nlp_cache["extract_skills_hybrid"](raw)
    del _nlp_cache["extract_skills_hybrid"]
    gc.collect()

    if "extract_keywords_hybrid" not in _nlp_cache:
        from backend.nlp_preprocessing import extract_keywords_hybrid
        _nlp_cache["extract_keywords_hybrid"] = extract_keywords_hybrid
    jd_skills_extracted = _nlp_cache["extract_keywords_hybrid"](jd_text)
    del _nlp_cache["extract_keywords_hybrid"]
    gc.collect()

    # Stage 9: Manual TF-IDF Vectorization (memory safe)
    from backend.nlp_preprocessing import compute_idf, compute_tfidf, cosine_similarity_sparse, tokenize
    idf = compute_idf([raw, jd_text])
    resume_tfidf = compute_tfidf(raw, idf)
    jd_tfidf = compute_tfidf(jd_text, idf)
    feature_names = list(idf.keys())
    tfidf_data = {
        'resume_tfidf_vector': [resume_tfidf.get(f, 0.0) for f in feature_names],
        'jd_tfidf_vector': [jd_tfidf.get(f, 0.0) for f in feature_names],
        'feature_names': feature_names
    }
    del idf, resume_tfidf, jd_tfidf, feature_names
    gc.collect()

    rid = str(uuid.uuid4())[:8]

    # Stage 10: DB Submission
    try:
        submission_count = submissions_collection().count_documents({})
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
        submissions_collection().insert_one(submission_doc)
    except Exception as e:
        print(f"MongoDB insertion warning: {str(e)}")
    gc.collect()

    # Stage 11: Skill/Keyword Cleaning
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
    junk_terms = {'general', 'dev', 'development', 'programming', 'coding', 'scripting', 'software', 'web', 'application'}
    clean_resume_skills = [s for s in resume_skills_extracted if s.lower() not in junk_terms]
    clean_jd_skills = [s for s in jd_skills_extracted if s.lower() not in junk_terms]
    clean_all_resume_skills = [s for s in all_resume_skills if s.lower() not in junk_terms]
    clean_all_jd_keywords = [s for s in all_jd_keywords if s.lower() not in junk_terms]
    if len(clean_all_resume_skills) == 0 and len(clean_resume_skills) > 0:
        resume_structured['technical_skills'] = clean_resume_skills[:15]
        resume_structured['tools'] = []
        resume_structured['frameworks'] = []
        resume_structured['programming_languages'] = []
        resume_structured['databases'] = []
    if len(clean_all_jd_keywords) == 0 and len(clean_jd_skills) > 0:
        jd_structured['required_skills'] = clean_jd_skills[:15]
        jd_structured['required_frameworks'] = []
        jd_structured['required_tools'] = []
        jd_structured['required_languages'] = []
        jd_structured['required_databases'] = []
    gc.collect()

    # Stage 12: Profile Construction
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
    gc.collect()

    # Stage 13: Profile Comparison
    if "compare_profiles" not in _nlp_cache:
        from backend.comparison_engine import compare_profiles
        _nlp_cache["compare_profiles"] = compare_profiles
    comparison_result = _nlp_cache["compare_profiles"](resume_profile_obj, job_profile_obj)
    del _nlp_cache["compare_profiles"]
    gc.collect()

    # Stage 14: Skill Suggestions
    all_jd_skills = (
        jd_structured['required_skills'] + 
        jd_structured['required_frameworks'] + 
        jd_structured['required_tools'] + 
        jd_structured['required_languages'] +
        jd_structured['required_databases']
    )
    if "generate_skill_suggestions" not in _nlp_cache:
        from backend.suggestion_engine import generate_skill_suggestions
        _nlp_cache["generate_skill_suggestions"] = generate_skill_suggestions
    skill_suggestions = _nlp_cache["generate_skill_suggestions"](
        jd_skills=all_jd_skills,
        resume_skills=all_resume_skills,
        job_role=jd_structured['job_role'],
        jd_text=jd_text,
        missing_skills=comparison_result['missing_skills']
    )
    del _nlp_cache["generate_skill_suggestions"]
    gc.collect()

    # Stage 15: DB Insert for Analysis
    try:
        resume_doc = {
            'resume_id': rid,
            'user_id': user_id,
            'profile': resume_profile_obj,
            'raw_text': raw,
            'created_at': datetime.utcnow()
        }
        resumes_collection().insert_one(resume_doc)
        jd_doc = {
            'jd_id': rid,
            'user_id': user_id,
            'profile': job_profile_obj,
            'raw_text': jd_text,
            'created_at': datetime.utcnow()
        }
        job_descriptions_collection().insert_one(jd_doc)
        analysis_doc = {
            'analysis_id': rid,
            'user_id': user_id,
            'resume_id': rid,
            'jd_id': rid,
            'comparison': comparison_result,
            'match_percentage': comparison_result['match_percentage'],
            'suggested_skills': skill_suggestions['suggested_skills'],
            'missing_skills_explained': skill_suggestions['missing_skills_explained'],
            'created_at': datetime.utcnow()
        }
        analysis_results_collection().insert_one(analysis_doc)
    except Exception as e:
        print(f"MongoDB insertion warning: {str(e)}")
    gc.collect()

    # Stage 16: Response Construction
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
        "skill_suggestions": skill_suggestions,
        "dataset_size": 0 if 'submission_count' not in locals() else submissions_collection().count_documents({})
    }

@app.get("/admin/analytics")
def get_admin_analytics(user_id: int = Depends(verify_token)):
    if not validate_admin_role(users_collection(), user_id):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        analytics = get_analytics_summary(
            users_collection(),
            submissions_collection(),
            analysis_results_collection()
        )
        
        top_missing = get_top_missing_skills(analysis_results_collection(), limit=20)
        top_roles = get_top_job_roles(submissions_collection(), limit=15)
        category_dist = get_skill_category_distribution(analysis_results_collection())
        rec_dist = get_recommendation_distribution(analysis_results_collection())
        recent = get_recent_analyses(analysis_results_collection(), limit=10)
        
        return {
            "summary": analytics,
            "top_missing_skills": top_missing,
            "top_job_roles": top_roles,
            "skill_category_distribution": category_dist,
            "recommendation_distribution": rec_dist,
            "recent_analyses": recent
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@app.get("/admin/validate")
def validate_admin(user_id: int = Depends(verify_token)):
    is_admin = validate_admin_role(users_collection(), user_id)
    return {"is_admin": is_admin}

@app.get("/health")
def health_check():
    """Fast health check endpoint for Render"""
    db_healthy = quick_health_check()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if db_healthy else "disconnected",
        "app_ready": app_ready
    }

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    file_path = f"frontend/dist/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("frontend/dist/index.html")


# Force HF rebuild
