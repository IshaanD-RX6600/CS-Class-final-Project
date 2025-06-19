from ursina import*
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()

# Enhanced visual settings for better texture appearance
window.fullscreen = False
window.title = 'Minecraft Clone - Enhanced Edition'

# Improve lighting and visuals
scene.fog_color = color.rgb(135, 206, 235)  # Sky blue fog
scene.fog_density = 0.02

# Add better lighting
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
sun.color = color.rgb(255, 244, 214)  # Warm sunlight

# Add ambient lighting for better texture visibility
AmbientLight(color=color.rgba(200, 200, 255, 100))

# Add textures dictionary for different block types
block_types = ['grass', 'stone', 'dirt', 'wood', 'brick', 'glass', 'water']
current_block_type = 0  # Index to track current block type

# Block colors (enhanced for better visual details)
block_colors = {
    'grass': color.rgb(76, 153, 0),  # Natural grass green
    'stone': color.rgb(128, 128, 128),  # Medium gray stone
    'dirt': color.rgb(139, 69, 19),  # Rich brown dirt
    'wood': color.rgb(160, 82, 45),  # Warm brown wood
    'brick': color.rgb(178, 34, 34),  # Deep red brick
    'glass': color.rgba(173, 216, 230, 150),  # Light blue glass with transparency
    'water': color.rgba(64, 164, 223, 180),  # Clear blue water with transparency
}

# Game states
# Day/night cycle removed for simplicity

# Enhanced player controller with improved settings
player = FirstPersonController(
    jump_height=2, 
    jump_duration=0.3,
    speed=6,  # Increased movement speed
    mouse_sensitivity=Vec2(50, 50)  # Better mouse control
)

# Enhanced sky with better colors
sky = Sky(texture='sky_sunset')

# Improve camera settings for better texture viewing
camera.fov = 75  # Slightly wider field of view
camera.clip_plane_far = 300  # Extended view distance

# Create text UI for instructions and block selection
instructions = Text(
    text="Left click: Place block\nRight click: Remove block\nScroll wheel: Change block type\n1-7: Select block from hotbar",
    position=(-0.85, 0.45),
    scale=0.7,
    color=color.white
)

block_display = Text(
    text=f"Current block: grass",
    position=(-0.85, 0.1),
    scale=0.8, 
    color=color.white
)

# Block count text (replacing game mode)
block_count_text = Text(
    text=f"Block type: {block_types[current_block_type]}",
    position=(-0.85, -0.1),
    scale=0.8,
    color=color.white
)

# Time display
time_display = Text(
    text="Minecraft Clone - Infinite World",
    position=(-0.85, -0.4),
    scale=0.8,
    color=color.white
)

# Optimized infinite world system
CHUNK_SIZE = 8  # Small chunks for better performance
RENDER_DISTANCE = 1  # Very close render distance to prevent lag
MAX_CHUNKS = 9  # Maximum chunks loaded at once (3x3 grid)
loaded_chunks = {}
boxes = []

def get_chunk_coord(world_x, world_z):
    """Convert world coordinates to chunk coordinates"""
    return (int(world_x // CHUNK_SIZE), int(world_z // CHUNK_SIZE))

def get_height_at(x, z):
    """Generate consistent but simple terrain height"""
    # Very simple terrain to avoid lag
    height = int(math.sin(x * 0.1) + math.sin(z * 0.1) + 2)
    return max(0, min(height, 4))  # Limit height to prevent too many blocks

def create_tree(x, y, z):
    """Create a proper tree structure"""
    tree_blocks = []
    
    # Tree trunk (2 blocks high)
    for trunk_y in range(y + 1, y + 3):
        trunk = Button(
            color=color.white,
            model='cube',
            position=(x, trunk_y, z),
            texture='wood.png',
            parent=scene,
            origin_y=0.5
        )
        tree_blocks.append(trunk)
        boxes.append(trunk)
    
    # Tree leaves (simple cross pattern)
    leaves_y = y + 3
    leaf_positions = [
        (x, leaves_y, z),      # Center
        (x+1, leaves_y, z),    # East
        (x-1, leaves_y, z),    # West
        (x, leaves_y, z+1),    # North
        (x, leaves_y, z-1),    # South
        (x, leaves_y+1, z),    # Top
    ]
    
    for leaf_x, leaf_y, leaf_z in leaf_positions:
        leaf = Button(
            color=color.white,
            model='cube',
            position=(leaf_x, leaf_y, leaf_z),
            texture='grass.png',
            parent=scene,
            origin_y=0.5
        )
        tree_blocks.append(leaf)
        boxes.append(leaf)
    
    return tree_blocks

def create_house(x, y, z):
    """Create a simple house structure"""
    house_blocks = []
    
    # House foundation (3x3)
    for hx in range(x, x + 3):
        for hz in range(z, z + 3):
            foundation = Button(
                color=color.white,
                model='cube',
                position=(hx, y, hz),
                texture='stone.png',
                parent=scene,
                origin_y=0.5
            )
            house_blocks.append(foundation)
            boxes.append(foundation)
    
    # House walls
    wall_positions = [
        # Front wall (with door opening)
        (x, y+1, z), (x+2, y+1, z),  # Skip middle for door
        (x, y+2, z), (x+1, y+2, z), (x+2, y+2, z),
        # Back wall
        (x, y+1, z+2), (x+1, y+1, z+2), (x+2, y+1, z+2),
        (x, y+2, z+2), (x+1, y+2, z+2), (x+2, y+2, z+2),
        # Side walls
        (x, y+1, z+1), (x, y+2, z+1),
        (x+2, y+1, z+1), (x+2, y+2, z+1),
    ]
    
    for wx, wy, wz in wall_positions:
        wall = Button(
            color=color.white,
            model='cube',
            position=(wx, wy, wz),
            texture='brick.png',
            parent=scene,
            origin_y=0.5
        )
        house_blocks.append(wall)
        boxes.append(wall)
    
    # Simple roof
    roof_positions = [
        (x, y+3, z), (x+1, y+3, z), (x+2, y+3, z),
        (x, y+3, z+1), (x+1, y+3, z+1), (x+2, y+3, z+1),
        (x, y+3, z+2), (x+1, y+3, z+2), (x+2, y+3, z+2),
    ]
    
    for rx, ry, rz in roof_positions:
        roof = Button(
            color=color.white,
            model='cube',
            position=(rx, ry, rz),
            texture='wood.png',
            parent=scene,
            origin_y=0.5
        )
        house_blocks.append(roof)
        boxes.append(roof)
    
    return house_blocks

def generate_chunk_fast(chunk_x, chunk_z):
    """Generate a chunk quickly with minimal blocks"""
    chunk_blocks = []
    
    # Only generate surface blocks to reduce lag
    for local_x in range(CHUNK_SIZE):
        for local_z in range(CHUNK_SIZE):
            world_x = chunk_x * CHUNK_SIZE + local_x
            world_z = chunk_z * CHUNK_SIZE + local_z
            
            height = get_height_at(world_x, world_z)
            
            # Only create top surface block
            surface_block = Button(
                color=color.white,
                model='cube',
                position=(world_x, height, world_z),
                texture='grass.png',
                parent=scene,
                origin_y=0.5
            )
            chunk_blocks.append(surface_block)
            boxes.append(surface_block)
            
            # Add one dirt block below if height > 0
            if height > 0:
                dirt_block = Button(
                    color=color.white,
                    model='cube',
                    position=(world_x, height - 1, world_z),
                    texture='dirt.png',
                    parent=scene,
                    origin_y=0.5
                )
                chunk_blocks.append(dirt_block)
                boxes.append(dirt_block)
    
    # Add structures to chunk (one per chunk max to avoid lag)
    structure_chance = random.randint(1, 3)
    
    if structure_chance == 1:  # 33% chance for a house
        # Place house in safe area of chunk
        house_x = chunk_x * CHUNK_SIZE + random.randint(1, CHUNK_SIZE - 4)
        house_z = chunk_z * CHUNK_SIZE + random.randint(1, CHUNK_SIZE - 4)
        house_y = get_height_at(house_x, house_z)
        house_blocks = create_house(house_x, house_y, house_z)
        chunk_blocks.extend(house_blocks)
        
    elif structure_chance == 2:  # 33% chance for a tree
        tree_x = chunk_x * CHUNK_SIZE + random.randint(1, CHUNK_SIZE - 2)
        tree_z = chunk_z * CHUNK_SIZE + random.randint(1, CHUNK_SIZE - 2)
        tree_y = get_height_at(tree_x, tree_z)
        tree_blocks = create_tree(tree_x, tree_y, tree_z)
        chunk_blocks.extend(tree_blocks)
    
    # 33% chance for no structure (empty chunk)
    
    return chunk_blocks

def load_chunk(chunk_x, chunk_z):
    """Load a chunk if it's not already loaded"""
    chunk_key = (chunk_x, chunk_z)
    if chunk_key not in loaded_chunks and len(loaded_chunks) < MAX_CHUNKS:
        chunk_blocks = generate_chunk_fast(chunk_x, chunk_z)
        loaded_chunks[chunk_key] = chunk_blocks

def unload_chunk(chunk_x, chunk_z):
    """Unload a chunk to save memory"""
    chunk_key = (chunk_x, chunk_z)
    if chunk_key in loaded_chunks:
        # Remove all blocks in this chunk
        for block in loaded_chunks[chunk_key]:
            if block in boxes:
                boxes.remove(block)
            destroy(block)
        del loaded_chunks[chunk_key]

def update_world_around_player():
    """Update chunks around the player's position - optimized"""
    player_chunk_x, player_chunk_z = get_chunk_coord(player.position.x, player.position.z)
    
    # Only load immediate surrounding chunks
    chunks_needed = []
    for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            chunk_x = player_chunk_x + dx
            chunk_z = player_chunk_z + dz
            chunks_needed.append((chunk_x, chunk_z))
    
    # Load needed chunks
    for chunk_key in chunks_needed:
        load_chunk(chunk_key[0], chunk_key[1])
    
    # Unload distant chunks
    chunks_to_unload = []
    for chunk_key in loaded_chunks.keys():
        if chunk_key not in chunks_needed:
            chunks_to_unload.append(chunk_key)
    
    for chunk_key in chunks_to_unload:
        unload_chunk(chunk_key[0], chunk_key[1])

# Initialize the world around spawn
player_spawn_chunk_x, player_spawn_chunk_z = get_chunk_coord(0, 0)
for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
    for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        load_chunk(player_spawn_chunk_x + dx, player_spawn_chunk_z + dz)

def lerp_color(color1, color2, t):
    # Custom function to linearly interpolate between two colors
    r = color1[0] + (color2[0] - color1[0]) * t
    g = color1[1] + (color2[1] - color1[1]) * t
    b = color1[2] + (color2[2] - color1[2]) * t
    return color.rgb(r, g, b)

# Frame counter for chunk loading optimization
frame_count = 0

def update():
    global frame_count
    frame_count += 1
    
    # Update UI
    block_display.text = f"Current block: {block_types[current_block_type]}"
    
    # Update world chunks every 60 frames (about once per second) to avoid lag
    if frame_count % 60 == 0:
        update_world_around_player()

def input(key):
    global current_block_type
    
    # Number keys for hotbar selection (1-7)
    for i in range(1, 8):
        if key == str(i) and i <= len(block_types):
            current_block_type = i - 1
            update_hotbar_selection()
            block_count_text.text = f"Block type: {block_types[current_block_type]}"
      # Scroll to change block type
    if key == 'scroll up':
        current_block_type = (current_block_type + 1) % len(block_types)
        update_hotbar_selection()
        block_count_text.text = f"Block type: {block_types[current_block_type]}"
        
    if key == 'scroll down':
        current_block_type = (current_block_type - 1) % len(block_types)
        update_hotbar_selection()
        block_count_text.text = f"Block type: {block_types[current_block_type]}"
      # Block placement/removal
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                # Get texture based on current block type
                texture_name = f"{block_types[current_block_type]}.png"
                
                new = Button(
                    color=color.white,  # Use white to show textures clearly
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

# Hotbar system
hotbar_slots = []
hotbar_background = Entity(model='cube', color=color.rgba(0, 0, 0, 100), scale=(8, 1, 0.1), position=(0, -4, 1), parent=camera.ui)

# Create hotbar slots
for i in range(len(block_types)):
    # Background slot
    slot_bg = Entity(
        model='cube',
        color=color.rgba(50, 50, 50, 150),
        scale=(0.8, 0.8, 0.1),
        position=(-3 + i * 1, -4, 0.9),
        parent=camera.ui
    )
    
    # Block preview in slot
    block_preview = Entity(
        model='cube',
        texture=f'{block_types[i]}.png',
        color=block_colors.get(block_types[i], color.white),
        scale=(0.6, 0.6, 0.6),
        position=(-3 + i * 1, -4, 0.8),
        parent=camera.ui
    )
    
    # Selection indicator (highlight)
    selection_indicator = Entity(
        model='cube',
        color=color.rgba(255, 255, 0, 200),
        scale=(0.9, 0.9, 0.05),
        position=(-3 + i * 1, -4, 0.7),
        parent=camera.ui,
        visible=False
    )
    
    # Number label
    number_label = Text(
        text=str(i + 1),
        position=(-3 + i * 1, -4.4, 0),
        scale=0.8,
        color=color.white,
        parent=camera.ui
    )
    
    hotbar_slots.append({
        'background': slot_bg,
        'preview': block_preview,
        'indicator': selection_indicator,
        'label': number_label,
        'block_type': block_types[i]
    })

# Show selection on first slot
hotbar_slots[current_block_type]['indicator'].visible = True

def update_hotbar_selection():
    """Update hotbar visual selection"""
    for i, slot in enumerate(hotbar_slots):
        if i == current_block_type:
            slot['indicator'].visible = True
            slot['background'].color = color.rgba(100, 100, 100, 200)
        else:
            slot['indicator'].visible = False
            slot['background'].color = color.rgba(50, 50, 50, 150)

update()
app.run()