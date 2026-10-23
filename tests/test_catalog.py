# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""Unit tests for the catalogue logic. They do not need PyQt6 or KDE."""
import io
import shlex
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest import mock

from brokentools_control_panel import APP_NAME, __version__, __main__ as entry
from brokentools_control_panel import catalog

REAL_PPCTL_OUTPUT = """performance:
  CpuDriver:  amd_pstate
  Degraded:   no

* balanced:
  CpuDriver:  amd_pstate
  PlatformDriver:     placeholder

power-saver:
  CpuDriver:  amd_pstate
  PlatformDriver:     placeholder
"""

KCM_LIST_SAMPLE = """The following modules are available:
kcm_fonts                    - Configure user interface fonts
kcm_nighttime                - Configure the day-night cycle times
"""


class CatalogIntegrity(unittest.TestCase):
    def test_categories_and_items_are_well_formed(self):
        kinds = {"kcm", "app", "term", "ask", "clip"}
        self.assertGreater(len(catalog.CATEGORIES), 5)
        for cat in catalog.CATEGORIES:
            self.assertTrue(cat["name"])
            self.assertTrue(cat["icons"])
            self.assertTrue(cat["items"], cat["name"])
            for item in cat["items"]:
                label = f"{cat['name']} / {item['name']}"
                self.assertTrue(item["name"], label)
                self.assertTrue(item["desc"], label)
                self.assertTrue(item["icons"], label)
                kind = item["action"][0]
                self.assertIn(kind, kinds, label)
                if kind == "kcm":
                    self.assertTrue(item["action"][1] and all(item["action"][1]), label)
                elif kind == "app":
                    self.assertTrue(item["action"][1] and item["action"][1][0], label)
                elif kind == "ask":
                    self.assertEqual(len(item["action"]), 4, label)
                    self.assertIn("{}", item["action"][3], label)
                else:
                    self.assertTrue(item["action"][1], label)

    def test_names_are_unique(self):
        cats = [c["name"] for c in catalog.CATEGORIES]
        self.assertEqual(len(cats), len(set(cats)))
        items = [i["name"] for c in catalog.CATEGORIES for i in c["items"]]
        self.assertEqual(len(items), len(set(items)))

    def test_only_the_power_category_has_the_profile_bar(self):
        flagged = [c["name"] for c in catalog.CATEGORIES if c.get("profiles")]
        self.assertEqual(len(flagged), 1)


class Availability(unittest.TestCase):
    def test_nothing_that_needs_kde_is_shown_without_kde(self):
        with mock.patch.object(catalog.shutil, "which", return_value=None):
            shown = catalog.load_available()
        for cat in shown:
            for item in cat["items"]:
                self.assertNotIn(item["action"][0], ("kcm", "app"), item["name"])

    def test_kcm_alternative_ids_are_resolved(self):
        item = catalog.K("Test", "desc", ["x"], ["kcm_missing", "kcm_present"])
        with mock.patch.object(catalog.shutil, "which", return_value="/usr/bin/kcmshell6"):
            ok, _ = catalog.check_item(item, {"kcm_present"})
        self.assertTrue(ok)
        self.assertEqual(item["resolved"], "kcm_present")

    def test_kcm_missing_is_hidden_with_a_reason(self):
        item = catalog.K("Test", "desc", ["x"], "kcm_missing")
        with mock.patch.object(catalog.shutil, "which", return_value="/usr/bin/kcmshell6"):
            ok, why = catalog.check_item(item, {"kcm_other"})
        self.assertFalse(ok)
        self.assertIn("kcm_missing", why)

    def test_kcm_list_is_parsed(self):
        fake = SimpleNamespace(stdout=KCM_LIST_SAMPLE)
        with mock.patch.object(catalog.shutil, "which", return_value="/usr/bin/kcmshell6"), \
                mock.patch.object(catalog.subprocess, "run", return_value=fake):
            ids = catalog.kcm_ids()
        self.assertTrue({"kcm_fonts", "kcm_nighttime"} <= ids)

    def test_print_check_runs_and_summarises(self):
        buf = io.StringIO()
        with mock.patch.object(catalog.shutil, "which", return_value=None), redirect_stdout(buf):
            self.assertEqual(catalog.print_check(), 0)
        self.assertIn("Shown:", buf.getvalue())
        self.assertIn("hidden:", buf.getvalue())


class Helpers(unittest.TestCase):
    def test_user_text_cannot_inject_shell_commands(self):
        text = "firefox vlc; rm -rf / $(reboot) `id`"
        self.assertEqual(shlex.split(catalog.quote_args(text)), text.split())

    def test_parse_profiles_from_real_output(self):
        self.assertEqual(catalog.parse_profiles(REAL_PPCTL_OUTPUT),
                         ["power-saver", "balanced", "performance"])

    def test_parse_profiles_ignores_garbage(self):
        self.assertEqual(catalog.parse_profiles(""), [])
        self.assertEqual(catalog.parse_profiles("Failed to connect to bus"), [])

    def test_cpu_status_has_all_keys(self):
        self.assertEqual(sorted(catalog.cpu_status()), ["avg", "driver", "epp", "max"])


class EntryPoint(unittest.TestCase):
    def test_version_and_help(self):
        for flag in ("--version", "--help"):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(entry.run(["prog", flag]), 0)
            self.assertIn(APP_NAME, buf.getvalue())
        self.assertRegex(__version__, r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
