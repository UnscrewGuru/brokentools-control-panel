# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 UnscrewGuru (BrokenTools by Unscrew Guru)
"""BrokenTools Control Panel - main window (PyQt6).

Run with:  python3 -m brokentools_control_panel
"""
import html
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize, QSettings, QTimer
from PyQt6.QtGui import QIcon, QPalette, QKeySequence, QShortcut, QGuiApplication
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QToolButton, QLineEdit, QComboBox, QStackedWidget,
    QScrollArea, QListWidget, QListWidgetItem, QFrame, QMessageBox, QInputDialog,
    QAbstractItemView, QButtonGroup,
)

from . import catalog, i18n
from .i18n import tr

APP_TITLE = "BrokenTools Control Panel"
ROOT_CRUMB = APP_TITLE
ICON_NAME = "brokentools-control-panel"   # icon theme name and .desktop file name


def themed_icon(names, fallback="preferences-system"):
    for name in names:
        if QIcon.hasThemeIcon(name):
            return QIcon.fromTheme(name)
    return QIcon.fromTheme(fallback)


def app_icon():
    """The application icon: from the icon theme (after installation),
    otherwise from the icons/ folder next to this file."""
    icon = QIcon.fromTheme(ICON_NAME)
    if not icon.isNull():
        return icon
    icon = QIcon()
    root = Path(__file__).resolve().parent / "icons" / "hicolor"
    for png in sorted(root.glob(f"*/apps/{ICON_NAME}.png")):
        icon.addFile(str(png))
    return icon if not icon.isNull() else themed_icon(["preferences-system"])


class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(app_icon())
        self.resize(1000, 700)
        self.setMinimumSize(640, 420)

        self.settings = QSettings("brokentools", "control-panel")
        self.language_pref = self._saved_language()
        i18n.set_language(i18n.resolve(self.language_pref))

        self.categories = catalog.load_available()
        self.power_timer = None
        self.state = "home"          # home | cat | all | search
        self.cat_index = None

        link = self.palette().color(QPalette.ColorRole.Link).name()
        self.link_css = (
            f"QPushButton#link, QPushButton#title {{ border: none; background: transparent;"
            f" text-align: left; color: {link}; padding: 2px 0; }}"
            f"QPushButton#title {{ font-size: 15px; }}"
            f"QPushButton#link:hover, QPushButton#title:hover {{ text-decoration: underline; }}"
        )

        QShortcut(QKeySequence("Ctrl+F"), self, activated=lambda: self.search.setFocus())
        QShortcut(QKeySequence("Alt+Left"), self, activated=self.go_back)
        self._build_ui()

    # ------------------------------------------------------------- building the UI

    def _saved_language(self):
        value = self.settings.value("language", "auto", type=str)
        return value if value in i18n.PREFERENCES else "auto"

    def _build_ui(self):
        """(Re)build the whole window content in the current language."""
        if self.power_timer is not None:
            self.power_timer.stop()
            self.power_timer.deleteLater()
            self.power_timer = None
        self.state = "home"
        self.cat_index = None

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_toolbar())
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        root.addWidget(line)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)
        self.page_home = self._build_home()
        self.page_cat = self._build_list_page()
        self.page_all = self._build_icon_page()
        for page in (self.page_home, self.page_cat, self.page_all):
            self.stack.addWidget(page)

        self.setCentralWidget(central)    # also schedules the old content for deletion
        self.show_home()

    def _build_toolbar(self):
        bar = QWidget()
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(10, 8, 10, 8)

        self.btn_back = QToolButton()
        self.btn_back.setIcon(themed_icon(["go-previous"], "go-previous"))
        self.btn_back.setToolTip(tr("back_tip"))
        self.btn_back.clicked.connect(self.go_back)
        self.btn_home = QToolButton()
        self.btn_home.setIcon(themed_icon(["go-home"], "go-home"))
        self.btn_home.setToolTip(tr("home_tip"))
        self.btn_home.clicked.connect(self.go_home)

        self.crumb = QLabel(ROOT_CRUMB)
        self.crumb.setStyleSheet("font-size: 14px;")

        self.mode_box = QComboBox()
        self.mode_box.addItems([tr("mode_category"), tr("mode_icons")])
        mode = self.settings.value("mode", 0, type=int)
        self.mode_box.setCurrentIndex(mode if mode in (0, 1) else 0)
        self.mode_box.currentIndexChanged.connect(self.on_mode)

        self.lang_box = QComboBox()
        self.lang_box.addItem(tr("lang_auto"), "auto")
        self.lang_box.addItem("English", "en")
        self.lang_box.addItem("Ελληνικά", "el")
        self.lang_box.setCurrentIndex(i18n.PREFERENCES.index(self.language_pref))
        self.lang_box.currentIndexChanged.connect(self.on_language)

        self.search = QLineEdit()
        self.search.setPlaceholderText(tr("search_placeholder"))
        self.search.setClearButtonEnabled(True)
        self.search.setMinimumWidth(260)
        self.search.textChanged.connect(self.on_search)

        lay.addWidget(self.btn_back)
        lay.addWidget(self.btn_home)
        lay.addWidget(self.crumb, 1)
        lay.addWidget(QLabel(tr("view_by")))
        lay.addWidget(self.mode_box)
        lay.addWidget(QLabel(tr("language_label")))
        lay.addWidget(self.lang_box)
        lay.addWidget(self.search)
        return bar

    def _build_home(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        body = QWidget()
        body.setStyleSheet(self.link_css)
        outer = QVBoxLayout(body)
        outer.setContentsMargins(28, 20, 28, 20)

        heading = QLabel(tr("heading"))
        heading.setStyleSheet("font-size: 20px;")
        outer.addWidget(heading)
        outer.addSpacing(14)

        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(22)
        for n, cat in enumerate(self.categories):
            grid.addWidget(self._category_card(n, cat), n // 2, n % 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        outer.addLayout(grid)
        outer.addStretch(1)
        scroll.setWidget(body)
        return scroll

    def _category_card(self, index, cat):
        card = QWidget()
        lay = QHBoxLayout(card)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        icon = QLabel()
        icon.setPixmap(themed_icon(cat["icons"]).pixmap(QSize(56, 56)))
        icon.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.addWidget(icon)

        col = QVBoxLayout()
        col.setSpacing(1)
        title = QPushButton(catalog.category_title(cat))
        title.setObjectName("title")
        title.setCursor(Qt.CursorShape.PointingHandCursor)
        title.clicked.connect(lambda _=False, i=index: self.open_category(i))
        col.addWidget(title)
        for item in cat["items"][:3]:
            btn = QPushButton(catalog.item_name(item))
            btn.setObjectName("link")
            btn.setToolTip(catalog.item_desc(item))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _=False, it=item: self.run_item(it))
            col.addWidget(btn)
        col.addStretch(1)
        lay.addLayout(col, 1)
        return card

    def _build_list_page(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(10, 10, 10, 0)
        self.profile_bar = self._build_profile_bar()
        self.profile_bar.hide()
        lay.addWidget(self.profile_bar)
        lst = QListWidget()
        lst.setFrameShape(QFrame.Shape.NoFrame)
        lst.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        lst.setMouseTracking(True)
        lst.setSpacing(2)
        lst.itemClicked.connect(self._on_list_click)
        self.list_cat = lst
        lay.addWidget(lst, 1)
        return page

    def _build_profile_bar(self):
        bar = QFrame()
        bar.setFrameShape(QFrame.Shape.StyledPanel)
        lay = QVBoxLayout(bar)
        top = QHBoxLayout()
        top.addWidget(QLabel(f"<b>{html.escape(tr('power_profile'))}</b>"))
        self.profile_buttons = {}
        group = QButtonGroup(self)
        group.setExclusive(True)
        for name in catalog.PROFILE_ORDER:
            btn = QPushButton(catalog.profile_label(name))
            btn.setCheckable(True)
            btn.setMinimumHeight(34)
            btn.clicked.connect(lambda _=False, n=name: self.set_profile(n))
            group.addButton(btn)
            top.addWidget(btn)
            self.profile_buttons[name] = btn
        top.addStretch(1)
        lay.addLayout(top)
        self.power_status = QLabel()
        self.power_status.setWordWrap(True)
        self.power_status.setTextFormat(Qt.TextFormat.PlainText)
        lay.addWidget(self.power_status)
        self.power_timer = QTimer(self)
        self.power_timer.setInterval(2000)
        self.power_timer.timeout.connect(self._power_tick)
        self.power_timer.start()
        return bar

    def _build_icon_page(self):
        lst = QListWidget()
        lst.setFrameShape(QFrame.Shape.NoFrame)
        lst.setViewMode(QListWidget.ViewMode.IconMode)
        lst.setIconSize(QSize(48, 48))
        lst.setGridSize(QSize(170, 104))
        lst.setSpacing(8)
        lst.setWordWrap(True)
        lst.setResizeMode(QListWidget.ResizeMode.Adjust)
        lst.setMovement(QListWidget.Movement.Static)
        lst.setUniformItemSizes(True)
        lst.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        lst.itemClicked.connect(self._on_list_click)
        return lst

    # ------------------------------------------------------------- navigation

    def _set_crumb(self, *parts):
        self.crumb.setText("  ›  ".join((ROOT_CRUMB,) + parts))
        self.btn_back.setEnabled(self.state in ("cat", "search"))

    def show_home(self):
        self.cat_index = None
        if self.mode_box.currentIndex() == 1:
            self.state = "all"
            self._fill_all("")
            self.stack.setCurrentWidget(self.page_all)
            self._set_crumb(tr("crumb_all"))
        else:
            self.state = "home"
            self.stack.setCurrentWidget(self.page_home)
            self._set_crumb()

    def go_home(self):
        self.search.blockSignals(True)
        self.search.clear()
        self.search.blockSignals(False)
        self.show_home()

    def go_back(self):
        self.go_home()

    def open_category(self, index):
        cat = self.categories[index]
        self.state = "cat"
        self.cat_index = index
        lst = self.list_cat
        lst.clear()
        for item in cat["items"]:
            li = QListWidgetItem()
            li.setData(Qt.ItemDataRole.UserRole, item)
            li.setSizeHint(QSize(0, 62))
            lst.addItem(li)
            lst.setItemWidget(li, self._row_widget(item))
        self._update_profile_bar(cat.get("profiles", False))
        self.stack.setCurrentWidget(self.page_cat)
        self._set_crumb(catalog.category_title(cat))

    def _row_widget(self, item):
        w = QWidget()
        w.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        lay = QHBoxLayout(w)
        lay.setContentsMargins(12, 4, 12, 4)
        lay.setSpacing(14)
        icon = QLabel()
        icon.setPixmap(themed_icon(item["icons"]).pixmap(QSize(36, 36)))
        lay.addWidget(icon)
        text = QLabel(f"<b>{html.escape(catalog.item_name(item))}</b><br>"
                      f"<span style='color:gray'>{html.escape(catalog.item_desc(item))}</span>")
        text.setTextFormat(Qt.TextFormat.RichText)
        text.setWordWrap(True)
        lay.addWidget(text, 1)
        return w

    def _fill_all(self, needle):
        needle = needle.strip().lower()
        lst = self.page_all
        lst.clear()
        rows = []
        for cat in self.categories:
            for item in cat["items"]:
                if not needle or needle in catalog.search_text(item, cat):
                    rows.append((item, catalog.category_title(cat)))
        rows.sort(key=lambda r: catalog.item_name(r[0]).lower())
        for item, cat_name in rows:
            li = QListWidgetItem(themed_icon(item["icons"]), catalog.item_name(item))
            li.setToolTip(f"{catalog.item_desc(item)}\n\n{tr('tip_category', cat=cat_name)}")
            li.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            li.setData(Qt.ItemDataRole.UserRole, item)
            lst.addItem(li)
        return len(rows)

    def on_search(self, text):
        if not text.strip():
            self.show_home()
            return
        self.state = "search"
        count = self._fill_all(text)
        self.stack.setCurrentWidget(self.page_all)
        self._set_crumb(tr("crumb_search", n=count))

    def on_mode(self, index):
        self.settings.setValue("mode", index)
        if self.state in ("home", "all"):
            self.show_home()

    def on_language(self, index):
        self.set_language_pref(i18n.PREFERENCES[index])

    def set_language_pref(self, pref):
        """Switch the interface language ("auto", "en" or "el") and remember the choice."""
        if pref not in i18n.PREFERENCES or pref == self.language_pref:
            return
        self.language_pref = pref
        self.settings.setValue("language", pref)
        i18n.set_language(i18n.resolve(pref))
        # rebuild after the current signal handler has returned (the combo box that
        # triggered this belongs to the content being replaced)
        QTimer.singleShot(0, self._build_ui)

    # ------------------------------------------------------------- power profiles

    def _update_profile_bar(self, show):
        if not show:
            self.profile_bar.hide()
            return
        available = catalog.profiles_available()
        for name, btn in self.profile_buttons.items():
            btn.setVisible(name in available)
        self.profile_bar.show()
        self.refresh_power()

    def refresh_power(self):
        available = catalog.profiles_available()
        if not available:
            self.power_status.setText(tr("ppd_missing"))
            return
        current = catalog.profile_current()
        for name, btn in self.profile_buttons.items():
            btn.setChecked(name == current)
        st = catalog.cpu_status()
        clock = (tr("cpu_clock", avg=st["avg"], max=st["max"])
                 if st["avg"] is not None else tr("cpu_clock_na"))
        self.power_status.setText(tr("cpu_status", driver=st["driver"], epp=st["epp"], clock=clock))

    def _power_tick(self):
        if self.state == "cat" and self.profile_bar.isVisible():
            self.refresh_power()

    def set_profile(self, name):
        ok, err = catalog.profile_set(name)
        if not ok:
            QMessageBox.warning(self, APP_TITLE, tr("profile_failed", err=err))
        self.refresh_power()

    # ------------------------------------------------------------- running items

    def _on_list_click(self, list_item):
        item = list_item.data(Qt.ItemDataRole.UserRole)
        if item:
            self.run_item(item)

    def run_item(self, item):
        kind = item["action"][0]
        try:
            if kind == "kcm":
                catalog.launch_kcm(item)
            elif kind == "app":
                catalog.launch_app(item["action"][1])
            elif kind == "term":
                catalog.run_in_terminal(catalog.item_command(item))
            elif kind == "ask":
                title, prompt = catalog.ask_texts(item)
                text, ok = QInputDialog.getText(self, title, prompt)
                if ok and text.strip():
                    catalog.run_in_terminal(item["action"][3].format(catalog.quote_args(text)))
            elif kind == "clip":
                self._copy_to_clipboard(item)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, APP_TITLE,
                                tr("run_failed", name=catalog.item_name(item), err=exc))

    def _copy_to_clipboard(self, item):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            output = catalog.run_capture(catalog.item_command(item))
        finally:
            QApplication.restoreOverrideCursor()
        QGuiApplication.clipboard().setText(output)
        QMessageBox.information(self, APP_TITLE, tr("copied", n=output.count("\n") + 1))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("brokentools-control-panel")
    app.setOrganizationName("BrokenTools")
    QGuiApplication.setDesktopFileName(ICON_NAME)
    win = ControlPanel()
    win.show()
    sys.exit(app.exec())
