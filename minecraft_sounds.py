from ursina import Audio

class SoundManager:
    def __init__(self):
        # Create sound effects
        self.break_sound = Audio('break_sound.wav', loop=False, autoplay=False)
        self.place_sound = Audio('place_sound.wav', loop=False, autoplay=False)
        self.walk_sound = Audio('walk_sound.wav', loop=False, autoplay=False)
        self.ambient_sound = Audio('ambient.wav', loop=True, autoplay=True, volume=0.5)
        
        self.footstep_timer = 0
    
    def play_break(self):
        """Play block breaking sound"""
        self.break_sound.play()
    
    def play_place(self):
        """Play block placing sound"""
        self.place_sound.play()
    
    def update_footsteps(self, player_is_moving, dt):
        """Play footstep sounds at intervals when the player is moving"""
        if player_is_moving:
            self.footstep_timer += dt
            if self.footstep_timer > 0.5:  # Play every half second
                self.walk_sound.play()
                self.footstep_timer = 0
    
    def play_ambient(self):
        """Start ambient background sounds"""
        if not self.ambient_sound.playing:
            self.ambient_sound.play()
    
    def stop_ambient(self):
        """Stop ambient background sounds"""
        if self.ambient_sound.playing:
            self.ambient_sound.stop()

# Note: You'll need to create or download sound files for this to work:
# - break_sound.wav - for block breaking
# - place_sound.wav - for block placing
# - walk_sound.wav - for player movement
# - ambient.wav - for background ambience
