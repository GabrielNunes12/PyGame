import pygame
# import physics class from Physics folder
from physics import PhysicsEngine
from UI import UI
from Entities.Player import Player
from World.world import World
from camera import Camera

class GameEngine:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Meu Jogo PyGame")
        self.clock = pygame.time.Clock()
        self.running = True

        self.physics = PhysicsEngine()
        self.ui = UI(self.screen)

        # Initialize world
        section_size = (800, 600)  # Each section is the size of the screen
        world_width = 3  # 3 sections horizontally
        world_height = 3  # 3 sections vertically
        assets_path = 'assets'  # Path to assets
        self.world = World(world_width, world_height, section_size, assets_path)

        # Calculate total world size in pixels
        world_pixel_width = world_width * section_size[0]
        world_pixel_height = world_height * section_size[1]
        # Initialize camera
        self.camera = Camera(self.screen_width, self.screen_height, world_pixel_width, world_pixel_height)

        # Initialize player
        player_width = 50
        player_height = 50
        player_x = self.screen_width // 2 - player_width // 2
        player_y = self.screen_height - player_height - 10  
        self.player = Player(player_x, player_y, player_width, player_height)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        self.player.handle_input(keys_pressed)
        self.player.apply_gravity(self.physics.gravity)
        self.player.update(self.physics)

        # Ground collision
        if self.player.rect.bottom >= self.world.world_height * self.world.section_size[1] - 10:
            self.player.rect.bottom = self.world.world_height * self.world.section_size[1] - 10
            self.player.velocity.y = 0
            self.player.on_ground = True
        else:
            self.player.on_ground = False

        # Platform collision
        for platform in self.world.platforms:
            if self.player.rect.colliderect(platform):
                if self.player.velocity.y > 0:  # Falling down
                    self.player.rect.bottom = platform.top
                    self.player.velocity.y = 0
                    self.player.on_ground = True

        # Left boundary
        if self.player.rect.left <= 0:
            self.player.rect.left = 0
            self.player.velocity.x = 0

        # Right boundary
        if self.player.rect.right >= self.world.world_width * self.world.section_size[0]:
            self.player.rect.right = self.world.world_width * self.world.section_size[0]
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
        self.ui.draw_text("Pressione Fechar para Sair", 10, 10)

        pygame.display.flip()
