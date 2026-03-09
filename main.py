import pygame
from enemy import Enemies
from image_effects import *
from weapons import Projectile
from player import Player
import random

pygame.init()

# window
win = pygame.display.set_mode((853, 213))
screen_width = 853
# name
pygame.display.set_caption("PyGame")

# character measurements
clock = pygame.time.Clock()

# Score
score = 0


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
shoot_cd = 0
bullets = []
run = True
while run:
    clock.tick(27)

    # player and enemy collision
    for goblin in goblins:
        if goblin.alive:
            if player.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player.hitbox[1] + player.hitbox[3] > goblin.hitbox[1]:
                if player.hitbox[0] + player.hitbox[2] > goblin.hitbox[0] and player.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    player.hit(win)
                    score -= 10

    # shooting cooldown
    if shoot_cd > 0:
        shoot_cd += 1
    if shoot_cd > 3:
        shoot_cd = 0

    # Ending the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # shooting and cleaning the bullet on the screen
    for bullet in bullets[:]:
        if bullet.type == "dot":
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

    if keys[pygame.K_l] and shoot_cd == 0:
        bullet_sound.play()
        # make sure the direction of the bullet
        if player.left:
            facing = -1
        else:
            facing = 1

        # drawing the bullet
        if len(bullets) < 5:
            if player.down:
                bullets.append(Projectile(round(player.x + player.width // 2),
                                          round(player.y + player.height // 2), 6, facing, "beam"))
            else:
                bullets.append(Projectile(round(player.x + player.width // 2),
                                          round(player.y + player.height // 2), 6, facing, "dot"))
        shoot_cd = 1

    # walking left
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
        player.down = False
        player.walk_count = (player.walk_count + 1) % len(frames)

    # walking right
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < screen_width - player.width:
        player.x += player.vel
        player.left = False
        player.right = True
        player.standing = False
        player.down = False
        player.walk_count = (player.walk_count + 1) % len(frames)

    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.left = False
        player.right = False
        player.standing = True
        player.down = True
        player.walk_count = (player.walk_count + 1) % len(frames_down)
    else:
        player.standing = True
        player.down = False
        player.walk_count = 0

    if not (player.is_jump):  # determine is jumping or not
        if keys[pygame.K_SPACE]:
            player.is_jump = True
    else:  # what happens actually jumping
        # make sure it follow the quadratic curve(moving down)
        if player.jump_count >= -8:
            negative = 1
            if player.jump_count < 0:  # To let the character move down
                negative = -1
            player.y -= (player.jump_count ** 2) * 0.5 * negative
            player.jump_count -= 1
        else:  # finish jumping
            player.is_jump = False
            player.jump_count = 8

    player.walk_count = (player.walk_count + 1) % len(frames)
    player.walk_count = (player.walk_count + 1) % len(frames_char)
    player.walk_count = (player.walk_count + 1) % len(frames_jump)

    redraw_game()

pygame.quit()
