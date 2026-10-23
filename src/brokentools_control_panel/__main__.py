# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""Entry point: python3 -m brokentools_control_panel [--check | --version | --help]"""
import sys

from . import APP_NAME, __version__

USAGE = f"""{APP_NAME} {__version__}

Usage: brokentools-control-panel [OPTION]

  (no option)   start the Control Panel window
  --check       print which items are shown or hidden on this system, and why
                (does not need PyQt6)
  --version     print the version
  --help        show this text
"""


def run(argv):
    args = argv[1:]
    if "--help" in args or "-h" in args:
        print(USAGE)
        return 0
    if "--version" in args:
        print(f"{APP_NAME} {__version__}")
        return 0
    if "--check" in args:
        from . import catalog
        return catalog.print_check()
    try:
        from .app import main
    except ModuleNotFoundError as exc:
        if exc.name and exc.name.startswith("PyQt6"):
            sys.stderr.write("PyQt6 is not installed.\n"
                             "On Arch / CachyOS:  sudo pacman -S python-pyqt6\n")
            return 1
        raise
    main()
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv))
