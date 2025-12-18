import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit, QTabWidget
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QUrl

class ChromeEmulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Chrome Emulator")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        self.toolbar.addAction(back_btn)

        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        self.toolbar.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        self.toolbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_bar)

        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(self.add_tab)
        self.toolbar.addAction(new_tab_btn)

        self.add_tab(QUrl("https://www.google.com"), "New Tab")

    def add_tab(self, url=None, label="New Tab"):
        browser = QWebEngineView()
        browser.setUrl(url or QUrl("https://www.google.com"))

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, b=browser: self.update_url(qurl, b))
        browser.loadFinished.connect(lambda _, i=i, b=browser: self.tabs.setTabText(i, b.page().title()))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        return self.tabs.currentWidget()

    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, qurl, browser):
        if browser == self.current_browser():
            self.url_bar.setText(qurl.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChromeEmulator()
    window.show()
    sys.exit(app.exec())
