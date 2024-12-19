# ui_components.py
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor


class UIComponents:
    def __init__(self, root, draw_callback):
        self.frame = ttk.Frame(root)
        self.frame.pack(pady=10, padx=10)

        # Store callback first
        self.draw_callback = draw_callback

        # Tree parameters
        self.height_var = tk.IntVar(value=300)
        self.width_var = tk.IntVar(value=200)
        self.layers_var = tk.IntVar(value=5)
        self.color_var = tk.StringVar(value='#2E8B57')

        # Create controls
        self._create_controls()

    def _create_controls(self):
        # Height control
        ttk.Label(self.frame, text="Height:").grid(row=0, column=0, padx=5, pady=5)
        height_scale = ttk.Scale(
            self.frame,
            from_=100,
            to=350,
            variable=self.height_var,
            orient="horizontal"
        )
        height_scale.grid(row=0, column=1, padx=5, pady=5)

        # Width control
        ttk.Label(self.frame, text="Width:").grid(row=1, column=0, padx=5, pady=5)
        width_scale = ttk.Scale(
            self.frame,
            from_=100,
            to=300,
            variable=self.width_var,
            orient="horizontal"
        )
        width_scale.grid(row=1, column=1, padx=5, pady=5)

        # Layers control
        ttk.Label(self.frame, text="Layers:").grid(row=2, column=0, padx=5, pady=5)
        layers_scale = ttk.Scale(
            self.frame,
            from_=3,
            to=8,
            variable=self.layers_var,
            orient="horizontal"
        )
        layers_scale.grid(row=2, column=1, padx=5, pady=5)

        # Color control
        ttk.Label(self.frame, text="Color:").grid(row=3, column=0, padx=5, pady=5)
        color_button = ttk.Button(
            self.frame,
            text="Choose color",
            command=self._choose_color
        )
        color_button.grid(row=3, column=1, padx=5, pady=5)

        # Draw button
        draw_button = ttk.Button(
            self.frame,
            text="Draw Tree",
            command=self.draw_callback
        )
        draw_button.grid(row=4, column=0, columnspan=2, pady=10)

    def _choose_color(self):
        # Default color if nothing is selected
        current_color = self.color_var.get() or '#2E8B57'
        try:
            result = askcolor(color=current_color)
            # Only update if we got a valid color hex value
            if result is not None and isinstance(result, tuple) and len(result) > 1 and isinstance(result[1], str):
                self.color_var.set(result[1])
        except Exception:
            # W przypadku błędu zachowaj aktualny kolor
            pass

    def get_parameters(self):
        return {
            'height': self.height_var.get(),
            'width': self.width_var.get(),
            'layers': self.layers_var.get(),
            'color': self.color_var.get()
        }