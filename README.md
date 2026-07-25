# ATS Resume Matcher

> Upload your resume + a job description → get an ATS match score, missing keywords, and a verdict. Built to solve a real problem: most resumes get filtered by bots before a human ever reads them.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange)

---

## What it does

- Upload your resume (PDF) and paste any job description
- Uses **TF-IDF + cosine similarity** (scikit-learn) to compute a match score (0–100%)
- Shows which important JD keywords are **missing from your resume**
- Saves every check to a database so you can track improvement over time
- No paid AI APIs — pure NLP, fully explainable

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend API | FastAPI |
| Matching Engine | scikit-learn (TF-IDF + cosine similarity) |
| PDF Parsing | pypdf |
| Database | SQLAlchemy ORM + SQLite (local) / MySQL (prod) |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | AWS EC2 (free tier) |

---

## Project Structure

```
ats-matcher/
├── app/
│   ├── main.py          # FastAPI app + endpoints
│   ├── matcher.py       # Core NLP matching logic
│   ├── models.py        # SQLAlchemy DB model
│   ├── database.py      # DB connection + session
│   └── pdf_utils.py     # PDF text extraction
├── static/
│   └── index.html       # Frontend UI
├── requirements.txt
└── README.md
```

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ats-matcher.git
cd ats-matcher

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload

# 5. Open in browser
# http://localhost:8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/analyze` | Upload PDF + JD, returns score + missing keywords |
| GET | `/history` | Returns last 20 match checks |
| GET | `/` | Serves the frontend |

### Example Response

```json
{
  "score": 63.4,
  "verdict": "Moderate match — consider adding some missing keywords.",
  "missing_keywords": ["docker", "postgresql", "ci", "pipelines", "aws"]
}
```

---

## Switch to MySQL (Production)

Set the `DATABASE_URL` environment variable before running:

```bash
export DATABASE_URL="mysql+pymysql://username:password@host:3306/ats_matcher"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Deploy on AWS EC2 (Free Tier)

```bash
# SSH into your EC2 instance, then:
git clone https://github.com/YOUR_USERNAME/ats-matcher.git
cd ats-matcher
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production, use `gunicorn` + `nginx` as a reverse proxy.

---

## Why I Built This

Every fresher applies to 100 jobs and hears back from 3. Most rejections happen before a human reads your resume — ATS software scores it against the JD and filters it out. I built this tool to make that invisible scoring process visible, so you can fix your resume before applying.

---

## Author

**[Janvhi Shukla]** — [GitHub](https://github.com/janvhishukla04) · [LinkedIn](https://linkedin.com/in/janvhi-shukla-9803962a6)
