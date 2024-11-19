import pygame
class Enemy:
    def __init__(self, life, attack_damage):
        self.enemy_life = life
        self.attack_damage = attack_damage
        self.health = 100
        self.max_health = 100

    def take_damage(self, amount):
        """Recebe dano e retorna se morreu"""
        self.health -= amount
        if self.health <= 0:
            return True
        return False

    def attack(self):
        print(f"Enemy attacks with {self.attack_damage} damage!")
    def draw(self, screen, camera_offset):
        # Desenha barra de vida
        if self.health < self.max_health:
            health_rect = pygame.Rect(
                self.rect.x - camera_offset[0],
                self.rect.y - camera_offset[1] - 10,
                self.rect.width * (self.health / self.max_health),
                5
            )
            pygame.draw.rect(screen, (255, 0, 0), health_rect)