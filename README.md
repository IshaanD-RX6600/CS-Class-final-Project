# Minecraft Clone

A simple Minecraft-like game created with Python and the Ursina engine.

## Features

- First-person exploration
- Place and break blocks
- Multiple block types (grass, stone, dirt, wood, brick, glass, water)
- Day/night cycle
- Creative and survival modes
- Procedurally generated terrain with:
  - Trees
  - Hills
  - Lakes
  - Random houses

## How to Run

1. Make sure you have Python installed (Python 3.6 or higher recommended)
2. Install the required packages:
   ```
   pip install ursina
   ```
3. Download the texture files (see below) or create your own
4. Run the game:
   ```
   python minecraft.py
   ```

## Controls

- WASD: Move around
- SPACE: Jump
- LEFT MOUSE: Place block
- RIGHT MOUSE: Break/remove block
- SCROLL WHEEL: Change block type
- E: Toggle between creative/survival mode
- F: Toggle day/night cycle on/off

## Required Texture Files

You need the following texture image files in the same directory as the script:
- grass.png
- dirt.png
- stone.png
- wood.png
- brick.png
- glass.png
- water.png

You can create simple textures or find free Minecraft-like textures online.

## Optional Sound Files

For sound effects (if implemented), you'll need:
- break_sound.wav
- place_sound.wav
- walk_sound.wav
- ambient.wav

## Credits

Created as a class project for CS class.
