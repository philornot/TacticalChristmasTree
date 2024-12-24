# tree_drawer.py
import tkinter as tk
import random
import math

from logger import NiceLogger

# Initialize logger
logger = NiceLogger(__name__).get_logger()


class TreeDrawer:
    def __init__(self, root):
        logger.debug("Initializing TreeDrawer")
        self.canvas = tk.Canvas(
            root,
            width=600,
            height=400,
            bg='#2b2b2b'  # Dark background
        )
        self.canvas.pack(pady=10)

    def get_random_color(self):
        """Generate a random bright color for decorations."""
        # Using brighter colors for decorations
        colors = [
            '#FF0000', '#FFD700', '#00FF00', '#FF69B4', '#00FFFF',
            '#FF4500', '#9400D3', '#FF1493', '#00FF7F', '#FF8C00'
        ]
        return random.choice(colors)

    def is_point_in_triangle(self, px, py, x1, y1, x2, y2, x3, y3):
        """Check if point (px,py) is inside triangle with vertices (x1,y1), (x2,y2), (x3,y3)."""

        def sign(x1, y1, x2, y2, x3, y3):
            return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

        d1 = sign(px, py, x1, y1, x2, y2)
        d2 = sign(px, py, x2, y2, x3, y3)
        d3 = sign(px, py, x3, y3, x1, y1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def draw_ornament(self, x, y, size=8):
        """Draw a Christmas ornament (bauble)."""
        color = self.get_random_color()
        # Draw the bauble
        self.canvas.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill=color,
            outline='#1f1f1f'
        )
        # Draw the cap of the bauble
        self.canvas.create_rectangle(
            x - size / 3, y - size - 2,
            x + size / 3, y - size,
            fill='#C0C0C0',
            outline='#1f1f1f'
        )

    def draw_chain_segment(self, x1, y1, x2, y2):
        """Draw a segment of a decorative chain."""
        color = self.get_random_color()
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=2,
            smooth=True
        )

    def clear_canvas(self):
        """Clear the canvas."""
        logger.debug("Clearing canvas")
        self.canvas.delete("all")

    def draw_tree(self, params):
        """Draw the Christmas tree based on provided parameters."""
        try:
            logger.debug("Drawing tree", extra={'metadata': params})

            # Extract parameters for the tree
            height = params['height']
            width = params['width']
            layers = params['layers']
            color = params['color']
            ornaments = params.get('ornaments', 5)
            chains = params.get('chains', 3)

            # Center the tree on the canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            start_x = canvas_width // 2
            start_y = canvas_height - 100

            # Calculate the height available for layers (excluding trunk)
            usable_height = height - 50
            layer_height = usable_height / layers

            # Store layer triangles for decoration placement
            layer_triangles = []

            # Draw layers from bottom to top
            for i in range(layers):
                current_layer = layers - i - 1
                layer_width = width * ((current_layer + 1) / layers)

                y_bottom = start_y - (i * layer_height)
                y_top = y_bottom - layer_height

                x_left = start_x - (layer_width / 2)
                x_right = start_x + (layer_width / 2)

                points = [
                    x_left, y_bottom,  # Bottom left
                    x_right, y_bottom,  # Bottom right
                    start_x, y_top  # Top center
                ]

                # Store triangle vertices for later use
                layer_triangles.append({
                    'vertices': [(x_left, y_bottom), (x_right, y_bottom), (start_x, y_top)],
                    'width': layer_width,
                    'y_bottom': y_bottom,
                    'y_top': y_top,
                    'center_x': start_x
                })

                # Create the triangle for this layer
                self.canvas.create_polygon(
                    points,
                    fill=color,
                    outline='#1f1f1f'
                )

            # Draw the trunk
            trunk_width = width / 6
            trunk_height = 50
            self.canvas.create_rectangle(
                start_x - trunk_width / 2,
                start_y,
                start_x + trunk_width / 2,
                start_y + trunk_height,
                fill='#8B4513',
                outline='#1f1f1f'
            )

            # Add ornaments
            attempts = 0
            ornaments_placed = 0
            max_attempts = ornaments * 10  # Limit attempts to avoid infinite loops

            while ornaments_placed < ornaments and attempts < max_attempts:
                attempts += 1

                # Select random layer
                layer = random.choice(layer_triangles)

                # Generate random position
                x_offset = random.uniform(-0.8, 0.8) * (layer['width'] / 2)
                y_offset = random.uniform(0.2, 0.8) * (layer['y_bottom'] - layer['y_top'])

                ornament_x = layer['center_x'] + x_offset
                ornament_y = layer['y_bottom'] - y_offset

                # Check if the ornament is inside the triangle
                vertices = layer['vertices']
                if self.is_point_in_triangle(
                        ornament_x, ornament_y,
                        vertices[0][0], vertices[0][1],  # Left point
                        vertices[1][0], vertices[1][1],  # Right point
                        vertices[2][0], vertices[2][1]  # Top point
                ):
                    self.draw_ornament(ornament_x, ornament_y)
                    ornaments_placed += 1

            # Add chains
            for _ in range(chains):
                # Select two different layers for chain endpoints
                layer_indices = sorted(random.sample(range(len(layer_triangles)), 2))
                start_layer = layer_triangles[layer_indices[0]]
                end_layer = layer_triangles[layer_indices[1]]

                # Create a wavy chain effect
                segments = 6
                prev_x = start_layer['center_x']
                prev_y = start_layer['y_bottom'] - random.uniform(0.2, 0.8) * (
                            start_layer['y_bottom'] - start_layer['y_top'])

                for s in range(1, segments + 1):
                    progress = s / segments

                    # Calculate next point with controlled randomness
                    next_x = start_layer['center_x'] + (random.uniform(-0.3, 0.3) * start_layer['width'])
                    next_y = start_layer['y_bottom'] - (progress * (start_layer['y_bottom'] - end_layer['y_bottom']))

                    # Add some wave effect
                    wave_offset = math.sin(progress * math.pi) * 10
                    next_x += wave_offset

                    self.draw_chain_segment(prev_x, prev_y, next_x, next_y)
                    prev_x, prev_y = next_x, next_y

            logger.debug("Tree drawn successfully with decorations")

        except Exception as e:
            logger.error(
                "Failed to draw tree",
                extra={
                    'metadata': {
                        'params': params,
                        'error': str(e)
                    }
                },
                exc_info=True
            )