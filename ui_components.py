import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

from translations import TRANSLATIONS


class UIComponents:
    def __init__(self, root, draw_callback, initial_lang='en'):
        self.frame = ttk.Frame(root)
        self.frame.pack(pady=10, padx=10)

        self.draw_callback = draw_callback
        self.current_lang = initial_lang

        # Tree parameters
        self.height_var = tk.IntVar(value=300)
        self.width_var = tk.IntVar(value=200)
        self.layers_var = tk.IntVar(value=5)
        self.color_var = tk.StringVar(value='#2E8B57')

        self._create_controls()

    def _create_controls(self):
        # Store references to labels and buttons for language updates
        self.labels = {'height': ttk.Label(self.frame, text=TRANSLATIONS[self.current_lang]['height'])}

        # Height control
        self.labels['height'].grid(row=0, column=0, padx=5, pady=5)
        height_scale = ttk.Scale(
            self.frame,
            from_=100,
            to=350,
            variable=self.height_var,
            orient="horizontal"
        )
        height_scale.grid(row=0, column=1, padx=5, pady=5)

        # Width control
        self.labels['width'] = ttk.Label(self.frame, text=TRANSLATIONS[self.current_lang]['width'])
        self.labels['width'].grid(row=1, column=0, padx=5, pady=5)
        width_scale = ttk.Scale(
            self.frame,
            from_=100,
            to=300,
            variable=self.width_var,
            orient="horizontal"
        )
        width_scale.grid(row=1, column=1, padx=5, pady=5)

        # Layers control
        self.labels['layers'] = ttk.Label(self.frame, text=TRANSLATIONS[self.current_lang]['layers'])
        self.labels['layers'].grid(row=2, column=0, padx=5, pady=5)
        layers_scale = ttk.Scale(
            self.frame,
            from_=3,
            to=8,
            variable=self.layers_var,
            orient="horizontal"
        )
        layers_scale.grid(row=2, column=1, padx=5, pady=5)

        # Color control
        self.labels['color'] = ttk.Label(self.frame, text=TRANSLATIONS[self.current_lang]['color'])
        self.labels['color'].grid(row=3, column=0, padx=5, pady=5)
        self.color_button = ttk.Button(
            self.frame,
            text=TRANSLATIONS[self.current_lang]['choose_color'],
            command=self._choose_color
        )
        self.color_button.grid(row=3, column=1, padx=5, pady=5)

        # Draw button
        self.draw_button = ttk.Button(
            self.frame,
            text=TRANSLATIONS[self.current_lang]['draw_tree'],
            command=self.draw_callback
        )
        self.draw_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_language(self, new_lang):
        self.current_lang = new_lang

        # Update all labels
        for key, label in self.labels.items():
            label.config(text=TRANSLATIONS[self.current_lang][key])

        # Update buttons
        self.color_button.config(text=TRANSLATIONS[self.current_lang]['choose_color'])
        self.draw_button.config(text=TRANSLATIONS[self.current_lang]['draw_tree'])

    def _choose_color(self):
        current_color = self.color_var.get() or '#2E8B57'
        try:
            result = askcolor(color=current_color)
            if result is not None and isinstance(result, tuple) and len(result) > 1 and isinstance(result[1], str):
                self.color_var.set(result[1])
        except Exception:
            pass

    def get_parameters(self):
        return {
            'height': self.height_var.get(),
            'width': self.width_var.get(),
            'layers': self.layers_var.get(),
            'color': self.color_var.get()
        }