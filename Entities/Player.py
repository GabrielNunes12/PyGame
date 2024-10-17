import pygame
import os

class Player:
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.friction = 2
        self.jump_strength = 15
        self.on_ground = False

        # Load player sprite
        sprite_path = os.path.join('assets', 'images', 'player.png')
        try:
            self.image = pygame.image.load(sprite_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error or FileNotFoundError:
            print(f"Unable to load sprite image at {sprite_path}. Using rectangle instead.")
            self.image = None

    def handle_input(self, keys_pressed):
        self.velocity.x = 0  # Reset horizontal velocity each frame

        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.velocity.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.velocity.x += self.speed
        if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and self.on_ground:
            self.velocity.y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self, gravity):
        self.velocity.y += gravity

    def update(self, physics):
         # Apply friction
        self.velocity.x += self.velocity.x * self.friction

        # Clamp the horizontal velocity
        if self.velocity.x > self.speed:
            self.velocity.x = self.speed
        elif self.velocity.x <= -self.speed:
            self.velocity.x = -self.speed

        # Apply movement
        self.rect.x += self.velocity.x
        physics.apply_gravity({'velocity_y': self.velocity.y, 'y': self.rect.y})
        self.rect.y += self.velocity.y

    def draw(self, screen, camera_offset):
        # Calculate screen position based on camera offset
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        if self.image:
            screen.blit(self.image, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.rect.width, self.rect.height))