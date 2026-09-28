from pathlib import Path
import pygame
from .settings import ASSETS_DIR

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

def list_images(folder: Path):
    if not folder.exists():
        return []
    return sorted(
        [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS],
        key=lambda p: str(p).lower()
    )

def load_image(path: Path, size=None):
    image = pygame.image.load(str(path)).convert_alpha()
    if size:
        image = pygame.transform.smoothscale(image, size)
    return image

def load_animation(folder_name: str, animation_name: str):
    folder = ASSETS_DIR / folder_name / animation_name
    paths = list_images(folder)
    return [load_image(p) for p in paths]

def load_first_image(folder_name: str, animation_name: str, size=None):
    frames = load_animation(folder_name, animation_name)
    if not frames:
        return None
    image = frames[0]
    if size:
        image = pygame.transform.smoothscale(image, size)
    return image

def find_images_recursive(folder_name: str):
    return list_images(ASSETS_DIR / folder_name)

def scenario_path(phase: int):
    names = {
        1: "fase_1_Casa_do_Snoopy.png",
        2: "fase_2_Parque.png",
        3: "fase_3_Floresta.png",
        4: "fase_4_Quarto_do_Misterio.png",
        5: "fase_5_Local_do_Resgate.png",
    }
    return ASSETS_DIR / "Cenarios_Completos" / names[phase]

def load_scenario(phase: int, size):
    path = scenario_path(phase)
    if not path.exists():
        raise FileNotFoundError(f"Cenário não encontrado: {path}")
    return load_image(path, size)
