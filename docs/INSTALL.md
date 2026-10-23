# Installation manual

This manual covers every supported way to install BrokenTools Control Panel, what the installer changes on your system, how to update and uninstall, and what to do when something does not work.

If you are new to Linux, start with the [step-by-step tutorial](TUTORIAL.md) instead.

**Contents**

1. [Supported systems](#supported-systems)
2. [Requirements](#requirements)
3. [Optional packages](#optional-packages)
4. [Method A: release archive (recommended)](#method-a-release-archive-recommended)
5. [Method B: git clone](#method-b-git-clone)
6. [Method C: run without installing](#method-c-run-without-installing)
7. [Method D: Arch package (PKGBUILD)](#method-d-arch-package-pkgbuild)
8. [What the installer does](#what-the-installer-does)
9. [Check that it works](#check-that-it-works)
10. [Update](#update)
11. [Uninstall](#uninstall)
12. [Troubleshooting](#troubleshooting)

Commands below work in **bash, zsh and fish**. Lines starting with `sudo` ask for your password.

---

## Supported systems

| System | Status |
| --- | --- |
| CachyOS, KDE Plasma 6 (Wayland or X11) | Developed and tested here |
| Other Arch-based distributions with Plasma 6 (EndeavourOS, Manjaro, Arch) | Expected to work |
| Other distributions with Plasma 6 | The window starts; Arch/pacman-specific items are hidden automatically |
| GNOME, Xfce and other desktops | Not supported (the KDE settings items need `kcmshell6`) |

## Requirements

| What | Why | Arch / CachyOS package |
| --- | --- | --- |
| Python 3.9 or newer | runs the program | `python` |
| PyQt6 | the window | `python-pyqt6` |
| `kcmshell6` | opens KDE settings pages | `kde-cli-tools` |
| KDE System Settings | the "All KDE settings" item | `systemsettings` |
| A terminal (Konsole is used first) | items that run a command | `konsole` |

Install them in one go:

```bash
sudo pacman -S --needed python python-pyqt6 kde-cli-tools systemsettings konsole
```

On a normal CachyOS KDE install most of these are already present, and `--needed` skips what you have.

> Never run `sudo pacman -Sy <package>` on Arch. Always update the whole system first with `sudo pacman -Syu` if your package databases are old.

## Optional packages

The Control Panel hides every item whose program is missing. Install a package to make its item appear. Package names are for the Arch and CachyOS repositories and can change over time.

| Package | Enables |
| --- | --- |
| `power-profiles-daemon` | the Power saver / Balanced / Performance buttons |
| `kinfocenter` | hardware information window |
| `plasma-systemmonitor` | the Task Manager style window |
| `discover` | graphical software centre |
| `partitionmanager` | disk and partition manager |
| `filelight` | what is using my disk space |
| `pavucontrol` | per-application volume control |
| `inxi` | full system summary, and the "copy info for help" item |
| `btop` | live resource monitor |
| `lm_sensors` | temperatures and fans (`sensors`) |
| `pciutils`, `util-linux`, `iproute2`, `networkmanager` | PCI devices, disks, IP addresses, network status |
| `lact` | AMD GPU power limit, clocks and fans |
| `powertop` | power consumption analysis |
| `btrfs-assistant` | Btrfs snapshots (needs a Btrfs file system) |
| `cachyos-hello`, `cachyos-kernel-manager`, `cachyos-packageinstaller`, `cachyos-rate-mirrors` | the CachyOS category (CachyOS repositories only) |

Everything works without them; you simply see fewer items.

---

## Method A: release archive (recommended)

1. Download `brokentools-control-panel-<version>.tar.gz` (and the `.sha256` file next to it) from the [Releases page](https://github.com/UnscrewGuru/brokentools-control-panel/releases).
2. Open a terminal in the folder where you saved them and verify the download:

   ```bash
   sha256sum -c brokentools-control-panel-1.0.0.tar.gz.sha256
   ```

   It must print `brokentools-control-panel-1.0.0.tar.gz: OK`.
3. Extract and install:

   ```bash
   tar xzf brokentools-control-panel-1.0.0.tar.gz
   cd brokentools-control-panel-1.0.0
   bash install.sh
   ```

Replace `1.0.0` with the version you downloaded.

## Method B: git clone

Use this if you want the latest development version or plan to change the code.

```bash
git clone https://github.com/UnscrewGuru/brokentools-control-panel.git
cd brokentools-control-panel
bash install.sh
```

To install a specific release instead of the latest code, add `git checkout v1.0.0` before `bash install.sh`.

## Method C: run without installing

Nothing is written outside the project folder. Good for trying it out.

```bash
git clone https://github.com/UnscrewGuru/brokentools-control-panel.git
cd brokentools-control-panel
env PYTHONPATH=src python3 -m brokentools_control_panel
```

(`env PYTHONPATH=...` is used on purpose: fish does not accept the bash form `PYTHONPATH=src python3 ...` in older versions.)

## Method D: Arch package (PKGBUILD)

This builds a normal pacman package that installs system-wide and can be removed with `pacman -R`. It downloads the tagged release from GitHub, so it works once a release exists.

```bash
git clone https://github.com/UnscrewGuru/brokentools-control-panel.git
cd brokentools-control-panel/packaging/arch
makepkg -si
```

Remove it later with `sudo pacman -Rns brokentools-control-panel`. An AUR package is planned but not published yet.

Do not mix Method D with Methods A or B on the same user account: you would get two menu entries.

---

## What the installer does

`install.sh` (methods A and B) works for the **current user only**. It refuses to run as root and never uses `sudo`. It creates:

| Path | What |
| --- | --- |
| `~/.local/share/brokentools-control-panel/` | the program (Python files and icons) and a copy of `uninstall.sh` |
| `~/.local/bin/brokentools-control-panel` | the command that starts it |
| `~/.local/share/applications/brokentools-control-panel.desktop` | the application menu entry |
| `~/.local/share/icons/hicolor/<size>/apps/brokentools-control-panel.png` | the icon, 9 sizes |
| `~/.config/brokentools/control-panel.conf` | created by the program when it first runs; only remembers the selected view |

It does not modify any system file and does not change your KDE settings.

Run `bash install.sh --check` to check the requirements without installing anything.

## Check that it works

```bash
brokentools-control-panel --version
brokentools-control-panel --check
```

`--check` does not need PyQt6. It lists every item as `[shown]` or `[hidden]` with the reason, for example `[hidden]  ... -> program lact not found`. Hidden items are normal: they simply do not exist on your system.

Then open **BrokenTools Control Panel** from the application menu.

If the command is "not found", `~/.local/bin` is not in your `PATH`. The menu entry still works. To fix the command:

```fish
fish_add_path ~/.local/bin
```

or, for bash and zsh, add `export PATH="$HOME/.local/bin:$PATH"` to `~/.profile` and log in again.

## Update

Method A: download and extract the new archive, then run `bash install.sh` again.
Method B: `git pull`, then `bash install.sh` again.
Method D: build the new version with `makepkg -si`.

The installer replaces the program files and keeps your settings.

## Uninstall

Methods A, B and C:

```bash
bash uninstall.sh            # from the project folder, or:
bash ~/.local/share/brokentools-control-panel/uninstall.sh
```

Add `--purge` to also delete the saved settings (`~/.config/brokentools/control-panel.conf`).

The uninstaller only removes the files listed in [What the installer does](#what-the-installer-does).

Method D: `sudo pacman -Rns brokentools-control-panel`.

---

## Troubleshooting

**`PyQt6 is not installed`**
Install it: `sudo pacman -S python-pyqt6`. On other distributions use the package named `python3-pyqt6` or `python-pyqt6`.

**The installer says a requirement is missing**
Run `bash install.sh --check`, install what it lists, and run `bash install.sh` again.

**The menu entry or icon does not show up**
Log out and in again, or refresh the KDE menu cache:

```bash
kbuildsycoca6
```

**An item I expect is missing**
Run `brokentools-control-panel --check` and read the reason next to it. Most of the time a package is not installed: see [Optional packages](#optional-packages). If a KDE settings item is hidden with `not in kcmshell6 --list`, your Plasma version uses a different name for that page. Please open an issue and attach the output of:

```bash
brokentools-control-panel --check
kcmshell6 --list
```

**Items that need a terminal do nothing**
The program looks for `konsole`, `alacritty`, `kitty`, `foot` or `xterm`, in that order. Install one, for example `sudo pacman -S konsole`.

**The Power profile buttons are missing or do nothing**
Install and enable the daemon:

```bash
sudo pacman -S power-profiles-daemon
sudo systemctl enable --now power-profiles-daemon
powerprofilesctl list
```

**The text is in the wrong language**
The default is your system language (Greek systems get Greek, everything else English). Pick English or Ελληνικά in the *Language* box at the top right of the window; the choice is remembered in `~/.config/brokentools/control-panel.conf`.

**Still stuck?**
Open an [issue](https://github.com/UnscrewGuru/brokentools-control-panel/issues) and include: your distribution and Plasma version, how you installed, and the output of `brokentools-control-panel --check`.
