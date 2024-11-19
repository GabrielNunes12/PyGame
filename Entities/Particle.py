import pygame
import math

class Particle:
    def __init__(self, x, y, direction, max_distance):
        self.pos = pygame.math.Vector2(x, y)
        self.direction = direction
        self.speed = 15
        self.size = 10
        self.max_distance = max_distance
        self.distance_traveled = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)
        
        # Efeito visual
        self.color = (255, 165, 0)  # Laranja
        self.trail = []
        self.max_trail_length = 5
        
    def update(self):
        # Atualiza posição
        movement = self.direction * self.speed
        self.pos += movement
        self.distance_traveled += movement.length()
        
        # Atualiza retângulo de colisão
        self.rect.center = self.pos
        
        # Atualiza trail
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
            
    def draw(self, screen, camera_offset):
        # Desenha trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            color = (*self.color, alpha)
            
            screen_pos = (
                int(pos.x - camera_offset[0]),
                int(pos.y - camera_offset[1])
            )
            
            pygame.draw.circle(
                screen,
                color,
                screen_pos,
                self.size * (i / len(self.trail))
            )
        
        # Desenha partícula principal
        screen_pos = (
            int(self.pos.x - camera_offset[0]),
            int(self.pos.y - camera_offset[1])
        )
        pygame.draw.circle(screen, self.color, screen_pos, self.size) 