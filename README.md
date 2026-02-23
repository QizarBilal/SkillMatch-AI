# SkillMatch AI

**Where Skills Meet Opportunities**

SkillMatch AI is an intelligent resume-job matching system that uses Natural Language Processing (NLP) and machine learning to analyze resumes and job descriptions, providing detailed compatibility scores and actionable suggestions for improvement.

## 🚀 Features

- **AI-Powered Matching**: Advanced NLP algorithms analyze skills, experience, and qualifications
- **Detailed Analytics**: Comprehensive reports with skill matching, experience analysis, and education verification
- **Smart Suggestions**: Personalized recommendations to improve resume-job fit
- **Admin Dashboard**: Manage submissions, view analytics, and monitor system performance
- **Secure Authentication**: JWT-based authentication with role-based access control
- **MongoDB Integration**: Scalable cloud database for storing resumes and analysis results
- **Modern UI**: Responsive React frontend with intuitive user experience

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SkillMatch.git
cd SkillMatch
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
MONGO_USERNAME=your_mongodb_username
MONGO_PASSWORD=your_mongodb_password
MONGO_CLUSTER=your_cluster.mongodb.net
MONGO_DATABASE=SkillMatch
JWT_SECRET_KEY=your_secure_secret_key_here
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker Only

```bash
# Build the image
docker build -t skillmatch-ai .

# Run the container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name skillmatch \
  skillmatch-ai
```

## 📊 MongoDB Setup

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Add a database user
4. Whitelist your IP address (or use `0.0.0.0/0` for testing)
5. Get your connection string and update `.env`

## 🔑 Default Credentials

**Admin Account:**
- Email: admin@skillmatch.com
- Password: admin123

**⚠️ Change these credentials in production!**

## 📁 Project Structure

```
SkillMatch/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── auth.py                 # Authentication logic
│   ├── admin.py                # Admin routes
│   ├── mongodb.py              # Database connection
│   ├── nlp_engine.py           # NLP processing
│   ├── nlp_preprocessing.py    # Text preprocessing
│   ├── comparison_engine.py    # Matching algorithm
│   ├── suggestion_engine.py    # Suggestions generator
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main app component
│   │   ├── Dashboard.jsx      # User dashboard
│   │   ├── Admin.jsx          # Admin panel
│   │   ├── Login.jsx          # Login page
│   │   └── Signup.jsx         # Registration page
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /login` - User login
- `GET /profile` - Get user profile

### Resume Analysis
- `POST /upload-resume` - Upload resume file
- `POST /upload-jd` - Upload job description
- `POST /analyze` - Analyze resume vs job description
- `GET /history` - Get analysis history

### Admin
- `GET /admin/submissions` - View all submissions
- `GET /admin/statistics` - System statistics
- `DELETE /admin/delete/{analysis_id}` - Delete analysis

## 🚀 Production Deployment

### Deploy to Railway

1. Fork this repository
2. Sign up at [Railway](https://railway.app)
3. Create new project from GitHub repo
4. Add environment variables from `.env.example`
5. Deploy!

### Deploy to Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Build Command: `pip install -r backend/requirements.txt && cd frontend && npm install && npm run build`
4. Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Deploy to Heroku

```bash
heroku create skillmatch-ai
heroku config:set MONGO_USERNAME=your_username
heroku config:set MONGO_PASSWORD=your_password
# ... add other env vars
git push heroku main
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🛡️ Security Considerations

1. **Never commit `.env` files**
2. Use strong JWT secret keys (32+ characters)
3. Change default admin credentials
4. Enable MongoDB IP whitelisting
5. Use HTTPS in production
6. Regularly update dependencies

## 📈 Performance Optimization

- NLP models are cached after first load
- MongoDB indexes on frequently queried fields
- Frontend assets are minified and compressed
- Docker multi-stage builds for smaller images

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Test connection
python backend/test_connection.py
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Author

- Mohammed Qizar Bilal - Full Stack Development & AI Integration

## 🙏 Acknowledgments

- spaCy for NLP processing
- FastAPI for the backend framework
- React for the frontend
- MongoDB Atlas for cloud database
- All contributors and supporters

## 📧 Contact

For questions or support, please open an issue or contact: bilalqizar@gmail.com

---

Made with ❤️ by **Mohammed Qizar Bilal** as part of **Infosys Springboard AI Internship**
