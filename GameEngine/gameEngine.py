import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pygame
# import physics class from Physics folder
from physics.physics_engine import PhysicsEngine
from UI import UI
from Entities.Player import Player
from World.world import World
from camera import Camera
from game.sound_manager import SoundManager

class GameEngine:
    def __init__(self):
        
        # Obtém informações do display
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        # Configura o display em tela cheia
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        pygame.display.set_caption("Collect all items")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize modules
        self.physics = PhysicsEngine()
        self.ui = UI(self.screen)

        # Initialize world
        section_size = (self.screen_width, self.screen_height)
        world_width = 3
        world_height = 3
        assets_path = 'assets'
        self.world = World(world_width, world_height, section_size, assets_path)
        sound_manager = SoundManager()
        sound_manager.play_background_music("assets/music/background_theme.mp3", volume=0.2)

        # Calculate total world size in pixels
        self.world_pixel_width = world_width * section_size[0]
        self.world_pixel_height = world_height * section_size[1]

        # Initialize camera
        self.camera = Camera(self.screen_width, self.screen_height, 
                           self.world_pixel_width, self.world_pixel_height)

        # Initialize player
        player_width = int(self.screen_width * 0.039)  # ~4% da largura da tela
        player_height = int(self.screen_height * 0.069)  # ~7% da altura da tela
        player_x = self.world_pixel_width // 2 - player_width // 2
        player_y = self.world_pixel_height // 2 - player_height // 2
        self.player = Player(player_x, player_y, player_width, player_height)

        # Initialize score
        self.score = 0

        # Load collection sound
        self.collect_sound = None
        collect_sound_path = path.join('assets', 'sounds', 'collect.wav')
        if path.exists(collect_sound_path):
            self.collect_sound = pygame.mixer.Sound(collect_sound_path)
        else:
            print(f"Collect sound not found at {collect_sound_path}. No sound will be played on collection.")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Adiciona opção de sair com ESC
                    self.running = False
                elif event.key == pygame.K_F11:   # Adiciona toggle fullscreen com F11
                    self.toggle_fullscreen()

    def toggle_fullscreen(self):
        """Alterna entre tela cheia e modo janela"""
        is_fullscreen = bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN)
        if is_fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        self.player.handle_input(keys_pressed, self.camera.offset)  # Passa o offset da câmera
        self.player.apply_gravity(self.physics.gravity)
        self.player.update(self.physics)
        # Ground collision
        if self.player.rect.bottom >= self.world.total_height - 10:
            self.player.rect.bottom = self.world.total_height - 10
            self.player.velocity.y = 0
            self.player.on_ground = True
            self.player.jump_count = 0  # Reseta o contador de pulos
        else:
            self.player.on_ground = False

        # Platform collision
        for platform in self.world.platforms:
            if self.player.rect.colliderect(platform):
                if self.player.velocity.y > 0:  # Falling down
                    self.player.rect.bottom = platform.top
                    self.player.velocity.y = 0
                    self.player.on_ground = True
                    self.player.jump_count = 0  # Reseta o contador de pulos quando tocar na plataforma

        # Collectible collision
        for collectible in self.world.collectibles:
            if not collectible.collected and self.player.rect.colliderect(collectible.rect):
                collectible.collected = True
                self.score += 1  # Increment score
                if self.collect_sound:
                    self.collect_sound.play()
        # Left boundary
        if self.player.rect.left <= 0:
            self.player.rect.left = 0
            self.player.velocity.x = 0

        # Right boundary
        if self.player.rect.right >= self.world.total_width:
            self.player.rect.right = self.world.total_width
            self.player.velocity.x = 0

        # Update camera based on player's position
        self.camera.update(self.player.rect)

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black

        # Draw the world based on camera offset
        self.world.draw(self.screen, self.camera.offset)

        # Draw the player relative to camera
        self.player.draw(self.screen, self.camera.offset)

        # Draw UI
        self.ui.draw_text(f"Score: {self.score}", 10, 10)
        self.ui.draw_text(f"BETA version", 5, 700, (100,100,200,4))


        pygame.display.flip()