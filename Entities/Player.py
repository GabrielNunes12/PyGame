import pygame
import os
import time  # Novo: para controlar o cooldown

class Player:
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.friction = 2
        self.jump_strength = 15
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2
        self.is_jumping = False
        self.facing_right = True
        
        # Novo: variáveis para controle do cooldown
        self.double_jump_available = True
        self.last_double_jump_time = 0
        self.double_jump_cooldown = 3  # 3 segundos de cooldown

        # Modificar o carregamento do sprite para guardar a imagem original
        sprite_path = os.path.join('assets', 'images', 'player.png')
        try:
            self.original_image = pygame.image.load(sprite_path).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (width, height))
            self.image = self.original_image
        except pygame.error or FileNotFoundError:
            print(f"Unable to load sprite image at {sprite_path}. Using rectangle instead.")
            self.image = None
            self.original_image = None

    def handle_input(self, keys_pressed):
        self.velocity.x = 0

        # Verifica o cooldown do double jump
        current_time = time.time()
        if not self.double_jump_available and current_time - self.last_double_jump_time >= self.double_jump_cooldown:
            self.double_jump_available = True
            self.jump_count = 0  # Reseta o contador quando o cooldown termina

        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.velocity.x -= self.speed
            if self.facing_right and self.image:  # Flip apenas se estiver virado para direita
                self.facing_right = False
                self.image = pygame.transform.flip(self.original_image, True, False)
                
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.velocity.x += self.speed
            if not self.facing_right and self.image:  # Flip apenas se estiver virado para esquerda
                self.facing_right = True
                self.image = pygame.transform.flip(self.image, True, False)
        # Lógica de pulo modificada
        if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and not self.is_jumping:
            # Só permite pular se o double jump estiver disponível
            if self.double_jump_available:
                if self.on_ground:  # Primeiro pulo
                    self.velocity.y = -self.jump_strength
                    self.on_ground = False
                    self.jump_count = 1
                    self.is_jumping = True
                elif self.jump_count == 1:  # Double jump
                    self.velocity.y = -self.jump_strength
                    self.jump_count = 2
                    self.is_jumping = True
                    self.double_jump_available = False
                    self.last_double_jump_time = current_time
                
        elif not (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]):
            self.is_jumping = False

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
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        if self.image:
            screen.blit(self.image, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.rect.width, self.rect.height))
        
        # Novo: Desenhar indicador de cooldown do double jump
        if not self.double_jump_available:
            current_time = time.time()
            remaining_cooldown = self.double_jump_cooldown - (current_time - self.last_double_jump_time)
            if remaining_cooldown > 0:
                cooldown_text = f"Double Jump: {remaining_cooldown:.1f}s"
                font = pygame.font.Font(None, 24)
                text_surface = font.render(cooldown_text, True, (255, 255, 255))
                screen.blit(text_surface, (screen_x, screen_y - 20))