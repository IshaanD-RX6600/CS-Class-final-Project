from ursina import *
import random

class ParticleSystem:
    def __init__(self, scene):
        self.scene = scene
        self.particles = []
    
    def create_break_particles(self, position, texture_name, count=8):
        """Create particles when a block is broken"""
        for i in range(count):
            # Random direction
            direction = Vec3(
                random.uniform(-1, 1),
                random.uniform(0.5, 2),
                random.uniform(-1, 1)
            ).normalized() * random.uniform(2, 5)
            
            # Create small cube as particle
            particle = Entity(
                model='cube',
                texture=texture_name,
                position=position,
                scale=0.1,
                color=color.white,
                billboard=True  # Always face camera
            )
            
            # Add to list with properties
            self.particles.append({
                'entity': particle,
                'velocity': direction,
                'lifetime': random.uniform(0.5, 1.5),
                'time': 0
            })
    
    def create_step_particles(self, position):
        """Create dust particles when player walks"""
        for i in range(3):
            # Random direction on ground plane
            direction = Vec3(
                random.uniform(-1, 1),
                random.uniform(0.1, 0.5),
                random.uniform(-1, 1)
            ).normalized() * random.uniform(0.5, 1.5)
            
            # Create small cube as particle
            particle = Entity(
                model='cube',
                color=color.rgba(150, 150, 150, 200),
                position=position + Vec3(0, -0.5, 0),
                scale=0.05,
                billboard=True
            )
            
            # Add to list with properties
            self.particles.append({
                'entity': particle,
                'velocity': direction,
                'lifetime': random.uniform(0.3, 0.7),
                'time': 0
            })
    
    def update(self, dt):
        """Update all particles"""
        particles_to_remove = []
        
        for particle in self.particles:
            # Update time
            particle['time'] += dt
            
            # Check if particle should be destroyed
            if particle['time'] >= particle['lifetime']:
                destroy(particle['entity'])
                particles_to_remove.append(particle)
                continue
                
            # Update position
            particle['entity'].position += particle['velocity'] * dt
            
            # Apply gravity
            particle['velocity'].y -= 9.8 * dt
            
            # Fade out
            progress = particle['time'] / particle['lifetime']
            particle['entity'].alpha = 1 - progress
        
        # Remove expired particles
        for particle in particles_to_remove:
            self.particles.remove(particle)
