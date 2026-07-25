import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_match_score(resume_text: str, jd_text: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([clean_text(resume_text), clean_text(jd_text)])
    return round(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100, 2)

def get_missing_keywords(resume_text: str, jd_text: str, top_n: int = 15) -> list:
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([jd_clean])
    word_scores = list(zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]))
    word_scores.sort(key=lambda x: x[1], reverse=True)
    resume_words = set(resume_clean.split())
    missing = [w for w, s in word_scores if w not in resume_words and s > 0]
    return missing[:top_n]

def analyze(resume_text: str, jd_text: str) -> dict:
    score = get_match_score(resume_text, jd_text)
    missing = get_missing_keywords(resume_text, jd_text)
    if score >= 75:
        verdict = "Strong match — your resume aligns well with this JD."
    elif score >= 50:
        verdict = "Moderate match — consider adding some missing keywords."
    else:
        verdict = "Weak match — your resume may get filtered by ATS."
    return {"score": score, "verdict": verdict, "missing_keywords": missing}
