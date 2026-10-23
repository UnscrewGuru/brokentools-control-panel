# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-10-22

First public release.

### Added
- Windows-style Control Panel window for KDE Plasma 6 (PyQt6): category view and large-icons view, search (`Ctrl+F`), Back and Home navigation, remembered view mode.
- Catalogue of more than 100 items in 10 categories: KDE settings pages (`kcmshell6`), system tools, hardware information, network tools and CachyOS tools.
- Items are hidden automatically when their program or KDE settings page does not exist on the system.
- Power profile switcher (Power saver, Balanced, Performance) with live CPU driver, EPP and clock information, using `power-profiles-daemon`.
- "Copy info for help" item that puts a system summary and recent errors on the clipboard.
- Command-line options `--check`, `--version` and `--help`.
- English and Greek interface. The language follows the system by default and can be switched from the toolbar; the choice is remembered. Search works in both languages.
- Per-user `install.sh` and `uninstall.sh` (no root), application icon in nine sizes, `.desktop` entry, Arch `PKGBUILD`.
- English installation manual and step-by-step tutorial.
- Unit tests for the catalogue logic and a GitHub Actions workflow.

### Known limitations
- Tested on CachyOS with KDE Plasma 6 only.

[1.0.0]: https://github.com/UnscrewGuru/brokentools-control-panel/releases/tag/v1.0.0
