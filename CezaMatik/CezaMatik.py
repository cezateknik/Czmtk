import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui.main_window import MainWindow
from utils.shortcut_creator import create_desktop_shortcut

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # For a more modern look across platforms
    
    # Create desktop shortcut when the application starts
    try:
        # Get the path to the current script or executable
        executable_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        # Create the shortcut (errors are handled inside the function)
        create_desktop_shortcut(executable_path)
    except Exception as e:
        print(f"Error creating shortcut: {str(e)}")

                # Set window icon - mainwindow'daydı


    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())