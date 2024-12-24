import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

from logger import NiceLogger
from settings import (
    MIN_HEIGHT, MAX_HEIGHT,
    MIN_WIDTH, MAX_WIDTH,
    MIN_LAYERS, MAX_LAYERS,
    MIN_ORNAMENTS, MAX_ORNAMENTS,
    DEFAULT_COLOR,
    DEFAULT_ORNAMENTS
)
from translations import TRANSLATIONS

# Initialize logger
logger = NiceLogger(__name__).get_logger()


class UIComponents:
    def __init__(self, root, draw_callback, initial_lang='en'):
        logger.debug("Initializing UI components", extra={
            'metadata': {'initial_lang': initial_lang}
        })

        self.frame = ttk.Frame(root)
        self.frame.pack(pady=10, padx=10)

        self.draw_callback = draw_callback
        self.current_lang = initial_lang

        # Tree parameters with validation
        self.height_var = tk.IntVar(value=300)
        self.width_var = tk.IntVar(value=200)
        self.layers_var = tk.IntVar(value=5)
        self.color_var = tk.StringVar(value=DEFAULT_COLOR)
        self.ornaments_var = tk.IntVar(value=DEFAULT_ORNAMENTS)

        self._create_controls()
        logger.debug("UI components initialized successfully")

    def update_language(self, new_lang):
        """Update UI language."""
        try:
            logger.debug(f"Updating language to: {new_lang}")
            self.current_lang = new_lang

            # Update all labels
            for key, label in self.labels.items():
                label.config(text=TRANSLATIONS[self.current_lang][key])

            # Update buttons
            self.color_button.config(
                text=TRANSLATIONS[self.current_lang]['choose_color']
            )
            self.draw_button.config(
                text=TRANSLATIONS[self.current_lang]['draw_tree']
            )

            logger.debug("Language update completed successfully")

        except Exception as e:
            logger.error(
                "Failed to update language",
                extra={
                    'metadata': {
                        'new_lang': new_lang,
                        'error': str(e)
                    }
                },
                exc_info=True
            )

    def _choose_color(self):
        """Open color picker dialog."""
        try:
            logger.debug("Opening color picker")
            current_color = self.color_var.get() or DEFAULT_COLOR

            result = askcolor(color=current_color)
            if result is not None and isinstance(result, tuple) and len(result) > 1:
                color_code = result[1]
                logger.debug(f"Color selected: {color_code}")
                self.color_var.set(color_code)
            else:
                logger.debug("Color selection cancelled")

        except Exception as e:
            logger.error(
                "Failed to handle color selection",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )

    def get_parameters(self):
        """Get current tree parameters."""
        try:
            params = {
                'height': self.height_var.get(),
                'width': self.width_var.get(),
                'layers': self.layers_var.get(),
                'color': self.color_var.get() or DEFAULT_COLOR,
                'ornaments': self.ornaments_var.get()
            }
            logger.debug("Retrieved parameters", extra={'metadata': params})
            return params

        except Exception as e:
            logger.error(
                "Failed to get parameters",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )
            # Return default values in case of error
            return {
                'height': 300,
                'width': 200,
                'layers': 5,
                'color': DEFAULT_COLOR,
                'ornaments': DEFAULT_ORNAMENTS
            }

    def _create_controls(self):
        """Create all UI controls."""
        try:
            logger.debug("Creating UI controls")

            # Store references to labels for language updates
            self.labels = {}

            # Height control
            self.labels['height'] = ttk.Label(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['height']
            )
            self.labels['height'].grid(row=0, column=0, padx=5, pady=5, sticky='w')

            height_scale = ttk.Scale(
                self.frame,
                from_=MIN_HEIGHT,
                to=MAX_HEIGHT,
                variable=self.height_var,
                orient="horizontal"
            )
            height_scale.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

            # Width control
            self.labels['width'] = ttk.Label(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['width']
            )
            self.labels['width'].grid(row=1, column=0, padx=5, pady=5, sticky='w')

            width_scale = ttk.Scale(
                self.frame,
                from_=MIN_WIDTH,
                to=MAX_WIDTH,
                variable=self.width_var,
                orient="horizontal"
            )
            width_scale.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

            # Layers control
            self.labels['layers'] = ttk.Label(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['layers']
            )
            self.labels['layers'].grid(row=2, column=0, padx=5, pady=5, sticky='w')

            layers_scale = ttk.Scale(
                self.frame,
                from_=MIN_LAYERS,
                to=MAX_LAYERS,
                variable=self.layers_var,
                orient="horizontal"
            )
            layers_scale.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

            # Color control
            self.labels['color'] = ttk.Label(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['color']
            )
            self.labels['color'].grid(row=3, column=0, padx=5, pady=5, sticky='w')

            self.color_button = ttk.Button(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['choose_color'],
                command=self._choose_color
            )
            self.color_button.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

            # Ornaments control
            self.labels['ornaments'] = ttk.Label(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['ornaments']
            )
            self.labels['ornaments'].grid(row=4, column=0, padx=5, pady=5, sticky='w')

            ornaments_scale = ttk.Scale(
                self.frame,
                from_=MIN_ORNAMENTS,
                to=MAX_ORNAMENTS,
                variable=self.ornaments_var,
                orient="horizontal"
            )
            ornaments_scale.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

            # Draw button
            self.draw_button = ttk.Button(
                self.frame,
                text=TRANSLATIONS[self.current_lang]['draw_tree'],
                command=self.draw_callback,
                style='Accent.TButton'
            )
            self.draw_button.grid(row=5, column=0, columnspan=2, pady=20)

            # Configure grid column weights for proper scaling
            self.frame.grid_columnconfigure(1, weight=1)

            logger.debug("UI controls created successfully")

        except Exception as e:
            logger.error(
                "Failed to create UI controls",
                extra={'metadata': {'error': str(e)}},
                exc_info=True
            )