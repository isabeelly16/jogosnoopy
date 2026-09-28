import pygame
from .settings import WHITE, BLACK, DARK, PURPLE, YELLOW

class UI:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 46)
        self.font = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 24)

    def text(self, screen, message, position, font=None, color=WHITE):
        font = font or self.font
        surface = font.render(message, True, color)
        screen.blit(surface, position)

    def hud(self, screen, score, phase, attempts, collected, total):
        pygame.draw.rect(screen, (35, 35, 50), (0, 0, 1152, 62))
        self.text(screen, f"Pontos: {score}", (20, 17))
        self.text(screen, f"Fase: {phase}/5", (240, 17))
        self.text(screen, f"Tentativas: {attempts}", (390, 17))
        self.text(screen, f"Pistas: {collected}/{total}", (620, 17))

    def interaction(self, screen, message):
        box = pygame.Rect(360, 625, 430, 55)
        pygame.draw.rect(screen, (20, 20, 30), box, border_radius=12)
        pygame.draw.rect(screen, YELLOW, box, 2, border_radius=12)
        self.text(screen, message, (385, 640), self.font_small, YELLOW)

    def dialog(self, screen, speaker, message):
        box = pygame.Rect(70, 525, 1012, 145)
        pygame.draw.rect(screen, (25, 25, 40), box, border_radius=18)
        pygame.draw.rect(screen, (220, 190, 90), box, 3, border_radius=18)
        self.text(screen, speaker, (95, 545), self.font, YELLOW)
        self.text(screen, message, (95, 585), self.font_small, WHITE)
        self.text(screen, "ENTER — continuar", (850, 635), self.font_small, (200, 200, 200))

    def pause(self, screen):
        overlay = pygame.Surface((1152, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))
        self.text(screen, "PAUSADO", (475, 250), self.font_big, WHITE)
        self.text(screen, "ESC — continuar", (460, 320), self.font, YELLOW)
        self.text(screen, "I — inventário", (465, 360), self.font, WHITE)
