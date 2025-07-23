from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

def launch_browser(url):
    print(f"Launching browser with URL: {url}")

    class LockedBrowser(QMainWindow):
        def __init__(self, url):
            super().__init__()
            self.setWindowTitle("Locked Browser")
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl(url))
            self.browser.page().setDevToolsPage(None)  
            self.setCentralWidget(self.browser)
            self.showFullScreen()

    app = QApplication(sys.argv)
    window = LockedBrowser(url)
    window.show()
    sys.exit(app.exec_())


