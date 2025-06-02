from PIL import Image, ImageDraw
import os

def create_texture(filename, color1, color2=None, pattern="solid"):
    """
    Create a simple texture file.
    filename: Name of the file to create
    color1: Main color (R,G,B)
    color2: Secondary color for patterns (R,G,B)
    pattern: 'solid', 'checkered', or 'gradient'
    """
    size = 64
    img = Image.new('RGB', (size, size), color=color1)
    
    if pattern == "checkered" and color2:
        draw = ImageDraw.Draw(img)
        for i in range(0, size, 16):
            for j in range(0, size, 16):
                if (i + j) % 32 == 0:
                    draw.rectangle([i, j, i+16, j+16], fill=color2)
    
    elif pattern == "gradient" and color2:
        draw = ImageDraw.Draw(img)
        for y in range(size):
            r = int(color1[0] + (color2[0] - color1[0]) * y / size)
            g = int(color1[1] + (color2[1] - color1[1]) * y / size)
            b = int(color1[2] + (color2[2] - color1[2]) * y / size)
            draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # Try to remove existing file first
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Removed existing file: {filename}")
    except Exception as e:
        print(f"Error removing {filename}: {e}")
    
    # Save the image
    try:
        img.save(filename, "PNG")
        print(f"Created texture: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# Create basic textures
create_texture("grass.png", (76, 153, 0), (0, 100, 0), "checkered")
create_texture("dirt.png", (101, 67, 33), (82, 46, 21), "checkered")
create_texture("stone.png", (128, 128, 128), (100, 100, 100), "checkered")
create_texture("wood.png", (133, 94, 66), (98, 73, 44), "gradient")
create_texture("brick.png", (156, 102, 68), (145, 62, 41), "checkered")
create_texture("glass.png", (200, 255, 255), (180, 235, 235), "solid")
create_texture("water.png", (64, 164, 223), (52, 152, 219), "gradient")

print("All textures created successfully!")
