import pygame
import os

class Animation:
    def __init__(self):
        self.animations = {}
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.2
        self.last_update = pygame.time.get_ticks()
        self.is_playing = True
        self.facing_right = True

    def load_animation(self, name, sprite_path, frame_count):
        """Carrega uma sequência de sprites para uma animação"""
        self.animations[name] = []
        for i in range(frame_count):
            frame_path = os.path.join(sprite_path, f"{name}_{i}.png")
            try:
                image = pygame.image.load(frame_path).convert_alpha()
                self.animations[name].append(image)
            except:
                print(f"Erro ao carregar frame: {frame_path}")

    def play(self, animation_name, force=False):
        """Inicia uma animação"""
        if self.current_animation != animation_name or force:
            self.current_animation = animation_name
            self.current_frame = 0
            self.is_playing = True

    def update(self):
        """Atualiza o frame atual da animação"""
        if not self.is_playing:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:
            self.current_frame += 1
            if self.current_frame >= len(self.animations[self.current_animation]):
                self.current_frame = 0
            self.last_update = current_time

    def get_current_frame(self):
        """Retorna o frame atual da animação"""
        if self.current_animation in self.animations:
            frame = self.animations[self.current_animation][self.current_frame]
            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
            return frame
        return None 