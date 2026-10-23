#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# BrokenTools Control Panel - per-user installer (no root, no sudo).
#
#   bash install.sh            install or update for the current user
#   bash install.sh --check    only check the requirements, change nothing
#
# Files created (all inside your home directory):
#   ~/.local/share/brokentools-control-panel/   the application
#   ~/.local/bin/brokentools-control-panel      launcher
#   ~/.local/share/applications/brokentools-control-panel.desktop   menu entry
#   ~/.local/share/icons/hicolor/*/apps/brokentools-control-panel.png   icons
set -euo pipefail

APP_ID="brokentools-control-panel"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
APP_DIR="$DATA_HOME/$APP_ID"
BIN_DIR="$HOME/.local/bin"
APPS_DIR="$DATA_HOME/applications"
ICONS_DIR="$DATA_HOME/icons"

say()  { printf '%s\n' "$*"; }
warn() { printf 'Warning: %s\n' "$*" >&2; }
die()  { printf 'Error: %s\n' "$*" >&2; exit 1; }

check_requirements() {
    local ok=1
    command -v python3 >/dev/null 2>&1 || { warn "python3 not found.  Install: sudo pacman -S python"; ok=0; }
    if command -v python3 >/dev/null 2>&1; then
        python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' \
            || { warn "Python 3.9 or newer is required."; ok=0; }
        python3 -c 'import PyQt6.QtWidgets' 2>/dev/null \
            || { warn "PyQt6 not found.  Install: sudo pacman -S python-pyqt6"; ok=0; }
    fi
    command -v kcmshell6 >/dev/null 2>&1 \
        || warn "kcmshell6 not found (package kde-cli-tools). The app starts, but the KDE settings items will be hidden."
    [ "$ok" -eq 1 ]
}

if [ "${1:-}" = "--check" ]; then
    if check_requirements; then say "All required components are present."; exit 0; fi
    exit 1
fi

[ "$(id -u)" -ne 0 ] || die "Do not run this installer as root. It installs for the current user only."
[ -d "$SRC_DIR/src/brokentools_control_panel" ] || die "Run install.sh from the project folder (src/brokentools_control_panel not found)."
check_requirements || die "Required components are missing (see above). Install them and run install.sh again."

say "Installing BrokenTools Control Panel..."

# 1. application files (replace any previous version, keep nothing else)
rm -rf "$APP_DIR/brokentools_control_panel"
mkdir -p "$APP_DIR" "$BIN_DIR" "$APPS_DIR" "$ICONS_DIR"
cp -r "$SRC_DIR/src/brokentools_control_panel" "$APP_DIR/"
chmod -R u+rwX,go+rX,go-w "$APP_DIR/brokentools_control_panel"   # the source files may be read-only
find "$APP_DIR" -name '__pycache__' -type d -prune -exec rm -rf {} +
install -m 755 "$SRC_DIR/uninstall.sh" "$APP_DIR/uninstall.sh"

# 2. launcher
sed "s|@APPDIR@|$APP_DIR|g" "$SRC_DIR/packaging/launcher.in" > "$BIN_DIR/$APP_ID"
chmod 755 "$BIN_DIR/$APP_ID"

# 3. menu entry (absolute path, so it works even if ~/.local/bin is not in PATH)
sed "s|@BINDIR@|$BIN_DIR|g" "$SRC_DIR/packaging/$APP_ID.desktop.in" > "$APPS_DIR/$APP_ID.desktop"
chmod 644 "$APPS_DIR/$APP_ID.desktop"

# 4. icons
rm -f "$ICONS_DIR"/hicolor/*/apps/"$APP_ID.png"   # an older copy may be read-only
cp -r "$SRC_DIR/src/brokentools_control_panel/icons/hicolor" "$ICONS_DIR/"
chmod -R u+rwX,go+rX,go-w "$ICONS_DIR"/hicolor/*/apps/"$APP_ID.png"
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t -f "$ICONS_DIR/hicolor" 2>/dev/null || true

# 5. refresh the KDE menu
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS_DIR" 2>/dev/null || true
command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 >/dev/null 2>&1 || true

say ""
say "Done. Search for \"BrokenTools Control Panel\" in the application menu,"
say "or run:  $BIN_DIR/$APP_ID"
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) say "Note: $BIN_DIR is not in your PATH, so typing the command name alone will not work."
       say "      fish:  fish_add_path ~/.local/bin      bash/zsh: add it to ~/.profile" ;;
esac
