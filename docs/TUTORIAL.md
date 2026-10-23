# Tutorial: from zero to your first launch

A step-by-step guide for people who are new to Linux, for example someone coming from Windows who misses the Control Panel. It takes about 10 minutes. You only need a CachyOS (or other Arch-based) system with the KDE Plasma desktop and an internet connection.

For the short reference version, see the [installation manual](INSTALL.md).

**Contents**

1. [Open a terminal](#step-1-open-a-terminal)
2. [Update your system (recommended)](#step-2-update-your-system-recommended)
3. [Install the requirements](#step-3-install-the-requirements)
4. [Get the program](#step-4-get-the-program)
5. [Install it](#step-5-install-it)
6. [Start it](#step-6-start-it)
7. [A short tour](#step-7-a-short-tour)
8. [What the categories mean](#what-the-categories-mean)
9. [Save power with one click](#step-8-save-power-with-one-click)
10. [Why is an item missing?](#step-9-why-is-an-item-missing)
11. [Ask for help the smart way](#step-10-ask-for-help-the-smart-way)
12. [Add your own item](#step-11-optional-add-your-own-item)
13. [Remove it](#remove-it)

---

## Step 1: Open a terminal

The terminal is the text window where you type commands. In KDE it is called **Konsole**.

Press the Start key, type `konsole` and press Enter. (On many systems `Ctrl`+`Alt`+`T` also works.)

You will see a line ending in `$` or `>`. That is where you type. After typing a command, press **Enter** to run it.

## Step 2: Update your system (recommended)

Arch-based systems are *rolling release*: you always update everything together.

```bash
sudo pacman -Syu
```

- `sudo` means "run this as administrator". It asks for your password. **Nothing appears while you type the password**, this is normal.
- `pacman` is the package manager (like Windows Update and "Programs and Features" in one).
- `-Syu` means "refresh the lists and upgrade everything".
- When it asks `Proceed with installation? [Y/n]`, press Enter to accept.

If you are in a hurry you can skip this step. Never use the shorter `sudo pacman -Sy something` form; on Arch it can leave your system half-updated.

## Step 3: Install the requirements

```bash
sudo pacman -S --needed python python-pyqt6 kde-cli-tools systemsettings konsole
```

`--needed` means "skip what I already have", so it is safe to run even if everything is installed. Typical results: *"there is nothing to do"* or a short list of small packages.

What these are: `python` runs the program, `python-pyqt6` draws its window, `kde-cli-tools` lets it open KDE's settings pages, `systemsettings` is KDE's own settings app, and `konsole` is the terminal it uses for commands.

## Step 4: Get the program

**Option 1: download the release archive (no extra tools needed)**

1. Open the [Releases page](https://github.com/UnscrewGuru/brokentools-control-panel/releases) and download `brokentools-control-panel-1.0.0.tar.gz` and its `.sha256` file into your **Downloads** folder.
2. In the terminal, go there and check the download is intact:

   ```bash
   cd ~/Downloads
   sha256sum -c brokentools-control-panel-1.0.0.tar.gz.sha256
   ```

   Expected: `brokentools-control-panel-1.0.0.tar.gz: OK`
3. Extract it:

   ```bash
   tar xzf brokentools-control-panel-1.0.0.tar.gz
   cd brokentools-control-panel-1.0.0
   ```

**Option 2: use git**

```bash
sudo pacman -S --needed git
git clone https://github.com/UnscrewGuru/brokentools-control-panel.git
cd brokentools-control-panel
```

Either way, you should now be inside the project folder. Check with `ls`: you should see `install.sh`, `README.md`, `src` and other files.

## Step 5: Install it

```bash
bash install.sh
```

Expected result:

```
Installing BrokenTools Control Panel...

Done. Search for "BrokenTools Control Panel" in the application menu,
or run:  /home/<you>/.local/bin/brokentools-control-panel
```

This installs for **your user only**. It does not use `sudo` and does not touch system files. If it complains that something is missing, install what it names (usually `python-pyqt6`) and run it again.

## Step 6: Start it

Press the Start key and type **BrokenTools Control Panel**. Click the result. If the entry does not appear yet, log out and in once, or run `kbuildsycoca6` in the terminal.

You can also start it from a terminal with `~/.local/bin/brokentools-control-panel`.

## Step 7: A short tour

When it opens you see **categories**, like the Windows 7 Control Panel. Each category shows its name and three quick links.

- **Click a category name** to see all its items with a description.
- **Click an item** to use it. Three things can happen:
  1. **A KDE settings page opens** (for example Display, Sound, Network).
  2. **A program opens** (for example System Monitor, Partition Manager).
  3. **A terminal opens** and runs a command, for example the list of recent system errors. The terminal stays open until you press **Enter**, so you can read the result. Some items first ask you to type something, such as a package name to search for.
- **Search**: press `Ctrl`+`F` and type a word (in English or Greek, for example `pacman`, `kernel`, `bluetooth`).
- **Back** (`Alt`+`Left`) and **Home** are in the top-left corner.
- **Language**: the *Language* box at the top right switches between Automatic (follows your system), English and Ελληνικά. The window rebuilds at once and remembers the choice.
- **View by**: switch between *Category* and *Large icons* (every item in one grid) at the top right. The program remembers your choice.

Items that change the system (installing or removing a package, updating) always run in the terminal where you can see the command, and ask for your `sudo` password. Hover over any item to read what it does.

### What the categories mean

The names below are the English ones; in Greek mode each has the Greek name shown in the first column.

| Category (Greek) | Category (English) | Typical items |
| --- | --- | --- |
| Σύστημα και ασφάλεια | System and security | system update, error logs, services, firewall, users |
| Προγράμματα | Programs | search / install / remove packages, default apps, startup programs |
| Εμφάνιση και εξατομίκευση | Appearance and personalization | theme, colours, fonts, icons, wallpaper, lock screen |
| Υλικό και ήχος | Hardware and sound | display, sound, keyboard, mouse, Bluetooth, disks |
| Δίκτυο και διαδίκτυο | Network and internet | connections, proxy, IP info, ping, open ports |
| Ρολόι, γλώσσα και περιοχή | Clock, language and region | date and time, language and formats, spell check |
| Συμπεριφορά και πρόσβαση | Behavior and accessibility | shortcuts, window behaviour, virtual desktops, notifications |
| Πληροφορίες και εργαλεία συστήματος | System information and tools | hardware info, task manager, `inxi`, temperatures, disk usage |
| Ενέργεια και απόδοση | Power and performance | power profiles, sleep and screen-off timers, GPU power |
| CachyOS | CachyOS tools | Hello, Kernel Manager, mirrors, running kernel |

## Step 8: Save power with one click

Open **Power and performance** (Greek: Ενέργεια και απόδοση). At the top you see three buttons:

| Button (English / Greek) | Use it when |
| --- | --- |
| Power saver / Εξοικονόμηση ενέργειας | idle, browsing, light work, saving electricity |
| Balanced / Ισορροπημένο | normal use (default) |
| Performance / Υψηλή απόδοση | games, rendering, compiling |

The line below shows live information: the CPU driver, the energy preference (EPP) and the current clock speed. Switch to *Power saver* and watch the clock drop when the computer is idle.

If the buttons are missing, install and start the service:

```bash
sudo pacman -S power-profiles-daemon
sudo systemctl enable --now power-profiles-daemon
```

On a desktop PC the profile mostly changes how aggressively the CPU boosts. Larger savings usually come from the **sleep and screen-off timers** (item *Power management*) and from the graphics card (item *AMD graphics card (LACT)*, which can lower its power limit; install with `sudo pacman -S lact`).

## Step 9: Why is an item missing?

The Control Panel hides items that cannot work on your computer, for example "CachyOS Package Installer" if that program is not installed. To see exactly what is hidden and why:

```bash
brokentools-control-panel --check
```

Example lines:

```
  [shown]   System errors (logs)
  [hidden]  AMD graphics card (LACT)  ->  program lact not found
```

To make a hidden item appear, install the missing program (see [optional packages](INSTALL.md#optional-packages)).

## Step 10: Ask for help the smart way

When something is wrong and you ask on a forum, a chat, or an AI assistant, the first thing people need is your system information and the latest errors. Open **System information and tools** and click **Copy info for help** (Greek: Αντιγραφή πληροφοριών για βοήθεια). A message confirms how many lines were copied. Paste them (`Ctrl`+`V`) into your question together with a description of the problem. This needs the `inxi` package (`sudo pacman -S inxi`).

## Step 11 (optional): Add your own item

All items live in one file: `src/brokentools_control_panel/catalog.py`. There are four kinds:

```python
# 1. Open a KDE settings page. The id comes from:  kcmshell6 --list
K("Night Light", "Screen colour by time of day", ["preferences-system-night-light"], "kcm_nighttime"),

# 2. Start a program
A("Filelight", "What uses my disk space", ["filelight"], "filelight"),

# 3. Run a command in a terminal (last argument: commands that must exist)
T("Failed services", "Services that did not start", ["dialog-warning"], "systemctl --failed", ["systemctl"]),

# 4. Ask for text first, then run a command ({} is replaced by what you typed)
Q("Search package", "Search the repositories", ["edit-find"], "Search", "Name:", "pacman -Ss {}", ["pacman"]),
```

Add your line inside a category's `"items": [ ... ]`, then install again (`bash install.sh` from the project folder) so your change is copied to the installed program. Test without installing with:

```bash
env PYTHONPATH=src python3 -m brokentools_control_panel --check
```

Icon names (the list in square brackets) are standard freedesktop icon names; the first one that exists in your icon theme is used.

## Remove it

```bash
bash ~/.local/share/brokentools-control-panel/uninstall.sh
```

This removes only the files the installer created. Add `--purge` to also delete the saved settings.

---

Something did not work as described? See [Troubleshooting](INSTALL.md#troubleshooting) or open an [issue](https://github.com/UnscrewGuru/brokentools-control-panel/issues) with the output of `brokentools-control-panel --check`.
