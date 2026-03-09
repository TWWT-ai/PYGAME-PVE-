import pygame
from image_effects import *
from weapons import Projectile


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
        self.down = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x+10, self.y, 45, 60)
        self.shoot_cd = 0

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if self.down:
            win.blit(frames_down[self.walk_count %
                     len(frames_down)], (self.x, self.y))
        elif not self.standing:
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
                win.blit(frames_char[0], (self.x, self.y))
        else:
            if self.right:
                win.blit(frames_char[self.walk_count], (self.x, self.y))
            elif self.left:
                flipped_frame = pygame.transform.flip(
                    frames_char[self.walk_count], True, False)
                win.blit(flipped_frame, (self.x, self.y))
            else:
                win.blit(frames_char[0], (self.x, self.y))
        self.hitbox = (self.x+10, self.y, 45, 60)

    def hit(self, win):
        self.x = 0
        self.y = 165
        self.is_jump = False
        self.jump_count = 8
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

    def move(self, keys, screen_width):
        # walking left
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 0:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
            self.down = False
            self.walk_count = (self.walk_count + 1) % len(frames)

        # walking right
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < screen_width - self.width:
            self.x += self.vel
            self.left = False
            self.right = True
            self.standing = False
            self.down = False
            self.walk_count = (self.walk_count + 1) % len(frames)

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.left = False
            self.right = False
            self.standing = True
            self.down = True
            self.walk_count = (self.walk_count + 1) % len(frames_down)
        else:
            self.standing = True
            self.down = False
            self.walk_count = 0

        if not (self.is_jump):  # determine is jumping or not
            if keys[pygame.K_SPACE]:
                self.is_jump = True
        else:  # what happens actually jumping
            # make sure it follow the quadratic curve(moving down)
            if self.jump_count >= -8:
                negative = 1
                if self.jump_count < 0:  # To let the character move down
                    negative = -1
                self.y -= (self.jump_count ** 2) * 0.5 * negative
                self.jump_count -= 1
            else:  # finish jumping
                self.is_jump = False
                self.jump_count = 8

        self.walk_count = (self.walk_count + 1) % len(frames)
        self.walk_count = (self.walk_count + 1) % len(frames_char)
        self.walk_count = (self.walk_count + 1) % len(frames_jump)

    def shoot(self, keys, bullets):
        # shooting cooldown
        if self.shoot_cd > 0:
            self.shoot_cd += 1
        if self.shoot_cd > 3:
            self.shoot_cd = 0
        if keys[pygame.K_l] and self.shoot_cd == 0:
            bullet_sound.play()
            # make sure the direction of the bullet
            if self.left:
                facing = -1
            else:
                facing = 1

            # drawing the bullet
            if len(bullets) < 5:
                if self.down:
                    bullets.append(Projectile(round(self.x + self.width // 2),
                                              round(self.y + self.height // 2), 6, facing, "beam"))
                else:
                    bullets.append(Projectile(round(self.x + self.width // 2),
                                              round(self.y + self.height // 2), 6, facing, "basic_attack"))
            self.shoot_cd = 1
