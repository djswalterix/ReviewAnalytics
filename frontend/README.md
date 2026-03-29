# Frontend — Dashboard React

Dashboard interattiva per la visualizzazione dei risultati ML e la predizione di recensioni in tempo reale.

## Tech Stack

- **React 19** con TypeScript
- **Mantine UI v8** — componente library (AppShell, Cards, Progress, RingProgress)
- **Chart.js** (via react-chartjs-2) — grafici a barre, orizzontali, matrici
- **Vite** — bundler e dev server
- **React Router** — navigazione SPA

## Struttura

```
src/
├── App.tsx                  # Layout principale (AppShell, theme, routing)
├── api.ts                   # Client API (fetch dashboard, predict)
├── main.tsx                 # Entry point React
│
├── pages/
│   ├── DashboardPage.tsx    # Pagina metriche e confronto modelli
│   └── PredictPage.tsx      # Pagina predizione recensioni
│
├── components/
│   ├── MetricCard.tsx       # Card con RingProgress per metriche percentuali
│   ├── ConfusionMatrixCard.tsx  # Matrice di confusione con heatmap
│   ├── PredictionCard.tsx   # Card risultati predizione con barre progress
│   └── WordImpactChart.tsx  # Grafico a barre orizzontali per impatto parole
│
└── hooks/
    ├── useDashboard.ts      # Hook per fetch dati dashboard (loading/error/data)
    └── usePredict.ts        # Hook per chiamata API predict (run/loading/error/result)
```

## Pagine

### DashboardPage

Mostra i risultati del training:

- **Metriche principali**: accuracy e F1 del miglior modello (con RingProgress animati)
- **Confronto modelli**: grafici a barre per accuracy e F1 di tutti i modelli (department e sentiment)
- **Matrici di confusione**: heatmap con colori giallo (corretti) e arancione (errori)
- **Feature importance**: top 10 parole positive e negative dal Logistic Regression

### PredictPage

Form per analizzare nuove recensioni:

- Inserimento titolo e corpo della recensione
- Risultati per ogni modello con barre di confidenza
- Grafico impatto parole sul sentiment (contributo di ogni parola)
- Grafico impatto parole per department

## Schema Colori

| Elemento            | Colore    | Hex              |
| ------------------- | --------- | ---------------- |
| Positivo / Corretto | Giallo    | `#fcc419`        |
| Negativo / Errore   | Arancione | `#ff922b`        |
| Tema primario       | Arancione | Mantine `orange` |

## Componenti Riutilizzabili

| Componente            | Props principali                       | Descrizione                          |
| --------------------- | -------------------------------------- | ------------------------------------ |
| `MetricCard`          | `label, value, color, tooltip`         | Card con RingProgress circolare      |
| `ConfusionMatrixCard` | `title, labels, matrix`                | Tabella con heatmap giallo/arancione |
| `PredictionCard`      | `title, predictions, colorFn`          | Lista predizioni con Progress bar    |
| `WordImpactChart`     | `title, labels, data, backgroundColor` | Barre orizzontali Chart.js           |

## Custom Hooks

| Hook           | Returns                           | Descrizione                               |
| -------------- | --------------------------------- | ----------------------------------------- |
| `useDashboard` | `{ data, error, loading }`        | Fetch automatico di `/dashboard` al mount |
| `usePredict`   | `{ result, error, loading, run }` | Chiamata `/predict` su invocazione        |

## Sviluppo

```bash
npm install
npm run dev
```

Dev server su `http://localhost:5173` con proxy verso l'API su `:8080`.
