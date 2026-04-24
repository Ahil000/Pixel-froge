import pygame
import random
import os

pygame.init()

# Skjerm
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chest Coin Catcher")

# Last bilder
bg = pygame.image.load("bg1.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

coin_img = pygame.image.load("2d gold coin.png")
bomb_img = pygame.image.load("2d bombe.png")
chest_img = pygame.image.load("chest.jpg")

# Skalering
coin_img = pygame.transform.scale(coin_img, (50, 50))
bomb_img = pygame.transform.scale(bomb_img, (50, 50))
chest_img = pygame.transform.scale(chest_img, (100, 80))

# Spiller
player_x = WIDTH // 2
player_y = HEIGHT - 120
player_speed = 7

# Objekter
coins = []
bombs = []

# Poeng
score = 0
font = pygame.font.SysFont(None, 40)

# Highscore
HS_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            return int(f.read())
    return 0

def save_highscore(hs):
    with open(HS_FILE, "w") as f:
        f.write(str(hs))

highscore = load_highscore()

# Klokke
clock = pygame.time.Clock()

running = True
game_over = False
new_high = False

while running:
    clock.tick(60)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
# Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        player_x = max(0, min(WIDTH - 100, player_x))

# Spawn coins
        if random.randint(1, 30) == 1:
            coins.append([random.randint(0, WIDTH - 50), 0])

        # Spawn bomber
        if random.randint(1, 60) == 1:
            bombs.append([random.randint(0, WIDTH - 50), 0])

        # Coins
        for coin in coins[:]:
            coin[1] += 5
            screen.blit(coin_img, coin)

            if player_y < coin[1] + 50 and player_x < coin[0] + 50 and player_x + 100 > coin[0]:
                coins.remove(coin)
                score += 1

            elif coin[1] > HEIGHT:
                coins.remove(coin)

# Bomber
        for bomb in bombs[:]:
            bomb[1] += 6
            screen.blit(bomb_img, bomb)

            if player_y < bomb[1] + 50 and player_x < bomb[0] + 50 and player_x + 100 > bomb[0]:
                game_over = True

            elif bomb[1] > HEIGHT:
                bombs.remove(bomb)

# Tegn spiller
        screen.blit(chest_img, (player_x, player_y))

# Tekst midt topp 
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        hs_text = font.render(f"High Score: {highscore}", True, (255, 255, 0))

        score_rect = score_text.get_rect(center=(WIDTH // 2, 20))
        hs_rect = hs_text.get_rect(center=(WIDTH // 2, 60))

        screen.blit(score_text, score_rect)
        screen.blit(hs_text, hs_rect)

    else:
# Highscore sjekk
        if score > highscore:
            highscore = score
            save_highscore(highscore)
            new_high = True

# Tekst midt topp 
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        hs_text = font.render(f"High Score: {highscore}", True, (255, 255, 0))

        go_rect = game_over_text.get_rect(center=(WIDTH // 2, 20))
        score_rect = score_text.get_rect(center=(WIDTH // 2, 60))
        hs_rect = hs_text.get_rect(center=(WIDTH // 2, 100))

        screen.blit(game_over_text, go_rect)
        screen.blit(score_text, score_rect)
        screen.blit(hs_text, hs_rect)

        if new_high:
            nh_text = font.render("NEW HIGH SCORE!", True, (0, 255, 0))
            nh_rect = nh_text.get_rect(center=(WIDTH // 2, 140))
            screen.blit(nh_text, nh_rect)

    pygame.display.update()

pygame.quit()