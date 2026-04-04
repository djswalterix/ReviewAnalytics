# ReviewAnalytics

Sistema di analisi automatica di recensioni alberghiere in italiano, basato su tecniche di **Natural Language Processing (NLP)** e **Machine Learning supervisionato**.

Il progetto copre l'intero ciclo di vita di un'applicazione ML: dalla generazione sintetica del dataset, all'addestramento e confronto di modelli, fino alla fruizione dei risultati tramite un'API REST e una dashboard interattiva.

## Architettura

```
ReviewAnalytics/
├── generator/          # Generatore sintetico di recensioni in italiano
│   ├── config.py       # Iperparametri (seed, num samples, pesi strategie)
│   ├── vocabulary.py   # Vocabolario: nomi, aggettivi, titoli per reparto
│   ├── grammar.py      # Regole grammaticali italiane: articoli, elisione, typo, noise
│   └── strategies.py   # 6 strategie di generazione a difficoltà crescente
│
├── backend/            # API REST e pipeline di training
│   ├── api.py          # Server FastAPI (predict, dashboard)
│   ├── train.py        # Training pipeline (TF-IDF + 3 modelli × 2 task)
│   └── stop_words.txt  # Lista di stop word italiane per il TF-IDF
│
├── frontend/           # Dashboard React + Mantine UI
│   └── src/
│       ├── components/ # Componenti riutilizzabili (MetricCard, Charts, ecc.)
│       ├── hooks/      # Custom hooks (useDashboard, usePredict)
│       └── pages/      # DashboardPage, PredictPage
│
├── Makefile            # Comandi rapidi (dev, train, build)
├── Dockerfile          # Build multi-stage per produzione
├── cloudbuild.yaml     # CI/CD Google Cloud Build
└── requirements.txt    # Dipendenze Python
```

## Obiettivi del Progetto

1. **Generazione dati**: creare un dataset sintetico bilanciato di recensioni italiane con etichette di _reparto_ (Housekeeping, Reception, F&B) e _sentiment_ (Positivo/Negativo), utilizzando strategie di complessità crescente per testare la robustezza dei modelli.

2. **Classificazione multiclasse e binaria**: addestrare e confrontare **Logistic Regression**, **K-Nearest Neighbors** e **Random Forest** su due task paralleli — classificazione del reparto e del sentiment.

3. **Interpretabilità**: estrarre e visualizzare i coefficienti del modello Logistic Regression per mostrare il contributo di ogni parola alla predizione.

4. **Fruibilità**: esporre i risultati tramite un'API REST e una dashboard interattiva con grafici, matrici di confusione e predizioni in tempo reale.

## Setup

### Prerequisiti

- Python 3.10+
- Node.js 18+
- pip

### Installazione

```bash
make install
```

Installa le dipendenze Python (`requirements.txt`) e quelle del frontend (`npm install`).

### Training dei Modelli

```bash
make train
```

Esegue in sequenza:

1. `python -m generator` — genera `dataset_recensioni.csv` (500 recensioni sintetiche)
2. `python -m backend.train` — addestra 6 modelli (3 per reparto, 3 per sentiment), salva i `.pkl` e `dashboard_data.json`

### Avvio in Sviluppo

```bash
make dev
```

Avvia in parallelo:

- **API** su `http://localhost:8080` (FastAPI con hot-reload)
- **Frontend** su `http://localhost:5173` (Vite dev server)

### Build di Produzione

```bash
make build
```

## Pipeline ML

```
CSV → Pulizia & Lemmatizzazione → TF-IDF Vectorizer (max 5000 features, bigrammi, sublinear_tf, stop words italiane)
         (rimozione punteggiatura                  │
          e normalizzazione morfologica)           ├── Reparto (3 classi)     ─→  Logistic Regression
                                                    │                           ─→  K-Nearest Neighbors
                                                    │                           ─→  Random Forest
                                                    │
                                                    └── Sentiment (2 classi)   ─→  Logistic Regression
                                                                                ─→  K-Nearest Neighbors
                                                                                ─→  Random Forest
```

**Preprocessing:**

- **Rimozione punteggiatura**: elimina tutti i caratteri speciali (es. "camera." → "camera")
- **Lemmatizzazione**: normalizza varianti morfologiche della stessa parola usando spaCy italiano (es. "pulita", "pulito", "pulite" → "pulito")

**Feature extraction:**

- **Title weighting**: il titolo viene ripetuto 2× per aumentarne l'influenza nel vettore TF-IDF
- **Valutazione**: accuracy e F1-score (binary per sentiment, macro per reparto)
- **Selezione**: il modello migliore per task viene scelto in base all'F1

## Tecnologie

| Layer               | Tecnologia                                 |
| ------------------- | ------------------------------------------ |
| Generazione dati    | Python, Faker                              |
| NLP / Preprocessing | spaCy (it_core_news_sm)                    |
| ML / Feature        | scikit-learn (TF-IDF, LogReg, KNN, RF)     |
| API                 | FastAPI, Uvicorn                           |
| Frontend            | React 19, TypeScript, Mantine UI, Chart.js |
| Build               | Vite, Docker multi-stage                   |
| CI/CD               | Google Cloud Build                         |

## Deploy

Il `Dockerfile` utilizza un build multi-stage:

1. **Stage 1** (Node): compila il frontend React
2. **Stage 2** (Python): copia API, modelli e frontend compilato

```bash
docker build -t review-analytics .
docker run -p 8080:8080 review-analytics
```

## API Endpoints

| Metodo | Endpoint     | Descrizione                                                            |
| ------ | ------------ | ---------------------------------------------------------------------- |
| `GET`  | `/dashboard` | Metriche, confronto modelli, matrici di confusione, feature importance |
| `POST` | `/predict`   | Predizione reparto e sentiment con confidenza e contributo parole      |
