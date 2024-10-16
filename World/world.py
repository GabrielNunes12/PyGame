
import pygame
import os

class World:
    def __init__(self, world_width, world_height, section_size, assets_path):
        """
        Initializes the world.

        :param world_width: Number of sections horizontally
        :param world_height: Number of sections vertically
        :param section_size: Size of each section in pixels (width, height)
        :param assets_path: Path to the assets directory
        """
        self.world_width = world_width
        self.world_height = world_height
        self.section_size = section_size
        self.assets_path = assets_path

        # Calculate total world size
        self.total_width = world_width * section_size[0]
        self.total_height = world_height * section_size[1]

        # Load or create sections
        self.sections = {}
        for x in range(world_width):
            for y in range(world_height):
                self.sections[(x, y)] = self.load_section(x, y)

        # Example: Adding platforms to specific sections
        self.platforms = []
        for (x, y), section in self.sections.items():
            if (x, y) == (1, 1):  # Middle section
                # Add a platform in the middle section
                platform_rect = pygame.Rect(
                    x * section_size[0] + 200,  # X position within world
                    y * section_size[1] + 500,  # Y position within world
                    400,  # Width
                    20    # Height
                )
                self.platforms.append(platform_rect)

    def load_section(self, x, y):
        """
        Loads a section of the world. For simplicity, we'll fill sections with different colors.

        :param x: Section's x-coordinate in the grid
        :param y: Section's y-coordinate in the grid
        :return: Surface representing the section
        """
        section_surface = pygame.Surface(self.section_size)

        # Simple color variation based on position
        color = (
            (x * 40) % 256,
            (y * 40) % 256,
            ((x + y) * 20) % 256
        )
        section_surface.fill(color)

        # TODO: add more images to be obstacle here

        return section_surface

    def draw(self, screen, camera_offset):
        """
        Draws the visible sections based on the camera offset.

        :param screen: The main screen surface
        :param camera_offset: Tuple representing the camera's x and y offset
        """
        section_width, section_height = self.section_size
        screen_width, screen_height = screen.get_size()

        # Determine the range of sections to draw based on camera offset
        start_x = max(camera_offset[0] // section_width, 0)
        start_y = max(camera_offset[1] // section_height, 0)
        end_x = min((camera_offset[0] + screen_width) // section_width + 1, self.world_width)
        end_y = min((camera_offset[1] + screen_height) // section_height + 1, self.world_height)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                section = self.sections.get((x, y))
                if section:
                    # Calculate the position to blit the section
                    blit_x = x * section_width - camera_offset[0]
                    blit_y = y * section_height - camera_offset[1]
                    screen.blit(section, (blit_x, blit_y))

        # Draw platforms
        for platform in self.platforms:
            screen_x = platform.x - camera_offset[0]
            screen_y = platform.y - camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, platform.width, platform.height))
