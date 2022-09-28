from setup import*


class Sfx_Sound():
    def __init__(self,path):
        self.sound = pygame.mixer.Sound(path)

    def play_sound(self,loop):
        self.sound.play(loop)

class Sfx_Music():
    pass