import pygame

pygame.init()

# window
win = pygame.display.set_mode((853, 213))
screen_width = 853
# name
pygame.display.set_caption("PyGame")

# Slicing the frame


def slicing(object, section, frame_width, frame_height):
    sliced = []
    for i in range(section):
        frame = object.subsurface(
            (i * frame_width, 0, frame_width, frame_height))
        sliced.append(frame)
    return sliced


# character image
walk = pygame.image.load("images\\64x64\\2d\\walk.png")
frames = slicing(walk, 6, 64, 64)


# Backgrounds
layers = [
    pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-7-sky-background.png"),
    pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-6-clouds.png"),
    pygame.image.load("images\\Adventure 2D Tileset\\Layers\\x32-layer-5-mountains-3.png"), pygame.image.load("images\\Adventure 2D Tileset\\Layers\\x32-layer-3-mountains-1.png"), pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-4-mountains-2.png"), pygame.image.load("images\\Adventure 2D Tileset\\Layers\\x32-layer-2-trees-2.png"),
    pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-1-trees-1.png")
]
# *scale down
layers = [pygame.transform.scale(layer, (853, 213)) for layer in layers]

char = pygame.image.load("images\\64x64\\2d\\idle.png")
frames_char = slicing(char, 6, 64, 64)

jump = pygame.image.load("images\\64x64\\2d\\jump.png")
frames_jump = slicing(jump, 6, 64, 64)

food = pygame.image.load("images\\PixelFishes\\PixelFishes.png")
frames_food = slicing(food, 1, 32, 32)

bullet_sound = pygame.mixer.Sound("Sounds\\mixkit-little-cat-pain-meow-87.wav")
hit_sound = pygame.mixer.Sound("Sounds\\anime-ahh.wav")
bg_music = pygame.mixer.music.load(
    "Sounds\\SSvid.net--Twinkle-Twinkle-Little-StarChildren-s-Song-Music-Box.mp3")
pygame.mixer.music.play(-1)

# character measurements
clock = pygame.time.Clock()

# Score
score = 0


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 8
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x+10, self.y, 45, 60)

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.is_jump:  # keep the jumping animation going if you press other key
                if self.left:
                    current_jump_frame = frames_jump[self.jump_count % len(
                        frames_jump)]
                    flipped_jump = pygame.transform.flip(
                        current_jump_frame, True, False)
                    win.blit(flipped_jump, (self.x, self.y))
                else:
                    current_jump_frame = frames_jump[self.jump_count % len(
                        frames_jump)]
                    win.blit(current_jump_frame, (self.x, self.y))
            elif self.left:
                flipped_frame = pygame.transform.flip(
                    frames[self.walk_count], True, False)
                win.blit(flipped_frame, (self.x, self.y))
            elif self.right:
                win.blit(frames[self.walk_count], (self.x, self.y))
        else:
            if self.right:
                win.blit(frames_char[self.walk_count], (self.x, self.y))
            else:
                flipped_frame = pygame.transform.flip(
                    frames_char[self.walk_count], True, False)
                win.blit(flipped_frame, (self.x, self.y))

        self.hitbox = (self.x+10, self.y, 45, 60)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)



    def hit(self):
        self.x = 0
        self.y = 165
        self.is_jump = False  # Add this line
        self.jump_count = 8   # Add this line
        self.walk_count = 0
        font1 = pygame.font.SysFont("Arial", 100)
        text = font1.render("-10", 1, (255, 0, 0))
        win.blit(text, (426 - (text.get_width()) /
                 2, 106.5 - (text.get_height())/2))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing

    def draw(self, win):  # drawuing the bullet
        # win.blit(frames_food, (self.x, self.y))
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemies():
    zombies_right = [
        pygame.image.load(
            "images\\Goblin\\Goblin\\PNG\\PNG Sequences\\Running\\0_Goblin_Running_000.png"),
    ]
    zombies_left = [
        pygame.image.load(
            "images\\Goblin\\Goblin\\PNG\\PNG Sequences\\Running left\\0_Goblin_Running_000.png"),
    ]
    death = pygame.image.load(
        "images\\Goblin\\Goblin\\PNG\\PNG Sequences\\Dying\\0_Goblin_Dying_014.png")

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkcount = 0
        self.vel = 5
        self.hitbox = (self.x+15, self.y, 32, 50)
        self.health = 60
        self.visible = True
        self.alive = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.alive:
                if self.walkcount + 1 <= 27:
                    self.walkcount = 0

                if self.vel > 0:
                    win.blit(
                        self.zombies_right[self.walkcount // 3], (self.x, self.y))
                    self.walkcount += 1
                    if self.walkcount >= len(self.zombies_right) * 3:
                        self.walkcount = 0
                else:
                    win.blit(
                        self.zombies_left[self.walkcount // 3], (self.x, self.y))
                    self.walkcount += 1
                    if self.walkcount >= len(self.zombies_right) * 3:
                        self.walkcount = 0
            else:  # print death image
                self.width = 0
                self.height = 0
                win.blit(self.death, (self.x, self.y))

            pygame.draw.rect(win, (255, 0, 0),
                             (self.hitbox[0] - 10, self.hitbox[1] - 20, 60, 10))
            pygame.draw.rect(win, (0, 255, 0),
                             (self.hitbox[0] - 10, self.hitbox[1] - 20, 60 - (60 - self.health), 10))
            self.hitbox = (self.x+15, self.y+12, 32, 50)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if not self.alive:
            return
        if self.vel > 0:
            if self.x - self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):  # collision with the bullet
        hit_sound.play()
        if self.health > 0:
            self.health -= 10
        else:
            self.alive = False


def redraw_game():
    # Creating the background
    for layer in layers:
        win.blit(layer, (0, 0))

    text = font.render("Score: " + str(score), 1, (255, 0, 0))
    win.blit(text, (426, 0))

    # Creating the player and enemy
    player.draw(win)
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
    goblin = Enemies(100 + i * 140, 159, 64, 64, 250 + i * 140)
    goblins.append(goblin)
    
for goblin in goblins:  # Draw all goblins
    goblin.draw(win)
shoot_cd = 0
bullets = []
run = True
while run:
    clock.tick(27)

    # player and enemy collision
    if goblin.alive:
        if player.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player.hitbox[1] + player.hitbox[3] > goblin.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > goblin.hitbox[0] and player.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                player.hit()
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
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.alive:
                    goblin.hit()
                    score += 10
                    bullets.pop(bullets.index(bullet))

        if 0 < bullet.x < 853:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # key press and checking the boundary
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_cd == 0:
        bullet_sound.play()
        # make sure the direction of the bullet
        if player.left:
            facing = -1
        else:
            facing = 1

        # drawing the bullet
        if len(bullets) < 10:
            bullets.append(Projectile(round(player.x + player.width // 2),
                           round(player.y + player.height // 2), 6, (0, 0, 0), facing))

        shoot_cd = 1

    # walking left
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
        player.walk_count = (player.walk_count + 1) % len(frames)

    # walking right
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < screen_width - player.width:
        player.x += player.vel
        player.left = False
        player.right = True
        player.standing = False
        player.walk_count = (player.walk_count + 1) % len(frames)
    else:
        player.standing = True
        player.walk_count = 0

    if not (player.is_jump):  # determine is jumping or not
        if keys[pygame.K_w]:
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
