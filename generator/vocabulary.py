"""
Italian hotel review vocabulary — gender-tagged nouns, adjective pairs,
titles, cross-department noise, and hedging phrases.
"""

from .config import fake

# =============================================================================
# Gender-tagged nouns per department
# Each entry: (noun, gender) where gender is "m" or "f"
# =============================================================================

NOUNS_HOUSEKEEPING = [
    ("camera", "f"), ("stanza", "f"), ("bagno", "m"), ("letto", "m"),
    ("doccia", "f"), ("pavimento", "m"), ("armadio", "m"), ("scrivania", "f"),
    ("minibar", "m"), ("materasso", "m"), ("specchio", "m"), ("lavandino", "m"),
    ("arredamento", "m"), ("pulizia", "f"), ("igiene", "f"), ("ordine", "m"),
    ("manutenzione", "f"),
]

NOUNS_RECEPTION = [
    ("reception", "f"), ("check-in", "m"), ("check-out", "m"),
    ("receptionist", "m"), ("portiere", "m"), ("concierge", "m"),
    ("personale", "m"), ("staff", "m"), ("accoglienza", "f"),
    ("assistenza", "f"), ("prenotazione", "f"), ("servizio clienti", "m"),
    ("hall", "f"), ("ingresso", "m"), ("portineria", "f"),
]

NOUNS_FB = [
    ("colazione", "f"), ("pranzo", "m"), ("cena", "f"), ("ristorante", "m"),
    ("bar", "m"), ("buffet", "m"), ("menu", "m"), ("cibo", "m"),
    ("caffè", "m"), ("cappuccino", "m"), ("cornetto", "m"), ("brioche", "f"),
    ("frutta", "f"), ("sala colazione", "f"), ("terrazza", "f"),
    ("servizio in camera", "m"), ("room service", "m"),
]

NOUNS_MAP = {
    "Housekeeping": NOUNS_HOUSEKEEPING,
    "Reception": NOUNS_RECEPTION,
    "F&B": NOUNS_FB,
}

# =============================================================================
# Gender-aware adjectives — (masculine_form, feminine_form)
# For invariable adjectives both forms are identical.
# =============================================================================

ADJ_POS_ROOM = [
    ("impeccabile", "impeccabile"), ("spazioso", "spaziosa"),
    ("luminoso", "luminosa"), ("confortevole", "confortevole"),
    ("moderno", "moderna"), ("pulitissimo", "pulitissima"),
    ("accogliente", "accogliente"), ("elegante", "elegante"),
    ("raffinato", "raffinata"), ("curato", "curata"),
    ("rilassante", "rilassante"), ("panoramico", "panoramica"),
    ("silenzioso", "silenziosa"), ("rinnovato", "rinnovata"),
    ("ampio", "ampia"), ("caldo", "calda"),
    ("intimo", "intima"), ("incantevole", "incantevole"),
    ("lussuoso", "lussuosa"), ("sofisticato", "sofisticata"),
    ("comodo", "comoda"), ("eccellente", "eccellente"),
    ("splendido", "splendida"), ("favoloso", "favolosa"),
    ("rifinito", "rifinita"), ("arioso", "ariosa"),
    ("romantico", "romantica"), ("maestoso", "maestosa"),
    ("perfetto", "perfetta"), ("ordinato", "ordinata"),
    ("profumato", "profumata"), ("funzionale", "funzionale"),
    ("fresco", "fresca"), ("solare", "solare"),
]

ADJ_NEG_ROOM = [
    ("sporco", "sporca"), ("angusto", "angusta"),
    ("buio", "buia"), ("scomodo", "scomoda"),
    ("vecchio", "vecchia"), ("polveroso", "polverosa"),
    ("freddo", "fredda"), ("rumoroso", "rumorosa"),
    ("fatiscente", "fatiscente"), ("trascurato", "trascurata"),
    ("datato", "datata"), ("maleodorante", "maleodorante"),
    ("umido", "umida"), ("trasandato", "trasandata"),
    ("caotico", "caotica"), ("minuscolo", "minuscola"),
    ("degradato", "degradata"), ("sciatto", "sciatta"),
    ("cupo", "cupa"), ("opprimente", "opprimente"),
    ("rovinato", "rovinata"), ("danneggiato", "danneggiata"),
    ("consumato", "consumata"), ("logoro", "logora"),
    ("obsoleto", "obsoleta"), ("scadente", "scadente"),
    ("deprimente", "deprimente"), ("squallido", "squallida"),
    ("gelido", "gelida"), ("bollente", "bollente"),
    ("soffocante", "soffocante"), ("orrendo", "orrenda"),
    ("terribile", "terribile"), ("disastroso", "disastrosa"),
    ("indecente", "indecente"), ("piccolo", "piccola"),
    ("stretto", "stretta"),
]

ADJ_POS_STAFF = [
    ("gentile", "gentile"), ("disponibile", "disponibile"),
    ("sorridente", "sorridente"), ("professionale", "professionale"),
    ("rapido", "rapida"), ("attento", "attenta"),
    ("cordiale", "cordiale"), ("premuroso", "premurosa"),
    ("accogliente", "accogliente"), ("efficiente", "efficiente"),
    ("preparato", "preparata"), ("educato", "educata"),
    ("discreto", "discreta"), ("puntuale", "puntuale"),
    ("competente", "competente"), ("paziente", "paziente"),
    ("formidabile", "formidabile"), ("amichevole", "amichevole"),
    ("collaborativo", "collaborativa"), ("ospitale", "ospitale"),
    ("dinamico", "dinamica"), ("brillante", "brillante"),
    ("empatico", "empatica"), ("caloroso", "calorosa"),
    ("affabile", "affabile"), ("gentilissimo", "gentilissima"),
    ("meticoloso", "meticolosa"), ("affidabile", "affidabile"),
    ("tempestivo", "tempestiva"), ("reattivo", "reattiva"),
    ("pronto", "pronta"), ("veloce", "veloce"),
    ("energico", "energica"), ("eccezionale", "eccezionale"),
    ("straordinario", "straordinaria"), ("esperto", "esperta"),
    ("qualificato", "qualificata"), ("impeccabile", "impeccabile"),
    ("eccellente", "eccellente"), ("ottimo", "ottima"),
    ("rispettoso", "rispettosa"), ("cortese", "cortese"),
    ("simpatico", "simpatica"), ("fantastico", "fantastica"),
]

ADJ_NEG_STAFF = [
    ("scortese", "scortese"), ("lento", "lenta"),
    ("maleducato", "maleducata"), ("assente", "assente"),
    ("impreparato", "impreparata"), ("svogliato", "svogliata"),
    ("arrogante", "arrogante"), ("distratto", "distratta"),
    ("irritante", "irritante"), ("indifferente", "indifferente"),
    ("sciatto", "sciatta"), ("ostile", "ostile"),
    ("disorganizzato", "disorganizzata"), ("inefficiente", "inefficiente"),
    ("saccente", "saccente"), ("sgarbato", "sgarbata"),
    ("brusco", "brusca"), ("incompetente", "incompetente"),
    ("incapace", "incapace"), ("pigro", "pigra"),
    ("negligente", "negligente"), ("superficiale", "superficiale"),
    ("antipatico", "antipatica"), ("nervoso", "nervosa"),
    ("aggressivo", "aggressiva"), ("villano", "villana"),
    ("presuntuoso", "presuntuosa"), ("altezzoso", "altezzosa"),
    ("freddo", "fredda"), ("scostante", "scostante"),
    ("disinteressato", "disinteressata"), ("sgradevole", "sgradevole"),
    ("pessimo", "pessima"), ("orribile", "orribile"),
    ("sbrigativo", "sbrigativa"), ("frettoloso", "frettolosa"),
    ("approssimativo", "approssimativa"), ("scorbutico", "scorbutica"),
]

ADJ_POS_FOOD = [
    ("delizioso", "deliziosa"), ("fresco", "fresca"),
    ("abbondante", "abbondante"), ("caldo", "calda"),
    ("squisito", "squisita"), ("prelibato", "prelibata"),
    ("genuino", "genuina"), ("invitante", "invitante"),
    ("sapido", "sapida"), ("ricercato", "ricercata"),
    ("fragrante", "fragrante"), ("croccante", "croccante"),
    ("succulento", "succulenta"), ("raffinato", "raffinata"),
    ("eccellente", "eccellente"), ("gustoso", "gustosa"),
    ("appetitoso", "appetitosa"), ("leggero", "leggera"),
    ("curato", "curata"), ("tipico", "tipica"),
    ("sublime", "sublime"), ("profumato", "profumata"),
    ("pregiato", "pregiata"), ("biologico", "biologica"),
    ("tradizionale", "tradizionale"), ("innovativo", "innovativa"),
    ("equilibrato", "equilibrata"), ("nutriente", "nutriente"),
    ("sano", "sana"), ("sostanzioso", "sostanziosa"),
    ("generoso", "generosa"), ("ricco", "ricca"),
    ("completo", "completa"), ("sfizioso", "sfiziosa"),
    ("goloso", "golosa"), ("irresistibile", "irresistibile"),
    ("fantastico", "fantastica"), ("magnifico", "magnifica"),
    ("superbo", "superba"), ("ottimo", "ottima"),
    ("buonissimo", "buonissima"), ("divino", "divina"),
    ("perfetto", "perfetta"),
]

ADJ_NEG_FOOD = [
    ("stantio", "stantia"), ("freddo", "fredda"),
    ("insapore", "insapore"), ("crudo", "cruda"),
    ("scadente", "scadente"), ("immangiabile", "immangiabile"),
    ("gommoso", "gommosa"), ("unto", "unta"),
    ("bruciato", "bruciata"), ("insipido", "insipida"),
    ("congelato", "congelata"), ("industriale", "industriale"),
    ("scotto", "scotta"), ("salato", "salata"),
    ("acido", "acida"), ("amaro", "amara"),
    ("secco", "secca"), ("pesante", "pesante"),
    ("indigesto", "indigesta"), ("scialbo", "scialba"),
    ("povero", "povera"), ("mediocre", "mediocre"),
    ("sgradevole", "sgradevole"), ("misero", "misera"),
    ("insufficiente", "insufficiente"), ("limitato", "limitata"),
    ("monotono", "monotona"), ("deludente", "deludente"),
    ("pessimo", "pessima"), ("orribile", "orribile"),
    ("nauseante", "nauseante"), ("rancido", "rancida"),
    ("vecchio", "vecchia"), ("riscaldato", "riscaldata"),
    ("precotto", "precotta"), ("costoso", "costosa"),
    ("duro", "dura"), ("molle", "molle"),
]

# Adjective pools mapped by (department, polarity)
ADJ_MAP = {
    ("Housekeeping", "pos"): ADJ_POS_ROOM,
    ("Housekeeping", "neg"): ADJ_NEG_ROOM,
    ("Reception", "pos"): ADJ_POS_STAFF,
    ("Reception", "neg"): ADJ_NEG_STAFF,
    ("F&B", "pos"): ADJ_POS_FOOD,
    ("F&B", "neg"): ADJ_NEG_FOOD,
}

# =============================================================================
# Cross-department noise — neutral filler sentences
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

# =============================================================================
# Hedging phrases for ambiguous reviews
# =============================================================================

HEDGES_POS = [
    "non male", "abbastanza buono", "discreto", "nella media alta",
    "sopra la media", "decente", "accettabile", "più che sufficiente",
]

HEDGES_NEG = [
    "non all'altezza", "sotto la media", "non proprio il massimo",
    "lascia a desiderare", "potrebbe fare di meglio", "non soddisfacente",
    "mediocre", "insufficiente",
]

# =============================================================================
# Titles — department + sentiment specific, plus generic
# =============================================================================

TITLES = {
    "positive": {
        "Housekeeping": [
            "Camera impeccabile", "Pulizia perfetta", "Stanza splendida",
            "Ambiente curatissimo", "Ottima manutenzione", "Camera da sogno",
            "Stanza eccellente", "Pulizia top", "Camera consigliatissima",
            "Ambiente perfetto", "Sistemazione ottima", "Camera fantastica",
        ],
        "Reception": [
            "Staff eccezionale", "Accoglienza top", "Personale fantastico",
            "Servizio impeccabile", "Reception efficiente", "Cordialità unica",
            "Personale gentilissimo", "Accoglienza calorosa", "Staff preparato",
            "Servizio eccellente", "Reception disponibile", "Team straordinario",
        ],
        "F&B": [
            "Colazione ottima", "Cibo delizioso", "Ristorante top",
            "Cucina eccellente", "Buffet ricchissimo", "Pranzo memorabile",
            "Cena fantastica", "Colazione abbondante", "Menu squisito",
            "Piatti deliziosi", "Qualità eccellente", "Gastronomia top",
        ],
    },
    "negative": {
        "Housekeeping": [
            "Camera deludente", "Pulizia scarsa", "Stanza sporca",
            "Manutenzione assente", "Ambiente trascurato", "Camera da incubo",
            "Stanza pessima", "Pulizia inesistente", "Camera da evitare",
            "Ambiente squallido", "Sistemazione indecente", "Camera orribile",
        ],
        "Reception": [
            "Staff scortese", "Accoglienza pessima", "Personale maleducato",
            "Servizio inesistente", "Reception disorganizzata", "Attesa infinita",
            "Personale sgarbato", "Accoglienza gelida", "Staff incompetente",
            "Servizio pessimo", "Reception assente", "Team impreparato",
        ],
        "F&B": [
            "Colazione scarsa", "Cibo immangiabile", "Ristorante deludente",
            "Cucina pessima", "Buffet povero", "Pranzo da dimenticare",
            "Cena pessima", "Colazione misera", "Menu scadente",
            "Piatti orribili", "Qualità assente", "Gastronomia pessima",
        ],
    },
    "generic": [
        "Hotel nella media", "Esperienza altalenante", "Poteva andare meglio",
        "Niente di speciale", "Soggiorno ok", "Recensione hotel",
        "La mia esperienza", "Vacanza a metà", "Hotel discreto",
        "Ci sono stato", "Weekend al mare", "Trasferta di lavoro",
        "Soggiorno breve", "Qualche giorno qui", "Hotel in centro",
        "Prima volta qui", "Seconda visita", "Consigli utili",
        "Pro e contro", "Opinione sincera", "Giudizio personale",
        "Nota dolente", "Alti e bassi", "Luci e ombre",
        "Hotel centrale", "Struttura recente", f"Soggiorno {fake.month_name()}",
    ],
}
