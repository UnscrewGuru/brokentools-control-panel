# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""Tests for the language support. They need neither PyQt6 nor KDE."""
import re
import unittest

from brokentools_control_panel import catalog, i18n, translations

GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")
PLACEHOLDER = re.compile(r"\{(\w+)\}")


def all_items():
    return [(cat, item) for cat in catalog.CATEGORIES for item in cat["items"]]


class LanguageTestCase(unittest.TestCase):
    def setUp(self):
        self.addCleanup(i18n.set_language, i18n.DEFAULT)


class CatalogueTranslations(LanguageTestCase):
    def test_every_category_and_item_has_an_english_entry(self):
        for cat, item in all_items():
            self.assertIn(cat["name"], translations.CATEGORY_NAMES_EN, cat["name"])
            self.assertIn(item["name"], translations.ITEMS_EN, item["name"])
            name, desc = translations.ITEMS_EN[item["name"]]
            self.assertTrue(name.strip() and desc.strip(), item["name"])

    def test_items_that_ask_for_text_have_english_dialog_texts(self):
        for _, item in all_items():
            if item["action"][0] == "ask":
                self.assertIn(item["name"], translations.ASK_EN, item["name"])

    def test_no_stale_entries(self):
        items = {item["name"] for _, item in all_items()}
        cats = {cat["name"] for cat in catalog.CATEGORIES}
        asks = {item["name"] for _, item in all_items() if item["action"][0] == "ask"}
        self.assertEqual(set(translations.ITEMS_EN), items)
        self.assertEqual(set(translations.CATEGORY_NAMES_EN), cats)
        self.assertEqual(set(translations.ASK_EN), asks)

    def test_english_item_names_are_unique(self):
        names = [translations.ITEMS_EN[item["name"]][0] for _, item in all_items()]
        self.assertEqual(len(names), len(set(names)))

    def test_english_texts_contain_no_greek(self):
        texts = [t for pair in translations.ITEMS_EN.values() for t in pair]
        texts += list(translations.CATEGORY_NAMES_EN.values())
        texts += [t for pair in translations.ASK_EN.values() for t in pair]
        texts += list(translations.COMMAND_TEXT_EN.values())
        for text in texts:
            self.assertIsNone(GREEK.search(text), text)

    def test_english_commands_contain_no_greek(self):
        for _, item in all_items():
            if item["action"][0] in ("term", "clip"):
                self.assertIsNone(GREEK.search(catalog.item_command(item, "en")), item["name"])

    def test_greek_commands_are_left_untouched(self):
        for _, item in all_items():
            if item["action"][0] in ("term", "clip"):
                self.assertEqual(catalog.item_command(item, "el"), item["action"][1])

    def test_helpers_follow_the_current_language(self):
        cat, item = all_items()[0]
        i18n.set_language("en")
        self.assertEqual(catalog.item_name(item), translations.ITEMS_EN[item["name"]][0])
        self.assertEqual(catalog.category_title(cat), translations.CATEGORY_NAMES_EN[cat["name"]])
        i18n.set_language("el")
        self.assertEqual(catalog.item_name(item), item["name"])
        self.assertEqual(catalog.item_desc(item), item["desc"])
        self.assertEqual(catalog.category_title(cat), cat["name"])

    def test_search_finds_items_in_both_languages(self):
        cat = [c for c in catalog.CATEGORIES if c["name"] == "Ενέργεια και απόδοση"][0]
        item = [i for i in cat["items"] if i["name"] == "Διαχείριση ενέργειας"][0]
        text = catalog.search_text(item, cat)
        self.assertIn("διαχείριση ενέργειας", text)
        self.assertIn("power management", text)


class WindowTexts(LanguageTestCase):
    def test_every_text_exists_in_both_languages(self):
        for key, entry in i18n.STRINGS.items():
            for lang in i18n.LANGUAGES:
                self.assertTrue(entry.get(lang, "").strip(), f"{key} [{lang}]")

    def test_english_texts_contain_no_greek(self):
        for key, entry in i18n.STRINGS.items():
            self.assertIsNone(GREEK.search(entry["en"]), key)

    def test_placeholders_match_between_languages(self):
        for key, entry in i18n.STRINGS.items():
            self.assertEqual(set(PLACEHOLDER.findall(entry["en"])),
                             set(PLACEHOLDER.findall(entry["el"])), key)

    def test_every_power_profile_has_a_label(self):
        for name in catalog.PROFILE_ORDER:
            self.assertIn("profile_" + name, i18n.STRINGS)
            i18n.set_language("en")
            self.assertTrue(catalog.profile_label(name))

    def test_tr_switches_language_and_formats(self):
        i18n.set_language("en")
        self.assertEqual(i18n.tr("crumb_search", n=3), "Search results (3)")
        i18n.set_language("el")
        self.assertEqual(i18n.tr("crumb_search", n=3), "Αποτελέσματα αναζήτησης (3)")
        self.assertEqual(i18n.tr("no-such-key"), "no-such-key")

    def test_unknown_language_falls_back_to_english(self):
        i18n.set_language("fr")
        self.assertEqual(i18n.get_language(), "en")


class LanguageDetection(unittest.TestCase):
    def test_greek_system(self):
        self.assertEqual(i18n.system_language({"LANG": "el_GR.UTF-8"}), "el")
        self.assertEqual(i18n.system_language({"LC_ALL": "el_GR.UTF-8", "LANG": "en_US.UTF-8"}), "el")

    def test_other_systems_get_english(self):
        for env in ({"LANG": "en_US.UTF-8"}, {"LANG": "de_DE.UTF-8"}, {"LANG": "es_ES.UTF-8"}, {}):
            self.assertEqual(i18n.system_language(env), "en", env)

    def test_c_locale_means_english(self):
        self.assertEqual(i18n.system_language({"LANG": "C"}), "en")
        self.assertEqual(i18n.system_language({"LC_ALL": "C", "LANG": "el_GR.UTF-8"}), "en")

    def test_language_variable_takes_priority(self):
        self.assertEqual(i18n.system_language({"LANG": "en_US.UTF-8", "LANGUAGE": "el:en"}), "el")
        self.assertEqual(i18n.system_language({"LANG": "el_GR.UTF-8", "LANGUAGE": "en"}), "en")

    def test_resolve_preference(self):
        self.assertEqual(i18n.resolve("en", {"LANG": "el_GR.UTF-8"}), "en")
        self.assertEqual(i18n.resolve("el", {"LANG": "en_US.UTF-8"}), "el")
        self.assertEqual(i18n.resolve("auto", {"LANG": "el_GR.UTF-8"}), "el")
        self.assertEqual(i18n.resolve("garbage", {"LANG": "en_US.UTF-8"}), "en")


if __name__ == "__main__":
    unittest.main()
