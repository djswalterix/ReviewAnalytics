# Generator — Generatore Sintetico di Recensioni

Modulo Python che genera un dataset di recensioni alberghiere italiane con etichette controllate di **department** e **sentiment**.

## Esecuzione

```bash
python -m generator
```

Produce `dataset_recensioni.csv` nella root del progetto con 500 recensioni (configurabile in `config.py`).

## Architettura del Modulo

```
generator/
├── __init__.py      # Funzione build_review(): orchestratore principale
├── __main__.py      # CLI entrypoint
├── config.py        # Iperparametri globali
├── vocabulary.py    # Nomi, aggettivi e titoli per reparto (gender-aware)
├── grammar.py       # Regole grammaticali italiane e data augmentation
└── strategies.py    # 6 strategie di generazione recensioni
```

## Strategie di Generazione

Le recensioni vengono generate con 6 strategie a complessità crescente, ciascuna con un peso configurabile in `config.py`:

| Strategia      | Peso | Descrizione                                                                            | Difficoltà per il modello |
| -------------- | ---- | -------------------------------------------------------------------------------------- | ------------------------- |
| `simple`       | 10%  | Frase singola, un reparto, sentiment diretto                                           | Bassa                     |
| `detailed`     | 20%  | Frase con intro/outro contestuali (es. "Siamo arrivati di lunedì...")                  | Bassa-media               |
| `negation`     | 15%  | Uso di negazioni per invertire il significato (es. "Non era affatto sporco")           | **Alta**                  |
| `mixed`        | 15%  | Due reparti menzionati, uno positivo e uno negativo; il department è quello "vincente" | **Alta**                  |
| `multi_aspect` | 20%  | Copre tutti e 3 i reparti in una frase; department casuale                             | Media                     |
| `ambiguous`    | 20%  | Linguaggio sfumato con hedging (es. "non male", "poteva andare peggio")                | **Molto alta**            |

Le strategie `negation` e `ambiguous` sono progettate specificamente per testare la capacità dei modelli di andare oltre semplici pattern di parole-chiave.

## Vocabolario (`vocabulary.py`)

Il vocabolario è organizzato per reparto e polarità. Ogni aggettivo è una coppia **(maschile, femminile)** per garantire la concordanza di genere:

- **Nomi**: 17 nomi Housekeeping, 15 Reception, 17 F&B — ciascuno con tag di genere (`"m"` / `"f"`)
- **Aggettivi**: ~35-45 aggettivi positivi e negativi per reparto (circa 250 aggettivi totali)
- **Hedges**: frasi sfumate per la strategia `ambiguous` (es. "nella norma", "accettabile")
- **Titoli**: generici, positivi e negativi per reparto — con 40% di probabilità di titolo generico (rumore intenzionale)
- **Cross-department noise**: frasi neutre su altri reparti, aggiunte al 40% delle recensioni per confondere i modelli

## Grammatica (`grammar.py`)

Gestisce le regole della lingua italiana:

- **Elisione degli articoli**: "il bagno" → "l'armadio", "la camera" → "l'igiene", "il → lo" per consonanti speciali (sp, st, z, gn, ps...)
- **Concordanza articolo-nome**: selezione automatica di articolo determinativo e indeterminativo in base al genere
- **Intro/outro casuali**: generati con Faker (città, nomi, giorni) per variabilità realistica
- **Iniezione di typo**: con probabilità del 5%, scambia due caratteri adiacenti in una parola (data augmentation)
- **Cross-department noise**: aggiunge una frase neutra su un reparto diverso da quello principale

## Configurazione (`config.py`)

| Parametro                      | Default   | Descrizione                                    |
| ------------------------------ | --------- | ---------------------------------------------- |
| `SEED`                         | 42        | Seed per riproducibilità                       |
| `NUM_SAMPLES`                  | 500       | Numero di recensioni da generare               |
| `STRATEGY_WEIGHTS`             | vedi file | Pesi delle 6 strategie (sommano a ~1.0)        |
| `TYPO_PROBABILITY`             | 0.05      | Probabilità di iniettare un typo               |
| `CROSS_DEPT_NOISE_PROBABILITY` | 0.40      | Probabilità di aggiungere rumore cross-reparto |

## Output

Ogni riga del CSV contiene:

| Campo        | Tipo | Descrizione                                       |
| ------------ | ---- | ------------------------------------------------- |
| `id`         | UUID | Identificativo univoco                            |
| `title`      | str  | Titolo della recensione (con rumore intenzionale) |
| `body`       | str  | Testo della recensione                            |
| `department` | str  | Reparto target (Housekeeping / Reception / F&B)   |
| `sentiment`  | str  | "positive" / "negative"                           |
| `target`     | int  | 1 = positivo, 0 = negativo                        |
| `strategy`   | str  | Strategia usata per la generazione                |
