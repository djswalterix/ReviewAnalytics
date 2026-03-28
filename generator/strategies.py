"""
Review generation strategies — each function produces (body, department).
"""

import random

from .config import fake, DEPARTMENTS
from .vocabulary import HEDGES_POS, HEDGES_NEG
from .grammar import (
    ARTICLES, art_noun, pick_noun, pick_adj,
    get_random_intro, get_random_outro,
)


# =============================================================================
# Unified single-department review builder
# =============================================================================

def build_dept_review(dept: str, sentiment: int) -> str:
    """Build a single-department review with correct gender agreement."""
    polarity = "pos" if sentiment == 1 else "neg"
    noun, gender = pick_noun(dept)
    adj = pick_adj(dept, polarity, gender)
    art_def_raw, art_indef = ARTICLES[gender]
    AN = art_noun(art_def_raw, noun)
    an = art_noun(art_def_raw.lower(), noun)

    if sentiment == 1:
        templates = [
            f"{AN} era {adj}.",
            f"{noun.capitalize()} {adj}, niente da dire.",
            f"Ho trovato {an} {adj} e ben curato." if gender == "m"
            else f"Ho trovato {an} {adj} e ben curata.",
            f"Devo dire che {an} era {adj}.",
            f"Piacevolmente sorpreso: {an} molto {adj}.",
            f"{AN} superava le aspettative: {adj}!",
            f"Finalmente {art_indef} {noun} {adj}.",
        ]
    else:
        templates = [
            f"{AN} era {adj}.",
            f"{noun.capitalize()} {adj}, pessima esperienza.",
            f"Purtroppo {an} era {adj}.",
            f"Ho trovato {an} {adj}. Inaccettabile.",
            f"Deluso: {an} {adj}.",
            f"{AN} lasciava a desiderare, troppo {adj}.",
            f"Non mi aspettavo {art_indef} {noun} così {adj}.",
            f"Vergognoso: {noun} {adj}.",
        ]

    # Reception templates can also include a fake name for realism
    if dept == "Reception":
        name = fake.first_name()
        adj_m = pick_adj(dept, polarity, "m")
        extra = [
            f"{name} era {adj_m}.",
            f"Personale {adj_m}, specialmente {name}.",
            f"Staff {adj_m}, complimenti a {name}.",
        ] if sentiment == 1 else [
            f"{name} si è dimostrato {adj_m}.",
            f"Personale {adj_m}, soprattutto {name}.",
            f"Staff {adj_m}, {name} in particolare.",
        ]
        templates.extend(extra)

    return random.choice(templates)


# =============================================================================
# Strategy functions
# =============================================================================

def build_simple_review(sentiment: int) -> tuple[str, str]:
    """Generate a simple, direct review (baseline difficulty)."""
    dept = random.choice(DEPARTMENTS)
    body = build_dept_review(dept, sentiment)
    return body, dept


def build_detailed_review(sentiment: int) -> tuple[str, str]:
    """Generate a detailed review with contextual intro/outro (medium difficulty)."""
    dept = random.choice(DEPARTMENTS)
    intro = get_random_intro()
    outro = get_random_outro()
    core = build_dept_review(dept, sentiment)
    parts = [p for p in [intro, core, outro] if p]
    return " ".join(parts), dept


def build_negation_review(sentiment: int) -> tuple[str, str]:
    """Generate reviews using negation patterns, challenging for simple models."""
    dept = random.choice(DEPARTMENTS)
    noun, gender = pick_noun(dept)
    art_def_raw = ARTICLES[gender][0]
    AN = art_noun(art_def_raw, noun)
    an = art_noun(art_def_raw.lower(), noun)

    if sentiment == 1:
        if dept == "Reception":
            adj_m = pick_adj(dept, "neg", "m")
            templates = [
                f"Il personale non era per niente {adj_m}. Molto professionali.",
                f"Non ho trovato staff {adj_m}. Anzi, gentilissimi.",
                f"Temevo receptionist {adj_m}, invece super disponibili.",
                f"Nessuno {adj_m} alla reception. Complimenti!",
            ]
        else:
            adj = pick_adj(dept, "neg", gender)
            templates = [
                f"{AN} non era affatto {adj}. Anzi, molto curato." if gender == "m"
                else f"{AN} non era affatto {adj}. Anzi, molto curata.",
                f"Avevo paura fosse {adj}, ma {an} era perfetto." if gender == "m"
                else f"Avevo paura fosse {adj}, ma {an} era perfetta.",
                f"Non posso dire che {an} fosse {adj}. Tutt'altro!",
                f"Niente {noun} {adj} come temevo. Ottimo!" if gender == "m"
                else f"Niente {noun} {adj} come temevo. Ottima!",
            ]
    else:
        if dept == "Reception":
            adj_m = pick_adj(dept, "pos", "m")
            adj_f = pick_adj(dept, "pos", "f")
            templates = [
                f"Non aspettatevi personale {adj_m}. Pessimi.",
                f"Di {adj_m} lo staff non aveva niente.",
                f"Il receptionist non era certo {adj_m}. Maleducato.",
                f"Scordatevi accoglienza {adj_f}. Disastro.",
            ]
        else:
            adj = pick_adj(dept, "pos", gender)
            templates = [
                f"Non aspettatevi {noun} {adj}. Pessimo." if gender == "m"
                else f"Non aspettatevi {noun} {adj}. Pessima.",
                f"{AN} non era certo {adj}. Delusione totale.",
                f"Di {adj} {an} non aveva nulla.",
                f"Scordatevi {noun} {adj}. Deludente.",
            ]

    return random.choice(templates), dept


def build_mixed_review(sentiment: int) -> tuple[str, str]:
    """Generate mixed-sentiment reviews where the winning aspect determines the department."""
    dept_lose, dept_win = random.sample(DEPARTMENTS, 2)

    lose_noun, lose_g = pick_noun(dept_lose)
    win_noun, win_g = pick_noun(dept_win)

    lose_AN = art_noun(ARTICLES[lose_g][0], lose_noun)
    lose_an = art_noun(ARTICLES[lose_g][0].lower(), lose_noun)
    win_an = art_noun(ARTICLES[win_g][0].lower(), win_noun)

    if sentiment == 1:
        lose_adj = pick_adj(dept_lose, "neg", lose_g)
        win_adj = pick_adj(dept_win, "pos", win_g)
        templates = [
            f"{lose_AN} era {lose_adj}, ma {win_an} {win_adj} ha salvato tutto.",
            f"{lose_noun.capitalize()} un po' {lose_adj}, però {win_an} {win_adj}. Promossi!",
            f"Nonostante {lose_an} {lose_adj}, {win_an} {win_adj} ha fatto la differenza.",
            f"Ok {lose_an} era {lose_adj}, ma {win_an} {win_adj} compensa.",
        ]
    else:
        lose_adj = pick_adj(dept_lose, "pos", lose_g)
        win_adj = pick_adj(dept_win, "neg", win_g)
        templates = [
            f"{lose_AN} era {lose_adj}, ma {win_an} {win_adj} ha rovinato tutto.",
            f"{lose_noun.capitalize()} {lose_adj}, peccato per {win_an} {win_adj}.",
            f"{lose_AN} anche {lose_adj}, però {win_an} {win_adj}. Mai più.",
            f"Bello: {lose_noun} {lose_adj}, ma {win_an} {win_adj} è inaccettabile.",
        ]

    return random.choice(templates), dept_win


def build_multi_aspect_review(sentiment: int) -> tuple[str, str]:
    """Generate reviews covering multiple hotel aspects (realistic, high difficulty)."""
    intro = get_random_intro()
    polarity = "pos" if sentiment == 1 else "neg"

    room_adj = pick_adj("Housekeeping", polarity, "f")
    staff_adj = pick_adj("Reception", polarity, "m")
    food_adj = pick_adj("F&B", polarity, "f")

    if sentiment == 1:
        templates = [
            f"{intro} Camera {room_adj}, personale {staff_adj}, colazione {food_adj}. Torneremo!",
            f"{intro} Stanza {room_adj}. Staff {staff_adj}. Cena {food_adj}. Top!",
            f"{intro} Tutto perfetto: camera {room_adj}, reception {staff_adj}, ristorante {food_adj}.",
        ]
    else:
        templates = [
            f"{intro} Camera {room_adj}, personale {staff_adj}, colazione {food_adj}. Mai più!",
            f"{intro} Stanza {room_adj}. Staff {staff_adj}. Cena {food_adj}. Disastro.",
            f"{intro} Tutto pessimo: camera {room_adj}, reception {staff_adj}, ristorante {food_adj}.",
        ]

    return random.choice(templates), random.choice(DEPARTMENTS)


def build_ambiguous_review(sentiment: int) -> tuple[str, str]:
    """Generate subtly positive/negative reviews with hedging language (hardest)."""
    dept = random.choice(DEPARTMENTS)

    if dept == "Reception":
        if sentiment == 1:
            hedge = random.choice(HEDGES_POS)
            templates = [
                f"Il personale era {hedge}. Non eccezionale, ma disponibile.",
                f"Reception {hedge}. Poteva andare peggio, anzi no, è andata bene.",
                f"Lo staff era {hedge}, devo ammettere che mi aspettavo peggio.",
                f"Accoglienza {hedge}. Niente effetto wow, ma professionali.",
            ]
        else:
            hedge = random.choice(HEDGES_NEG)
            templates = [
                f"Il personale era {hedge}. Non terribile, ma nemmeno soddisfacente.",
                f"Reception {hedge}. Mi aspettavo di più per il prezzo pagato.",
                f"Lo staff {hedge}, purtroppo non all'altezza delle aspettative.",
                f"Accoglienza {hedge}. Un peccato, rovinava l'esperienza.",
            ]
    else:
        noun, gender = pick_noun(dept)
        art_def_raw = ARTICLES[gender][0]
        AN = art_noun(art_def_raw, noun)
        an = art_noun(art_def_raw.lower(), noun)
        contrast_polarity = "neg" if sentiment == 1 else "pos"
        contrast_adj = pick_adj(dept, contrast_polarity, gender)

        if sentiment == 1:
            hedge = random.choice(HEDGES_POS)
            templates = [
                f"{AN} era {hedge}. Non perfetto, ma ci siamo trovati bene." if gender == "m"
                else f"{AN} era {hedge}. Non perfetta, ma ci siamo trovati bene.",
                f"Ok {an} poteva sembrare {contrast_adj} a primo impatto, ma poi {hedge}.",
                f"{AN}? {hedge.capitalize()}. Niente di eccezionale, ma funzionale.",
                f"Sinceramente {an} era {hedge}, meglio del previsto.",
            ]
        else:
            hedge = random.choice(HEDGES_NEG)
            templates = [
                f"{AN} sembrava {contrast_adj} dalle foto, in realtà {hedge}.",
                f"Mi aspettavo {noun} {contrast_adj}, ma era {hedge}.",
                f"{AN}? {hedge.capitalize()}. Peccato, dalle recensioni sembrava meglio.",
                f"Sulla carta {an} doveva essere {contrast_adj}. Invece {hedge}.",
            ]

    return random.choice(templates), dept


# Strategy dispatcher
STRATEGY_BUILDERS = {
    "simple": build_simple_review,
    "detailed": build_detailed_review,
    "negation": build_negation_review,
    "mixed": build_mixed_review,
    "multi_aspect": build_multi_aspect_review,
    "ambiguous": build_ambiguous_review,
}
