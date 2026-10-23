# Contributing

Thank you for helping. The most valuable contributions are small: a fixed settings-page name, a new item, a clearer description, or a bug report with real output from your system.

## Reporting a bug

Please open an issue and attach the output of:

```bash
brokentools-control-panel --check
```

and tell us your distribution, Plasma version (`plasmashell --version`) and how you installed the program. For a missing or broken KDE settings item also attach `kcmshell6 --list`.

## Development setup

```bash
git clone https://github.com/UnscrewGuru/brokentools-control-panel.git
cd brokentools-control-panel
sudo pacman -S --needed python python-pyqt6 kde-cli-tools systemsettings

env PYTHONPATH=src python3 -m brokentools_control_panel            # run the window
env PYTHONPATH=src python3 -m brokentools_control_panel --check    # see shown / hidden items
env PYTHONPATH=src python3 -m unittest discover -s tests -v        # run the tests
```

The tests need neither PyQt6 nor KDE; if PyQt6 is installed, `tests/test_gui_smoke.py` also opens the real window offscreen.

## Project layout

```
src/brokentools_control_panel/
    catalog.py      the list of items (Greek names are the keys), plus the logic that checks and runs them (no Qt)
    translations.py English names and descriptions of every item and category
    i18n.py         language detection and the window texts (English and Greek)
    app.py          the PyQt6 window
    __main__.py     command-line entry point
    icons/          application icon, nine sizes
packaging/          launcher and .desktop templates, Arch PKGBUILD
docs/               installation manual and tutorial
tests/              unit tests (the window smoke test is skipped when PyQt6 is missing)
```

## Adding or fixing an item

Everything is in `catalog.py`; no GUI code is needed. An item is one call:

| Helper | Does | Example |
| --- | --- | --- |
| `K(name, desc, icons, ids)` | opens a KDE settings page; `ids` is one id or a list of alternatives (the first that exists in `kcmshell6 --list` is used) | `K("Fonts", "...", ["preferences-desktop-font"], "kcm_fonts")` |
| `A(name, desc, icons, argv)` | starts a program | `A("Filelight", "...", ["filelight"], "filelight")` |
| `T(name, desc, icons, cmd, requires)` | runs a command in a terminal; `requires` lists commands that must exist | `T("Free space", "...", ["drive-harddisk"], "df -h", ["df"])` |
| `Q(name, desc, icons, title, prompt, cmd, requires)` | asks for text, then runs `cmd` with `{}` replaced (the text is shell-quoted) | see the tutorial |
| `C(name, desc, icons, cmd, requires)` | runs a command silently and copies the output to the clipboard | |

Guidelines:

- Commands must work in **both fish and bash**: use `;`, `|` and `||`, and avoid `for` loops, `$(...)` and `VAR=value cmd`.
- Do not add commands that delete or overwrite data. Anything that changes the system must run in a visible terminal.
- Give a list of icon names, most specific first. They are standard freedesktop names.
- Keep descriptions to one short line.
- Never put user-typed text into a command without `catalog.quote_args()`.

## Translations

The catalogue in `catalog.py` is written in Greek, which is the key for everything else. Every new item needs an entry in `ITEMS_EN` in `translations.py`:

```python
"Γραμματοσειρές": ("Fonts", "Fonts and text rendering"),   # Greek name -> (English name, English description)
```

Items that ask for text (`Q`) also need an `ASK_EN` entry. Window texts live in `i18n.STRINGS`, with an `en` and an `el` version of each. The tests fail if an item has no English text, if a translation is left over, if English text contains Greek letters, or if placeholders such as `{n}` differ between languages. To add another language, extend `i18n.LANGUAGES`, the lookups in `translations.py` and the language box in `app.py`.

## Before opening a pull request

1. `env PYTHONPATH=src python3 -m unittest discover -s tests` passes.
2. `env PYTHONPATH=src python3 -m brokentools_control_panel --check` runs without errors.
3. For changes to the window, mention what you tried (view mode, search, the changed screen). Screenshots help.
4. Add a line to the `Unreleased` section of `CHANGELOG.md`.

By contributing you agree that your contribution is licensed under GPL-3.0-or-later, the license of this project.
