# 🚀 Smart Internship Screening Dashboard

## Why This Architecture?

### Business Problem Solved
When you're hiring for internships at scale, you face:
- **Volume Overload**: 100+ applications for 5 spots
- **Manual Screening Time**: 5-10 min per resume = 40+ hours
- **Inconsistent Evaluation**: Different reviewers = different standards
- **Referral Blindness**: Hard to track which referral sources yield best hires

### Technical Solution
This MVP automates 80% of initial screening while maintaining human oversight for final decisions.

**Architecture Decisions:**

1. **React Frontend** - Modern, component-based UI for rapid iteration
2. **Node.js/Express Backend** - JavaScript everywhere = faster development
3. **Python AI Service** - Best ML/NLP libraries for resume parsing
4. **SQLite** - Zero-config database perfect for MVP demonstration
5. **D3.js** - Professional data visualization for referral networks

## Tech Stack (Matches Industry Standards)

### Frontend
- React 18 with Hooks
- Tailwind CSS (rapid UI development)
- React Router (navigation)
- D3.js (network graphs)
- Axios (API calls)

### Backend
- Node.js + Express
- JWT authentication
- SQLite3 (production would use PostgreSQL)
- RESTful API design

### AI Layer
- Python 3.9+
- spaCy (NLP)
- scikit-learn (scoring algorithm)
- Flask (microservice)

## 🎯 Core Features

1. **Resume Upload & Auto-Parse**
   - Drag-drop interface
   - Extracts: Name, College, CGPA, Skills, Projects, Experience

2. **AI-Powered Scoring**
   - Skills match analysis
   - CGPA weighting
   - Project complexity assessment
   - Experience bonus points

3. **Candidate Dashboard**
   - Sortable by score, CGPA, skills
   - Quick filters (college tier, skill tags)
   - Bulk actions (shortlist, reject)

4. **Referral Network Visualizer** (X-Factor)
   - Interactive graph of referral connections
   - Color-coded by conversion rate
   - Identifies "golden referrers"

## 📁 Project Structure

```
internship-screener/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Main page views
│   │   ├── services/        # API integration
│   │   └── utils/           # Helper functions
│   └── package.json
│
├── backend/                  # Node.js API
│   ├── src/
│   │   ├── routes/          # API endpoints
│   │   ├── controllers/     # Business logic
│   │   ├── models/          # Database models
│   │   ├── middleware/      # Auth, validation
│   │   └── config/          # Configuration
│   └── package.json
│
├── ai-service/              # Python ML service
│   ├── app.py               # Flask API
│   ├── parser.py            # Resume parsing logic
│   ├── scorer.py            # Candidate scoring
│   └── requirements.txt
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.9+
- npm or yarn

### Installation

```bash
# 1. Clone and navigate
cd internship-screener

# 2. Install Backend
cd backend
npm install
npm run dev    # Runs on http://localhost:5000

# 3. Install AI Service (new terminal)
cd ../ai-service
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py  # Runs on http://localhost:5001

# 4. Install Frontend (new terminal)
cd ../frontend
npm install
npm start      # Runs on http://localhost:3000
```

### Test Data
The system comes pre-loaded with 20 sample candidates. Upload new resumes via the dashboard.

## 🎨 Key Implementation Highlights

### 1. Intelligent Resume Parsing
```python
# Uses NLP to extract structured data from unstructured text
entities = nlp(resume_text)
skills = extract_skills(entities)  # Custom skill extraction
projects = identify_projects(resume_text)
```

### 2. Multi-Factor Scoring Algorithm
```javascript
score = (
  skillsMatch * 0.4 +      // 40% weight
  cgpaScore * 0.25 +       // 25% weight
  projectScore * 0.20 +    // 20% weight
  experienceScore * 0.15   // 15% weight
)
```

### 3. Real-time Network Analysis
Uses force-directed graph layout to show referral clusters and identify high-value referrers.

## 🔒 Security Features
- JWT-based authentication
- Input sanitization
- SQL injection protection
- Rate limiting on API endpoints

## 🔄 Production Considerations

### What I'd Add for Production:
1. **Database**: Migrate to PostgreSQL with proper indexing
2. **File Storage**: S3 for resume PDFs instead of local storage
3. **Caching**: Redis for frequently accessed candidate lists
4. **Email**: Automated notifications to shortlisted candidates
5. **Analytics**: Hiring funnel metrics and time-to-hire tracking
6. **Integrations**: LinkedIn API, ATS systems
7. **Testing**: Jest + Pytest with 80%+ coverage

### Scalability Path:
- Current: Handles 1000 applications
- With optimization: 10,000+ applications
- Containerize with Docker
- Deploy on AWS/GCP with auto-scaling

## 📈 Business Impact

**Time Saved:**
- Manual screening: 10 min/candidate × 500 = 83 hours
- With this tool: 2 min/candidate × 50 shortlisted = 1.6 hours
- **ROI: 98% time reduction**

**Quality Improvement:**
- Consistent evaluation criteria
- No unconscious bias in initial screening
- Data-driven referral optimization

## 🎓 Learning Outcomes

Building this taught me:
1. Full-stack architecture with microservices
2. AI/ML integration in production apps
3. Real-time data visualization
4. Designing for HR/recruiting workflows
5. Balancing automation with human oversight

## 📞 Contact
Built by Mridul.

Ready to discuss how I can bring this thinking to your team.