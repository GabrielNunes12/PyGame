import pygame
import os
import time  # Novo: para controlar o cooldown
from .Animation import Animation
import math
from .Particle import Particle  # Nova classe que vamos criar

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
        self.animation = Animation()
        self.load_animations(width, height)
        self.attacking = False
        self.attack_cooldown = 0.5  # segundos
        self.last_attack_time = 0
        self.attack_particles = []
        self.attack_damage = 50  # Dano base
        self.attack_range = 300  # Alcance máximo do ataque
        
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

    def attack(self, camera_offset=(0,0)):
        """Inicia um ataque"""
        self.attacking = True
        # Pega a posição do mouse
        mouse_pos = pygame.mouse.get_pos()
        # Converte para coordenadas do mundo
        world_mouse_pos = (
            mouse_pos[0] + camera_offset[0],
            mouse_pos[1] + camera_offset[1]
        )
        
        # Calcula direção do ataque
        direction = pygame.math.Vector2(
            world_mouse_pos[0] - self.rect.centerx,
            world_mouse_pos[1] - self.rect.centery
        )
        if direction.length() > 0:
            direction = direction.normalize()
            
        # Cria partícula de ataque
        particle = Particle(
            self.rect.centerx,
            self.rect.centery,
            direction,
            self.attack_range
        )
        self.attack_particles.append(particle)


    def handle_input(self, keys_pressed, camera_offset=(0,0)):
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
        mouse_buttons = pygame.mouse.get_pressed()
        current_time = time.time()
        
        if mouse_buttons[0] and current_time - self.last_attack_time >= self.attack_cooldown:  # Botão esquerdo
            self.attack(camera_offset)
            self.last_attack_time = current_time


        # Atualiza animações baseado no estado
        if self.velocity.x != 0:
            self.animation.play("run")
        elif self.velocity.y < 0:
            self.animation.play("jump")
        elif self.velocity.y > 0:
            self.animation.play("fall")
        else:
            self.animation.play("idle")
        # Atualiza a direção do sprite
        if self.velocity.x > 0:
            self.animation.facing_right = True
        elif self.velocity.x < 0:
            self.animation.facing_right = False


    def apply_gravity(self, gravity):
        self.velocity.y += gravity

    def calculate_damage(self, distance):
        """Calcula dano baseado na distância"""
        # Quanto mais perto, mais dano (linear falloff)
        damage_multiplier = 1 - (distance / self.attack_range)
        return max(self.attack_damage * damage_multiplier, 10)  # Mínimo de 10 de dano


    def update(self, physics, enemies = []):
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

         # Atualiza partículas e verifica colisões
        for particle in self.attack_particles[:]:  # Copia a lista para evitar problemas de modificação
            particle.update()
            
            # Remove partículas que atingiram seu alcance máximo
            if particle.distance_traveled >= particle.max_distance:
                self.attack_particles.remove(particle)
                continue
                
            # Verifica colisão com inimigos
            for enemy in enemies:
                if particle.rect.colliderect(enemy.rect):
                    # Calcula distância entre player e inimigo
                    distance = math.hypot(
                        enemy.rect.centerx - self.rect.centerx,
                        enemy.rect.centery - self.rect.centery
                    )
                    
                    # Aplica dano baseado na distância
                    damage = self.calculate_damage(distance)
                    enemy.take_damage(damage)
                    
                    # Remove a partícula após atingir
                    self.attack_particles.remove(particle)
                    break
        self.animation.update()

    def draw(self, screen, camera_offset):
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        current_frame = self.animation.get_current_frame()
        if current_frame:
            screen.blit(current_frame, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.rect.width, self.rect.height))
        # Desenha partículas de ataque
        for particle in self.attack_particles:
            particle.draw(screen, camera_offset)
        # Novo: Desenhar indicador de cooldown do double jump
        if not self.double_jump_available:
            current_time = time.time()
            remaining_cooldown = self.double_jump_cooldown - (current_time - self.last_double_jump_time)
            if remaining_cooldown > 0:
                cooldown_text = f"Double Jump: {remaining_cooldown:.1f}s"
                font = pygame.font.Font(None, 24)
                text_surface = font.render(cooldown_text, True, (255, 255, 255))
                screen.blit(text_surface, (screen_x, screen_y - 20))

    def load_animations(self, width, height):
        """Carrega todas as animações do player"""
        animations_data = {
            "idle": 2,      # Reduzindo para 2 frames inicialmente
            "run": 2,       # Reduzindo para 2 frames
            "jump": 2,
            "fall": 2,
            "attack": 2
        }
        
        # Certifique-se de que o diretório existe
        sprite_dir = os.path.join('assets', 'sprites', 'player')
        if not os.path.exists(sprite_dir):
            os.makedirs(sprite_dir)
            print(f"Criado diretório: {sprite_dir}")
        
        for anim_name, frame_count in animations_data.items():
            self.animation.load_animation(
                anim_name,
                sprite_dir,
                frame_count
            )
            
            # Verifica se a animação foi carregada e tem frames
            if anim_name in self.animation.animations:
                # Redimensiona todos os frames da animação
                self.animation.animations[anim_name] = [
                    pygame.transform.scale(frame, (width, height))
                    for frame in self.animation.animations[anim_name]
                ]