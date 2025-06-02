from ursina import*
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.fullscreen = False
window.title = 'Minecraft Clone'

# Add textures dictionary for different block types
block_types = ['grass', 'stone', 'dirt', 'wood', 'brick', 'glass', 'water']
current_block_type = 0  # Index to track current block type

# Block colors (for special rendering)
block_colors = {
    'grass': color.white,
    'stone': color.white,
    'dirt': color.white,
    'wood': color.white,
    'brick': color.white,
    'glass': color.rgba(255, 255, 255, 120),  # semi-transparent
    'water': color.rgba(70, 130, 180, 180),  # semi-transparent blue
}

# Game states
day_night_cycle = 0  # 0-100 where 0 is noon and 50 is midnight
day_speed = 0.1  # How fast the day changes

player = FirstPersonController(jump_height=2, jump_duration=0.3)
Sky()

# Create text UI for instructions and block selection
instructions = Text(
    text="Left click: Place block\nRight click: Remove block\nScroll wheel: Change block type\nF: Toggle day/night",
    position=(-0.85, 0.45),
    scale=0.8,
    color=color.white
)

block_display = Text(
    text=f"Current block: grass",
    position=(-0.85, 0.4),
    scale=0.8, 
    color=color.white
)

# Block count text (replacing game mode)
block_count_text = Text(
    text=f"Block type: {block_types[current_block_type]}",
    position=(-0.85, 0.35),
    scale=0.8,
    color=color.white
)

# Time display
time_display = Text(
    text="Time: Day",
    position=(-0.85, 0.30),
    scale=0.8,
    color=color.white
)

# Generate simple terrain with hills
boxes = []
for i in range(30):  # Expanded world size
    for j in range(30):
        # Create varied terrain height
        height = random.randint(0, 2)
        for k in range(height + 1):
            # Choose block texture based on height
            if k == height:
                texture_name = 'grass.png'  # Top layer is grass
            else:
                texture_name = 'dirt.png'   # Lower layers are dirt
                
            box = Button(
                color=color.white,
                model='cube',
                position=(j-15, k-1, i-15),  # Centered around player
                texture=texture_name,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)

# Generate a small lake
lake_x = random.randint(-10, 10)
lake_z = random.randint(-10, 10)
for lx in range(lake_x-3, lake_x+4):
    for lz in range(lake_z-3, lake_z+4):
        # Only add water if within an oval shape
        if ((lx-lake_x)**2 + (lz-lake_z)**2) < 16:
            box = Button(
                color=block_colors['water'],
                model='cube',
                position=(lx, -0.5, lz),  # Slightly lower than ground level
                texture='water.png',
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)

# Generate some random stone blocks
for _ in range(20):
    x = random.randint(-15, 15)
    z = random.randint(-15, 15)
    y = random.randint(-1, 1)
    
    box = Button(
        color=color.white,
        model='cube',
        position=(x, y, z),
        texture='stone.png',
        parent=scene,
        origin_y=0.5
    )
    boxes.append(box)

# Generate some random trees
for _ in range(8):
    x = random.randint(-14, 14)
    z = random.randint(-14, 14)
    
    # Tree trunk
    for y in range(4):
        box = Button(
            color=color.white,
            model='cube',
            position=(x, y, z),
            texture='wood.png',
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)
    
    # Tree leaves
    for lx in range(x-2, x+3):
        for ly in range(4, 7):
            for lz in range(z-2, z+3):
                # Skip some blocks to make the leaves less cube-like
                if random.random() < 0.7:
                    box = Button(
                        color=color.green,
                        model='cube',
                        position=(lx, ly, lz),
                        texture='grass.png',
                        parent=scene,
                        origin_y=0.5
                    )
                    boxes.append(box)

# Generate a small house
house_x = random.randint(-10, 10)
house_z = random.randint(-10, 10)

# House foundation
for x in range(house_x, house_x+5):
    for z in range(house_z, house_z+5):
        box = Button(
            color=color.white,
            model='cube',
            position=(x, 0, z),
            texture='brick.png',
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

# House walls
for x in range(house_x, house_x+5):
    for y in range(1, 4):
        for z in range(house_z, house_z+5):
            # Skip if it's not a wall
            if x > house_x and x < house_x+4 and z > house_z and z < house_z+4:
                continue
            # Add door
            if x == house_x+2 and z == house_z and y < 3:
                continue
            # Add windows
            if ((x == house_x+1 or x == house_x+3) and z == house_z and y == 2) or \
               ((z == house_z+1 or z == house_z+3) and x == house_x and y == 2):
                box = Button(
                    color=block_colors['glass'],
                    model='cube',
                    position=(x, y, z),
                    texture='glass.png',
                    parent=scene,
                    origin_y=0.5
                )
            else:
                box = Button(
                    color=color.white,
                    model='cube',
                    position=(x, y, z),
                    texture='brick.png',
                    parent=scene,
                    origin_y=0.5
                )
            boxes.append(box)

# House roof
for x in range(house_x-1, house_x+6):
    for z in range(house_z-1, house_z+6):
        box = Button(
            color=color.white,
            model='cube',
            position=(x, 4, z),
            texture='wood.png',
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

def lerp_color(color1, color2, t):
    # Custom function to linearly interpolate between two colors
    r = color1[0] + (color2[0] - color1[0]) * t
    g = color1[1] + (color2[1] - color1[1]) * t
    b = color1[2] + (color2[2] - color1[2]) * t
    return color.rgb(r, g, b)

def update():
    global day_night_cycle
    
    # Day-night cycle update
    day_night_cycle = (day_night_cycle + day_speed * time.dt) % 100
    
    # Update sky color based on time
    if day_night_cycle < 25:  # Morning to noon
        sky_color = lerp_color((120, 120, 255), (0, 160, 255), day_night_cycle/25)
        brightness = 1.0
        time_text = "Morning"
    elif day_night_cycle < 50:  # Noon to sunset
        sky_color = lerp_color((0, 160, 255), (255, 80, 0), (day_night_cycle-25)/25)
        brightness = 1.0 - 0.3*((day_night_cycle-25)/25)
        time_text = "Afternoon"
    elif day_night_cycle < 75:  # Sunset to midnight
        sky_color = lerp_color((50, 0, 80), (0, 0, 40), (day_night_cycle-50)/25)
        brightness = 0.7 - 0.6*((day_night_cycle-50)/25)
        time_text = "Night"
    else:  # Midnight to sunrise
        sky_color = lerp_color((0, 0, 40), (120, 120, 255), (day_night_cycle-75)/25)
        brightness = 0.1 + 0.9*((day_night_cycle-75)/25)
        time_text = "Dawn"
    
    # Apply sky color and ambient lighting
    scene.fog_color = sky_color
    scene.fog_density = 0.01 + (0.03 if day_night_cycle > 50 and day_night_cycle < 75 else 0)
      # Set ambient lighting
    for box in boxes:
        if hasattr(box, 'color') and hasattr(box.color, 'r'):
            # Handle transparency separately
            if hasattr(box.color, 'a'):
                box.color = color.rgba(
                    box.color.r * brightness,
                    box.color.g * brightness,
                    box.color.b * brightness,
                    box.color.a
                )
            else:
                box.color = color.rgb(
                    box.color.r * brightness,
                    box.color.g * brightness,
                    box.color.b * brightness
                )
    
    # Update UI
    time_display.text = f"Time: {time_text}"
    block_display.text = f"Current block: {block_types[current_block_type]}"

def input(key):
    global current_block_type, day_speed
    
    # Scroll to change block type
    if key == 'scroll up':
        current_block_type = (current_block_type + 1) % len(block_types)
        block_count_text.text = f"Block type: {block_types[current_block_type]}"
        
    if key == 'scroll down':
        current_block_type = (current_block_type - 1) % len(block_types)
        block_count_text.text = f"Block type: {block_types[current_block_type]}"
    
    # Toggle day/night speed
    if key == 'f':
        if day_speed > 0:
            day_speed = 0  # Pause day cycle
        else:
            day_speed = 0.1  # Resume day cycle
    
    # Block placement/removal    
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                # Get texture based on current block type
                texture_name = f"{block_types[current_block_type]}.png"
                block_color = block_colors.get(block_types[current_block_type], color.white)
                
                new = Button(
                    color=block_color,
                    model='cube',
                    position=box.position + mouse.normal,
                    texture=texture_name,
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(new)
            
            if key == 'right mouse down':
                # Remove the block
                boxes.remove(box)
                destroy(box)

app.run()