import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import joblib
import json
from datetime import datetime
from backend.preprocessing import preprocess_and_lemmatize

BASE_DIR = Path(__file__).parent.parent
SEED = 42
np.random.seed(SEED)


BACKEND_DIR = Path(__file__).parent


def load_stop_words(filepath=BACKEND_DIR / 'stop_words.txt'):
    """Load stop words from a text file, ignoring comments and empty lines"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def evaluate_model(model, X_test, y_test):
    """Evaluate a model and return metrics dictionary"""
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    num_classes = len(np.unique(y_test))
    # Use binary F1 for 2-class problems (sentiment), macro F1 for multi-class (department)
    average = 'binary' if num_classes == 2 else 'macro'
    f1 = f1_score(y_test, preds, average=average)
    return {'accuracy': accuracy, 'f1_macro': f1, 'predictions': preds}


# Title weight multiplier (titles are repeated to increase their influence)
TITLE_WEIGHT = 2


def train_model():
    # 1. Load and preprocess data
    df = pd.read_csv(BASE_DIR / 'dataset_recensioni.csv')
    
    # Weight titles by repeating them
    df['full_text'] = df.apply(lambda row: (row['title'] + ' ') * TITLE_WEIGHT + row['body'], axis=1)
    
    dept_map = {'Housekeeping': 0, 'Reception': 1, 'F&B': 2}
    df['dept_label'] = df['department'].map(dept_map)

    # 2. Train/test split
    X_text_train, X_text_test, yd_train, yd_test, ys_train, ys_test = train_test_split(
        df['full_text'].values, 
        df['dept_label'].values, 
        df['target'].values, 
        test_size=0.2, 
        random_state=SEED
    )

    # 3. TF-IDF Vectorization
    stop_words = load_stop_words()
    
    # Pre-process: remove punctuation and lemmatize
    X_text_train_clean = [preprocess_and_lemmatize(text) for text in X_text_train]
    X_text_test_clean = [preprocess_and_lemmatize(text) for text in X_text_test]
    
    vectorizer = TfidfVectorizer(
        max_features=2000, 
        stop_words=stop_words,
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    X_train = vectorizer.fit_transform(X_text_train_clean)
    X_test = vectorizer.transform(X_text_test_clean)
    joblib.dump(vectorizer, BASE_DIR / 'vectorizer.pkl')

    # 4. Define models
    dept_models = {
        'Logistic Regression': LogisticRegression(solver='lbfgs', max_iter=1000, random_state=SEED, C=1.0),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=6, weights='distance', metric='cosine'),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=1, max_features='sqrt', random_state=SEED)
    }
    
    sent_models = {
        'Logistic Regression': LogisticRegression(solver='lbfgs', max_iter=1000, random_state=SEED, C=1.0),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=6, weights='distance', metric='cosine'),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=1, max_features='sqrt', random_state=SEED)
    }

    dept_names = ['Housekeeping', 'Reception', 'F&B']
    sent_names = ['Negative', 'Positive']
    
    # 5. Train and evaluate all models
    dept_results = {}
    sent_results = {}
    
    for model_name, model in dept_models.items():
        model.fit(X_train, yd_train)
        dept_results[model_name] = evaluate_model(model, X_test, yd_test)
    
    for model_name, model in sent_models.items():
        model.fit(X_train, ys_train)
        sent_results[model_name] = evaluate_model(model, X_test, ys_test)
    # 6. Find best models
    best_dept_name = max(dept_results, key=lambda x: dept_results[x]['f1_macro'])
    best_sent_name = max(sent_results, key=lambda x: sent_results[x]['f1_macro'])
    
    best_dept_result = dept_results[best_dept_name]
    best_sent_result = sent_results[best_sent_name]
    
    # 7. Compute confusion matrices for best models
    dept_cm = confusion_matrix(yd_test, best_dept_result['predictions'])
    sent_cm = confusion_matrix(ys_test, best_sent_result['predictions'])

    # 8. Extract feature importance from Logistic Regression coefficients
    feature_names = vectorizer.get_feature_names_out()
    lr_sent = sent_models['Logistic Regression']
    sent_coefs = lr_sent.coef_[0]

    top_pos_idx = np.argsort(sent_coefs)[-10:][::-1]
    top_neg_idx = np.argsort(sent_coefs)[:10]

    top_pos_words = [
        {"word": feature_names[i], "coefficient": float(sent_coefs[i])}
        for i in top_pos_idx
    ]
    top_neg_words = [
        {"word": feature_names[i], "coefficient": float(sent_coefs[i])}
        for i in top_neg_idx
    ]
    # 9. Build dashboard data
    dashboard_data = {
        "metrics": {
            "department_accuracy": float(best_dept_result['accuracy']),
            "sentiment_accuracy": float(best_sent_result['accuracy']),
            "department_f1": float(best_dept_result['f1_macro']),
            "sentiment_f1": float(best_sent_result['f1_macro'])
        },
        "model_comparison": {
            "department": {name: {"accuracy": r['accuracy'], "f1": r['f1_macro']} for name, r in dept_results.items()},
            "sentiment": {name: {"accuracy": r['accuracy'], "f1": r['f1_macro']} for name, r in sent_results.items()}
        },
        "confusion_matrix": {
            "department": dept_cm.tolist(),
            "sentiment": sent_cm.tolist(),
            "labels_dept": dept_names,
            "labels_sent": sent_names
        },
        "feature_importance": {
            "positive": top_pos_words,
            "negative": top_neg_words
        },
        "model_info": {
            "best_department_model": best_dept_name,
            "best_sentiment_model": best_sent_name,
            "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    # 10. Persist trained models and dashboard data
    joblib.dump(dept_models, BASE_DIR / 'all_dept_models.pkl')
    joblib.dump(sent_models, BASE_DIR / 'all_sent_models.pkl')
    
    with open(BASE_DIR / 'dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

    print("Training complete!")
    print(f"   Best Department Model: {best_dept_name} (F1: {best_dept_result['f1_macro']:.4f})")
    print(f"   Best Sentiment Model: {best_sent_name} (F1: {best_sent_result['f1_macro']:.4f})")
    print("   Dashboard data saved to 'dashboard_data.json'")


if __name__ == "__main__":
    train_model()