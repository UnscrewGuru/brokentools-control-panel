# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""BrokenTools Control Panel - catalogue of items and the logic that checks and runs them.

No Qt dependency. Names and descriptions are written in Greek here; the English versions live in
translations.py (see i18n.py for the language handling).

Every item has one action:
  ("kcm", [ids])           open a KDE settings page with kcmshell6 (the first id that exists is used)
  ("app", [argv])          start a graphical program
  ("term", "command")      run a command in a terminal that stays open until Enter is pressed
  ("ask", title, prompt, "command with {}")   ask for text and put it (shell-quoted) into {}
  ("clip", "command")      run a command and copy its output to the clipboard
Items whose program or settings page does not exist on the system are hidden automatically.
"""
import glob
import shlex
import shutil
import subprocess

from . import i18n
from .i18n import tr
from . import translations


def _it(name, desc, icons, action, requires=()):
    return {"name": name, "desc": desc, "icons": list(icons),
            "action": action, "requires": list(requires), "resolved": None}


def K(name, desc, icons, ids):
    return _it(name, desc, icons, ("kcm", [ids] if isinstance(ids, str) else list(ids)))


def A(name, desc, icons, argv):
    return _it(name, desc, icons, ("app", [argv] if isinstance(argv, str) else list(argv)))


def T(name, desc, icons, cmd, requires=()):
    return _it(name, desc, icons, ("term", cmd), requires)


def Q(name, desc, icons, title, prompt, cmd, requires=()):
    return _it(name, desc, icons, ("ask", title, prompt, cmd), requires)


def C(name, desc, icons, cmd, requires=()):
    return _it(name, desc, icons, ("clip", cmd), requires)


CATEGORIES = [
    {
        "name": "Σύστημα και ασφάλεια",
        "icons": ["preferences-system", "security-high"],
        "items": [
            T("Ενημέρωση συστήματος", "Κατεβάζει και εγκαθιστά όλες τις ενημερώσεις (pacman -Syu)",
              ["system-software-update"], "sudo pacman -Syu", ["pacman"]),
            T("Σφάλματα συστήματος (logs)", "Τα σφάλματα της τρέχουσας εκκίνησης - σαν το Event Viewer (journalctl)",
              ["view-list-text", "text-x-log"], "journalctl -b -p err -e", ["journalctl"]),
            T("Μηνύματα πυρήνα και drivers", "Προειδοποιήσεις του kernel για υλικό και drivers",
              ["utilities-log-viewer", "view-list-text"], "journalctl -k -b -p warning -e", ["journalctl"]),
            T("Υπηρεσίες που τρέχουν", "Ενεργές υπηρεσίες systemd - σαν το Services.msc",
              ["preferences-system-services", "system-run"],
              "systemctl list-units --type=service --state=running", ["systemctl"]),
            T("Υπηρεσίες με σφάλμα", "Τι απέτυχε να ξεκινήσει (systemctl --failed)",
              ["dialog-warning"], "systemctl --failed", ["systemctl"]),
            T("Χρόνος εκκίνησης", "Πόσο κράτησε η εκκίνηση και ποιες υπηρεσίες την καθυστέρησαν",
              ["chronometer", "preferences-system-time"],
              "systemd-analyze; echo; systemd-analyze blame | head -n 20", ["systemd-analyze"]),
            K("Χρήστες και λογαριασμοί", "Προσθήκη, αλλαγή κωδικού και διαχείριση χρηστών",
              ["system-users", "preferences-system-users"], "kcm_users"),
            K("Τείχος προστασίας", "Κανόνες δικτύου εισερχομένων και εξερχομένων συνδέσεων",
              ["security-high", "preferences-system-firewall"], "kcm_firewall"),
            K("Πορτοφόλι κωδικών (KWallet)", "Αποθηκευμένοι κωδικοί και κλειδιά των εφαρμογών",
              ["kwalletmanager", "wallet-open"], "kcm_kwallet5"),
            K("Λογαριασμοί διαδικτύου", "Google, Nextcloud και άλλοι λογαριασμοί για τις εφαρμογές KDE",
              ["preferences-system-users", "internet-mail"], "kcm_kaccounts"),
            K("Υπηρεσίες παρασκηνίου (KDE)", "Οι background υπηρεσίες του KDE (kded)",
              ["preferences-system-services", "system-run"], "kcm_kded"),
            K("Ασφάλεια υλικολογισμικού", "Πληροφορίες ασφάλειας UEFI/firmware (μόνο προβολή)",
              ["security-medium", "computer"], "kcm_firmware_security"),
            A("Αντίγραφα ασφαλείας και snapshots", "Επαναφορά συστήματος με btrfs snapshots (Btrfs Assistant)",
              ["document-revert", "drive-harddisk"], "btrfs-assistant"),
        ],
    },
    {
        "name": "Προγράμματα",
        "icons": ["applications-all", "preferences-desktop-default-applications"],
        "items": [
            A("Εφαρμογές (Discover)", "Γραφικός τρόπος εγκατάστασης και ενημέρωσης προγραμμάτων",
              ["plasmadiscover", "system-software-install"], "plasma-discover"),
            Q("Αναζήτηση πακέτου", "Ψάχνει πακέτα στα αποθετήρια (pacman -Ss)",
              ["edit-find", "system-search"], "Αναζήτηση πακέτου", "Όνομα ή λέξη-κλειδί:",
              "pacman -Ss {}", ["pacman"]),
            Q("Εγκατάσταση πακέτου", "Εγκαθιστά πακέτο (pacman -S)",
              ["list-add", "system-software-install"], "Εγκατάσταση πακέτου", "Όνομα πακέτου:",
              "sudo pacman -S {}", ["pacman"]),
            Q("Απεγκατάσταση πακέτου", "Αφαιρεί πακέτο και τις άχρηστες εξαρτήσεις του (pacman -Rns)",
              ["list-remove", "edit-delete"], "Απεγκατάσταση πακέτου", "Όνομα πακέτου:",
              "sudo pacman -Rns {}", ["pacman"]),
            Q("Πληροφορίες πακέτου", "Έκδοση, μέγεθος και εξαρτήσεις εγκατεστημένου πακέτου (pacman -Qi)",
              ["help-about", "dialog-information"], "Πληροφορίες πακέτου", "Όνομα πακέτου:",
              "pacman -Qi {}", ["pacman"]),
            T("Εγκατεστημένα πακέτα", "Τα πακέτα που εγκατέστησες εσύ (pacman -Qe)",
              ["view-list-details", "applications-all"], "pacman -Qe | less", ["pacman", "less"]),
            T("Ορφανά πακέτα", "Πακέτα που δεν χρειάζεται πια κανένα άλλο (μόνο προβολή)",
              ["edit-clear-history", "dialog-information"],
              "pacman -Qtdq || echo 'Δεν υπάρχουν ορφανά πακέτα.'", ["pacman"]),
            K("Προεπιλεγμένες εφαρμογές", "Ποιο πρόγραμμα ανοίγει browser, email, αρχεία, terminal",
              ["preferences-desktop-default-applications", "application-x-executable"], "kcm_componentchooser"),
            K("Συσχετίσεις αρχείων", "Ποιο πρόγραμμα ανοίγει κάθε τύπο αρχείου",
              ["preferences-desktop-filetype-association", "document-open"], "kcm_filetypes"),
            K("Προγράμματα με την εκκίνηση", "Τι ξεκινά αυτόματα όταν μπεις στο σύστημα",
              ["system-run", "preferences-system-session-services"], "kcm_autostart"),
            K("Δικαιώματα Flatpak", "Δικαιώματα πρόσβασης των Flatpak εφαρμογών",
              ["flatpak-discover", "preferences-system-privacy"], "kcm_flatpak"),
        ],
    },
    {
        "name": "Εμφάνιση και εξατομίκευση",
        "icons": ["preferences-desktop-theme-global", "preferences-desktop-theme"],
        "items": [
            K("Γενικό θέμα", "Πλήρες look & feel (Breeze, σκούρο, ανοιχτό κ.ά.)",
              ["preferences-desktop-theme-global", "preferences-desktop-theme"], "kcm_lookandfeel"),
            K("Χρώματα", "Χρωματικό σχήμα εφαρμογών",
              ["preferences-desktop-color"], "kcm_colors"),
            K("Γραμματοσειρές", "Γραμματοσειρές και εξομάλυνση κειμένου",
              ["preferences-desktop-font"], "kcm_fonts"),
            K("Εικονίδια", "Θέμα εικονιδίων",
              ["preferences-desktop-icons"], "kcm_icons"),
            K("Στυλ εφαρμογών", "Εμφάνιση κουμπιών και στοιχείων των εφαρμογών",
              ["preferences-desktop-theme-applications", "preferences-desktop-theme"], "kcm_style"),
            K("Εφαρμογές GTK", "Εμφάνιση των GTK εφαρμογών (Firefox, GIMP κ.ά.)",
              ["gtk-3", "preferences-desktop-theme-applications"], "kcm_gtk"),
            K("Στυλ Plasma", "Εμφάνιση του πάνελ, των μενού και των widgets",
              ["preferences-desktop-plasma-theme", "preferences-desktop-theme"], ["kcm_desktoptheme", "kcm_plasmatheme"]),
            K("Δρομέας ποντικιού", "Θέμα και μέγεθος του δρομέα",
              ["preferences-cursors", "input-mouse"], "kcm_cursortheme"),
            K("Διακοσμήσεις παραθύρων", "Τίτλοι και κουμπιά των παραθύρων",
              ["preferences-system-windows"], ["kcm_kwindecoration", "kwindecoration"]),
            K("Εφέ επιφάνειας εργασίας", "Animations, διαφάνειες και εφέ του KWin",
              ["preferences-desktop-effects", "preferences-system-windows-effects"], "kcm_kwin_effects"),
            K("Οθόνη εκκίνησης (splash)", "Η εικόνα που φαίνεται καθώς φορτώνει η επιφάνεια εργασίας",
              ["preferences-desktop-launch-feedback", "preferences-system-splash"], "kcm_splashscreen"),
            K("Οθόνη κλειδώματος", "Συμπεριφορά και εμφάνιση του κλειδώματος",
              ["preferences-desktop-user-password", "system-lock-screen"], "kcm_screenlocker"),
            K("Οθόνη σύνδεσης", "Θέμα της οθόνης εισόδου",
              ["preferences-system-login", "system-log-out"], ["kcm_plasmalogin", "kcm_sddm"]),
            K("Φόντο επιφάνειας εργασίας", "Ταπετσαρία και slideshow",
              ["preferences-desktop-wallpaper", "image-x-generic"], "kcm_wallpaper"),
            K("Animations", "Ταχύτητα και στυλ των animations",
              ["preferences-desktop-effects", "media-playback-start"], "kcm_animations"),
            K("Οθόνη εκκίνησης συστήματος (Plymouth)", "Η εικόνα που φαίνεται κατά την εκκίνηση του υπολογιστή",
              ["preferences-system-startup", "preferences-desktop-boot"], "kcm_plymouth"),
            K("Εγκατάσταση γραμματοσειρών", "Προσθήκη, προεπισκόπηση και διαχείριση fonts",
              ["preferences-desktop-font", "font-x-generic"], "kcm_fontinst"),
            K("Ήχοι ειδοποιήσεων", "Θέμα ήχων του συστήματος",
              ["preferences-desktop-sound", "audio-volume-medium"], "kcm_soundtheme"),
        ],
    },
    {
        "name": "Υλικό και ήχος",
        "icons": ["preferences-desktop-peripherals", "computer"],
        "items": [
            K("Οθόνη και προβολή", "Ανάλυση, ρυθμός ανανέωσης, κλίμακα, πολλαπλές οθόνες",
              ["preferences-desktop-display", "video-display"], "kcm_kscreen"),
            K("Νυχτερινό φως", "Θερμοκρασία χρώματος οθόνης τη νύχτα",
              ["preferences-system-night-light", "redshift"], ["kcm_nighttime", "kcm_nightlight"]),
            K("Ήχος", "Συσκευές εξόδου και εισόδου, ένταση",
              ["preferences-desktop-sound", "audio-card"], "kcm_pulseaudio"),
            A("Ανάμειξη ήχου (pavucontrol)", "Αναλυτικός έλεγχος έντασης ανά εφαρμογή",
              ["multimedia-volume-control", "audio-volume-high"], "pavucontrol"),
            K("Πληκτρολόγιο", "Διάταξη (Ελληνικά/English), ταχύτητα επανάληψης, συντομεύσεις",
              ["preferences-desktop-keyboard", "input-keyboard"], "kcm_keyboard"),
            K("Ποντίκι", "Ταχύτητα, επιτάχυνση, κουμπιά",
              ["input-mouse", "preferences-desktop-mouse"], "kcm_mouse"),
            K("Touchpad", "Ρυθμίσεις touchpad (laptop)",
              ["input-touchpad", "preferences-desktop-touchpad"], "kcm_touchpad"),
            K("Εκτυπωτές", "Προσθήκη και διαχείριση εκτυπωτών",
              ["printer", "preferences-devices-printer"], "kcm_printer_manager"),
            K("Bluetooth", "Συσκευές Bluetooth",
              ["preferences-system-bluetooth", "bluetooth"], "kcm_bluetooth"),
            K("Χειριστήρια παιχνιδιών", "Gamepad και joystick",
              ["input-gamepad", "preferences-desktop-gaming"], "kcm_gamecontroller"),
            K("Tablet γραφικών", "Ρυθμίσεις tablet και στυλό",
              ["input-tablet", "preferences-desktop-tablet"], "kcm_tablet"),
            K("Οθόνη αφής", "Ρυθμίσεις touchscreen",
              ["input-touchscreen", "preferences-desktop-touchscreen"], "kcm_touchscreen"),
            K("Αυτόματη προσάρτηση δίσκων", "Τι γίνεται όταν συνδέεις δίσκο ή USB",
              ["drive-removable-media", "drive-harddisk"], "kcm_device_automounter"),
            K("Ενέργειες συσκευών", "Ποια προγράμματα προτείνονται όταν συνδέεις νέα συσκευή",
              ["preferences-desktop-peripherals", "drive-removable-media-usb"], "kcm_solid_actions"),
            K("Thunderbolt", "Διαχείριση συσκευών Thunderbolt",
              ["thunderbolt", "preferences-desktop-peripherals"], "kcm_bolt"),
            A("Διαχείριση δίσκων (Partition Manager)", "Δημιουργία, αλλαγή μεγέθους και μορφοποίηση partitions",
              ["partitionmanager", "drive-harddisk"], "partitionmanager"),
        ],
    },
    {
        "name": "Δίκτυο και διαδίκτυο",
        "icons": ["preferences-system-network", "network-wired"],
        "items": [
            K("Συνδέσεις δικτύου", "Wi-Fi, Ethernet, VPN, διευθύνσεις IP και DNS",
              ["preferences-system-network", "network-wireless"], "kcm_networkmanagement"),
            K("Proxy", "Ρυθμίσεις διαμεσολαβητή",
              ["preferences-system-network-proxy", "preferences-system-network"], ["kcm_proxy", "proxy"]),
            K("Κοινή χρήση φακέλων (Samba)", "Μοίρασμα φακέλων σε τοπικό δίκτυο",
              ["preferences-system-network-share", "folder-remote"], "kcm_sambashare"),
            K("Απομακρυσμένη επιφάνεια εργασίας", "Επιτρέπει σύνδεση στον υπολογιστή σου μέσω RDP",
              ["krdc", "preferences-desktop-remote-desktop"], "kcm_krdpserver"),
            K("Συντομεύσεις αναζήτησης web", "Συντομεύσεις τύπου gg: στο Dolphin και στο KRunner",
              ["preferences-web-browser-shortcuts", "internet-web-browser"], ["kcm_webshortcuts", "webshortcuts"]),
            T("Πληροφορίες δικτύου", "Διευθύνσεις IP και κατάσταση συνδέσεων",
              ["network-wired", "network-workgroup"], "ip -br addr; echo; nmcli device status", ["ip", "nmcli"]),
            T("Έλεγχος σύνδεσης (ping)", "Δοκιμάζει αν υπάρχει πρόσβαση στο διαδίκτυο",
              ["network-connect", "network-wired"], "ping -c 4 archlinux.org", ["ping"]),
            T("Ανοιχτές θύρες", "Ποιες θύρες ακούει το σύστημα (ss -tuln)",
              ["security-medium", "network-server"], "ss -tuln", ["ss"]),
        ],
    },
    {
        "name": "Ρολόι, γλώσσα και περιοχή",
        "icons": ["preferences-system-time", "preferences-desktop-locale"],
        "items": [
            K("Ημερομηνία και ώρα", "Ζώνη ώρας, αυτόματος συγχρονισμός",
              ["preferences-system-time", "clock"], "kcm_clock"),
            K("Γλώσσα και μορφές", "Γλώσσα συστήματος, νόμισμα, ημερομηνίες, αριθμοί",
              ["preferences-desktop-locale", "preferences-desktop-language"], "kcm_regionandlang"),
            K("Ορθογραφικός έλεγχος", "Λεξικά και ρυθμίσεις ορθογραφίας",
              ["tools-check-spelling", "preferences-desktop-spell-checker"], "kcm_spellchecking"),
            T("Κατάσταση ώρας (timedatectl)", "Ζώνη ώρας και συγχρονισμός NTP",
              ["preferences-system-time", "clock"], "timedatectl status", ["timedatectl"]),
        ],
    },
    {
        "name": "Συμπεριφορά και πρόσβαση",
        "icons": ["preferences-desktop-accessibility", "preferences-system-windows"],
        "items": [
            K("Συντομεύσεις πληκτρολογίου", "Global συντομεύσεις και συντομεύσεις εφαρμογών",
              ["preferences-desktop-keyboard-shortcut", "input-keyboard"], "kcm_keys"),
            K("Συμπεριφορά παραθύρων", "Focus, μετακίνηση, μεγέθυνση, snapping",
              ["preferences-system-windows-behavior", "preferences-system-windows"], "kcm_kwinoptions"),
            K("Κανόνες παραθύρων", "Ειδικοί κανόνες ανά εφαρμογή (θέση, μέγεθος κ.ά.)",
              ["preferences-system-windows-actions", "preferences-system-windows"], "kcm_kwinrules"),
            K("Εικονικές επιφάνειες εργασίας", "Πλήθος και διάταξη desktops",
              ["preferences-desktop", "view-grid"], "kcm_kwin_virtualdesktops"),
            K("Εναλλαγή παραθύρων (Alt+Tab)", "Εμφάνιση και λειτουργία του task switcher",
              ["preferences-system-tabbox", "preferences-system-windows"], "kcm_kwintabbox"),
            K("Άκρες οθόνης", "Ενέργειες όταν ο δείκτης πηγαίνει σε γωνία",
              ["preferences-desktop-edges", "preferences-system-windows"], "kcm_kwinscreenedges"),
            K("Σενάρια KWin", "Scripts για τον window manager",
              ["preferences-system-windows-script", "text-x-script"], "kcm_kwin_scripts"),
            K("Συμπεριφορά χώρου εργασίας", "Κλικ, animations, tooltips και άλλα",
              ["preferences-desktop-plasma", "preferences-system"], "kcm_workspace"),
            K("Αναζήτηση (KRunner)", "Πού ψάχνει η γρήγορη αναζήτηση (Alt+Space)",
              ["krunner", "system-search"], "kcm_plasmasearch"),
            K("Αναζήτηση αρχείων (Baloo)", "Ευρετηρίαση αρχείων και φάκελοι που εξαιρούνται",
              ["preferences-system-search", "system-search"], "kcm_baloofile"),
            K("Ειδοποιήσεις", "Ποιες εφαρμογές στέλνουν ειδοποιήσεις και πώς",
              ["preferences-desktop-notification", "notifications"], "kcm_notifications"),
            K("Δραστηριότητες (Activities)", "Ξεχωριστοί χώροι εργασίας",
              ["preferences-desktop-activities", "activities"], "kcm_activities"),
            K("Πρόσβαση (accessibility)", "Βοηθήματα για όραση, ακοή και πληκτρολόγηση",
              ["preferences-desktop-accessibility", "accessibility"], "kcm_access"),
            K("Εικονικό πληκτρολόγιο", "On-screen πληκτρολόγιο",
              ["input-keyboard-virtual", "input-keyboard"], "kcm_virtualkeyboard"),
            K("Εκκίνηση και αποσύνδεση", "Αποκατάσταση συνεδρίας, επιβεβαίωση τερματισμού",
              ["system-log-out", "preferences-system-session-services"], "kcm_smserver"),
            K("Τοποθεσίες προσωπικών αρχείων", "Πού είναι τα Έγγραφα, οι Λήψεις, η Επιφάνεια εργασίας",
              ["folder-documents", "folder"], "kcm_desktoppaths"),
            K("Ιστορικό δραστηριότητας αρχείων", "Τι θυμάται το σύστημα για τα πρόσφατα αρχεία",
              ["document-open-recent", "view-history"], "kcm_recentFiles"),
            A("Όλες οι Ρυθμίσεις συστήματος (KDE)", "Ανοίγει ολόκληρο το System Settings του KDE",
              ["preferences-system", "systemsettings"], "systemsettings"),
        ],
    },
    {
        "name": "Πληροφορίες και εργαλεία συστήματος",
        "icons": ["utilities-system-monitor", "help-about"],
        "items": [
            A("Πληροφορίες υλικού (KInfoCenter)", "CPU, GPU, RAM, δίσκοι, δίκτυο, πληροφορίες συστήματος",
              ["hwinfo", "help-about"], "kinfocenter"),
            K("Πληροφορίες συστήματος", "Διανομή, έκδοση Plasma/Qt/kernel, επεξεργαστής και μνήμη",
              ["help-about", "computer"], "kcm_about-distro"),
            K("Πληροφορίες επεξεργαστή", "Αναλυτικά στοιχεία του CPU",
              ["cpu", "computer"], "kcm_cpu"),
            K("Πληροφορίες μνήμης", "Χρήση και στοιχεία της μνήμης RAM",
              ["media-memory", "computer"], "kcm_memory"),
            K("Πληροφορίες Vulkan", "Υποστήριξη Vulkan και στοιχεία της GPU (χρήσιμο για παιχνίδια)",
              ["video-card", "computer"], "kcm_vulkan"),
            K("Συσκευές USB", "Ποιες συσκευές USB είναι συνδεδεμένες",
              ["drive-removable-media-usb", "computer"], "kcm_usb"),
            K("Αισθητήρες", "Θερμοκρασίες, ανεμιστήρες, τάσεις (γραφικά)",
              ["temperature-normal", "sensors-temperature"], "kcm_sensors"),
            K("Block devices", "Δίσκοι και partitions όπως τα βλέπει το σύστημα",
              ["drive-harddisk", "drive-partition"], "kcm_block_devices"),
            A("Διαχείριση εργασιών (System Monitor)", "Διεργασίες, CPU, μνήμη, δίσκος - σαν το Task Manager",
              ["utilities-system-monitor"], "plasma-systemmonitor"),
            T("Σύνοψη υπολογιστή (inxi)", "Πλήρης περιγραφή υλικού και συστήματος (inxi -Fxz)",
              ["computer", "hwinfo"], "inxi -Fxz", ["inxi"]),
            C("Αντιγραφή πληροφοριών για βοήθεια (LLM)",
              "Αντιγράφει στο clipboard σύνοψη συστήματος και τα τελευταία σφάλματα, έτοιμα για επικόλληση σε LLM",
              ["edit-copy", "klipper"],
              "inxi -Fxz; echo; echo '--- Σφάλματα της τρέχουσας εκκίνησης (journalctl) ---'; "
              "journalctl -b -p err --no-pager -n 40", ["inxi", "journalctl"]),
            T("Συσκευές PCI και drivers", "Ποια κάρτα χρησιμοποιεί ποιον driver (lspci -k)",
              ["preferences-devices-pci", "computer"], "lspci -k | less", ["lspci", "less"]),
            T("Κάρτα γραφικών", "Μοντέλο GPU και driver που χρησιμοποιεί",
              ["video-card", "computer"], "lspci -k | grep -A3 -Ei 'vga|3d|display'", ["lspci", "grep"]),
            T("Δίσκοι και partitions", "Διάταξη δίσκων και συστήματα αρχείων (lsblk -f)",
              ["drive-harddisk", "drive-partition"], "lsblk -f", ["lsblk"]),
            T("Ελεύθερος χώρος", "Χώρος ανά partition (df -h)",
              ["drive-harddisk", "folder"], "df -h", ["df"]),
            T("Μνήμη RAM", "Χρήση μνήμης και swap (free -h)",
              ["media-memory", "computer"], "free -h", ["free"]),
            T("Θερμοκρασίες", "Αισθητήρες θερμοκρασίας και ανεμιστήρων (sensors)",
              ["temperature-normal", "sensors-temperature"], "sensors", ["sensors"]),
            T("Παρακολούθηση σε πραγματικό χρόνο (btop)", "CPU, RAM, δίσκοι, δίκτυο σε ζωντανή προβολή",
              ["utilities-system-monitor"], "btop", ["btop"]),
            A("Χρήση χώρου δίσκου (Filelight)", "Γραφική εικόνα του τι πιάνει χώρο",
              ["filelight", "drive-harddisk"], "filelight"),
        ],
    },
    {
        "name": "Ενέργεια και απόδοση",
        "icons": ["preferences-system-power-management", "battery"],
        "profiles": True,
        "items": [
            K("Διαχείριση ενέργειας", "Πότε σβήνει η οθόνη, πότε κάνει suspend ο υπολογιστής, κλείδωμα",
              ["preferences-system-power-management", "battery"],
              ["kcm_powerdevilprofilesconfig", "powerdevilprofilesconfig"]),
            T("Ρολόι επεξεργαστή (ζωντανά)", "Τα MHz κάθε πυρήνα του επεξεργαστή, ανανεώνεται κάθε δευτερόλεπτο",
              ["cpu", "utilities-system-monitor"], "watch -n 1 'grep MHz /proc/cpuinfo'", ["watch", "grep"]),
            T("Ισχύς κάρτας γραφικών (W)", "Πόσα watt τραβά τώρα η GPU (αν το αναφέρει ο driver)",
              ["video-card", "utilities-system-monitor"],
              "cat /sys/class/drm/card*/device/hwmon/hwmon*/power1_average | awk '{printf \"GPU: %.1f W\\n\", $1/1000000}'",
              ["cat", "awk"]),
            A("Κάρτα γραφικών AMD (LACT)", "Όριο ισχύος, ρολόγια και ανεμιστήρες της GPU",
              ["lact", "video-card"], "lact"),
            T("Τι καταναλώνει ενέργεια (powertop)", "Ανάλυση κατανάλωσης και προτάσεις εξοικονόμησης",
              ["utilities-system-monitor", "battery"], "sudo powertop", ["powertop"]),
            T("Τεχνική κατάσταση προφίλ", "Τρέχον προφίλ, driver επεξεργαστή και προτίμηση ενέργειας (EPP)",
              ["dialog-information", "preferences-system"],
              "powerprofilesctl get; echo; powerprofilesctl list; echo; "
              "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver "
              "/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference",
              ["powerprofilesctl", "cat"]),
        ],
    },
    {
        "name": "CachyOS",
        "icons": ["start-here", "preferences-system"],
        "items": [
            A("CachyOS Hello", "Η εφαρμογή καλωσορίσματος και βασικών ρυθμίσεων της διανομής",
              ["cachyos-hello", "start-here"], "cachyos-hello"),
            A("CachyOS Kernel Manager", "Εγκατάσταση και αλλαγή πυρήνων (kernels)",
              ["cachyos-kernel-manager", "applications-system"], "cachyos-kernel-manager"),
            A("CachyOS Package Installer", "Έτοιμα πακέτα εφαρμογών και ρυθμίσεων της CachyOS",
              ["cachyos-pi", "system-software-install"], "cachyos-packageinstaller"),
            T("Βελτιστοποίηση mirrors", "Επιλέγει τους ταχύτερους mirrors για τα πακέτα",
              ["network-server", "preferences-system-network"], "sudo cachyos-rate-mirrors", ["cachyos-rate-mirrors"]),
            T("Τρέχων πυρήνας", "Ποιος kernel τρέχει και ποιοι είναι εγκατεστημένοι",
              ["computer", "utilities-terminal"], "uname -r; echo; pacman -Q | grep -E '^linux'", ["pacman"]),
        ],
    },
]


# ---------------------------------------------------------------- language

def _lang(lang):
    return lang or i18n.get_language()


def category_title(cat, lang=None):
    if _lang(lang) == "en":
        return translations.CATEGORY_NAMES_EN.get(cat["name"], cat["name"])
    return cat["name"]


def item_name(item, lang=None):
    if _lang(lang) == "en":
        return translations.ITEMS_EN.get(item["name"], (item["name"], item["desc"]))[0]
    return item["name"]


def item_desc(item, lang=None):
    if _lang(lang) == "en":
        return translations.ITEMS_EN.get(item["name"], (item["name"], item["desc"]))[1]
    return item["desc"]


def ask_texts(item, lang=None):
    """(dialog title, prompt) of an item that asks for text first."""
    if _lang(lang) == "en" and item["name"] in translations.ASK_EN:
        return translations.ASK_EN[item["name"]]
    return item["action"][1], item["action"][2]


def item_command(item, lang=None):
    """The shell command of a term/clip item, with its echo messages in the given language."""
    cmd = item["action"][1]
    if _lang(lang) == "en":
        for greek, english in translations.COMMAND_TEXT_EN.items():
            cmd = cmd.replace(greek, english)
    return cmd


def search_text(item, cat):
    """Lower-case text searched by the search box: both languages, so either can be typed."""
    parts = [item["name"], item["desc"], cat["name"],
             item_name(item, "en"), item_desc(item, "en"), category_title(cat, "en")]
    return " ".join(parts).lower()


# ---------------------------------------------------------------- availability

def kcm_ids():
    """The set of kcm modules known to kcmshell6, or None if it cannot be determined."""
    exe = shutil.which("kcmshell6")
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "--list"], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return None
    ids = set()
    for line in out.splitlines():
        line = line.strip()
        if line:
            ids.add(line.split()[0])
    return ids or None


def check_item(item, ids):
    """Return (available, reason). For kcm items the id that was found is kept in item["resolved"]."""
    kind = item["action"][0]
    if kind == "kcm":
        if not shutil.which("kcmshell6"):
            return False, "kcmshell6 not found"
        candidates = item["action"][1]
        if ids is None:
            item["resolved"] = candidates[0]
            return True, ""
        for c in candidates:
            if c in ids:
                item["resolved"] = c
                return True, ""
        return False, "not in `kcmshell6 --list`: " + ", ".join(candidates)
    if kind == "app":
        argv = item["action"][1]
        if not shutil.which(argv[0]):
            return False, f"program {argv[0]} not found"
        return True, ""
    for req in item["requires"]:
        if not shutil.which(req):
            return False, f"command {req} not found"
    return True, ""


def load_available():
    """Categories with only the items that exist on this system (empty categories are dropped)."""
    ids = kcm_ids()
    result = []
    for cat in CATEGORIES:
        items = [i for i in cat["items"] if check_item(i, ids)[0]]
        if items:
            result.append({"name": cat["name"], "icons": cat["icons"], "items": items,
                           "profiles": cat.get("profiles", False)})
    return result


def print_check():
    """Print what is shown and what is hidden on this system, and why (English, for bug reports)."""
    ids = kcm_ids()
    print("kcmshell6:", shutil.which("kcmshell6") or "NOT FOUND")
    print("kcm modules:", len(ids) if ids else "unknown")
    print("terminal:", (find_terminal() or ["NOT FOUND"])[0])
    print("shell:", "fish" if shutil.which("fish") else "bash")
    shown = hidden = 0
    for cat in CATEGORIES:
        print(f"\n== {category_title(cat, 'en')}")
        for it in cat["items"]:
            ok, why = check_item(it, ids)
            if ok:
                shown += 1
                print(f"  [shown]   {item_name(it, 'en')}")
            else:
                hidden += 1
                print(f"  [hidden]  {item_name(it, 'en')}  ->  {why}")
    print(f"\nShown: {shown}, hidden: {hidden}")
    return 0


# ---------------------------------------------------------------- running items

TERMINALS = [("konsole", ["-e"]), ("alacritty", ["-e"]), ("kitty", []),
             ("foot", []), ("xterm", ["-e"])]


def find_terminal():
    for exe, flag in TERMINALS:
        path = shutil.which(exe)
        if path:
            return [path] + flag
    return None


def quote_args(text):
    """Split text into words and quote each one for the shell (user text must never reach a command unquoted)."""
    return " ".join(shlex.quote(p) for p in text.split())


def _spawn(argv):
    subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)


def launch_kcm(item):
    exe = shutil.which("kcmshell6")
    if not exe:
        raise RuntimeError(tr("err_no_kcmshell"))
    _spawn([exe, item["resolved"] or item["action"][1][0]])


def launch_app(argv):
    _spawn(list(argv))


def run_in_terminal(cmd):
    term = find_terminal()
    if not term:
        raise RuntimeError(tr("err_no_terminal"))
    done = tr("press_enter")
    if shutil.which("fish"):
        script = ["fish", "-c", f"{cmd}; echo; read -P '{done} ' _x"]
    else:
        script = ["bash", "-c", f"{cmd}; echo; read -r -p '{done} ' _x"]
    _spawn(term + script)


def run_capture(cmd, timeout=60):
    proc = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)
    return (proc.stdout + ("\n" + proc.stderr if proc.stderr.strip() else "")).strip()


# ---------------------------------------------------------------- power profiles

PROFILE_ORDER = ["power-saver", "balanced", "performance"]


def profile_label(name):
    return tr("profile_" + name)


def _ppctl(*args, timeout=6):
    exe = shutil.which("powerprofilesctl")
    if not exe:
        return None
    try:
        return subprocess.run([exe, *args], capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None


def parse_profiles(text):
    """Available profiles from the output of `powerprofilesctl list`, in a fixed order."""
    found = set()
    for line in text.splitlines():
        t = line.strip().lstrip("*").strip()
        if t.endswith(":") and t[:-1] in PROFILE_ORDER:
            found.add(t[:-1])
    return [p for p in PROFILE_ORDER if p in found]


def profiles_available():
    proc = _ppctl("list")
    return parse_profiles(proc.stdout) if proc and proc.returncode == 0 else []


def profile_current():
    proc = _ppctl("get")
    return proc.stdout.strip() if proc and proc.returncode == 0 else ""


def profile_set(name):
    """Return (success, error message)."""
    proc = _ppctl("set", name, timeout=10)
    if proc is None:
        return False, tr("err_no_ppctl")
    return proc.returncode == 0, (proc.stderr or proc.stdout).strip()


def cpu_status():
    base = "/sys/devices/system/cpu"

    def read(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return fh.read().strip()
        except OSError:
            return "?"

    freqs = []
    for path in glob.glob(base + "/cpu[0-9]*/cpufreq/scaling_cur_freq"):
        try:
            freqs.append(int(read(path)) / 1000)
        except ValueError:
            pass
    return {
        "driver": read(base + "/cpu0/cpufreq/scaling_driver"),
        "epp": read(base + "/cpu0/cpufreq/energy_performance_preference"),
        "avg": round(sum(freqs) / len(freqs)) if freqs else None,
        "max": round(max(freqs)) if freqs else None,
    }
