import pygame
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