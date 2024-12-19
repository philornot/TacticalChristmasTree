import tkinter as tk
from tkinter import ttk
import sv_ttk
from tree_drawer import TreeDrawer
from ui_components import UIComponents
from file_handler import save_canvas_as_image
from translations import TRANSLATIONS


class TacticalChristmasTree:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tactical Christmas Tree")
        self.root.geometry("800x800")

        # Initial language setting
        self.current_lang = 'en'

        # Enable dark theme
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

    def toggle_language(self):
        # Switch language
        self.current_lang = 'pl' if self.current_lang == 'en' else 'en'

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

    def draw_tree(self):
        params = self.ui.get_parameters()
        self.drawer.clear_canvas()
        self.drawer.draw_tree(params)
        self.export_button.config(state="normal")

    def export_tree(self):
        save_canvas_as_image(self.drawer.canvas)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TacticalChristmasTree()
    app.run()