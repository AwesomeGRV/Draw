"""
Advanced Animation System with Pygame
Interactive graphics, particle systems, and physics simulations
"""

import pygame
import numpy as np
import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional
import colorsys
from enum import Enum


class AnimationType(Enum):
    """Enumeration of animation types"""
    PARTICLE_SYSTEM = "Particle System"
    FIREWORKS = "Fireworks"
    FOUNTAIN = "Fountain"
    SNOW = "Snow"
    RAIN = "Rain"
    STARFIELD = "Starfield"
    WAVES = "Waves"
    FRACTAL_TREE = "Fractal Tree"
    SNAKE = "Snake Game"
    BOUNCING_BALLS = "Bouncing Balls"


@dataclass
class Vector2D:
    """2D vector for physics calculations"""
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)
    
    def distance_to(self, other):
        return (self - other).magnitude()


class Particle:
    """Base particle class"""
    
    def __init__(self, position: Vector2D, velocity: Vector2D, 
                 color: Tuple[int, int, int], size: float = 2.0, lifetime: float = 1.0):
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector2D(0, 0)
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alive = True
    
    def apply_force(self, force: Vector2D):
        """Apply force to particle (F = ma, assuming m = 1)"""
        self.acceleration = self.acceleration + force
    
    def update(self, dt: float):
        """Update particle physics"""
        # Update velocity and position
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        
        # Reset acceleration
        self.acceleration = Vector2D(0, 0)
        
        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
    
    def draw(self, screen: pygame.Surface):
        """Draw particle on screen"""
        if self.alive:
            # Fade based on lifetime
            alpha = self.lifetime / self.max_lifetime
            color = tuple(int(c * alpha) for c in self.color)
            
            pygame.draw.circle(screen, color, 
                             (int(self.position.x), int(self.position.y)), 
                             int(self.size))


class FireworkParticle(Particle):
    """Firework particle with trail effect"""
    
    def __init__(self, position: Vector2D, velocity: Vector2D, 
                 color: Tuple[int, int, int], size: float = 3.0, lifetime: float = 2.0):
        super().__init__(position, velocity, color, size, lifetime)
        self.trail = []
        self.max_trail_length = 10
    
    def update(self, dt: float):
        """Update with trail"""
        # Add current position to trail
        self.trail.append((self.position.x, self.position.y, self.lifetime / self.max_lifetime))
        
        # Limit trail length
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        super().update(dt)
    
    def draw(self, screen: pygame.Surface):
        """Draw particle with trail"""
        if self.alive:
            # Draw trail
            for i, (x, y, alpha) in enumerate(self.trail):
                trail_alpha = alpha * (i / len(self.trail))
                trail_color = tuple(int(c * trail_alpha) for c in self.color)
                trail_size = self.size * (i / len(self.trail))
                pygame.draw.circle(screen, trail_color, (int(x), int(y)), int(trail_size))
            
            # Draw particle
            super().draw(screen)


class PhysicsObject:
    """Physics-enabled object"""
    
    def __init__(self, position: Vector2D, velocity: Vector2D, 
                 radius: float, mass: float = 1.0, color: Tuple[int, int, int] = (255, 255, 255)):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.restitution = 0.8  # Bounciness
    
    def update(self, dt: float, width: int, height: int):
        """Update physics and handle boundaries"""
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Apply gravity
        self.velocity.y += 500 * dt  # Gravity acceleration
        
        # Handle boundary collisions
        if self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.velocity.x = -self.velocity.x * self.restitution
        elif self.position.x + self.radius >= width:
            self.position.x = width - self.radius
            self.velocity.x = -self.velocity.x * self.restitution
        
        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y = -self.velocity.y * self.restitution
        elif self.position.y + self.radius >= height:
            self.position.y = height - self.radius
            self.velocity.y = -self.velocity.y * self.restitution
    
    def check_collision(self, other):
        """Check collision with another object"""
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)
    
    def resolve_collision(self, other):
        """Resolve collision with another object"""
        # Calculate collision normal
        normal = (other.position - self.position).normalize()
        
        # Calculate relative velocity
        relative_velocity = other.velocity - self.velocity
        
        # Calculate relative velocity along collision normal
        velocity_along_normal = (relative_velocity.x * normal.x + 
                                relative_velocity.y * normal.y)
        
        # Don't resolve if velocities are separating
        if velocity_along_normal > 0:
            return
        
        # Calculate restitution
        e = min(self.restitution, other.restitution)
        
        # Calculate impulse scalar
        j = -(1 + e) * velocity_along_normal
        j /= 1/self.mass + 1/other.mass
        
        # Apply impulse
        impulse = normal * j
        self.velocity = self.velocity - impulse * (1/self.mass)
        other.velocity = other.velocity + impulse * (1/other.mass)
        
        # Separate objects
        overlap = (self.radius + other.radius) - self.position.distance_to(other.position)
        separation = normal * (overlap / 2)
        self.position = self.position - separation
        other.position = other.position + separation
    
    def draw(self, screen: pygame.Surface):
        """Draw the object"""
        pygame.draw.circle(screen, self.color, 
                         (int(self.position.x), int(self.position.y)), 
                         int(self.radius))


class ParticleSystem:
    """Particle system manager"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.particles: List[Particle] = []
        self.gravity = Vector2D(0, 100)
    
    def add_particle(self, particle: Particle):
        """Add a particle to the system"""
        self.particles.append(particle)
    
    def update(self, dt: float):
        """Update all particles"""
        # Update particles
        for particle in self.particles[:]:
            particle.apply_force(self.gravity)
            particle.update(dt)
            
            # Remove dead particles
            if not particle.alive:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)


class FireworksSystem(ParticleSystem):
    """Fireworks particle system"""
    
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.gravity = Vector2D(0, 50)
        self.launch_timer = 0
        self.launch_interval = 2.0
    
    def launch_firework(self):
        """Launch a new firework"""
        # Random launch position
        x = random.randint(100, self.width - 100)
        y = self.height
        
        # Launch velocity
        vx = random.uniform(-50, 50)
        vy = random.uniform(-500, -400)
        
        # Random color
        hue = random.random()
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = tuple(int(c * 255) for c in rgb)
        
        # Create launch particle
        launch_particle = FireworkParticle(
            Vector2D(x, y), 
            Vector2D(vx, vy), 
            color, 
            size=4, 
            lifetime=2.0
        )
        
        self.add_particle(launch_particle)
    
    def explode_firework(self, particle: Particle):
        """Explode a firework into multiple particles"""
        num_particles = random.randint(30, 50)
        
        for _ in range(num_particles):
            # Random explosion direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            
            velocity = Vector2D(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            # Vary color slightly
            base_color = particle.color
            color = tuple(
                max(0, min(255, c + random.randint(-50, 50))) 
                for c in base_color
            )
            
            # Create explosion particle
            explosion_particle = FireworkParticle(
                particle.position,
                velocity,
                color,
                size=random.uniform(1, 3),
                lifetime=random.uniform(1.0, 2.0)
            )
            
            self.add_particle(explosion_particle)
    
    def update(self, dt: float):
        """Update fireworks system"""
        # Launch new fireworks periodically
        self.launch_timer += dt
        if self.launch_timer >= self.launch_interval:
            self.launch_firework()
            self.launch_timer = 0
        
        # Update particles
        for particle in self.particles[:]:
            particle.apply_force(self.gravity)
            particle.update(dt)
            
            # Check for explosion (when launch particle starts falling)
            if (isinstance(particle, FireworkParticle) and 
                particle.velocity.y > 0 and 
                particle.lifetime > particle.max_lifetime * 0.5):
                self.explode_firework(particle)
                self.particles.remove(particle)
            elif not particle.alive:
                self.particles.remove(particle)


class FountainSystem(ParticleSystem):
    """Fountain particle system"""
    
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.gravity = Vector2D(0, 200)
        self.spawn_position = Vector2D(width // 2, height - 50)
        self.spawn_timer = 0
        self.spawn_interval = 0.05
    
    def update(self, dt: float):
        """Update fountain system"""
        # Spawn new particles
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_particles()
            self.spawn_timer = 0
        
        # Update existing particles
        super().update(dt)
    
    def spawn_particles(self):
        """Spawn new fountain particles"""
        num_particles = random.randint(3, 7)
        
        for _ in range(num_particles):
            # Random angle and speed
            angle = random.uniform(-math.pi/3, -2*math.pi/3)  # Upward cone
            speed = random.uniform(200, 400)
            
            velocity = Vector2D(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            # Blue-white color
            blue_component = random.randint(150, 255)
            color = (random.randint(100, 200), random.randint(150, 255), blue_component)
            
            particle = Particle(
                self.spawn_position,
                velocity,
                color,
                size=random.uniform(1, 3),
                lifetime=random.uniform(2, 3)
            )
            
            self.add_particle(particle)


class BouncingBallsSimulation:
    """Bouncing balls physics simulation"""
    
    def __init__(self, width: int, height: int, num_balls: int = 10):
        self.width = width
        self.height = height
        self.balls: List[PhysicsObject] = []
        
        # Create random balls
        for _ in range(num_balls):
            position = Vector2D(
                random.randint(50, width - 50),
                random.randint(50, height // 2)
            )
            velocity = Vector2D(
                random.randint(-200, 200),
                random.randint(-100, 100)
            )
            radius = random.randint(10, 30)
            mass = radius / 10  # Mass proportional to size
            
            # Random color
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )
            
            ball = PhysicsObject(position, velocity, radius, mass, color)
            self.balls.append(ball)
    
    def update(self, dt: float):
        """Update physics simulation"""
        # Update each ball
        for ball in self.balls:
            ball.update(dt, self.width, self.height)
        
        # Check collisions between balls
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if self.balls[i].check_collision(self.balls[j]):
                    self.balls[i].resolve_collision(self.balls[j])
    
    def draw(self, screen: pygame.Surface):
        """Draw all balls"""
        for ball in self.balls:
            ball.draw(screen)


class StarField:
    """Animated starfield background"""
    
    def __init__(self, width: int, height: int, num_stars: int = 200):
        self.width = width
        self.height = height
        self.stars = []
        
        for _ in range(num_stars):
            star = {
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'z': random.uniform(0.1, 1.0),  # Depth
                'brightness': random.uniform(0.3, 1.0)
            }
            self.stars.append(star)
    
    def update(self, dt: float):
        """Update star positions"""
        for star in self.stars:
            # Move stars towards viewer
            star['z'] -= dt * 0.5
            
            # Reset star if it gets too close
            if star['z'] <= 0:
                star['x'] = random.randint(0, self.width)
                star['y'] = random.randint(0, self.height)
                star['z'] = 1.0
    
    def draw(self, screen: pygame.Surface):
        """Draw stars"""
        for star in self.stars:
            # Calculate screen position with perspective
            screen_x = int((star['x'] - self.width/2) / star['z'] + self.width/2)
            screen_y = int((star['y'] - self.height/2) / star['z'] + self.height/2)
            
            # Calculate size based on depth
            size = int((1 - star['z']) * 3 + 1)
            
            # Calculate brightness
            brightness = int(star['brightness'] * (1 - star['z']) * 255)
            color = (brightness, brightness, brightness)
            
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                pygame.draw.circle(screen, color, (screen_x, screen_y), size)


class WaveSimulation:
    """Wave simulation using sine functions"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.time = 0
        self.wave_points = []
        self.num_points = 100
    
    def update(self, dt: float):
        """Update wave animation"""
        self.time += dt
        
        # Calculate wave points
        self.wave_points = []
        for i in range(self.num_points):
            x = i * self.width / self.num_points
            
            # Multiple sine waves for complexity
            y1 = math.sin(x * 0.01 + self.time * 2) * 50
            y2 = math.sin(x * 0.02 + self.time * 3) * 30
            y3 = math.cos(x * 0.005 + self.time * 1) * 20
            
            y = self.height // 2 + y1 + y2 + y3
            self.wave_points.append((x, y))
    
    def draw(self, screen: pygame.Surface):
        """Draw waves"""
        if len(self.wave_points) > 1:
            # Draw multiple wave layers with different colors
            colors = [(0, 100, 200), (0, 150, 255), (100, 200, 255)]
            
            for color_index, color in enumerate(colors):
                offset = color_index * 20
                points = [(x, y + offset) for x, y in self.wave_points]
                
                if len(points) > 1:
                    pygame.draw.lines(screen, color, False, points, 2)


class AnimationEngine:
    """Main animation engine"""
    
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Advanced Animation System")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_animation = None
        self.animations = {}
        
        # Initialize animations
        self.init_animations()
        
        # UI font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def init_animations(self):
        """Initialize all animation types"""
        self.animations[AnimationType.PARTICLE_SYSTEM] = ParticleSystem(self.width, self.height)
        self.animations[AnimationType.FIREWORKS] = FireworksSystem(self.width, self.height)
        self.animations[AnimationType.FOUNTAIN] = FountainSystem(self.width, self.height)
        self.animations[AnimationType.STARFIELD] = StarField(self.width, self.height)
        self.animations[AnimationType.WAVES] = WaveSimulation(self.width, self.height)
        self.animations[AnimationType.BOUNCING_BALLS] = BouncingBallsSimulation(self.width, self.height)
        
        # Set default animation
        self.current_animation = AnimationType.FIREWORKS
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.current_animation = AnimationType.FIREWORKS
                elif event.key == pygame.K_2:
                    self.current_animation = AnimationType.FOUNTAIN
                elif event.key == pygame.K_3:
                    self.current_animation = AnimationType.BOUNCING_BALLS
                elif event.key == pygame.K_4:
                    self.current_animation = AnimationType.STARFIELD
                elif event.key == pygame.K_5:
                    self.current_animation = AnimationType.WAVES
                elif event.key == pygame.K_SPACE:
                    # Reset current animation
                    self.reset_current_animation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add particles at mouse position
                if self.current_animation == AnimationType.PARTICLE_SYSTEM:
                    self.add_particles_at_mouse(event.pos)
    
    def add_particles_at_mouse(self, mouse_pos):
        """Add particles at mouse position"""
        particle_system = self.animations[AnimationType.PARTICLE_SYSTEM]
        
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            
            velocity = Vector2D(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
            
            particle = Particle(
                Vector2D(mouse_pos[0], mouse_pos[1]),
                velocity,
                color,
                size=random.uniform(2, 5),
                lifetime=random.uniform(1, 3)
            )
            
            particle_system.add_particle(particle)
    
    def reset_current_animation(self):
        """Reset the current animation"""
        animation_type = self.current_animation
        
        if animation_type == AnimationType.FIREWORKS:
            self.animations[animation_type] = FireworksSystem(self.width, self.height)
        elif animation_type == AnimationType.FOUNTAIN:
            self.animations[animation_type] = FountainSystem(self.width, self.height)
        elif animation_type == AnimationType.BOUNCING_BALLS:
            self.animations[animation_type] = BouncingBallsSimulation(self.width, self.height)
        elif animation_type == AnimationType.STARFIELD:
            self.animations[animation_type] = StarField(self.width, self.height)
        elif animation_type == AnimationType.WAVES:
            self.animations[animation_type] = WaveSimulation(self.width, self.height)
        elif animation_type == AnimationType.PARTICLE_SYSTEM:
            self.animations[animation_type] = ParticleSystem(self.width, self.height)
    
    def update(self, dt: float):
        """Update current animation"""
        if self.current_animation and self.current_animation in self.animations:
            self.animations[self.current_animation].update(dt)
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill((0, 0, 20))  # Dark blue background
        
        # Draw current animation
        if self.current_animation and self.current_animation in self.animations:
            self.animations[self.current_animation].draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface"""
        # Title
        title_text = self.font.render(f"Animation: {self.current_animation.value}", True, (255, 255, 255))
        self.screen.blit(title_text, (10, 10))
        
        # Instructions
        instructions = [
            "Press 1-5: Switch animations",
            "Press SPACE: Reset animation",
            "Press ESC: Exit",
            "Click: Add particles (in Particle System mode)"
        ]
        
        y_offset = 50
        for instruction in instructions:
            text = self.small_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
        
        # Animation list
        y_offset = self.height - 150
        animations_list = [
            "1. Fireworks",
            "2. Fountain", 
            "3. Bouncing Balls",
            "4. Starfield",
            "5. Waves"
        ]
        
        for anim_text in animations_list:
            text = self.small_font.render(anim_text, True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
    
    def run(self):
        """Main game loop"""
        print("Advanced Animation System")
        print("=" * 40)
        print("Controls:")
        print("1-5: Switch between animations")
        print("SPACE: Reset current animation")
        print("ESC: Exit")
        print("Click: Add particles (in Particle System mode)")
        print()
        print("Starting animation engine...")
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()


def main():
    """Main function to run the animation system"""
    engine = AnimationEngine()
    engine.run()


if __name__ == "__main__":
    main()
