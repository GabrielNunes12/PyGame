import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = None
        
    def play_background_music(self, music_file, volume=0.5, loop=-1):
        """
        Toca música ambiente
        :param music_file: Caminho para o arquivo de música
        :param volume: Volume entre 0.0 e 1.0
        :param loop: -1 para loop infinito, ou número de repetições
        """
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop)
        except pygame.error as e:
            print(f"Erro ao carregar música: {e}")
            
    def stop_background_music(self):
        """Para a música ambiente"""
        pygame.mixer.music.stop() 