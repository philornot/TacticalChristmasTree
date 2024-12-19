import sys
import tkinter as tk
import webbrowser
from tkinter import ttk

import sv_ttk

from file_handler import save_canvas_as_image
from logger import NiceLogger
from settings import PROJECT_NAME, PROJECT_VERSION, ICON_PATH
from translations import TRANSLATIONS
from tree_drawer import TreeDrawer
from ui_components import UIComponents
from update_checker import check_for_updates, install_update

# Initialize logger
logger = NiceLogger(__name__).get_logger()


class TacticalChristmasTree:
    def __init__(self):
        logger.info(f"Initializing {PROJECT_NAME} v{PROJECT_VERSION}")
        logger.debug("Starting application initialization", extra={
            'metadata': {'project': PROJECT_NAME, 'version': PROJECT_VERSION, 'icon_path': str(ICON_PATH)}})

        self.update_installer_path = None
        self.latest_version = None
        self.release_url = None

        try:
            logger.debug("Creating main window")
            self.root = tk.Tk()
            self.root.title(TRANSLATIONS['en']['window_title'])
            self.root.geometry("800x800")
            logger.debug("Main window created",
                         extra={'metadata': {'title': self.root.title(), 'geometry': self.root.geometry()}})

            # Register close handler
            logger.debug("Registering window close handler")
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

            # Set window icons
            if ICON_PATH.exists():
                try:
                    logger.debug("Setting window icons", extra={'metadata': {'icon_path': str(ICON_PATH)}})

                    # Main icon for taskbar/window
                    self.root.wm_iconbitmap(default=str(ICON_PATH))
                    logger.debug("Main icon set successfully")

                    # Photo image for other contexts
                    icon_photo = tk.PhotoImage(file=str(ICON_PATH.with_suffix('.png')))
                    self.root.iconphoto(True, icon_photo)
                    logger.debug("Photo icon set successfully")

                except Exception as e:
                    logger.error(
                        "Failed to set window icons",
                        extra={'metadata': {
                            'icon_path': str(ICON_PATH), 'error': str(e), 'error_type': type(e).__name__
                        }},
                        exc_info=True
                    )

            # Initial language setting
            self.current_lang = 'en'
            logger.debug("Initial language set", extra={'metadata': {'language': self.current_lang}})

            # Enable dark theme
            logger.debug("Applying dark theme using sv_ttk")
            sv_ttk.set_theme("dark")

            # Create language switch button
            logger.debug("Creating language switch button")
            self.lang_button = ttk.Button(
                self.root,
                text=TRANSLATIONS[self.current_lang]['switch_to_pl'],
                command=self.toggle_language,
                style='Accent.TButton'
            )
            self.lang_button.pack(anchor='ne', padx=10, pady=5)
            logger.debug("Language button created and packed")

            # Initialize UI components
            logger.debug("Initializing UI components")
            self.ui = UIComponents(self.root, self.draw_tree, self.current_lang)
            logger.debug("UI components initialized")

            logger.debug("Initializing tree drawer")
            self.drawer = TreeDrawer(self.root)
            logger.debug("Tree drawer initialized")

            # Export button
            logger.debug("Creating export button")
            self.export_button = ttk.Button(
                self.root,
                text=TRANSLATIONS[self.current_lang]['export_tree'],
                command=self.export_tree,
                state="disabled"
            )
            self.export_button.pack(pady=20)
            logger.debug("Export button created and packed")

            # Bottom frame for version and update info
            logger.debug("Creating bottom frame for version and updates")
            self.bottom_frame = ttk.Frame(self.root)
            self.bottom_frame.pack(side='bottom', fill='x', padx=5, pady=5)

            # Version label
            logger.debug("Creating version label")
            self.version_label = ttk.Label(self.bottom_frame, text=f"v{PROJECT_VERSION}", font=('Segoe UI', 8),
                                           foreground='gray')
            self.version_label.pack(side='left')
            logger.debug("Version label created and packed")

            # Update notification frame
            logger.debug("Creating update notification frame")
            self.update_frame = ttk.Frame(self.bottom_frame)
            self.update_frame.pack(side='left', padx=(10, 0))

            logger.debug("Creating update notification components")
            # Update available label
            self.update_label = ttk.Label(self.update_frame, font=('Segoe UI', 8), foreground='#00aa00')

            # Update info label
            self.update_info_label = ttk.Label(self.update_frame, font=('Segoe UI', 8), foreground='gray')

            # Release notes link
            self.update_link = ttk.Label(self.update_frame, font=('Segoe UI', 8), foreground='#0066cc', cursor='hand2')
            self.update_link.bind('<Button-1>', self.open_release_notes)

            # Update now button
            self.update_now_button = ttk.Button(self.update_frame, style='Accent.TButton', command=self.update_now)
            logger.debug("Update notification components created")

            logger.info("Application initialized successfully")

        except Exception as e:
            logger.critical(
                "Failed to initialize application", extra={
                    'metadata': {'error': str(e), 'error_type': type(e).__name__, 'project': PROJECT_NAME,
                                 'version': PROJECT_VERSION}},
                exc_info=True
            )
            sys.exit(1)

    def show_update_notification(self):
        """Display update notification with details."""
        try:
            if self.latest_version:
                logger.debug("Showing update notification", extra={
                    'metadata': {'current_version': PROJECT_VERSION, 'new_version': self.latest_version,
                                 'release_url': self.release_url}})

                # Update available text
                logger.debug("Configuring update notification text")
                self.update_label.config(
                    text=TRANSLATIONS[self.current_lang]['update_available'].format(version=self.latest_version))
                self.update_label.pack(side='left')

                # Info about automatic installation
                logger.debug("Configuring update info text")
                self.update_info_label.config(text=TRANSLATIONS[self.current_lang]['update_info'])
                self.update_info_label.pack(side='left', padx=(5, 0))

                # Link to release notes
                logger.debug("Configuring release notes link")
                self.update_link.config(text=TRANSLATIONS[self.current_lang]['see_release'])
                self.update_link.pack(side='left', padx=(5, 0))

                # Update now button
                logger.debug("Configuring update now button")
                self.update_now_button.config(text=TRANSLATIONS[self.current_lang]['update_now'])
                self.update_now_button.pack(side='left', padx=(5, 0))

                logger.debug("Update notification components configured and packed")

        except Exception as e:
            logger.error("Failed to show update notification", extra={
                'metadata': {'error': str(e), 'error_type': type(e).__name__, 'latest_version': self.latest_version,
                             'release_url': self.release_url}}, exc_info=True)

    def open_release_notes(self, event=None):
        """Open release notes in default browser."""
        try:
            if self.release_url:
                logger.info("Opening release notes",
                            extra={'metadata': {'url': self.release_url, 'event': str(event) if event else None}})
                webbrowser.open(self.release_url)
                logger.debug("Release notes opened successfully")
        except Exception as e:
            logger.error("Failed to open release notes",
                         extra={'metadata': {'error': str(e), 'error_type': type(e).__name__, 'url': self.release_url}},
                         exc_info=True)

    def update_now(self):
        """Trigger immediate update."""
        try:
            logger.info("Immediate update requested")
            if self.update_installer_path:
                logger.debug("Starting immediate update process", extra={
                    'metadata': {'installer_path': self.update_installer_path, 'current_version': PROJECT_VERSION,
                                 'new_version': self.latest_version}})
                self.on_close()  # This will trigger the update
        except Exception as e:
            logger.error("Failed to trigger immediate update", extra={
                'metadata': {'error': str(e), 'error_type': type(e).__name__,
                             'installer_path': self.update_installer_path}}, exc_info=True)

    def on_close(self):
        """Handle application closing and trigger update if available."""
        try:
            logger.info("Application closing initiated")

            logger.debug("Destroying main window")
            self.root.destroy()
            logger.debug("Main window destroyed successfully")

            # Install update if available
            if self.update_installer_path:
                logger.info("Installing update after close", extra={
                    'metadata': {'installer_path': self.update_installer_path, 'current_version': PROJECT_VERSION,
                                 'new_version': self.latest_version}})
                install_update(self.update_installer_path)
                logger.debug("Update installation process initiated")

        except Exception as e:
            logger.error("Error during application close",
                         extra={'metadata': {'error': str(e), 'error_type': type(e).__name__}}, exc_info=True)

    def toggle_language(self):
        """Toggle between English and Polish language."""
        new_lang = None  # Initialize before try block
        try:
            # Switch language
            new_lang = 'pl' if self.current_lang == 'en' else 'en'
            logger.info("Language switch initiated", extra={'metadata': {'from': self.current_lang, 'to': new_lang}})
            self.current_lang = new_lang

            logger.debug("Updating window title")
            self.root.title(TRANSLATIONS[self.current_lang]['window_title'])

            logger.debug("Updating language button")
            self.lang_button.config(
                text=TRANSLATIONS[self.current_lang]['switch_to_pl']
                if self.current_lang == 'en'
                else TRANSLATIONS[self.current_lang]['switch_to_en']
            )

            logger.debug("Updating UI components language")
            self.ui.update_language(self.current_lang)

            logger.debug("Updating export button text")
            self.export_button.config(
                text=TRANSLATIONS[self.current_lang]['export_tree']
            )

            # Update the update notification if it's visible
            if self.latest_version:
                logger.debug("Updating update notification language")
                self.show_update_notification()

            logger.debug("Language switch completed successfully")

        except Exception as e:
            logger.error(
                "Failed to switch language",
                extra={
                    'metadata': {
                        'from_lang': self.current_lang, 'to_lang': new_lang, 'error': str(e),
                        'error_type': type(e).__name__
                    }
                },
                exc_info=True
            )

    def draw_tree(self):
        """Draw the Christmas tree with current parameters."""
        params = None  # Initialize before try block
        try:
            logger.debug("Drawing tree initiated")
            params = self.ui.get_parameters()
            logger.debug("Tree parameters obtained", extra={'metadata': params})

            logger.debug("Clearing canvas")
            self.drawer.clear_canvas()

            logger.debug("Drawing tree with parameters")
            self.drawer.draw_tree(params)

            logger.debug("Enabling export button")
            self.export_button.config(state="normal")

            logger.debug("Tree drawn successfully")

        except Exception as e:
            logger.error(
                "Failed to draw tree", extra={'metadata': {'error': str(e), 'error_type': type(e).__name__,
                                                           'params': params}},
                exc_info=True
            )

    def export_tree(self):
        """Export the tree as an image."""
        try:
            logger.info("Tree export initiated")
            logger.debug("Getting canvas for export")
            save_canvas_as_image(self.drawer.canvas)
            logger.info("Tree exported successfully")

        except Exception as e:
            logger.error(
                "Failed to export tree", extra={'metadata': {'error': str(e), 'error_type': type(e).__name__}},
                exc_info=True
            )

    def run(self):
        """Run the main application loop."""
        try:
            logger.info("Starting application main loop")

            # Check for updates
            logger.debug("Checking for updates")
            update_info = check_for_updates()

            if update_info:
                logger.debug("Update available, processing update info", extra={'metadata': update_info})
                self.update_installer_path = update_info['installer_path']
                self.latest_version = update_info['version']
                self.release_url = update_info['release_url']

                logger.debug("Showing update notification")
                self.show_update_notification()
            else:
                logger.debug("No updates available")

            logger.debug("Starting tkinter main loop")
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
