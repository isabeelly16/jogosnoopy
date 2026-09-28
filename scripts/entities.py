import pygame
from .assets import load_first_image, find_images_recursive
from .settings import ASSETS_DIR

class NPC:
    def __init__(self, folder, animation, name, position):
        self.name = name
        self.frames = []
        from .assets import load_animation
        self.frames = load_animation(folder, animation)

        if self.frames:
            self.image = pygame.transform.smoothscale(self.frames[0], (80, 80))
        else:
            self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (180, 100, 180), (40, 40), 30)

        self.rect = self.image.get_rect(center=position)

class Clue:
    def __init__(self, image, name, description, position, points):
        self.image = image
        self.name = name
        self.description = description
        self.points = points
        self.collected = False
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

class GameState:
    def __init__(self):
        self.score = 0
        self.attempts = 3
        self.phase = 1
        self.clues = []
        self.inventory = []

    def add_clue(self, clue):
        if clue.collected:
            return
        clue.collected = True
        self.score += clue.points
        self.inventory.append(clue.name)
