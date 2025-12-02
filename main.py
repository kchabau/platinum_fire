"""
Platinum Fire - Data Management Tool

Main entry point for the application.
Run this file to start the GUI application.
"""

from gui.app import UploadApp


def main() -> None:
    """Main entry point for the application."""
    app = UploadApp()
    app.mainloop()


if __name__ == "__main__":
    main()
