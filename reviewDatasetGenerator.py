
"""
Hotel Review Dataset Generator
Generates synthetic Italian hotel reviews with controlled sentiment and department labels.
Designed to create challenging training data with high entropy (negations, mixed sentiment, etc.)
"""

import pandas as pd
import random
from faker import Faker

# Configuration
fake = Faker('it_IT')
Faker.seed(42)
random.seed(42)

NUM_SAMPLES = 500

# =============================================================================
# VOCABULARY - Extensive Italian hotel review lexicon
# =============================================================================

VOCAB = {
    # Positive adjectives for rooms/facilities
    "pos_room": [
        "impeccabile", "spaziosa", "luminosa", "confortevole", "moderna", "pulitissima",
        "accogliente", "elegante", "raffinata", "curata", "rilassante", "panoramica",
        "silenziosa", "rinnovata", "ampia", "calda", "intima", "incantevole",
        "lussuosa", "sofisticata", "tecnologica", "climatizzata", "comoda", "eccellente",
        "splendida", "favolosa", "rifinita", "ariosa", "romantica", "maestosa",
        "di design", "perfetta", "paradisiaca", "rigenerante", "ordinata", "profumata",
        "funzionale", "ben arredata", "dotata di tutto", "con vista", "ben illuminata",
        "insonorizzata", "ben riscaldata", "fresca", "ventilata", "solare"
    ],
    
    # Negative adjectives for rooms/facilities
    "neg_room": [
        "sporca", "angusta", "buia", "scomoda", "vecchia", "polverosa", "fredda",
        "rumorosa", "fatiscente", "trascurata", "datata", "maleodorante", "umida",
        "trasandata", "caotica", "minuscola", "degradata", "sciatta", "cupa",
        "opprimente", "puzzolente", "rovinata", "danneggiata", "consumata", "logora",
        "obsoleta", "scadente", "deprimente", "squallida", "gelida", "bollente",
        "soffocante", "ammuffita", "scrostata", "orrenda", "terribile", "disastrosa",
        "indecente", "invivibile", "lurida", "impresentabile", "piccola", "stretta",
        "mal tenuta", "con macchie", "con polvere", "con ragnatele", "senza finestre",
        "troppo calda", "troppo fredda", "con odori strani", "piena di insetti"
    ],
    
    # Positive adjectives for staff
    "pos_staff": [
        "gentile", "disponibile", "sorridente", "professionale", "rapido", "attento",
        "cordiale", "premuroso", "accogliente", "efficiente", "preparato", "educato",
        "discreto", "puntuale", "competente", "alla mano", "paziente", "formidabile",
        "amichevole", "collaborativo", "ospitale", "dinamico", "brillante", "empatico",
        "caloroso", "affabile", "gentilissimo", "meticoloso", "affidabile", "tempestivo",
        "reattivo", "pronto", "veloce", "energico", "entusiasta", "solare", "eccezionale",
        "straordinario", "esperto", "qualificato", "impeccabile", "eccellente", "ottimo",
        "rispettoso", "sensibile", "diplomatico", "multilingue", "cortese", "simpatico",
        "fantastico", "super disponibile", "sempre presente", "molto preparato"
    ],
    
    # Negative adjectives for staff
    "neg_staff": [
        "scortese", "lento", "maleducato", "assente", "impreparato", "svogliato",
        "arrogante", "distratto", "irritante", "indifferente", "sciatto", "ostile",
        "disorganizzato", "inefficiente", "saccente", "sgarbato", "brusco", "incompetente",
        "incapace", "pigro", "negligente", "superficiale", "antipatico", "intrattabile",
        "nervoso", "aggressivo", "villano", "presuntuoso", "altezzoso", "freddo",
        "scostante", "poco disponibile", "mai presente", "introvabile", "inesistente",
        "mancante", "assente", "disinteressato", "sgradevole", "pessimo", "orribile",
        "inqualificabile", "non professionale", "poco preparato", "poco cortese",
        "sbrigativo", "frettoloso", "approssimativo", "poco attento", "scorbutico"
    ],
    
    # Positive adjectives for food
    "pos_food": [
        "delizioso", "fresco", "abbondante", "gourmet", "caldo", "squisito", "prelibato",
        "genuino", "invitante", "sapido", "ricercato", "fragrante", "croccante",
        "succulento", "raffinato", "eccellente", "gustoso", "appetitoso", "leggero",
        "curato", "tipico", "sublime", "profumato", "pregiato", "biologico",
        "artigianale", "fatto in casa", "tradizionale", "innovativo", "equilibrato",
        "nutriente", "sano", "sostanzioso", "generoso", "ricco", "variegato", "completo",
        "sfizioso", "goloso", "irresistibile", "fantastico", "magnifico", "superbo",
        "ottimo", "buonissimo", "divino", "spaziale", "stellato", "di qualità",
        "ben presentato", "ben cotto", "perfetto", "da leccarsi i baffi",
        "velocissimo", "puntuale", "immediato", "fumante"
    ],
    
    # Negative adjectives for food
    "neg_food": [
        "stantio", "freddo", "insapore", "crudo", "scadente", "immangiabile", "gommoso",
        "unto", "bruciato", "insipido", "congelato", "industriale", "scotto", "salato",
        "acido", "amaro", "secco", "pesante", "indigesto", "scialbo", "povero",
        "mediocre", "sgradevole", "misero", "insufficiente", "limitato", "monotono",
        "deludente", "pessimo", "orribile", "nauseante", "schifoso", "scaduto",
        "avariato", "marcio", "maleodorante", "grasso", "oleoso", "duro", "molle",
        "acquoso", "annacquato", "risicato", "costoso", "rancido", "vecchio",
        "riscaldato", "precotto", "di plastica", "senza gusto", "poco fresco",
        "porzioni minuscole", "niente di speciale", "non all'altezza"
    ],
    
    # Nouns for each department
    "nouns_housekeeping": [
        "camera", "stanza", "bagno", "letto", "doccia", "asciugamani", "lenzuola",
        "pavimento", "finestre", "armadio", "scrivania", "minibar", "aria condizionata",
        "riscaldamento", "tv", "wifi", "prese elettriche", "materasso", "cuscini",
        "coperte", "tende", "specchio", "lavandino", "wc", "bidet", "phon",
        "pulizia", "igiene", "ordine", "manutenzione", "arredamento"
    ],
    
    "nouns_reception": [
        "reception", "check-in", "check-out", "receptionist", "portiere", "concierge",
        "personale", "staff", "accoglienza", "assistenza", "informazioni", "prenotazione",
        "chiavi", "documento", "pagamento", "fattura", "richieste", "reclami",
        "servizio clienti", "front desk", "hall", "ingresso", "portineria"
    ],
    
    "nouns_fb": [
        "colazione", "pranzo", "cena", "ristorante", "bar", "buffet", "menu",
        "piatti", "cibo", "bevande", "caffè", "cappuccino", "cornetto", "brioche",
        "frutta", "dolci", "primi", "secondi", "contorni", "antipasti", "dessert",
        "vino", "acqua", "succo", "pane", "formaggio", "salumi", "uova",
        "sala colazione", "terrazza", "servizio in camera", "room service",
        "colazione in camera"
    ]
}

# =============================================================================
# TEMPLATE FUNCTIONS - Generate diverse review structures
# =============================================================================

def get_random_intro():
    """Generate a random contextual introduction to add variability."""
    templates = [
        f"Siamo arrivati di {fake.day_of_week()} verso le {random.randint(8, 23)}.",
        f"Dopo un viaggio da {fake.city()},",
        "Ho prenotato tramite Booking.",
        "Abbiamo soggiornato per il weekend.",
        f"Ero qui per lavoro con {fake.first_name()}.",
        "Non sapevo cosa aspettarmi.",
        f"Abbiamo scelto questo hotel per la posizione.",
        "Prima volta in questa struttura.",
        f"Soggiorno di {random.randint(1, 7)} notti.",
        "Hotel consigliato da amici.",
        f"Prenotato {random.randint(1, 30)} giorni prima.",
        "Viaggio in famiglia.",
        "Vacanza romantica.",
        "Trasferta di lavoro.",
        ""  # Sometimes no intro
    ]
    return random.choice(templates)


def get_random_outro():
    """Generate a random closing statement to add variability."""
    templates = [
        f"Comunque torneremo.",
        "Vedremo la prossima volta.",
        f"Pagato {random.randint(50, 300)}€ a notte.",
        "Nel complesso ok.",
        "Potrebbe migliorare.",
        "Lo consiglio.",
        "Non lo consiglio.",
        "Rapporto qualità-prezzo discreto.",
        f"Voto: {random.randint(1, 10)}/10.",
        "Esperienza da ripetere.",
        "Mai più.",
        "Forse ci torniamo.",
        ""  # Sometimes no outro
    ]
    return random.choice(templates)


def build_housekeeping_review(sentiment):
    """Build a review focused on Housekeeping (room, cleanliness, facilities)."""
    noun = random.choice(VOCAB["nouns_housekeeping"])
    
    if sentiment == 1:  # Positive
        adj = random.choice(VOCAB["pos_room"])
        templates = [
            f"La {noun} era {adj}.",
            f"{noun.capitalize()} {adj}, niente da dire.",
            f"Che bella {noun}! Davvero {adj}.",
            f"Ho trovato la {noun} {adj} e ben curata.",
            f"Devo dire che la {noun} era {adj}.",
            f"Piacevolmente sorpreso dalla {noun}, molto {adj}.",
            f"La {noun} superava le aspettative: {adj}!",
            f"Finalmente una {noun} {adj}.",
        ]
    else:  # Negative
        adj = random.choice(VOCAB["neg_room"])
        templates = [
            f"La {noun} era {adj}.",
            f"{noun.capitalize()} {adj}, pessima esperienza.",
            f"Purtroppo la {noun} era {adj}.",
            f"Ho trovato la {noun} {adj}. Inaccettabile.",
            f"Deluso dalla {noun}: {adj}.",
            f"La {noun} lasciava a desiderare, troppo {adj}.",
            f"Non mi aspettavo una {noun} così {adj}.",
            f"Vergognoso: {noun} {adj}.",
        ]
    
    return random.choice(templates)


def build_reception_review(sentiment):
    """Build a review focused on Reception (staff, check-in, service)."""
    noun = random.choice(VOCAB["nouns_reception"])
    name = fake.first_name()
    
    if sentiment == 1:  # Positive
        adj = random.choice(VOCAB["pos_staff"])
        templates = [
            f"Il {noun} era {adj}.",
            f"{name} al {noun} è stato {adj}.",
            f"Personale {adj}, specialmente {name}.",
            f"Check-in veloce con staff {adj}.",
            f"Ho trovato il {noun} molto {adj}.",
            f"{name} ci ha accolto in modo {adj}.",
            f"Servizio {adj} alla {noun}.",
            f"Staff {adj}, complimenti a {name}.",
        ]
    else:  # Negative
        adj = random.choice(VOCAB["neg_staff"])
        templates = [
            f"Il {noun} era {adj}.",
            f"{name} al {noun} si è dimostrato {adj}.",
            f"Personale {adj}, soprattutto {name}.",
            f"Check-in interminabile, staff {adj}.",
            f"Ho trovato il {noun} {adj}.",
            f"{name} ci ha trattato in modo {adj}.",
            f"Servizio {adj} alla {noun}.",
            f"Staff {adj}, {name} in particolare.",
        ]
    
    return random.choice(templates)


def build_fb_review(sentiment):
    """Build a review focused on F&B (food, breakfast, restaurant)."""
    noun = random.choice(VOCAB["nouns_fb"])
    
    if sentiment == 1:  # Positive
        adj = random.choice(VOCAB["pos_food"])
        templates = [
            f"La {noun} era {adj}.",
            f"{noun.capitalize()} {adj}, ottima!",
            f"Ho apprezzato la {noun}: {adj}.",
            f"Che {noun} {adj}!",
            f"La {noun} mi ha sorpreso: {adj}.",
            f"Finalmente una {noun} {adj}.",
            f"La {noun} vale da sola il soggiorno: {adj}.",
            f"Complimenti per la {noun}, davvero {adj}.",
        ]
    else:  # Negative
        adj = random.choice(VOCAB["neg_food"])
        templates = [
            f"La {noun} era {adj}.",
            f"{noun.capitalize()} {adj}, deludente.",
            f"Purtroppo la {noun} era {adj}.",
            f"La {noun} lasciava a desiderare: {adj}.",
            f"Mi aspettavo di meglio dalla {noun}: {adj}.",
            f"La {noun} era decisamente {adj}.",
            f"Evitate la {noun}: {adj}.",
            f"Pessima {noun}, {adj}.",
        ]
    
    return random.choice(templates)


# =============================================================================
# CROSS-DEPARTMENT NOISE - Realistic tangential mentions
# =============================================================================

CROSS_DEPT_NOISE = {
    "Housekeeping": [
        "Il personale delle pulizie era nella norma.",
        "Niente da segnalare sulla manutenzione.",
        "Camera nella media per la categoria.",
        "Il bagno funzionava, niente di più.",
        "Lenzuola cambiate regolarmente.",
        "Aria condizionata funzionante.",
        "La stanza era quella che ci si aspetta.",
    ],
    "Reception": [
        "Check-in nella norma.",
        "Alla reception tutto regolare.",
        "Personale presente ma niente di memorabile.",
        "Il concierge ci ha dato qualche indicazione.",
        "Nessun problema al check-out.",
        "Lo staff faceva il suo lavoro.",
        "Accoglienza standard.",
    ],
    "F&B": [
        "La colazione era quella classica da hotel.",
        "Al bar niente di speciale.",
        "Il caffè era decente.",
        "Buffet nella norma.",
        "Abbiamo mangiato qualcosa al ristorante.",
        "Colazione continentale standard.",
        "Il minibar aveva i soliti prodotti.",
    ],
}


def add_cross_dept_noise(body: str, main_dept: str) -> str:
    """With 40% probability, append a neutral sentence about another department."""
    if random.random() < 0.4:
        other_depts = [d for d in CROSS_DEPT_NOISE if d != main_dept]
        noise_dept = random.choice(other_depts)
        noise = random.choice(CROSS_DEPT_NOISE[noise_dept])
        if random.random() < 0.5:
            return f"{noise} {body}"
        else:
            return f"{body} {noise}"
    return body


# =============================================================================
# REVIEW STRATEGIES - Different complexity levels for model training
# =============================================================================

def build_simple_review(sentiment):
    """Generate a simple, direct review (baseline difficulty)."""
    dept = random.choice(["Housekeeping", "Reception", "F&B"])
    
    if dept == "Housekeeping":
        body = build_housekeeping_review(sentiment)
    elif dept == "Reception":
        body = build_reception_review(sentiment)
    else:
        body = build_fb_review(sentiment)
    
    return body, dept


def build_detailed_review(sentiment):
    """Generate a detailed review with contextual intro/outro (medium difficulty)."""
    dept = random.choice(["Housekeeping", "Reception", "F&B"])
    intro = get_random_intro()
    outro = get_random_outro()
    
    if dept == "Housekeeping":
        core = build_housekeeping_review(sentiment)
    elif dept == "Reception":
        core = build_reception_review(sentiment)
    else:
        core = build_fb_review(sentiment)
    
    parts = [p for p in [intro, core, outro] if p]  # Filter empty strings
    body = " ".join(parts)
    
    return body, dept


def build_negation_review(sentiment):
    """Generate reviews using negation patterns, challenging for simple models."""
    if sentiment == 1:  # Positive expressed through negation of negative
        dept = random.choice(["Housekeeping", "Reception", "F&B"])
        if dept == "Housekeeping":
            adj = random.choice(VOCAB["neg_room"])
            noun = random.choice(VOCAB["nouns_housekeeping"])
            templates = [
                f"La {noun} non era affatto {adj}. Anzi, molto curata.",
                f"Avevo paura fosse {adj}, ma la {noun} era perfetta.",
                f"Non posso dire che la {noun} fosse {adj}. Tutt'altro!",
                f"Niente {noun} {adj} come temevo. Ottima!",
            ]
        elif dept == "Reception":
            adj = random.choice(VOCAB["neg_staff"])
            templates = [
                f"Il personale non era per niente {adj}. Molto professionali.",
                f"Non ho trovato staff {adj}. Anzi, gentilissimi.",
                f"Temevo receptionist {adj}, invece super disponibili.",
                f"Nessuno {adj} alla reception. Complimenti!",
            ]
        else:
            adj = random.choice(VOCAB["neg_food"])
            noun = random.choice(VOCAB["nouns_fb"])
            templates = [
                f"La {noun} non era {adj}. Anzi, deliziosa!",
                f"Niente {noun} {adj} come in altri hotel. Ottima!",
                f"Non posso dire che la {noun} fosse {adj}. Buonissima!",
                f"Temevo {noun} {adj}, invece sorpresa positiva.",
            ]
        body = random.choice(templates)
        
    else:  # Negative expressed through negation of positive
        dept = random.choice(["Housekeeping", "Reception", "F&B"])
        if dept == "Housekeeping":
            adj = random.choice(VOCAB["pos_room"])
            noun = random.choice(VOCAB["nouns_housekeeping"])
            templates = [
                f"Non aspettatevi una {noun} {adj}. Tutt'altro.",
                f"La {noun} non era certo {adj}. Delusione totale.",
                f"Di {adj} la {noun} non aveva nulla.",
                f"Scordatevi una {noun} {adj}. Pessima.",
            ]
        elif dept == "Reception":
            adj = random.choice(VOCAB["pos_staff"])
            templates = [
                f"Non aspettatevi personale {adj}. Pessimi.",
                f"Di {adj} lo staff non aveva niente.",
                f"Il receptionist non era certo {adj}. Maleducato.",
                f"Scordatevi accoglienza {adj}. Disastro.",
            ]
        else:
            adj = random.choice(VOCAB["pos_food"])
            noun = random.choice(VOCAB["nouns_fb"])
            templates = [
                f"Non aspettatevi {noun} {adj}. Immangiabile.",
                f"La {noun} non era affatto {adj}. Pessima.",
                f"Di {adj} la {noun} non aveva nulla.",
                f"Scordatevi una {noun} {adj}. Deludente.",
            ]
        body = random.choice(templates)
    
    return body, dept


def build_mixed_review(sentiment):
    """Generate mixed-sentiment reviews where the final sentiment prevails (high difficulty)."""
    name = fake.first_name()
    
    if sentiment == 1:  # Positive wins
        # Start negative, end positive
        neg_part = random.choice(VOCAB["neg_food"] + VOCAB["neg_room"])
        pos_part = random.choice(VOCAB["pos_staff"])
        templates = [
            f"Il cibo era {neg_part}, ma lo staff {pos_part} ha salvato tutto.",
            f"Camera un po' {neg_part}, però {name} alla reception {pos_part}. Promossi!",
            f"Nonostante la colazione {neg_part}, il personale {pos_part} ha fatto la differenza.",
            f"Ok la stanza era {neg_part}, ma il servizio {pos_part} compensa.",
        ]
        body = random.choice(templates)
        dept = "Reception"  # Classified as Reception since staff determines the outcome
        
    else:  # Negative wins
        # Start positive, end negative
        pos_part = random.choice(VOCAB["pos_room"] + VOCAB["pos_food"])
        neg_part = random.choice(VOCAB["neg_staff"])
        templates = [
            f"La camera era {pos_part}, ma il personale {neg_part} ha rovinato tutto.",
            f"Colazione {pos_part}, peccato per lo staff {neg_part}.",
            f"Stanza anche {pos_part}, però {name} {neg_part}. Mai più.",
            f"Bello l'hotel, {pos_part}, ma il servizio {neg_part} è inaccettabile.",
        ]
        body = random.choice(templates)
        dept = "Reception"  # Classified as Reception since staff determines the outcome
    
    return body, dept


def build_multi_aspect_review(sentiment):
    """Generate reviews covering multiple hotel aspects (realistic, high difficulty)."""
    intro = get_random_intro()
    
    if sentiment == 1:  # Overall positive
        room_adj = random.choice(VOCAB["pos_room"])
        staff_adj = random.choice(VOCAB["pos_staff"])
        food_adj = random.choice(VOCAB["pos_food"])
        templates = [
            f"{intro} Camera {room_adj}, personale {staff_adj}, colazione {food_adj}. Torneremo!",
            f"{intro} Stanza {room_adj}. Staff {staff_adj}. Cena {food_adj}. Top!",
            f"{intro} Tutto perfetto: camera {room_adj}, reception {staff_adj}, ristorante {food_adj}.",
        ]
    else:  # Overall negative
        room_adj = random.choice(VOCAB["neg_room"])
        staff_adj = random.choice(VOCAB["neg_staff"])
        food_adj = random.choice(VOCAB["neg_food"])
        templates = [
            f"{intro} Camera {room_adj}, personale {staff_adj}, colazione {food_adj}. Mai più!",
            f"{intro} Stanza {room_adj}. Staff {staff_adj}. Cena {food_adj}. Disastro.",
            f"{intro} Tutto pessimo: camera {room_adj}, reception {staff_adj}, ristorante {food_adj}.",
        ]
    
    body = random.choice(templates)
    # Assign a random department since all three aspects are mentioned equally
    dept = random.choice(["Housekeeping", "Reception", "F&B"])
    
    return body, dept


def build_ambiguous_review(sentiment):
    """Generate subtly positive/negative reviews with hedging language (hardest).
    
    Uses qualifiers like 'abbastanza', 'non male', 'discreto' that make
    sentiment harder to detect.
    """
    dept = random.choice(["Housekeeping", "Reception", "F&B"])
    
    hedges_pos = [
        "non male", "abbastanza buono", "discreto", "nella media alta",
        "sopra la media", "decente", "accettabile", "più che sufficiente",
    ]
    hedges_neg = [
        "non all'altezza", "sotto la media", "non proprio il massimo",
        "lascia a desiderare", "potrebbe fare di meglio", "non soddisfacente",
        "mediocre", "insufficiente",
    ]
    
    if dept == "Housekeeping":
        noun = random.choice(VOCAB["nouns_housekeeping"])
        if sentiment == 1:
            hedge = random.choice(hedges_pos)
            contrast_adj = random.choice(VOCAB["neg_room"])
            templates = [
                f"La {noun} era {hedge}. Non perfetta, ma ci siamo trovati bene.",
                f"Ok la {noun} poteva sembrare {contrast_adj} a primo impatto, ma poi {hedge}.",
                f"La {noun}? {hedge.capitalize()}. Niente di eccezionale, ma funzionale.",
                f"Sinceramente la {noun} era {hedge}, meglio del previsto.",
            ]
        else:
            hedge = random.choice(hedges_neg)
            contrast_adj = random.choice(VOCAB["pos_room"])
            templates = [
                f"La {noun} sembrava {contrast_adj} dalle foto, in realtà {hedge}.",
                f"Mi aspettavo una {noun} {contrast_adj}, ma era {hedge}.",
                f"La {noun}? {hedge.capitalize()}. Peccato, dalle recensioni sembrava meglio.",
                f"Sulla carta la {noun} doveva essere {contrast_adj}. Invece {hedge}.",
            ]
    elif dept == "Reception":
        if sentiment == 1:
            hedge = random.choice(hedges_pos)
            templates = [
                f"Il personale era {hedge}. Non eccezionale, ma disponibile.",
                f"Reception {hedge}. Poteva andare peggio, anzi no, è andata bene.",
                f"Lo staff era {hedge}, devo ammettere che mi aspettavo peggio.",
                f"Accoglienza {hedge}. Niente effetto wow, ma professionali.",
            ]
        else:
            hedge = random.choice(hedges_neg)
            templates = [
                f"Il personale era {hedge}. Non terribile, ma nemmeno soddisfacente.",
                f"Reception {hedge}. Mi aspettavo di più per il prezzo pagato.",
                f"Lo staff {hedge}, purtroppo non all'altezza delle aspettative.",
                f"Accoglienza {hedge}. Un peccato, rovinava l'esperienza.",
            ]
    else:  # F&B
        noun = random.choice(VOCAB["nouns_fb"])
        if sentiment == 1:
            hedge = random.choice(hedges_pos)
            templates = [
                f"La {noun} era {hedge}. Non gourmet, ma buona.",
                f"{noun.capitalize()} {hedge}. Niente di straordinario, ma soddisfacente.",
                f"Ho trovato la {noun} {hedge}, più di quello che mi aspettavo.",
                f"La {noun} era {hedge}. Per essere un hotel, promossa.",
            ]
        else:
            hedge = random.choice(hedges_neg)
            templates = [
                f"La {noun} era {hedge}. Non immangiabile, ma neanche buona.",
                f"{noun.capitalize()} {hedge}. Mi aspettavo qualcosa di più.",
                f"Purtroppo la {noun} era {hedge}, un peccato.",
                f"La {noun} {hedge}. Per il prezzo pagato, deludente.",
            ]
    
    body = random.choice(templates)
    return body, dept


# =============================================================================
# TITLE GENERATION - Meaningful titles that reflect content
# =============================================================================

TITLES = {
    'positive': {
        'Housekeeping': [
            "Camera impeccabile", "Pulizia perfetta", "Stanza splendida",
            "Ambiente curatissimo", "Ottima manutenzione", "Camera da sogno",
            "Stanza eccellente", "Pulizia top", "Camera consigliatissima",
            "Ambiente perfetto", "Sistemazione ottima", "Camera fantastica"
        ],
        'Reception': [
            "Staff eccezionale", "Accoglienza top", "Personale fantastico",
            "Servizio impeccabile", "Reception efficiente", "Cordialità unica",
            "Personale gentilissimo", "Accoglienza calorosa", "Staff preparato",
            "Servizio eccellente", "Reception disponibile", "Team straordinario"
        ],
        'F&B': [
            "Colazione ottima", "Cibo delizioso", "Ristorante top",
            "Cucina eccellente", "Buffet ricchissimo", "Pranzo memorabile",
            "Cena fantastica", "Colazione abbondante", "Menu squisito",
            "Piatti deliziosi", "Qualità eccellente", "Gastronomia top"
        ]
    },
    'negative': {
        'Housekeeping': [
            "Camera deludente", "Pulizia scarsa", "Stanza sporca",
            "Manutenzione assente", "Ambiente trascurato", "Camera da incubo",
            "Stanza pessima", "Pulizia inesistente", "Camera da evitare",
            "Ambiente squallido", "Sistemazione indecente", "Camera orribile"
        ],
        'Reception': [
            "Staff scortese", "Accoglienza pessima", "Personale maleducato",
            "Servizio inesistente", "Reception disorganizzata", "Attesa infinita",
            "Personale sgarbato", "Accoglienza gelida", "Staff incompetente",
            "Servizio pessimo", "Reception assente", "Team impreparato"
        ],
        'F&B': [
            "Colazione scarsa", "Cibo immangiabile", "Ristorante deludente",
            "Cucina pessima", "Buffet povero", "Pranzo da dimenticare",
            "Cena pessima", "Colazione misera", "Menu scadente",
            "Piatti orribili", "Qualità assente", "Gastronomia pessima"
        ]
    },
    'generic': [
        "Hotel nella media", "Esperienza altalenante", "Poteva andare meglio",
        "Niente di speciale", "Soggiorno ok", "Recensione hotel",
        "La mia esperienza", "Vacanza a metà", "Hotel discreto",
        "Ci sono stato", "Weekend al mare", "Trasferta di lavoro",
        "Soggiorno breve", "Qualche giorno qui", "Hotel in centro",
        "Prima volta qui", "Seconda visita", "Consigli utili",
        "Pro e contro", "Opinione sincera", "Giudizio personale",
        "Nota dolente", "Alti e bassi", "Luci e ombre",
        "Hotel centrale", "Struttura recente", f"Soggiorno {fake.month_name()}",
    ]
}


def generate_title(sentiment: int, department: str) -> str:
    """Generate a title with realistic noise.
    
    40% generic (no dept/sentiment leak), 10% wrong department,
    50% matching department+sentiment.
    """
    r = random.random()
    if r < 0.4:
        return random.choice(TITLES['generic'])
    elif r < 0.5:
        # Wrong department title to add noise
        wrong_dept = random.choice([d for d in ["Housekeeping", "Reception", "F&B"] if d != department])
        sentiment_key = 'positive' if sentiment == 1 else 'negative'
        return random.choice(TITLES[sentiment_key][wrong_dept])
    else:
        sentiment_key = 'positive' if sentiment == 1 else 'negative'
        return random.choice(TITLES[sentiment_key][department])


# =============================================================================
# MAIN REVIEW BUILDER
# =============================================================================

def build_review(target):
    """
    Build a single review with controlled sentiment.
    
    Args:
        target: 1 for positive, 0 for negative
    
    Returns:
        dict with review data
    """
    # Select generation strategy with weighted probabilities
    # Higher weight on complex strategies to improve model robustness
    strategy = random.choices(
        ["simple", "detailed", "negation", "mixed", "multi_aspect", "ambiguous"],
        weights=[0.10, 0.20, 0.15, 0.15, 0.20, 0.20],
        k=1
    )[0]
    
    if strategy == "simple":
        body, dept = build_simple_review(target)
    elif strategy == "detailed":
        body, dept = build_detailed_review(target)
    elif strategy == "negation":
        body, dept = build_negation_review(target)
    elif strategy == "mixed":
        body, dept = build_mixed_review(target)
    elif strategy == "ambiguous":
        body, dept = build_ambiguous_review(target)
    else:  # multi_aspect
        body, dept = build_multi_aspect_review(target)
    
    # Add cross-department noise to blur department boundaries
    body = add_cross_dept_noise(body, dept)
    
    # Generate meaningful title based on sentiment and department
    title = generate_title(target, dept)
    
    return {
        "id": fake.uuid4(),
        "title": title,
        "body": body,
        "department": dept,
        "sentiment": "positive" if target == 1 else "negative",
        "target": target,
        "strategy": strategy
    }


# =============================================================================
# DATASET GENERATION
# =============================================================================

if __name__ == "__main__":
    print(f"Generating {NUM_SAMPLES} synthetic Italian hotel reviews...")
    
    # Generate balanced dataset
    data = []
    for i in range(NUM_SAMPLES):
        target = i % 2  # Alternating 0, 1 for balance
        data.append(build_review(target))
    
    # Shuffle to mix strategies
    random.shuffle(data)
    
    df = pd.DataFrame(data)
    
    # Validation
    print("\nDataset Statistics:")
    print(f"   Total samples: {len(df)}")
    print(f"   Unique reviews: {df['body'].nunique()} ({df['body'].nunique()/len(df):.1%})")
    print(f"\n   Sentiment distribution:")
    print(f"   {df['sentiment'].value_counts().to_dict()}")
    print(f"\n   Department distribution:")
    print(f"   {df['department'].value_counts().to_dict()}")
    print(f"\n   Strategy distribution:")
    print(f"   {df['strategy'].value_counts().to_dict()}")
    
    # Check uniqueness
    unique_pct = df['body'].nunique() / len(df)
    if unique_pct < 0.95:
        print("\nWARNING: Too many duplicates. Consider expanding vocabulary.")
    
    # Save
    df.to_csv("dataset_recensioni.csv", index=False)
    print("\nDataset saved to 'dataset_recensioni.csv'")
    
    # Preview challenging examples
    print("\nSample negation reviews (challenging for models):")
    print(df[df['strategy'] == 'negation'][['body', 'target']].head(3).to_string())
    
    print("\nSample mixed reviews (challenging for models):")
    print(df[df['strategy'] == 'mixed'][['body', 'target']].head(3).to_string())