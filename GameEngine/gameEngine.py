import pygame
# import physics class from Physics folder
from physics import PhysicsEngine
from UI import UI
from Entities.Player import Player
from World.world import World
from camera import Camera
from os import path

class GameEngine:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Collect all items")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize modules
        self.physics = PhysicsEngine()
        self.ui = UI(self.screen)

        # Initialize world
        section_size = (1280, 720)  # Each section is the size of the screen
        world_width = 3  # 3 sections horizontally
        world_height = 3  # 3 sections vertically
        assets_path = 'assets'  # Path to assets
        self.world = World(world_width, world_height, section_size, assets_path)

        # Calculate total world size in pixels
        self.world_pixel_width = world_width * section_size[0]  # 2400
        self.world_pixel_height = world_height * section_size[1]  # 1800

        # Initialize camera
        self.camera = Camera(self.screen_width, self.screen_height, self.world_pixel_width, self.world_pixel_height)

        # Initialize player
        player_width = 50
        player_height = 50
        player_x = self.world_pixel_width // 2 - player_width // 2  # 1175
        player_y = self.world_pixel_height // 2 - player_height // 2  # 875
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

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        self.player.handle_input(keys_pressed)
        self.player.apply_gravity(self.physics.gravity)
        self.player.update(self.physics)

        # Ground collision
        if self.player.rect.bottom >= self.world.total_height - 10:
            self.player.rect.bottom = self.world.total_height - 10
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