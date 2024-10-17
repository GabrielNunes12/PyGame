import pygame
class UI:
    def __init__(self, screen, font_path=None, font_size=24):
        self.screen = screen
        self.font_size = font_size
        self.font_path = font_path or pygame.font.get_default_font()
        self.font = pygame.font.Font(self.font_path, self.font_size)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        """
        Renders and draws text on the screen.

        :param text: The text to render
        :param x: X-coordinate on the screen
        :param y: Y-coordinate on the screen
        :param color: Text color
        """
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))