import pygame
from .settings import PLAYER_SPEED, ANIMATION_SPEED
from .assets import load_animation


class Player:

    def __init__(self):

        # ==============================
        # CARREGAR SPRITES
        # ==============================

        self.idle = {
            "down": self.load_first("parado", 2),
            "up": self.load_first("parado", 3),
            "left": self.load_first("parado", 1),
            "right": self.load_first("parado", 0),
        }

        self.walk = {
            "down": self.load_animation("andando_frente"),
            "up": self.load_animation("andando_costas"),
            "left": self.load_animation("andando_esquerda"),
            "right": self.load_animation("andando_direita"),
        }

        self.investigating = self.load_animation("investigando")
        self.pickup = self.load_animation("pegando_pista")
        self.victory = self.load_animation("vitoria")
        self.defeat = self.load_animation("derrota")

        # ==============================
        # DIREÇÃO
        # ==============================

        self.direction = "down"

        # ==============================
        # ESTADO
        # ==============================

        self.state = "idle"

        # ==============================
        # ANIMAÇÃO
        # ==============================

        self.frame = 0
        self.animation_timer = 0

        # ==============================
        # VELOCIDADE
        # ==============================

        self.speed = PLAYER_SPEED

        # ==============================
        # IMAGEM INICIAL
        # ==============================

        self.image = self.idle["down"]

        self.image = pygame.transform.smoothscale(
            self.image,
            (90, 90)
        )

        # ==============================
        # POSIÇÃO
        # ==============================

        self.rect = self.image.get_rect()

        self.rect.center = (150, 500)

    # ==================================================
    # CARREGAR PRIMEIRO SPRITE
    # ==================================================

    def load_first(self, folder, index):

        frames = load_animation(
            "Snoopy",
            folder
        )

        if not frames:
            return pygame.Surface(
                (90, 90),
                pygame.SRCALPHA
            )

        index = min(index, len(frames) - 1)

        return frames[index]

    # ==================================================
    # CARREGAR ANIMAÇÃO
    # ==================================================

    def load_animation(self, folder):

        return load_animation(
            "Snoopy",
            folder
        )

    # ==================================================
    # ATUALIZAR
    # ==================================================

    def update(self, dt, keys):

        dx = 0
        dy = 0

        # ==============================
        # MOVIMENTO
        # ==============================

        if keys[pygame.K_a]:

            dx -= 1
            self.direction = "left"

        if keys[pygame.K_d]:

            dx += 1
            self.direction = "right"

        if keys[pygame.K_w]:

            dy -= 1
            self.direction = "up"

        if keys[pygame.K_s]:

            dy += 1
            self.direction = "down"

        # ==============================
        # MOVENDO
        # ==============================

        if dx != 0 or dy != 0:

            self.state = "walk"

            # evita andar mais rápido na diagonal
            length = (dx ** 2 + dy ** 2) ** 0.5

            dx /= length
            dy /= length

            self.rect.x += int(
                dx * self.speed * dt
            )

            self.rect.y += int(
                dy * self.speed * dt
            )

        # ==============================
        # PARADO
        # ==============================

        else:

            self.state = "idle"

            # MUITO IMPORTANTE:
            # NÃO anima o idle

            self.frame = 0

        # ==============================
        # LIMITES DA TELA
        # ==============================

        self.rect.left = max(
            0,
            self.rect.left
        )

        self.rect.right = min(
            1152,
            self.rect.right
        )

        self.rect.top = max(
            70,
            self.rect.top
        )

        self.rect.bottom = min(
            720,
            self.rect.bottom
        )

        # ==============================
        # ATUALIZAR SPRITE
        # ==============================

        self.update_animation(dt)

    # ==================================================
    # ANIMAÇÃO
    # ==================================================

    def update_animation(self, dt):

        # --------------------------------
        # PARADO
        # --------------------------------

        if self.state == "idle":

            image = self.idle[self.direction]

            self.image = pygame.transform.smoothscale(
                image,
                (90, 90)
            )

            return

        # --------------------------------
        # ANDANDO
        # --------------------------------

        if self.state == "walk":

            frames = self.walk[self.direction]

            if not frames:

                image = self.idle[self.direction]

                self.image = pygame.transform.smoothscale(
                    image,
                    (90, 90)
                )

                return

            self.animation_timer += dt

            if self.animation_timer >= ANIMATION_SPEED:

                self.animation_timer = 0

                self.frame += 1

                if self.frame >= len(frames):

                    self.frame = 0

            image = frames[self.frame]

            self.image = pygame.transform.smoothscale(
                image,
                (90, 90)
            )

    def set_action(self, action):

        if action in [
            "investigating",
            "pickup",
            "victory",
            "defeat"
        ]:

            self.state = action

            self.frame = 0

            self.animation_timer = 0