# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""English texts for the catalogue.

The catalogue (catalog.py) is written with Greek names and descriptions. Each entry here maps the
Greek name to its English version, so the key of every entry is the exact Greek name used in
catalog.py. The unit tests fail if an item or category has no English entry (or an entry is stale).

When you add an item to catalog.py, add its English text here too.
"""

CATEGORY_NAMES_EN = {
    "Σύστημα και ασφάλεια": "System and security",
    "Προγράμματα": "Programs",
    "Εμφάνιση και εξατομίκευση": "Appearance and personalization",
    "Υλικό και ήχος": "Hardware and sound",
    "Δίκτυο και διαδίκτυο": "Network and internet",
    "Ρολόι, γλώσσα και περιοχή": "Clock, language and region",
    "Συμπεριφορά και πρόσβαση": "Behavior and accessibility",
    "Πληροφορίες και εργαλεία συστήματος": "System information and tools",
    "Ενέργεια και απόδοση": "Power and performance",
    "CachyOS": "CachyOS",
}

# Greek item name -> (English name, English description)
ITEMS_EN = {
    # --- System and security
    "Ενημέρωση συστήματος": ("System update", "Downloads and installs all updates (pacman -Syu)"),
    "Σφάλματα συστήματος (logs)": ("System errors (logs)", "Errors from the current boot, like the Windows Event Viewer (journalctl)"),
    "Μηνύματα πυρήνα και drivers": ("Kernel and driver messages", "Kernel warnings about hardware and drivers"),
    "Υπηρεσίες που τρέχουν": ("Running services", "Active systemd services, like Services.msc"),
    "Υπηρεσίες με σφάλμα": ("Failed services", "What failed to start (systemctl --failed)"),
    "Χρόνος εκκίνησης": ("Boot time", "How long the boot took and which services slowed it down"),
    "Χρήστες και λογαριασμοί": ("Users and accounts", "Add users, change passwords and manage accounts"),
    "Τείχος προστασίας": ("Firewall", "Rules for incoming and outgoing network connections"),
    "Πορτοφόλι κωδικών (KWallet)": ("Password wallet (KWallet)", "Saved passwords and keys of your applications"),
    "Λογαριασμοί διαδικτύου": ("Online accounts", "Google, Nextcloud and other accounts for KDE applications"),
    "Υπηρεσίες παρασκηνίου (KDE)": ("Background services (KDE)", "The KDE background services (kded)"),
    "Ασφάλεια υλικολογισμικού": ("Firmware security", "UEFI/firmware security information (view only)"),
    "Αντίγραφα ασφαλείας και snapshots": ("Backups and snapshots", "System restore with Btrfs snapshots (Btrfs Assistant)"),
    # --- Programs
    "Εφαρμογές (Discover)": ("Applications (Discover)", "Graphical way to install and update programs"),
    "Αναζήτηση πακέτου": ("Search packages", "Searches the repositories for packages (pacman -Ss)"),
    "Εγκατάσταση πακέτου": ("Install package", "Installs a package (pacman -S)"),
    "Απεγκατάσταση πακέτου": ("Remove package", "Removes a package and its unused dependencies (pacman -Rns)"),
    "Πληροφορίες πακέτου": ("Package information", "Version, size and dependencies of an installed package (pacman -Qi)"),
    "Εγκατεστημένα πακέτα": ("Installed packages", "The packages you installed yourself (pacman -Qe)"),
    "Ορφανά πακέτα": ("Orphaned packages", "Packages that no other package needs any more (view only)"),
    "Προεπιλεγμένες εφαρμογές": ("Default applications", "Which program opens the browser, email, files and terminal"),
    "Συσχετίσεις αρχείων": ("File associations", "Which program opens each file type"),
    "Προγράμματα με την εκκίνηση": ("Startup programs", "What starts automatically when you log in"),
    "Δικαιώματα Flatpak": ("Flatpak permissions", "Access permissions of Flatpak applications"),
    # --- Appearance and personalization
    "Γενικό θέμα": ("Global theme", "Complete look and feel (Breeze, dark, light and more)"),
    "Χρώματα": ("Colors", "Color scheme of the applications"),
    "Γραμματοσειρές": ("Fonts", "Fonts and text smoothing"),
    "Εικονίδια": ("Icons", "Icon theme"),
    "Στυλ εφαρμογών": ("Application style", "Look of buttons and widgets in applications"),
    "Εφαρμογές GTK": ("GTK applications", "Look of GTK applications (Firefox, GIMP and others)"),
    "Στυλ Plasma": ("Plasma style", "Look of the panel, menus and widgets"),
    "Δρομέας ποντικιού": ("Mouse cursor", "Cursor theme and size"),
    "Διακοσμήσεις παραθύρων": ("Window decorations", "Titlebars and window buttons"),
    "Εφέ επιφάνειας εργασίας": ("Desktop effects", "Animations, transparency and KWin effects"),
    "Οθόνη εκκίνησης (splash)": ("Splash screen", "The image shown while the desktop loads"),
    "Οθόνη κλειδώματος": ("Lock screen", "Behavior and look of the lock screen"),
    "Οθόνη σύνδεσης": ("Login screen", "Theme of the login screen"),
    "Φόντο επιφάνειας εργασίας": ("Desktop wallpaper", "Wallpaper and slideshow"),
    "Animations": ("Animations", "Speed and style of animations"),
    "Οθόνη εκκίνησης συστήματος (Plymouth)": ("Boot splash (Plymouth)", "The image shown while the computer starts"),
    "Εγκατάσταση γραμματοσειρών": ("Install fonts", "Add, preview and manage fonts"),
    "Ήχοι ειδοποιήσεων": ("Notification sounds", "The system sound theme"),
    # --- Hardware and sound
    "Οθόνη και προβολή": ("Display", "Resolution, refresh rate, scale and multiple monitors"),
    "Νυχτερινό φως": ("Night Light", "Screen color temperature at night"),
    "Ήχος": ("Sound", "Output and input devices, volume"),
    "Ανάμειξη ήχου (pavucontrol)": ("Audio mixer (pavucontrol)", "Detailed per-application volume control"),
    "Πληκτρολόγιο": ("Keyboard", "Layout (Greek/English), repeat rate, shortcuts"),
    "Ποντίκι": ("Mouse", "Speed, acceleration and buttons"),
    "Touchpad": ("Touchpad", "Touchpad settings (laptop)"),
    "Εκτυπωτές": ("Printers", "Add and manage printers"),
    "Bluetooth": ("Bluetooth", "Bluetooth devices"),
    "Χειριστήρια παιχνιδιών": ("Game controllers", "Gamepad and joystick"),
    "Tablet γραφικών": ("Graphics tablet", "Tablet and pen settings"),
    "Οθόνη αφής": ("Touchscreen", "Touchscreen settings"),
    "Αυτόματη προσάρτηση δίσκων": ("Automatic disk mounting", "What happens when you plug in a disk or USB drive"),
    "Ενέργειες συσκευών": ("Device actions", "Which programs are offered when you connect a new device"),
    "Thunderbolt": ("Thunderbolt", "Manage Thunderbolt devices"),
    "Διαχείριση δίσκων (Partition Manager)": ("Disk management (Partition Manager)", "Create, resize and format partitions"),
    # --- Network and internet
    "Συνδέσεις δικτύου": ("Network connections", "Wi-Fi, Ethernet, VPN, IP addresses and DNS"),
    "Proxy": ("Proxy", "Proxy server settings"),
    "Κοινή χρήση φακέλων (Samba)": ("Folder sharing (Samba)", "Share folders on the local network"),
    "Απομακρυσμένη επιφάνεια εργασίας": ("Remote desktop", "Lets others connect to this computer through RDP"),
    "Συντομεύσεις αναζήτησης web": ("Web search shortcuts", "Shortcuts such as gg: in Dolphin and KRunner"),
    "Πληροφορίες δικτύου": ("Network information", "IP addresses and connection status"),
    "Έλεγχος σύνδεσης (ping)": ("Connection test (ping)", "Tests whether the internet is reachable"),
    "Ανοιχτές θύρες": ("Open ports", "Which ports the system is listening on (ss -tuln)"),
    # --- Clock, language and region
    "Ημερομηνία και ώρα": ("Date and time", "Time zone and automatic synchronization"),
    "Γλώσσα και μορφές": ("Language and formats", "System language, currency, dates and numbers"),
    "Ορθογραφικός έλεγχος": ("Spell checking", "Dictionaries and spelling options"),
    "Κατάσταση ώρας (timedatectl)": ("Time status (timedatectl)", "Time zone and NTP synchronization"),
    # --- Behavior and accessibility
    "Συντομεύσεις πληκτρολογίου": ("Keyboard shortcuts", "Global shortcuts and application shortcuts"),
    "Συμπεριφορά παραθύρων": ("Window behavior", "Focus, moving, maximizing and snapping"),
    "Κανόνες παραθύρων": ("Window rules", "Special per-application rules (position, size and more)"),
    "Εικονικές επιφάνειες εργασίας": ("Virtual desktops", "Number and layout of desktops"),
    "Εναλλαγή παραθύρων (Alt+Tab)": ("Window switching (Alt+Tab)", "Look and behavior of the task switcher"),
    "Άκρες οθόνης": ("Screen edges", "Actions when the pointer reaches a corner or an edge"),
    "Σενάρια KWin": ("KWin scripts", "Scripts for the window manager"),
    "Συμπεριφορά χώρου εργασίας": ("Workspace behavior", "Clicks, animations, tooltips and more"),
    "Αναζήτηση (KRunner)": ("Search (KRunner)", "Where the quick search looks (Alt+Space)"),
    "Αναζήτηση αρχείων (Baloo)": ("File search (Baloo)", "File indexing and excluded folders"),
    "Ειδοποιήσεις": ("Notifications", "Which applications send notifications, and how"),
    "Δραστηριότητες (Activities)": ("Activities", "Separate workspaces for different tasks"),
    "Πρόσβαση (accessibility)": ("Accessibility", "Aids for vision, hearing and typing"),
    "Εικονικό πληκτρολόγιο": ("Virtual keyboard", "On-screen keyboard"),
    "Εκκίνηση και αποσύνδεση": ("Session start and logout", "Session restore and shutdown confirmation"),
    "Τοποθεσίες προσωπικών αρχείων": ("Personal file locations", "Where Documents, Downloads and Desktop are"),
    "Ιστορικό δραστηριότητας αρχείων": ("File activity history", "What the system remembers about recent files"),
    "Όλες οι Ρυθμίσεις συστήματος (KDE)": ("All KDE System Settings", "Opens the complete KDE System Settings"),
    # --- System information and tools
    "Πληροφορίες υλικού (KInfoCenter)": ("Hardware information (KInfoCenter)", "CPU, GPU, RAM, disks, network and system information"),
    "Πληροφορίες συστήματος": ("System information", "Distribution, Plasma/Qt/kernel versions, processor and memory"),
    "Πληροφορίες επεξεργαστή": ("Processor information", "Detailed CPU information"),
    "Πληροφορίες μνήμης": ("Memory information", "RAM usage and details"),
    "Πληροφορίες Vulkan": ("Vulkan information", "Vulkan support and GPU details (useful for games)"),
    "Συσκευές USB": ("USB devices", "Which USB devices are connected"),
    "Αισθητήρες": ("Sensors", "Temperatures, fans and voltages (graphical)"),
    "Block devices": ("Block devices", "Disks and partitions as the system sees them"),
    "Διαχείριση εργασιών (System Monitor)": ("Task manager (System Monitor)", "Processes, CPU, memory and disk, like the Windows Task Manager"),
    "Σύνοψη υπολογιστή (inxi)": ("Computer summary (inxi)", "Full description of the hardware and system (inxi -Fxz)"),
    "Αντιγραφή πληροφοριών για βοήθεια (LLM)": ("Copy info for help", "Copies a system summary and the latest errors to the clipboard, ready to paste into a forum post or an AI assistant"),
    "Συσκευές PCI και drivers": ("PCI devices and drivers", "Which card uses which driver (lspci -k)"),
    "Κάρτα γραφικών": ("Graphics card", "GPU model and the driver it uses"),
    "Δίσκοι και partitions": ("Disks and partitions", "Disk layout and file systems (lsblk -f)"),
    "Ελεύθερος χώρος": ("Free space", "Space per partition (df -h)"),
    "Μνήμη RAM": ("Memory (RAM)", "Memory and swap usage (free -h)"),
    "Θερμοκρασίες": ("Temperatures", "Temperature and fan sensors (sensors)"),
    "Παρακολούθηση σε πραγματικό χρόνο (btop)": ("Live monitoring (btop)", "CPU, RAM, disks and network in a live view"),
    "Χρήση χώρου δίσκου (Filelight)": ("Disk usage (Filelight)", "A graphical view of what takes up space"),
    # --- Power and performance
    "Διαχείριση ενέργειας": ("Power management", "When the screen turns off, when the computer suspends, locking"),
    "Ρολόι επεξεργαστή (ζωντανά)": ("CPU clock (live)", "The MHz of every CPU core, refreshed every second"),
    "Ισχύς κάρτας γραφικών (W)": ("Graphics card power (W)", "How many watts the GPU draws right now (if the driver reports it)"),
    "Κάρτα γραφικών AMD (LACT)": ("AMD graphics card (LACT)", "Power limit, clocks and fans of the GPU"),
    "Τι καταναλώνει ενέργεια (powertop)": ("What uses power (powertop)", "Power consumption analysis and saving suggestions"),
    "Τεχνική κατάσταση προφίλ": ("Power profile details", "Current profile, CPU driver and energy preference (EPP)"),
    # --- CachyOS
    "CachyOS Hello": ("CachyOS Hello", "The welcome app with the basic settings of the distribution"),
    "CachyOS Kernel Manager": ("CachyOS Kernel Manager", "Install and switch kernels"),
    "CachyOS Package Installer": ("CachyOS Package Installer", "Ready-made sets of applications and settings from CachyOS"),
    "Βελτιστοποίηση mirrors": ("Optimize mirrors", "Picks the fastest mirrors for packages"),
    "Τρέχων πυρήνας": ("Running kernel", "Which kernel is running and which ones are installed"),
}

# Items that ask for text first: Greek item name -> (English dialog title, English prompt)
ASK_EN = {
    "Αναζήτηση πακέτου": ("Search packages", "Name or keyword:"),
    "Εγκατάσταση πακέτου": ("Install package", "Package name:"),
    "Απεγκατάσταση πακέτου": ("Remove package", "Package name:"),
    "Πληροφορίες πακέτου": ("Package information", "Package name:"),
}

# Greek text that appears inside shell commands (echo messages) -> English replacement
COMMAND_TEXT_EN = {
    "Δεν υπάρχουν ορφανά πακέτα.": "No orphaned packages.",
    "--- Σφάλματα της τρέχουσας εκκίνησης (journalctl) ---": "--- Errors from the current boot (journalctl) ---",
}
