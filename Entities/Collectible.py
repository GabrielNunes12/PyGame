
import pygame
import os

class Collectible:
    def __init__(self, x, y, width=30, height=30, image_path=None):
        """
        Initializes the collectible item.

        :param x: X-coordinate in the world
        :param y: Y-coordinate in the world
        :param width: Width of the collectible
        :param height: Height of the collectible
        :param image_path: Path to the collectible image
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False

        if image_path and os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            print(f"Unable to load collectible image at {image_path}. Using circle instead.")
            self.image = None

    def draw(self, screen, camera_offset):
        """
        Draws the collectible on the screen based on camera offset.

        :param screen: The main screen surface
        :param camera_offset: Tuple representing the camera's x and y offset
        """
        if self.collected:
            return  # Do not draw if already collected

        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        if self.image:
            screen.blit(self.image, (screen_x, screen_y))
        else:
            # Draw a simple circle as a placeholder
            pygame.draw.circle(screen, (255, 215, 0), (screen_x + self.rect.width // 2, screen_y + self.rect.height // 2), self.rect.width // 2)