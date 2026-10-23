# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""Smoke test of the real window. Skipped automatically when PyQt6 is not installed.

It runs headless (Qt "offscreen" platform), never shows a window and never launches an item.
Your saved settings are not touched: Qt is pointed at a temporary settings folder.
"""
import os
import tempfile
import unittest

os.environ["QT_QPA_PLATFORM"] = "offscreen"

try:
    from PyQt6.QtCore import QSettings
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:
    HAVE_QT = False

from brokentools_control_panel import catalog, i18n


@unittest.skipUnless(HAVE_QT, "PyQt6 is not installed")
class WindowSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        QSettings.setPath(QSettings.Format.NativeFormat, QSettings.Scope.UserScope, cls.tmp.name)
        cls.app = QApplication.instance() or QApplication([])
        from brokentools_control_panel.app import ControlPanel
        cls.ControlPanel = ControlPanel

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()
        i18n.set_language(i18n.DEFAULT)

    def make_window(self, language):
        settings = QSettings("brokentools", "control-panel")
        settings.setValue("language", language)
        settings.setValue("mode", 0)
        win = self.ControlPanel()
        self.addCleanup(win.deleteLater)
        return win

    def test_window_opens_in_the_chosen_language(self):
        for language, placeholder in (("en", "Search the Control Panel (Ctrl+F)"),
                                      ("el", "Αναζήτηση στον Πίνακα Ελέγχου (Ctrl+F)")):
            win = self.make_window(language)
            self.assertEqual(win.search.placeholderText(), placeholder)

    def test_every_category_opens(self):
        win = self.make_window("en")
        self.assertGreater(len(win.categories), 0)
        for index in range(len(win.categories)):
            win.open_category(index)
            self.assertEqual(win.state, "cat")
            self.assertEqual(win.list_cat.count(), len(win.categories[index]["items"]))
        win.go_home()
        self.assertIn(win.state, ("home", "all"))

    def test_search_works_in_both_languages(self):
        win = self.make_window("en")
        total = sum(len(c["items"]) for c in win.categories)
        self.assertEqual(win._fill_all(""), total)
        english = win._fill_all("kernel")
        self.assertGreater(english, 0)
        self.assertEqual(win._fill_all("πυρήνα") > 0, True)   # Greek words match in English mode too
        self.assertEqual(win._fill_all("zzzz-no-such-item"), 0)

    def test_language_can_be_switched_while_running(self):
        win = self.make_window("en")
        self.assertEqual(i18n.get_language(), "en")
        win.set_language_pref("el")
        self.app.processEvents()                       # runs the queued rebuild
        self.assertEqual(i18n.get_language(), "el")
        self.assertEqual(win.search.placeholderText(), "Αναζήτηση στον Πίνακα Ελέγχου (Ctrl+F)")
        self.assertEqual(QSettings("brokentools", "control-panel").value("language"), "el")
        win.set_language_pref("en")
        self.app.processEvents()
        self.assertEqual(win.search.placeholderText(), "Search the Control Panel (Ctrl+F)")
        win.open_category(0)                           # the rebuilt window still works
        self.assertEqual(win.state, "cat")

    def test_large_icon_view_lists_every_item(self):
        win = self.make_window("en")
        win.mode_box.setCurrentIndex(1)
        self.assertEqual(win.state, "all")
        self.assertEqual(win.page_all.count(), sum(len(c["items"]) for c in win.categories))
        win.mode_box.setCurrentIndex(0)
        self.assertEqual(win.state, "home")


if __name__ == "__main__":
    unittest.main()
