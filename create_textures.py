from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np

def add_noise(image, intensity=0.1):
    """Add subtle noise to make texture more realistic"""
    pixels = np.array(image)
    noise = np.random.normal(0, intensity * 255, pixels.shape)
    noisy_pixels = np.clip(pixels + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_pixels)

def add_detail_lines(draw, size, color, num_lines=3):
    """Add detail lines to texture"""
    for _ in range(num_lines):
        x1 = random.randint(0, size)
        y1 = random.randint(0, size)
        x2 = random.randint(0, size)
        y2 = random.randint(0, size)
        line_color = tuple(max(0, min(255, c + random.randint(-20, 20))) for c in color)
        draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)

def add_spots(draw, size, base_color, num_spots=5):
    """Add random spots for texture detail"""
    for _ in range(num_spots):
        x = random.randint(0, size - 5)
        y = random.randint(0, size - 5)
        spot_size = random.randint(2, 4)
        spot_color = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in base_color)
        draw.ellipse([x, y, x + spot_size, y + spot_size], fill=spot_color)

def create_grass_texture():
    """Create detailed grass texture"""
    size = 64
    image = Image.new('RGB', (size, size), (34, 139, 34))  # Forest green base
    draw = ImageDraw.Draw(image)
    
    # Add grass blade details
    for _ in range(20):
        x = random.randint(0, size - 2)
        y = random.randint(0, size - 8)
        blade_color = (random.randint(20, 50), random.randint(120, 160), random.randint(20, 50))
        draw.line([(x, y), (x + random.randint(-1, 1), y + random.randint(4, 8))], 
                 fill=blade_color, width=1)
    
    # Add some darker spots for depth
    add_spots(draw, size, (25, 100, 25), 8)
    
    # Add subtle noise
    image = add_noise(image, 0.05)
    
    return image

def create_dirt_texture():
    """Create detailed dirt texture - darker, more earthy"""
    size = 64
    base_color = (92, 51, 23)  # Much darker brown/earth tone
    image = Image.new('RGB', (size, size), base_color)
    draw = ImageDraw.Draw(image)
    
    # Add rich soil patches with varied earth tones
    for _ in range(25):
        x = random.randint(0, size - 4)
        y = random.randint(0, size - 4)
        patch_size = random.randint(2, 5)
        # Use darker earth colors
        patch_color = (
            random.randint(60, 100),  # Dark brown/red
            random.randint(35, 60),   # Dark brown
            random.randint(15, 35)    # Very dark brown
        )
        draw.ellipse([x, y, x + patch_size, y + patch_size], fill=patch_color)
    
    # Add clay-like streaks
    for _ in range(8):
        x1 = random.randint(0, size)
        y1 = random.randint(0, size)
        x2 = x1 + random.randint(-8, 8)
        y2 = y1 + random.randint(-3, 3)
        clay_color = (random.randint(70, 90), random.randint(40, 55), random.randint(20, 30))
        draw.line([(x1, y1), (x2, y2)], fill=clay_color, width=2)
    
    # Add small pebbles and debris
    for _ in range(12):
        x = random.randint(0, size - 2)
        y = random.randint(0, size - 2)
        pebble_color = (random.randint(100, 130), random.randint(90, 110), random.randint(80, 100))
        draw.ellipse([x, y, x + 2, y + 2], fill=pebble_color)
    
    # Add earthy noise
    image = add_noise(image, 0.12)
    
    return image

def create_stone_texture():
    """Create detailed stone texture"""
    size = 64
    base_color = (128, 128, 128)  # Gray
    image = Image.new('RGB', (size, size), base_color)
    draw = ImageDraw.Draw(image)
    
    # Add stone cracks
    for _ in range(8):
        x1 = random.randint(0, size)
        y1 = random.randint(0, size)
        x2 = x1 + random.randint(-10, 10)
        y2 = y1 + random.randint(-10, 10)
        crack_color = tuple(max(0, c - random.randint(20, 40)) for c in base_color)
        draw.line([(x1, y1), (x2, y2)], fill=crack_color, width=random.randint(1, 2))
    
    # Add mineral spots
    for _ in range(10):
        x = random.randint(0, size - 4)
        y = random.randint(0, size - 4)
        mineral_color = tuple(max(0, min(255, c + random.randint(-20, 60))) for c in base_color)
        draw.ellipse([x, y, x + random.randint(2, 4), y + random.randint(2, 4)], fill=mineral_color)
    
    # Add texture noise
    image = add_noise(image, 0.06)
    
    return image

def create_wood_texture():
    """Create detailed wood texture - realistic brown wood with prominent grain"""
    size = 64
    base_color = (139, 101, 60)  # Realistic medium brown wood color
    image = Image.new('RGB', (size, size), base_color)
    draw = ImageDraw.Draw(image)
    
    # Create prominent vertical wood grain lines
    for x in range(0, size, 2):
        for y in range(size):
            # Create wavy grain pattern
            wave_offset = int(3 * np.sin(y * 0.3 + x * 0.1))
            if 0 <= x + wave_offset < size:
                grain_color = (
                    random.randint(120, 160),  # Medium brown
                    random.randint(80, 120),   # Darker brown
                    random.randint(40, 80)     # Dark brown accent
                )
                draw.point((x + wave_offset, y), fill=grain_color)
    
    # Add distinct wood rings/circles for tree growth patterns
    center_x, center_y = size // 2, size // 2
    for radius in range(5, 35, 6):
        ring_color = (
            max(80, base_color[0] - random.randint(20, 40)),
            max(60, base_color[1] - random.randint(20, 40)),
            max(30, base_color[2] - random.randint(10, 20))
        )
        # Draw partial rings for natural look
        for angle in range(0, 360, 3):
            x = int(center_x + radius * np.cos(np.radians(angle)))
            y = int(center_y + radius * np.sin(np.radians(angle)))
            if 0 <= x < size and 0 <= y < size:
                draw.point((x, y), fill=ring_color)
    
    # Add prominent wood knots
    for _ in range(2):
        center_x = random.randint(15, size - 15)
        center_y = random.randint(15, size - 15)
        knot_color = (random.randint(70, 100), random.randint(50, 80), random.randint(25, 45))
        # Draw concentric circles for knot
        for r in range(1, 8):
            draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                        outline=knot_color, width=1)
    
    # Add lighter wood highlights (still brown tones)
    for _ in range(15):
        x = random.randint(0, size - 3)
        y = random.randint(0, size - 8)
        highlight_color = (random.randint(160, 180), random.randint(120, 140), random.randint(70, 90))
        draw.line([(x, y), (x + random.randint(-1, 1), y + random.randint(4, 8))], 
                 fill=highlight_color, width=1)
    
    # Minimal noise to preserve grain detail
    image = add_noise(image, 0.03)
    
    return image

def create_brick_texture():
    """Create detailed brick texture"""
    size = 64
    mortar_color = (200, 200, 200)  # Light gray mortar
    brick_color = (178, 34, 34)     # Fire brick
    
    image = Image.new('RGB', (size, size), mortar_color)
    draw = ImageDraw.Draw(image)
    
    # Draw brick pattern
    brick_height = 8
    brick_width = 16
    mortar_width = 2
    
    for row in range(0, size, brick_height + mortar_width):
        offset = (brick_width // 2) if (row // (brick_height + mortar_width)) % 2 else 0
        for col in range(-offset, size, brick_width + mortar_width):
            # Draw individual brick
            x1 = col
            y1 = row
            x2 = min(col + brick_width, size)
            y2 = min(row + brick_height, size)
            
            if x1 < size and y1 < size:
                # Vary brick color slightly
                varied_color = tuple(max(0, min(255, c + random.randint(-20, 20))) for c in brick_color)
                draw.rectangle([x1, y1, x2, y2], fill=varied_color)
    
    # Add wear and aging
    add_spots(draw, size, brick_color, 15)
    image = add_noise(image, 0.03)
    
    return image

def create_water_texture():
    """Create animated water texture"""
    size = 64
    base_color = (64, 164, 223)  # Deep sky blue
    image = Image.new('RGB', (size, size), base_color)
    draw = ImageDraw.Draw(image)
    
    # Add wave patterns
    for y in range(0, size, 4):
        for x in range(size):
            wave_intensity = np.sin(x * 0.3) * 10 + np.sin(y * 0.2) * 5
            wave_color = tuple(max(0, min(255, int(c + wave_intensity))) for c in base_color)
            draw.point((x, y), fill=wave_color)
    
    # Add ripple effects
    for _ in range(5):
        center_x = random.randint(10, size - 10)
        center_y = random.randint(10, size - 10)
        for radius in range(2, 8, 2):
            ripple_color = tuple(max(0, min(255, c + random.randint(-15, 15))) for c in base_color)
            draw.ellipse([center_x - radius, center_y - radius, 
                         center_x + radius, center_y + radius], outline=ripple_color)
    
    return image

def create_glass_texture():
    """Create semi-transparent glass texture"""
    size = 64
    base_color = (173, 216, 230)  # Light blue
    image = Image.new('RGBA', (size, size), (*base_color, 100))  # Semi-transparent
    draw = ImageDraw.Draw(image)
    
    # Add glass reflections
    for _ in range(8):
        x1 = random.randint(0, size)
        y1 = random.randint(0, size)
        x2 = x1 + random.randint(-15, 15)
        y2 = y1 + random.randint(-15, 15)
        reflection_color = (*base_color, random.randint(50, 150))
        draw.line([(x1, y1), (x2, y2)], fill=reflection_color, width=1)
    
    # Convert back to RGB for compatibility
    background = Image.new('RGB', (size, size), (255, 255, 255))
    image = Image.alpha_composite(background.convert('RGBA'), image).convert('RGB')
    
    return image

def create_all_textures():
    """Create all block textures and save them"""
    textures = {
        'grass.png': create_grass_texture,
        'dirt.png': create_dirt_texture,
        'stone.png': create_stone_texture,
        'wood.png': create_wood_texture,
        'brick.png': create_brick_texture,
        'water.png': create_water_texture,
        'glass.png': create_glass_texture
    }
    
    print("Creating detailed block textures...")
    
    for filename, create_func in textures.items():
        print(f"Creating {filename}...")
        texture = create_func()
        texture.save(filename)
        print(f"Saved {filename}")
    
    print("All textures created successfully!")

if __name__ == "__main__":
    create_all_textures()
