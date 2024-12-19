import sys
import tkinter as tk
from tkinter import ttk

import sv_ttk

from file_handler import save_canvas_as_image
from logger import NiceLogger
from settings import PROJECT_NAME, PROJECT_VERSION, ICON_PATH
from translations import TRANSLATIONS
from tree_drawer import TreeDrawer
from ui_components import UIComponents
from update_checker import check_for_updates

# Initialize logger
logger = NiceLogger(__name__).get_logger()


class TacticalChristmasTree:
    def __init__(self):
        logger.info(f"Initializing {PROJECT_NAME} v{PROJECT_VERSION}")

        try:
            self.root = tk.Tk()
            self.root.title(TRANSLATIONS['en']['window_title'])
            self.root.geometry("800x800")

            # Set window icons in multiple formats
            if ICON_PATH.exists():
                try:
                    logger.debug(f"Setting window icons from: {ICON_PATH}")

                    # Load main .ico file for taskbar/window
                    self.root.wm_iconbitmap(default=str(ICON_PATH))

                    # Load as photo image for other places
                    icon_photo = tk.PhotoImage(file=str(ICON_PATH.with_suffix('.png')))
                    self.root.iconphoto(True, icon_photo)

                    logger.debug("Window icons set successfully")
                except Exception as e:
                    logger.error(
                        "Failed to set window icons",
                        extra={'metadata': {
                            'icon_path': str(ICON_PATH),
                            'error': str(e)
                        }},
                        exc_info=True
                    )

            # Initial language setting
            self.current_lang = 'en'
            logger.debug(f"Initial language set to: {self.current_lang}")

            # Enable dark theme
            logger.debug("Applying dark theme")
            sv_ttk.set_theme("dark")

            # Create language switch button
            self.lang_button = ttk.Button(
                self.root,
                text=TRANSLATIONS[self.current_lang]['switch_to_pl'],
                command=self.toggle_language,
                style='Accent.TButton'
            )
            self.lang_button.pack(anchor='ne', padx=10, pady=5)

            # Initialize components
            logger.debug("Initializing UI components")
            self.ui = UIComponents(self.root, self.draw_tree, self.current_lang)
            self.drawer = TreeDrawer(self.root)

            # Export button
            self.export_button = ttk.Button(
                self.root,
                text=TRANSLATIONS[self.current_lang]['export_tree'],
                command=self.export_tree,
                state="disabled"
            )
            self.export_button.pack(pady=20)

            logger.info("Application initialized successfully")

        except Exception as e:
            logger.critical(
                "Failed to initialize application",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )
            sys.exit(1)

    def toggle_language(self):
        """Toggle between English and Polish language."""
        try:
            # Switch language
            new_lang = 'pl' if self.current_lang == 'en' else 'en'
            logger.info(f"Switching language from {self.current_lang} to {new_lang}")
            self.current_lang = new_lang

            # Update window title
            self.root.title(TRANSLATIONS[self.current_lang]['window_title'])

            # Update button text
            self.lang_button.config(
                text=TRANSLATIONS[self.current_lang]['switch_to_pl']
                if self.current_lang == 'en'
                else TRANSLATIONS[self.current_lang]['switch_to_en']
            )

            # Update UI components
            self.ui.update_language(self.current_lang)

            # Update export button
            self.export_button.config(
                text=TRANSLATIONS[self.current_lang]['export_tree']
            )

            logger.debug("Language switch completed successfully")

        except Exception as e:
            logger.error(
                "Failed to switch language",
                extra={
                    'metadata': {
                        'from_lang': self.current_lang,
                        'to_lang': 'pl' if self.current_lang == 'en' else 'en',
                        'error': str(e)
                    }
                },
                exc_info=True
            )

    def draw_tree(self):
        """Draw the Christmas tree with current parameters."""
        try:
            params = self.ui.get_parameters()
            logger.debug("Drawing tree", extra={'metadata': params})

            self.drawer.clear_canvas()
            self.drawer.draw_tree(params)
            self.export_button.config(state="normal")

            logger.debug("Tree drawn successfully")

        except Exception as e:
            logger.error(
                "Failed to draw tree",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )

    def export_tree(self):
        """Export the tree as an image."""
        try:
            logger.info("Exporting tree as image")
            save_canvas_as_image(self.drawer.canvas)
            logger.info("Tree exported successfully")

        except Exception as e:
            logger.error(
                "Failed to export tree",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )

    def run(self):
        """Run the main application loop."""
        try:
            logger.info("Starting application main loop")
            # Check for updates
            check_for_updates()
            # Start main loop
            self.root.mainloop()
            logger.info("Application closed normally")

        except Exception as e:
            logger.critical(
                "Unexpected error in main loop",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )
            sys.exit(1)


if __name__ == "__main__":
    try:
        app = TacticalChristmasTree()
        app.run()
    except Exception as e:
        logger.critical(
            "Fatal application error",
            extra={'metadata': {'error': str(e)}},
            exc_info=True
        )
        sys.exit(1)
