from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import joblib
import json
import numpy as np
import csv
import io
from datetime import datetime, timezone
from backend.preprocessing import preprocess_and_lemmatize

BASE_DIR = Path(__file__).parent.parent

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
    """Validate input, apply title weighting, lemmatize, and return vectorized features"""
    body = body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="Review body cannot be empty")
    if title:
        text = (title.strip() + ' ') * TITLE_WEIGHT + body
    else:
        text = body
    text = preprocess_and_lemmatize(text)
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


class BatchPredictionRow(BaseModel):
    row: int
    title: Optional[str] = None
    body: str
    reparto_consigliato: str
    modello_reparto: str
    probabilita_reparto: Optional[float] = None
    sentiment: str
    modello_sentiment: str
    probabilita_sentiment: Optional[float] = None
    predicted_at: str


class BatchPredictResponse(BaseModel):
    total_rows: int
    results: List[BatchPredictionRow]


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


def _best_prediction(predictions: List[PredictionResult]) -> tuple[str, Optional[float], str]:
    """Return label, confidence, and model with highest confidence (or fallback to first)."""
    if not predictions:
        return "", None, ""

    with_conf = [p for p in predictions if p.confidence is not None]
    if with_conf:
        best = max(with_conf, key=lambda p: p.confidence if p.confidence is not None else -1.0)
        return best.prediction, best.confidence, best.model

    return predictions[0].prediction, None, predictions[0].model


@app.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch_csv(file: UploadFile = File(...)):
    """Predict department and sentiment in batch from uploaded CSV.

    Required columns: `body`
    Optional columns: `title`
    """
    filename = (file.filename or "").lower()
    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")

    content = await file.read()
    try:
        text_stream = io.StringIO(content.decode("utf-8"))
    except UnicodeDecodeError:
        text_stream = io.StringIO(content.decode("latin-1"))

    reader = csv.DictReader(text_stream)
    if not reader.fieldnames or "body" not in reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV must contain a 'body' column")

    results: List[BatchPredictionRow] = []
    for idx, row in enumerate(reader, start=1):
        body = (row.get("body") or "").strip()
        title = (row.get("title") or "").strip() or None
        if not body:
            continue

        X = prepare_text(title, body)

        dept_predictions: List[PredictionResult] = []
        for model_name, model in dept_models.items():
            pred_idx = int(model.predict(X)[0])
            pred_label = DEPT_LABELS[pred_idx]
            confidence = None
            if hasattr(model, "predict_proba"):
                confidence = float(np.max(model.predict_proba(X)[0]))
            dept_predictions.append(
                PredictionResult(model=model_name, prediction=pred_label, confidence=confidence)
            )

        sent_predictions: List[PredictionResult] = []
        for model_name, model in sent_models.items():
            pred_idx = int(model.predict(X)[0])
            pred_label = SENT_LABELS[pred_idx]
            confidence = None
            if hasattr(model, "predict_proba"):
                confidence = float(np.max(model.predict_proba(X)[0]))
            sent_predictions.append(
                PredictionResult(model=model_name, prediction=pred_label, confidence=confidence)
            )

        best_dept, best_dept_prob, best_dept_model = _best_prediction(dept_predictions)
        best_sent, best_sent_prob, best_sent_model = _best_prediction(sent_predictions)

        results.append(
            BatchPredictionRow(
                row=idx,
                title=title,
                body=body,
                reparto_consigliato=best_dept,
                modello_reparto=best_dept_model,
                probabilita_reparto=best_dept_prob,
                sentiment=best_sent,
                modello_sentiment=best_sent_model,
                probabilita_sentiment=best_sent_prob,
                predicted_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    return BatchPredictResponse(total_rows=len(results), results=results)


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


# Serve the built frontend in production
FRONTEND_DIR = BASE_DIR / "frontend" / "dist"
if FRONTEND_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        """Serve the React SPA for any non-API route"""
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")
