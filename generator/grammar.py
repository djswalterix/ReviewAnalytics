"""
Italian grammar helpers — article elision, gender-aware adjective picking,
typo injection, and template utilities.
"""

import random

from .config import fake, DEPARTMENTS, TYPO_PROBABILITY, CROSS_DEPT_NOISE_PROBABILITY
from .vocabulary import NOUNS_MAP, ADJ_MAP, CROSS_DEPT_NOISE, TITLES

# Article lookup: maps gender to (definite article, indefinite article)
ARTICLES = {"m": ("Il", "un"), "f": ("La", "una")}

VOWELS = set("aeiouAEIOU")

# Consonant clusters that require "lo" instead of "il" in masculine
_LO_PREFIXES = (
    "sp", "st", "sc", "sf", "sm", "sn", "sl", "sb", "sd", "sg", "sv", "sr",
    "z", "gn", "ps", "pn", "x", "y",
)


# =============================================================================
# Article handling
# =============================================================================

def articulate(article: str, noun: str) -> str:
    """Apply Italian article elision/mutation before vowels and special consonants."""
    if not noun:
        return article
    first = noun[0]
    art_lower = article.lower()
    is_upper = article[0].isupper()

    if art_lower in ("il", "lo"):
        if first in VOWELS:
            return "L'" if is_upper else "l'"
        if any(noun.lower().startswith(p) for p in _LO_PREFIXES):
            return "Lo" if is_upper else "lo"
        return "Il" if is_upper else "il"

    if art_lower == "la":
        if first in VOWELS:
            return "L'" if is_upper else "l'"
        return article

    return article


def art_noun(article: str, noun: str) -> str:
    """Combine article and noun with correct spacing (no space after apostrophe)."""
    art = articulate(article, noun)
    if art.endswith("'"):
        return f"{art}{noun}"
    return f"{art} {noun}"


# =============================================================================
# Vocabulary pickers
# =============================================================================

def pick_noun(dept: str) -> tuple[str, str]:
    """Pick a random noun for the department. Returns (noun, gender)."""
    return random.choice(NOUNS_MAP[dept])


def pick_adj(dept: str, polarity: str, gender: str) -> str:
    """Pick a gender-agreed adjective. polarity is 'pos' or 'neg'."""
    pair = random.choice(ADJ_MAP[(dept, polarity)])
    return pair[0] if gender == "m" else pair[1]


# =============================================================================
# Template fillers
# =============================================================================

def get_random_intro() -> str:
    """Generate a random contextual introduction to add variability."""
    templates = [
        f"Siamo arrivati di {fake.day_of_week()} verso le {random.randint(8, 23)}.",
        f"Dopo un viaggio da {fake.city()},",
        "Ho prenotato tramite Booking.",
        "Abbiamo soggiornato per il weekend.",
        f"Ero qui per lavoro con {fake.first_name()}.",
        "Non sapevo cosa aspettarmi.",
        "Abbiamo scelto questo hotel per la posizione.",
        "Prima volta in questa struttura.",
        f"Soggiorno di {random.randint(1, 7)} notti.",
        "Hotel consigliato da amici.",
        f"Prenotato {random.randint(1, 30)} giorni prima.",
        "Viaggio in famiglia.",
        "Vacanza romantica.",
        "Trasferta di lavoro.",
        "",  # Sometimes no intro
    ]
    return random.choice(templates)


def get_random_outro() -> str:
    """Generate a random closing statement to add variability."""
    templates = [
        "Comunque torneremo.",
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
        "",  # Sometimes no outro
    ]
    return random.choice(templates)


# =============================================================================
# Data augmentation
# =============================================================================

def maybe_inject_typo(text: str) -> str:
    """With TYPO_PROBABILITY chance, swap two adjacent characters in one word."""
    if random.random() >= TYPO_PROBABILITY:
        return text
    words = text.split()
    candidates = [(i, w) for i, w in enumerate(words) if len(w) >= 4]
    if not candidates:
        return text
    idx, word = random.choice(candidates)
    pos = random.randint(1, len(word) - 2)
    chars = list(word)
    chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
    words[idx] = "".join(chars)
    return " ".join(words)


def add_cross_dept_noise(body: str, main_dept: str) -> str:
    """With configured probability, prepend or append a neutral sentence about another department."""
    if random.random() < CROSS_DEPT_NOISE_PROBABILITY:
        other_depts = [d for d in CROSS_DEPT_NOISE if d != main_dept]
        noise_dept = random.choice(other_depts)
        noise = random.choice(CROSS_DEPT_NOISE[noise_dept])
        if random.random() < 0.5:
            return f"{noise} {body}"
        else:
            return f"{body} {noise}"
    return body


# =============================================================================
# Title generation
# =============================================================================

def generate_title(sentiment: int, department: str) -> str:
    """Generate a title with realistic noise.

    40% generic (no dept/sentiment leak), 10% wrong department,
    50% matching department+sentiment.
    """
    r = random.random()
    sentiment_key = "positive" if sentiment == 1 else "negative"
    if r < 0.4:
        return random.choice(TITLES["generic"])
    elif r < 0.5:
        wrong_dept = random.choice([d for d in DEPARTMENTS if d != department])
        return random.choice(TITLES[sentiment_key][wrong_dept])
    else:
        return random.choice(TITLES[sentiment_key][department])
