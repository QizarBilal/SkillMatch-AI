# 🎯 SkillMatch AI - Enterprise AI ATS Engine

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LLaMA-3](https://img.shields.io/badge/LLaMA--3-70B-purple?style=for-the-badge)

SkillMatch AI is a next-generation Applicant Tracking System (ATS) powered by **Llama-3 70B** through the Groq API, SpaCy NLP, and a React & Vite frontend. It goes beyond simple keyword matching to perform deep, universal semantic analyses between Resumes and Job Descriptions across *any* industry.

## 🚀 Live Demo
Experience the full power of SkillMatch AI live on Hugging Face Spaces:
👉 **[SkillMatch AI - Live Deployment](https://qizarbilal-skillmatch-ai.hf.space/)**

---

## ✨ Features

- **🌐 Universal LLM Engine**: Parses Resumes and Job Descriptions natively for Technical (Engineering, Software) AND Non-Technical (Nursing, Management, Healthcare) roles without relying on rigid hardcoded dictionaries.
- **📊 Precise AI Match Scoring**: Calculates compatibility scores by weighing required core skills, bonus/additional skills, education validity, and experience gaps.
- **📥 Clean PDF Report Exports**: Generates structured, fully-text-selectable Executive Analysis Reports instantly via pure `jsPDF` and `jspdf-autotable`.
- **🎓 Interactive Learning Roadmaps**: Identifies exactly what skills a candidate is missing, prioritizes them, and provides 1-click animated UI triggers that immediately launch curated video tutorial searches.
- **🔒 Secure Architecture**: Employs bcrypt password hashing, HTTP-Only JWT tokens, backend-enforced admin privileges, and SMTP-driven Email OTP verification. 
- **📈 Admin Analytics Dashboard (Premium)**: Advanced administrative insights into the top missing skills across all applicants, user telemetry, and dynamic job-market requirement distributions.

---

## 🏗️ Architecture Stack

### Backend
- **Framework**: Python 3.10+, FastAPI, Uvicorn (ASGI)
- **AI/NLP**: Groq API (LLaMA-3 70B), SpaCy, NLTK, Scikit-learn (TF-IDF Vectorization)
- **Database**: MongoDB Atlas (NoSQL) with Motor Asyncio
- **Security**: JWT (PyJWT), Passlib (Bcrypt), Brevo SMTP

### Frontend
- **Framework**: React.js 18+ (Vite Build Pipeline)
- **Styling**: Vanilla CSS with modern Glassmorphism, tailored Hover micro-animations, Grid & Flexbox
- **PDF Generation**: jsPDF, jspdf-autotable
- **Routing**: React Router DOM

---

## 🛠️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/QizarBilal/SkillMatch-AI.git
cd SkillMatch-AI
```

### 2. Backend Config
```bash
cd backend
pip install -r requirements.txt
```
Create a `.env` file in the root containing your database & API keys:
```env
MONGO_USERNAME=xxx
MONGO_PASSWORD=xxx
MONGO_CLUSTER=xxx
MONGO_DATABASE=SkillMatch

JWT_SECRET_KEY=your_secure_secret
JWT_ALGORITHM=HS256

GROQ_API_KEY=gsk_your_groq_llama_key

SMTP_USER=xxx
SMTP_PASS=xxx
EMAIL_FROM=xxx
```

### 3. Frontend Config
```bash
cd frontend
npm install
npm run dev
```

### 4. Boot the Server
```bash
# In another terminal window from /backend:
python -m uvicorn main:app --port 8000 --env-file ../.env
```
Visit `http://localhost:5173`!

---

💡 *Designed and engineered for efficiency, beauty, and true utility by Mohammed Qizar Bilal.*
