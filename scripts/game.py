import pygame
from .settings import WIDTH, HEIGHT, FPS, ASSETS_DIR, WHITE, YELLOW
from .assets import load_scenario, find_images_recursive
from .player import Player
from .entities import NPC, Clue, GameState
from .ui import UI

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snoopy: O Mistério do Woodstock")
        self.clock = pygame.time.Clock()

        self.ui = UI()
        self.state = GameState()
        self.player = Player()

        self.running = True
        self.menu = True
        self.paused = False
        self.inventory_open = False
        self.dialog_open = False
        self.dialog_index = 0

        self.scenario = None
        self.npcs = []
        self.clues = []
        self.load_phase(1)

    def load_phase(self, phase):
        self.state.phase = phase
        self.state.attempts = 3
        self.scenario = load_scenario(phase, (WIDTH, HEIGHT))
        self.player.rect.center = (150, 500)

        self.npcs = []
        if phase == 1:
            self.npcs = [
                NPC("Charlie_Brown", "parado", "Charlie Brown", (900, 420))
            ]
        elif phase == 2:
            self.npcs = [
                NPC("Charlie_Brown", "parado", "Charlie Brown", (350, 330)),
                NPC("Lucy", "parado", "Lucy", (800, 430)),
            ]
        elif phase == 3:
            self.npcs = [
                NPC("Schroeder", "parado", "Schroeder", (850, 420))
            ]
        elif phase == 4:
            self.npcs = [
                NPC("Lucy", "parado", "Lucy", (780, 400))
            ]
        elif phase == 5:
            self.npcs = [
                NPC("Woodstock", "parado", "Woodstock", (900, 420))
            ]

        self.create_clues(phase)

    def create_clues(self, phase):
        self.clues = []

        paths = find_images_recursive("Objetos_Pistas")
        images = []

        for path in paths:
            try:
                image = pygame.image.load(str(path)).convert_alpha()
                image = pygame.transform.smoothscale(image, (55, 55))
                images.append(image)
            except pygame.error:
                pass

        # No início, usamos os primeiros assets da pasta de pistas.
        # Depois você pode trocar pelos objetos exatos de cada fase.
        positions = [
            (320, 250),
            (560, 410),
            (780, 260),
            (950, 520),
            (480, 560),
        ]

        names = [
            "Pena amarela",
            "Bilhete misterioso",
            "Pegadas",
            "Fotografia",
            "Chave",
        ]

        descriptions = [
            "Uma pena amarela. Parece ser de Woodstock.",
            "O bilhete diz: Siga as pistas.",
            "Pegadas pequenas levam para outra área.",
            "Uma fotografia pode revelar uma informação importante.",
            "Uma chave. Talvez abra alguma coisa.",
        ]

        points = [100, 150, 100, 200, 200]

        for i in range(min(5, len(images))):
            self.clues.append(
                Clue(images[i], names[i], descriptions[i], positions[i], points[i])
            )

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()

            if not self.menu and not self.paused and not self.dialog_open:
                keys = pygame.key.get_pressed()
                self.player.update(dt, keys)
                self.check_interactions()

            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type != pygame.KEYDOWN:
                continue

            if self.menu:
                if event.key == pygame.K_RETURN:
                    self.menu = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                continue

            if self.dialog_open:
                if event.key == pygame.K_RETURN:
                    self.dialog_open = False
                continue

            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused

            elif event.key == pygame.K_i and not self.paused:
                self.inventory_open = not self.inventory_open

            elif event.key == pygame.K_e and not self.paused:
                self.interact()

            if self.paused and event.key == pygame.K_ESCAPE:
                self.paused = False

    def interact(self):
        # Primeiro tenta falar com NPC.
        for npc in self.npcs:
            if self.player.rect.colliderect(npc.rect.inflate(45, 45)):
                self.dialog_open = True
                self.dialog_index = 0
                return

        # Depois tenta pegar uma pista.
        for clue in self.clues:
            if not clue.collected and self.player.rect.colliderect(clue.rect.inflate(35, 35)):
                self.player.set_action("pickup")
                self.state.add_clue(clue)

                # Se todas as pistas da fase forem encontradas, avança.
                if self.all_clues_collected():
                    self.advance_phase()
                return

    def check_interactions(self):
        # Não coleta automaticamente: apenas mostra a dica de interação.
        near_npc = any(
            self.player.rect.colliderect(n.rect.inflate(45, 45))
            for n in self.npcs
        )
        near_clue = any(
            not c.collected and self.player.rect.colliderect(c.rect.inflate(35, 35))
            for c in self.clues
        )

        self.near_interaction = near_npc or near_clue

    def all_clues_collected(self):
        return len(self.clues) > 0 and all(c.collected for c in self.clues)

    def advance_phase(self):
        if self.state.phase < 5:
            self.state.phase += 1
            self.load_phase(self.state.phase)
        else:
            self.dialog_open = True

    def draw(self):
        if self.menu:
            self.draw_menu()
            return

        self.screen.blit(self.scenario, (0, 0))

        for clue in self.clues:
            clue.draw(self.screen)

        for npc in self.npcs:
            self.screen.blit(npc.image, npc.rect)

        self.screen.blit(self.player.image, self.player.rect)

        self.ui.hud(
            self.screen,
            self.state.score,
            self.state.phase,
            self.state.attempts,
            sum(c.collected for c in self.clues),
            len(self.clues),
        )

        if getattr(self, "near_interaction", False):
            self.ui.interaction(self.screen, "E — INVESTIGAR / INTERAGIR")

        if self.inventory_open:
            self.draw_inventory()

        if self.paused:
            self.ui.pause(self.screen)

        if self.dialog_open:
            if self.state.phase == 5 and self.all_clues_collected():
                self.ui.dialog(
                    self.screen,
                    "MISTÉRIO RESOLVIDO!",
                    "Você encontrou Woodstock e concluiu a investigação!",
                )
            else:
                self.ui.dialog(
                    self.screen,
                    "NPC",
                    "Você viu alguma coisa? Talvez esta pista ajude na investigação.",
                )

        pygame.display.flip()

    def draw_menu(self):
        self.screen.fill((55, 45, 75))
        self.ui.text(self.screen, "SNOOPY", (440, 150), self.ui.font_big, WHITE)
        self.ui.text(self.screen, "O MISTÉRIO DO WOODSTOCK", (330, 205), self.ui.font_big, YELLOW)
        self.ui.text(self.screen, "ENTER — NOVO JOGO", (420, 350), self.ui.font, WHITE)
        self.ui.text(self.screen, "ESC — SAIR", (480, 400), self.ui.font, WHITE)
        pygame.display.flip()

    def draw_inventory(self):
        box = pygame.Rect(180, 100, 792, 500)
        pygame.draw.rect(self.screen, (35, 35, 50), box, border_radius=20)
        pygame.draw.rect(self.screen, YELLOW, box, 3, border_radius=20)

        self.ui.text(self.screen, "INVENTÁRIO", (470, 130), self.ui.font_big, YELLOW)

        if not self.state.inventory:
            self.ui.text(self.screen, "Nenhuma pista encontrada.", (390, 250), self.ui.font)
        else:
            y = 220
            for item in self.state.inventory:
                self.ui.text(self.screen, "• " + item, (300, y), self.ui.font)
                y += 45

        self.ui.text(self.screen, "I — fechar", (510, 550), self.ui.font_small, WHITE)
