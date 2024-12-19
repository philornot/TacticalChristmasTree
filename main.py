import tkinter as tk
from tkinter import ttk
import sv_ttk
from tree_drawer import TreeDrawer
from ui_components import UIComponents
from file_handler import save_canvas_as_image


class ChristmasTreeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tactical Christmas Tree")
        self.root.geometry("800x800")

        # Enable dark theme
        sv_ttk.set_theme("dark")

        # Initialize components
        self.ui = UIComponents(self.root, self.draw_tree)
        self.drawer = TreeDrawer(self.root)

        # Export button with padding
        self.export_button = ttk.Button(
            self.root,
            text="Export Tree",
            command=self.export_tree,
            state="disabled"
        )
        self.export_button.pack(pady=20)

    def draw_tree(self):
        # Get parameters from UI
        params = self.ui.get_parameters()

        # Clear and draw new tree
        self.drawer.clear_canvas()
        self.drawer.draw_tree(params)

        # Enable export button
        self.export_button.config(state="normal")

    def export_tree(self):
        save_canvas_as_image(self.drawer.canvas)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ChristmasTreeApp()
    app.run()