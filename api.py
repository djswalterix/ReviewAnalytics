from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import joblib
import json
import numpy as np

BASE_DIR = Path(__file__).parent

app = FastAPI(
    title="Review Analytics API",
    description="API for hotel review classification (Department & Sentiment)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and vectorizer at startup
try:
    vectorizer = joblib.load(BASE_DIR / 'vectorizer.pkl')
    dept_models = joblib.load(BASE_DIR / 'all_dept_models.pkl')
    sent_models = joblib.load(BASE_DIR / 'all_sent_models.pkl')
except FileNotFoundError as e:
    raise RuntimeError(f"Model files not found. Run train.py first. Error: {e}")

DEPT_LABELS = ['Housekeeping', 'Reception', 'F&B']
SENT_LABELS = ['Negative', 'Positive']


# Title weight multiplier (must match train.py)
TITLE_WEIGHT = 2


def prepare_text(title: Optional[str], body: str):
    """Validate input, apply title weighting, and return vectorized features"""
    body = body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="Review body cannot be empty")
    if title:
        text = (title.strip() + ' ') * TITLE_WEIGHT + body
    else:
        text = body
    X = vectorizer.transform([text])
    return X


class ReviewRequest(BaseModel):
    title: Optional[str] = None
    body: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "Camera deludente",
                "body": "La camera era sporca e il personale scortese"
            }]
        }
    }


class PredictionResult(BaseModel):
    model: str
    prediction: str
    confidence: Optional[float] = None


class WordImpact(BaseModel):
    word: str
    impact: float


class DepartmentWordImpact(BaseModel):
    word: str
    department: str
    impact: float


class PredictResponse(BaseModel):
    review: str
    department: List[PredictionResult]
    sentiment: List[PredictionResult]
    sentiment_word_contributions: List[WordImpact] = Field(
        description="Per-word sentiment impact extracted from the Logistic Regression model only"
    )
    department_word_contributions: List[DepartmentWordImpact] = Field(
        description="Per-word department impact extracted from the Logistic Regression model only"
    )


@app.get("/dashboard")
def get_dashboard():
    """Return the dashboard data JSON with model metrics and comparisons"""
    try:
        with open(BASE_DIR / 'dashboard_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard data not found. Run train.py first.")


@app.post("/predict", response_model=PredictResponse)
def predict_review(request: ReviewRequest):
    """Predict department and sentiment for a review using all trained models"""
    X = prepare_text(request.title, request.body)
    
    # Predict using all department models
    dept_predictions = []
    for model_name, model in dept_models.items():
        pred_idx = int(model.predict(X)[0])
        pred_label = DEPT_LABELS[pred_idx]
        
        # Retrieve confidence score if the model supports probability estimation
        confidence = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)[0]
            confidence = float(np.max(proba))
        
        dept_predictions.append(PredictionResult(
            model=model_name,
            prediction=pred_label,
            confidence=confidence
        ))
    
    # Predict using all sentiment models
    sent_predictions = []
    for model_name, model in sent_models.items():
        pred_idx = int(model.predict(X)[0])
        pred_label = SENT_LABELS[pred_idx]
        
        # Retrieve confidence score if the model supports probability estimation
        confidence = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)[0]
            confidence = float(np.max(proba))
        
        sent_predictions.append(PredictionResult(
            model=model_name,
            prediction=pred_label,
            confidence=confidence
        ))
    
    return PredictResponse(
        review=request.body,
        department=dept_predictions,
        sentiment=sent_predictions,
        sentiment_word_contributions=get_sentiment_word_contributions(X),
        department_word_contributions=get_department_word_contributions(X)
    )


def get_sentiment_word_contributions(X) -> list[WordImpact]:
    """Extract per-word sentiment impact using the Logistic Regression model.

    Args:
        X: Sparse matrix of vectorized text features from the TF-IDF vectorizer
            corresponding to a single review.

    Returns:
        A list of WordImpact objects representing the contribution of each
        non-zero word feature to the sentiment prediction.
    """
    if 'Logistic Regression' not in sent_models:
        return []

    lr_model = sent_models['Logistic Regression']
    if lr_model.coef_.shape[0] != 1:
        return []  # Binary classification expected; skip if multiclass

    feature_names = vectorizer.get_feature_names_out()
    non_zero_indices = X[0].nonzero()[1]

    word_impacts = []
    for idx in non_zero_indices:
        word = feature_names[idx]
        impact = float(X[0, idx] * lr_model.coef_[0][idx])
        word_impacts.append(WordImpact(word=word, impact=impact))

    return sorted(word_impacts, key=lambda w: w.impact)


def get_department_word_contributions(X) -> list[DepartmentWordImpact]:
    """Extract per-word department impact using the Logistic Regression model.

    Args:
        X: Sparse matrix of vectorized text features from the TF-IDF vectorizer
            corresponding to a single review.
    """
    if 'Logistic Regression' not in dept_models:
        return []

    lr_model = dept_models['Logistic Regression']
    feature_names = vectorizer.get_feature_names_out()
    non_zero_indices = X[0].nonzero()[1]

    word_impacts = []
    for idx in non_zero_indices:
        word = feature_names[idx]
        tfidf_value = X[0, idx]
        # Select the class with the strongest absolute impact for this word
        class_impacts = [
            (DEPT_LABELS[c], float(tfidf_value * lr_model.coef_[c][idx]))
            for c in range(len(DEPT_LABELS))
        ]
        dept, impact = max(class_impacts, key=lambda x: abs(x[1]))
        word_impacts.append(DepartmentWordImpact(word=word, department=dept, impact=impact))

    return sorted(word_impacts, key=lambda w: abs(w.impact), reverse=True)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "models_loaded": True}
