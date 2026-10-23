# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""Interface language: system detection, the current language, and the window texts.

Supported languages: "en" (English) and "el" (Greek).
The texts of the catalogue items live in translations.py; everything else is here.
No Qt dependency.
"""
import os

LANGUAGES = ("en", "el")
PREFERENCES = ("auto", "en", "el")      # what the user can choose; "auto" follows the system
DEFAULT = "en"

_current = DEFAULT


def system_language(env=None):
    """Return "el" if the system language is Greek, otherwise "en".

    Follows the gettext rules: the locale is the first of LC_ALL, LC_MESSAGES, LANG that is set
    (a "C"/"POSIX" locale means "no translation"); LANGUAGE, if set, then takes priority.
    """
    env = os.environ if env is None else env
    locale = ""
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        if env.get(var):
            locale = env[var]
            break
    if locale in ("", "C", "POSIX"):
        return DEFAULT
    wanted = env.get("LANGUAGE", "").split(":")[0].strip() or locale
    return "el" if wanted.lower().startswith("el") else "en"


def resolve(preference, env=None):
    """Turn a saved preference ("auto", "en", "el") into a language code."""
    return preference if preference in LANGUAGES else system_language(env)


def set_language(lang):
    global _current
    _current = lang if lang in LANGUAGES else DEFAULT


def get_language():
    return _current


STRINGS = {
    # toolbar
    "back_tip": {"en": "Back (Alt+Left)", "el": "Πίσω (Alt+←)"},
    "home_tip": {"en": "Home", "el": "Αρχική"},
    "search_placeholder": {"en": "Search the Control Panel (Ctrl+F)",
                           "el": "Αναζήτηση στον Πίνακα Ελέγχου (Ctrl+F)"},
    "view_by": {"en": "View by:", "el": "Προβολή κατά:"},
    "mode_category": {"en": "Category", "el": "Κατηγορία"},
    "mode_icons": {"en": "Large icons", "el": "Μεγάλα εικονίδια"},
    "language_label": {"en": "Language:", "el": "Γλώσσα:"},
    "lang_auto": {"en": "Automatic", "el": "Αυτόματη"},
    # pages
    "heading": {"en": "Adjust your computer's settings",
                "el": "Προσαρμογή των ρυθμίσεων του υπολογιστή σας"},
    "crumb_all": {"en": "All items", "el": "Όλα τα στοιχεία"},
    "crumb_search": {"en": "Search results ({n})", "el": "Αποτελέσματα αναζήτησης ({n})"},
    "tip_category": {"en": "Category: {cat}", "el": "Κατηγορία: {cat}"},
    # power profiles
    "power_profile": {"en": "Power profile", "el": "Προφίλ ενέργειας"},
    "profile_power-saver": {"en": "Power saver", "el": "Εξοικονόμηση ενέργειας"},
    "profile_balanced": {"en": "Balanced", "el": "Ισορροπημένο"},
    "profile_performance": {"en": "Performance", "el": "Υψηλή απόδοση"},
    "ppd_missing": {
        "en": "power-profiles-daemon was not found. Install it with: sudo pacman -S power-profiles-daemon "
              "&& sudo systemctl enable --now power-profiles-daemon",
        "el": "Δεν βρέθηκε το power-profiles-daemon. Εγκατάσταση: sudo pacman -S power-profiles-daemon "
              "&& sudo systemctl enable --now power-profiles-daemon"},
    "cpu_clock": {"en": "average clock {avg} MHz, maximum {max} MHz",
                  "el": "μέσο ρολόι {avg} MHz, μέγιστο {max} MHz"},
    "cpu_clock_na": {"en": "clock: not available", "el": "ρολόι: μη διαθέσιμο"},
    "cpu_status": {"en": "CPU: driver {driver}, energy preference (EPP) \"{epp}\", {clock}",
                   "el": "Επεξεργαστής: driver {driver}, προτίμηση ενέργειας (EPP) «{epp}», {clock}"},
    "profile_failed": {"en": "The power profile was not changed.\n\n{err}",
                       "el": "Δεν άλλαξε το προφίλ ενέργειας.\n\n{err}"},
    # running items
    "run_failed": {"en": "Could not run:\n{name}\n\n{err}",
                   "el": "Δεν ήταν δυνατή η εκτέλεση:\n{name}\n\n{err}"},
    "copied": {
        "en": "{n} lines were copied to the clipboard.\nPaste them (Ctrl+V) into your forum post or "
              "AI chat together with a description of the problem.",
        "el": "Αντιγράφηκαν {n} γραμμές στο clipboard.\nΚάνε επικόλληση (Ctrl+V) στη συνομιλία με το LLM "
              "μαζί με την περιγραφή του προβλήματος."},
    "press_enter": {"en": "Press Enter to close...", "el": "Πάτα Enter για κλείσιμο..."},
    "err_no_kcmshell": {"en": "kcmshell6 was not found.", "el": "Δεν βρέθηκε το kcmshell6."},
    "err_no_terminal": {
        "en": "No terminal found (konsole, alacritty, kitty, foot, xterm).",
        "el": "Δεν βρέθηκε terminal (konsole, alacritty, kitty, foot, xterm)."},
    "err_no_ppctl": {
        "en": "powerprofilesctl was not found (package power-profiles-daemon).",
        "el": "Δεν βρέθηκε το powerprofilesctl (πακέτο power-profiles-daemon)."},
}


def tr(key, **values):
    """Text for the current language. Falls back to English, then to the key itself."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(_current) or entry["en"]
    return text.format(**values) if values else text
