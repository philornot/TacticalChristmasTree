from tkinter import filedialog

from PIL import ImageGrab


def save_canvas_as_image(canvas):
    # Get canvas position and dimensions
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # Choose save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        # Capture canvas area screenshot
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(file_path)
