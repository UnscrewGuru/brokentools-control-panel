#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# BrokenTools Control Panel - uninstaller for the per-user install.
#
#   bash uninstall.sh            remove the application, launcher, menu entry and icons
#   bash uninstall.sh --purge    also remove the saved settings (~/.config/brokentools)
set -euo pipefail

APP_ID="brokentools-control-panel"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"

# Only ever touch files this project created.
rm -rf "${DATA_HOME:?}/$APP_ID"
rm -f  "$HOME/.local/bin/$APP_ID"
rm -f  "$DATA_HOME/applications/$APP_ID.desktop"
for png in "$DATA_HOME"/icons/hicolor/*/apps/"$APP_ID.png"; do
    [ -e "$png" ] && rm -f "$png"
done

if [ "${1:-}" = "--purge" ]; then
    rm -f "$CONFIG_HOME/brokentools/control-panel.conf"
    rmdir "$CONFIG_HOME/brokentools" 2>/dev/null || true
fi

command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t -f "$DATA_HOME/icons/hicolor" 2>/dev/null || true
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$DATA_HOME/applications" 2>/dev/null || true
command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 >/dev/null 2>&1 || true

echo "BrokenTools Control Panel has been removed."
