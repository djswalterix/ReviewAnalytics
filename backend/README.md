# Backend — API e Training Pipeline

Server FastAPI per la predizione di recensioni e pipeline di addestramento dei modelli scikit-learn.

## Struttura

```
backend/
├── api.py          # Server REST (FastAPI)
├── train.py        # Pipeline di training
└── stop_words.txt  # Stop word italiane per il TF-IDF
```

## Training (`train.py`)

```bash
python -m backend.train
```

### Pipeline

1. **Caricamento dati**: legge `dataset_recensioni.csv` dalla root
2. **Preprocessing**: concatena titolo (ripetuto 2×) e corpo — `(title + " ") × 2 + body`
3. **Vettorizzazione TF-IDF**: max 1000 feature, stop word italiane da `stop_words.txt`
4. **Training**: addestra 3 modelli × 2 task (department e sentiment)
5. **Valutazione**: accuracy e F1 su test set (80/20 split, seed=42)
6. **Selezione**: il modello con F1 più alto diventa il "best model"
7. **Persistenza**: salva modelli (`.pkl`), vettorizzatore e `dashboard_data.json`

### Modelli

| Modello                 | Configurazione                                  |
| ----------------------- | ----------------------------------------------- |
| **Logistic Regression** | solver=lbfgs, max_iter=1000, C=1.0              |
| **K-Nearest Neighbors** | k=5, weights=distance, metric=cosine            |
| **Random Forest**       | 100 estimators, max_depth=10, max_features=sqrt |

Ogni modello viene addestrato due volte: una per la classificazione del **department** (3 classi) e una per il **sentiment** (2 classi).

### Stop Word (`stop_words.txt`)

Lista curata di stop word italiane usate dal TF-IDF Vectorizer per filtrare parole grammaticali prive di contenuto semantico (articoli, preposizioni, congiunzioni, pronomi). Questo migliora la qualità delle feature estratte concentrando il modello sulle parole significative.

### File prodotti

| File                  | Contenuto                                   |
| --------------------- | ------------------------------------------- |
| `vectorizer.pkl`      | TF-IDF vectorizer addestrato                |
| `all_dept_models.pkl` | Dizionario con i 3 modelli department       |
| `all_sent_models.pkl` | Dizionario con i 3 modelli sentiment        |
| `dept_model.pkl`      | Miglior modello department                  |
| `sent_model.pkl`      | Miglior modello sentiment                   |
| `dashboard_data.json` | Metriche, confronti e matrici di confusione |

## API (`api.py`)

```bash
uvicorn backend.api:app --host 0.0.0.0 --port 8080 --reload
```

### Endpoints

#### `POST /predict`

Analizza una recensione con tutti i modelli addestrati.

**Request:**

```json
{
  "title": "Camera deludente",
  "body": "La camera era sporca e il personale scortese"
}
```

**Response:**

```json
{
  "review": "La camera era sporca e il personale scortese",
  "department": [
    {
      "model": "Logistic Regression",
      "prediction": "Housekeeping",
      "confidence": 0.87
    }
  ],
  "sentiment": [
    {
      "model": "Logistic Regression",
      "prediction": "Negative",
      "confidence": 0.92
    }
  ],
  "sentiment_word_contributions": [{ "word": "sporca", "impact": -0.42 }],
  "department_word_contributions": [
    { "word": "camera", "department": "Housekeeping", "impact": 0.65 }
  ]
}
```

Il campo `sentiment_word_contributions` mostra l'impatto di ogni parola sulla predizione, calcolato moltiplicando il valore TF-IDF per il coefficiente Logistic Regression. Valori positivi spingono verso "Positivo", negativi verso "Negativo".

Il campo `department_word_contributions` assegna ogni parola al reparto dove ha il coefficiente assoluto più forte.

#### `GET /dashboard`

Restituisce `dashboard_data.json` con:

- Metriche del miglior modello (accuracy, F1)
- Confronto tra tutti i modelli
- Matrici di confusione
- Feature importance (top 10 parole positive/negative)
- Info sul modello (nome, data training)

#### `GET /health`

Health check per il monitoraggio.

### Serving Frontend

In produzione (quando `frontend/dist/` esiste), l'API serve direttamente i file React compilati come SPA con fallback su `index.html`.
