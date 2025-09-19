"""This script displays the browser the student uses to acess the internent. 
I used a more advanced GUI library called PyQt5 to display my own custom 
browser. I used classes because the lockedbrowser needs to be used mulitple
times, and must run on different urls at different settings. I also display 
dev tools so the browser is locked. """


from PyQt5.QtWidgets import QApplication, QMainWindow  # Core GUI components
from PyQt5.QtWebEngineWidgets import QWebEngineView    # Browser widget
from PyQt5.QtCore import QUrl                          # URL handling
import sys                                             # System functions


def launch_browser(url):
    """Launch a fullscreen PyQt5 browser locked to the given URL."""
    print(f"Launching browser with URL: {url}")  # Debug log

    class LockedBrowser(QMainWindow): # Classes for reuseability 
        """A locked fullscreen browser window without dev tools."""

        def __init__(self, url):
            super().__init__()
            self.setWindowTitle("Locked Browser")

            # Browser widget
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl(url))
            self.browser.page().setDevToolsPage(None)  # Disable dev tools
            self.setCentralWidget(self.browser)

            # Open in fullscreen
            self.showFullScreen()

    app = QApplication(sys.argv)      # Initialize PyQt application
    window = LockedBrowser(url)       # Create browser window
    window.show()                     # Show window
    sys.exit(app.exec_())             # Keep GUI running until closed
 



