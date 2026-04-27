import pygame
import random
import os

pygame.init()

# Skjerm
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chest Coin Catcher")

# Bilder
bg = pygame.image.load("bg1.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

coin_img = pygame.image.load("2d gold coin.png")
bomb_img = pygame.image.load("2d bombe.png")
chest_img = pygame.image.load("chest.jpg")
logo_img = pygame.image.load("logo 1.png")

coin_img = pygame.transform.scale(coin_img, (50, 50))
bomb_img = pygame.transform.scale(bomb_img, (50, 50))
logo_img = pygame.transform.scale(logo_img, (50, 50))
chest_img = pygame.transform.scale(chest_img, (100, 80))

# Chest
chest = pygame.Rect(WIDTH//2, HEIGHT-100, 100, 80)
speed = 7

# Objekter
objects = []

# Score
score = 0

# Fonts
score_font = pygame.font.SysFont(None, 40)
highscore_font = pygame.font.SysFont(None, 50)
gameover_font = pygame.font.SysFont(None, 60)

# Highscore
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

highscore = load_highscore()

# Outline tekst
def draw_text_with_outline(text, font, color, outline_color, center_pos):
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)

    rect = base.get_rect(center=center_pos)

    for dx in [-2, 2]:
        for dy in [-2, 2]:
            screen.blit(outline, (rect.x + dx, rect.y + dy))

    screen.blit(base, rect)

clock = pygame.time.Clock()
running = True
game_over = False
new_highscore = False

# Spawn system
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 800)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT and not game_over:
            x = random.randint(0, WIDTH - 50)

            r = random.random()
            if r < 0.3:
                objects.append({"rect": pygame.Rect(x, 0, 50, 50), "type": "logo"})
            elif r < 0.7:
                objects.append({"rect": pygame.Rect(x, 0, 50, 50), "type": "coin"})
            else:
                objects.append({"rect": pygame.Rect(x, 0, 50, 50), "type": "bomb"})

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                score = 0
                objects.clear()
                game_over = False
                new_highscore = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and chest.x > 0:
            chest.x -= speed
        if keys[pygame.K_RIGHT] and chest.x < WIDTH - chest.width:
            chest.x += speed

# Oppdater objekter
    for obj in objects[:]:
        obj["rect"].y += 5

        if obj["rect"].colliderect(chest):
            if obj["type"] == "coin":
                score += 1
            elif obj["type"] == "logo":
                score += 10
            elif obj["type"] == "bomb":
                game_over = True
                if score > highscore:
                    highscore = score
                    save_highscore(score)
                    new_highscore = True
            objects.remove(obj)

        elif obj["rect"].y > HEIGHT:
            objects.remove(obj)

# Tegn bakgrunn
    screen.blit(bg, (0, 0))

# Tegn objekter
    for obj in objects:
        if obj["type"] == "coin":
            screen.blit(coin_img, obj["rect"])
        elif obj["type"] == "bomb":
            screen.blit(bomb_img, obj["rect"])
        elif obj["type"] == "logo":
            screen.blit(logo_img, obj["rect"])

# Tegn chest
    screen.blit(chest_img, chest)

# Mindre og ryddigere UI
    draw_text_with_outline(
        f"Score: {score}",
        score_font,
        (255, 255, 255),
        (0, 0, 0),
        (WIDTH // 2, 40)
    )

    draw_text_with_outline(
        f"High Score: {highscore}",
        highscore_font,
        (255, 255, 0),
        (0, 0, 0),
        (WIDTH // 2, 85)
    )

# Game Over
    if game_over:
        draw_text_with_outline(
            "GAME OVER",
            gameover_font,
            (255, 0, 0),
            (0, 0, 0),
            (WIDTH // 2, HEIGHT // 2 - 40)
        )

        if new_highscore:
            draw_text_with_outline(
                "NEW HIGH SCORE!",
                score_font,
                (0, 255, 0),
                (0, 0, 0),
                (WIDTH // 2, HEIGHT // 2 + 20)
            )

        draw_text_with_outline(
            "Press R to restart",
            score_font,
            (255, 255, 255),
            (0, 0, 0),
            (WIDTH // 2, HEIGHT // 2 + 80)
        )

    pygame.display.flip()

pygame.quit()