import pygame
from enemy import Enemies
from image_effects import *
from weapons import Projectile
from player import Player
import random
from main_menu import MainMenu

pygame.init()

# window
SCREEN_WIDTH = 853
SCREEN_HEIGHT = 213
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# name
pygame.display.set_caption("PyGame")

# character measurements
clock = pygame.time.Clock()

# Game variables
score = 0
game_running = False
menu_state = "main"

def redraw_game():
    # Creating the background
    for layer in layers:
        win.blit(layer, (0, 0))

    text = font.render("Score: " + str(score), 1, (255, 0, 0))
    win.blit(text, (426, 0))

    # Creating the player and enemy
    player.draw(win)
    for goblin in goblins:
        goblin.draw(win)

    # drawing the bullet
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# main loop
font = pygame.font.SysFont("Arial", 30, True, False)
player = Player(0, 165, 64, 64)
main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
NUMBER_OF_ENEMY = 5
goblins = []
for i in range(NUMBER_OF_ENEMY):
    goblin = Enemies(x=100 + i * 140,
                     y=159,
                     width=64,
                     height=64,
                     end=250 + i * 140,
                     velocity=random.randint(1, 5))
    goblins.append(goblin)

for goblin in goblins:  # Draw all goblins
    goblin.draw(win)

bullets = []
run = True

while run:
    clock.tick(27)

    if not game_running:
        action = main_menu.main_menu(win=win)
        if action == "play":
            game_running = True
            pygame.display.set_caption("PyGame")
        elif action == "quit":
            run = False
    else:
        redraw_game()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_running = False

    # player and enemy collision
    for goblin in goblins:
        if goblin.alive:
            if player.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player.hitbox[1] + player.hitbox[3] > goblin.hitbox[1]:
                if player.hitbox[0] + player.hitbox[2] > goblin.hitbox[0] and player.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    player.hit(win)
                    score -= 10

    # Ending the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # shooting and cleaning the bullet on the screen
    for bullet in bullets[:]:
        if bullet.type == "basic_attack":
            for goblin in goblins:
                if goblin.alive:
                    if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                        if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                            if goblin.alive:
                                goblin.hit()
                                score += 10
                                bullets.pop(bullets.index(bullet))
                                break

            if bullet in bullets:
                if 0 < bullet.x < 853:
                    bullet.x += bullet.vel
                else:
                    bullets.remove(bullet)
        elif bullet.type == "beam" and player.down:
            for goblin in goblins:
                if goblin.alive:
                    if abs(goblin.hitbox[1] - bullet.y) < goblin.hitbox[3]:

                        if bullet.facing == 1 and goblin.x > bullet.x:
                            goblin.hit()
                            score += 10

                        if bullet.facing == -1 and goblin.x < bullet.x:
                            goblin.hit()
                            score += 10

            bullet.life -= 1
            if bullet.life <= 0:
                bullets.remove(bullet)

    # key press and checking the boundary
    keys = pygame.key.get_pressed()
    player.move(keys, SCREEN_WIDTH)
    player.shoot(keys, bullets)
    redraw_game()

pygame.quit()
