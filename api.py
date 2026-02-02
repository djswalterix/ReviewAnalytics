from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import joblib
import json
import numpy as np

app = FastAPI(
    title="Review Analytics API",
    description="API for hotel review classification (Department & Sentiment)",
    version="1.0.0"
)

# Load models and vectorizer at startup
try:
    vectorizer = joblib.load('vectorizer.pkl')
    dept_models = joblib.load('all_dept_models.pkl')
    sent_models = joblib.load('all_sent_models.pkl')
except FileNotFoundError as e:
    raise RuntimeError(f"Model files not found. Run train.py first. Error: {e}")

DEPT_LABELS = ['Housekeeping', 'Reception', 'F&B']
SENT_LABELS = ['Negative', 'Positive']


class ReviewRequest(BaseModel):
    text: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "La camera era sporca e il personale scortese"}]
        }
    }


class PredictionResult(BaseModel):
    model: str
    prediction: str
    confidence: Optional[float] = None


class PredictResponse(BaseModel):
    review: str
    department: List[PredictionResult]
    sentiment: List[PredictionResult]


@app.get("/dashboard")
def get_dashboard():
    """Return the dashboard data JSON with model metrics and comparisons"""
    try:
        with open('dashboard_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard data not found. Run train.py first.")


@app.post("/predict", response_model=PredictResponse)
def predict_review(request: ReviewRequest):
    """Predict department and sentiment for a review using all trained models"""
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Review text cannot be empty")
    
    # Vectorize the input
    X = vectorizer.transform([text])
    
    # Get predictions from all department models
    dept_predictions = []
    for model_name, model in dept_models.items():
        pred_idx = model.predict(X)[0]
        pred_label = DEPT_LABELS[pred_idx]
        
        # Get confidence if model supports predict_proba
        confidence = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)[0]
            confidence = float(np.max(proba))
        
        dept_predictions.append(PredictionResult(
            model=model_name,
            prediction=pred_label,
            confidence=confidence
        ))
    
    # Get predictions from all sentiment models
    sent_predictions = []
    for model_name, model in sent_models.items():
        pred_idx = int(model.predict(X)[0])
        pred_label = SENT_LABELS[pred_idx]
        
        # Get confidence if model supports predict_proba
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
        review=text,
        department=dept_predictions,
        sentiment=sent_predictions
    )


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "models_loaded": True}
