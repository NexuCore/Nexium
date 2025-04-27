import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QApplication, QLineEdit, QVBoxLayout, QWidget,
                             QTabWidget, QToolBar, QMainWindow, QAction,
                             QMenuBar, QShortcut, QSizePolicy)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://nexucore.github.io/Synax/"))
        self.layout.addWidget(self.browser)

    def navigate_to(self, url_or_query):
        """Navigate to URL or perform search query"""
        if not url_or_query:
            return
            
        # Check if input is a URL
        if ('.' in url_or_query or 
            url_or_query.startswith(('http://', 'https://', 'file://'))):
            if not url_or_query.startswith(('http://', 'https://', 'file://')):
                url_or_query = 'https://' + url_or_query
            self.browser.setUrl(QUrl(url_or_query))
        else:
            # Treat as search query
            search_url = f"https://nexucore.github.io/Synax/?q={url_or_query}"
            self.browser.setUrl(QUrl(search_url))


class SynaxBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexium")
        self.setWindowIcon(QIcon.fromTheme("terminal"))
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize UI components
        self.init_ui()
        
        # Create first tab
        self.add_new_tab(home=True)

    def init_ui(self):
        """Initialize all UI components"""
        self.setup_tabs()
        self.create_menu_bar()
        self.create_toolbar()
        self.setup_shortcuts()
        self.apply_styles()

    def setup_tabs(self):
        """Initialize tab widget"""
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)

    def create_menu_bar(self):
        """Create the main menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu('&File')
        
        new_tab_action = QAction('&New Tab', self)
        new_tab_action.setShortcut('Ctrl+T')
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
        
        close_tab_action = QAction('&Close Tab', self)
        close_tab_action.setShortcut('Ctrl+W')
        close_tab_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Navigation menu
        nav_menu = menu_bar.addMenu('&Navigation')
        
        back_action = QAction('&Back', self)
        back_action.setShortcut('Alt+Left')
        back_action.triggered.connect(self.go_back)
        nav_menu.addAction(back_action)
        
        forward_action = QAction('&Forward', self)
        forward_action.setShortcut('Alt+Right')
        forward_action.triggered.connect(self.go_forward)
        nav_menu.addAction(forward_action)
        
        reload_action = QAction('&Reload', self)
        reload_action.setShortcut('F5')
        reload_action.triggered.connect(self.reload_page)
        nav_menu.addAction(reload_action)
        
        home_action = QAction('&Home', self)
        home_action.setShortcut('Alt+Home')
        home_action.triggered.connect(self.go_home)
        nav_menu.addAction(home_action)

    def create_toolbar(self):
        """Create navigation toolbar"""
        nav_bar = QToolBar("Navigation")
        nav_bar.setMovable(False)
        nav_bar.setIconSize(QApplication.primaryScreen().availableGeometry().size() / 40)
        self.addToolBar(nav_bar)

        # Navigation buttons
        back_btn = QAction(QIcon.fromTheme("go-previous"), "Back", self)
        back_btn.setShortcut('Alt+Left')
        back_btn.triggered.connect(self.go_back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction(QIcon.fromTheme("go-next"), "Forward", self)
        forward_btn.setShortcut('Alt+Right')
        forward_btn.triggered.connect(self.go_forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction(QIcon.fromTheme("view-refresh"), "Reload", self)
        reload_btn.setShortcut('F5')
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        home_btn = QAction(QIcon.fromTheme("go-home"), "Home", self)
        home_btn.setShortcut('Alt+Home')
        home_btn.triggered.connect(self.go_home)
        nav_bar.addAction(home_btn)

        new_tab_btn = QAction(QIcon.fromTheme("tab-new"), "New Tab", self)
        new_tab_btn.setShortcut('Ctrl+T')
        new_tab_btn.triggered.connect(self.add_new_tab)
        nav_bar.addAction(new_tab_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.url_bar.setClearButtonEnabled(True)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

    def setup_shortcuts(self):
        """Configure keyboard shortcuts"""
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.add_new_tab)

        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)

        self.shortcut_next_tab = QShortcut(QKeySequence("Ctrl+Tab"), self)
        self.shortcut_next_tab.activated.connect(self.next_tab)

        self.shortcut_prev_tab = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        self.shortcut_prev_tab.activated.connect(self.previous_tab)

    def apply_styles(self):
        """Apply custom styles to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #fff;
            }
            QTabWidget::pane {
                border: 0;
                background: #252525;
            }
            QTabBar::tab {
                background: #333;
                color: #fff;
                padding: 8px 15px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
                font-size: 12px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #505050;
                border-bottom: 2px solid #4CAF50;
            }
            QTabBar::tab:hover {
                background: #404040;
            }
            QToolBar {
                background: #252525;
                border: none;
                padding: 4px;
                spacing: 4px;
            }
            QToolButton {
                background: transparent;
                padding: 4px;
                border-radius: 4px;
                color: #fff;
            }
            QToolButton:hover {
                background: #404040;
            }
            QLineEdit {
                background: #333;
                color: #fff;
                border: 1px solid #444;
                border-radius: 15px;
                padding: 5px 10px;
                font-size: 14px;
                selection-background-color: #4CAF50;
            }
            QMenuBar {
                background: #252525;
                color: #fff;
            }
            QMenuBar::item {
                background: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background: #404040;
            }
            QMenu {
                background: #333;
                color: #fff;
                border: 1px solid #444;
            }
            QMenu::item:selected {
                background: #4CAF50;
                color: #fff;
            }
        """)

    def add_new_tab(self, url=None, home=False):
        """Add a new browser tab"""
        new_tab = BrowserTab()
        
        # Determine URL to load
        if home:
            target_url = QUrl("https://nexucore.github.io/Synax/")
        elif url:
            target_url = QUrl(url) if isinstance(url, str) else url
        else:
            target_url = QUrl("https://nexucore.github.io/Synax/")
        
        # Add tab to interface
        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        # Connect signals for tab updates
        def update_title(title):
            self.tabs.setTabText(index, title[:20] + "..." if len(title) > 20 else title)
        
        def update_icon(icon):
            self.tabs.setTabIcon(index, icon)
            
        def update_url(qurl):
            if qurl.toString() != "about:blank":
                self.url_bar.setText(qurl.toString())

        new_tab.browser.titleChanged.connect(update_title)
        new_tab.browser.iconChanged.connect(update_icon)
        new_tab.browser.urlChanged.connect(update_url)
        
        # Load the URL
        new_tab.browser.setUrl(target_url)
        return new_tab

    def close_current_tab(self):
        """Close the currently active tab"""
        self.close_tab(self.tabs.currentIndex())

    def close_tab(self, index):
        """Close tab at specified index"""
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget:
                widget.deleteLater()
            self.tabs.removeTab(index)

    def next_tab(self):
        """Switch to next tab"""
        current = self.tabs.currentIndex()
        self.tabs.setCurrentIndex(current + 1 if current < self.tabs.count() - 1 else 0)

    def previous_tab(self):
        """Switch to previous tab"""
        current = self.tabs.currentIndex()
        self.tabs.setCurrentIndex(current - 1 if current > 0 else self.tabs.count() - 1)

    def current_browser(self):
        """Get the current browser widget"""
        current_widget = self.tabs.currentWidget()
        return current_widget.browser if current_widget else None

    def navigate_to_url(self):
        """Navigate to URL in address bar"""
        url_or_query = self.url_bar.text().strip()
        if current_tab := self.tabs.currentWidget():
            current_tab.navigate_to(url_or_query)

    def go_back(self):
        """Navigate back in history"""
        if browser := self.current_browser():
            browser.back()

    def go_forward(self):
        """Navigate forward in history"""
        if browser := self.current_browser():
            browser.forward()

    def reload_page(self):
        """Reload current page"""
        if browser := self.current_browser():
            browser.reload()

    def update_url_bar(self, index):
        """Update URL bar when tab changes"""
        if index >= 0 and (current_widget := self.tabs.widget(index)):
            self.url_bar.setText(current_widget.browser.url().toString())

    def go_home(self):
        """Navigate to home page"""
        if browser := self.current_browser():
            browser.setUrl(QUrl("https://nexucore.github.io/Synax/"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SynaxBrowser()
    window.show()
    sys.exit(app.exec_())
