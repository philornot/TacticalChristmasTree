import tkinter as tk


class TreeDrawer:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=600, height=400, bg='#2b2b2b'  # Dark background
        )
        self.canvas.pack(pady=10)

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_tree(self, params):
        # Extract parameters for the tree
        height = params['height']
        width = params['width']
        layers = params['layers']
        color = params['color']

        # Center the tree on the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        start_x = canvas_width // 2
        start_y = canvas_height - 100  # Leave more space for the trunk

        # Calculate the height available for layers (excluding trunk)
        usable_height = height - 50
        layer_height = usable_height / layers

        # Draw layers from bottom to top
        for i in range(layers):
            # Calculate current layer number (reversed to start from bottom)
            current_layer = layers - i - 1

            # Calculate layer width - widest at bottom, narrowest at top
            layer_width = width * ((current_layer + 1) / layers)

            # Calculate y-coordinates for the current triangle
            y_bottom = start_y - (i * layer_height)
            y_top = y_bottom - layer_height

            # Define triangle points:
            # - Two points at the bottom (left and right)
            # - One point at the top (center)
            points = [
                start_x - (layer_width / 2), y_bottom,  # Bottom left
                start_x + (layer_width / 2), y_bottom,  # Bottom right
                start_x, y_top  # Top center
            ]

            # Create the triangle for this layer
            self.canvas.create_polygon(
                points,
                fill=color,
                outline='#1f1f1f'  # Dark outline for better visibility
            )

        # Draw the trunk at the bottom
        trunk_width = width / 6
        trunk_height = 50
        self.canvas.create_rectangle(
            start_x - trunk_width / 2,  # Left side of trunk
            start_y,  # Top of trunk
            start_x + trunk_width / 2,  # Right side of trunk
            start_y + trunk_height,  # Bottom of trunk
            fill='#8B4513',  # Brown color for trunk
            outline='#1f1f1f'  # Dark outline
        )