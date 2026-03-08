import pygame
from image_effects import *
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

    def __init__(self, x, y, width, height, end, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkcount = 0
        self.vel = velocity
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