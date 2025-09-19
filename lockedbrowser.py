from PyQt5.QtWidgets import QApplication, QMainWindow  # Core PyQt5 GUI components
from PyQt5.QtWebEngineWidgets import QWebEngineView   # Browser widget for displaying web pages
from PyQt5.QtCore import QUrl                          # URL handling in PyQt5
import sys                                             # System-level functions for app control

def launch_browser(url):
    print(f"Launching browser with URL: {url}")  # Debug/log the URL being opened

    class LockedBrowser(QMainWindow):
        def __init__(self, url): # Runs when setting up a window.
            super().__init__()  # Initialize the parent QMainWindow
            self.setWindowTitle("Locked Browser")  
            self.browser = QWebEngineView()        # Initialize web engine view
            self.browser.setUrl(QUrl(url))         # Load the provided URL
            self.browser.page().setDevToolsPage(None)  # Disable dev tools for security
            self.setCentralWidget(self.browser)    # Set browser as central widget
            self.showFullScreen()                  # Open window in fullscreen mode

    app = QApplication(sys.argv)                    # Initialize PyQt application
    window = LockedBrowser(url)                     # Create instance of locked browser
    window.show()                                   # Show the window
    sys.exit(app.exec_())                           # (app.exec) Keeps the GUI open until the user closes it. 




