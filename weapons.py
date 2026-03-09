import pygame
from image_effects import *
class Projectile():
    def __init__(self, x, y, radius, facing, bullet_type):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.vel = 8*facing
        self.type = bullet_type
        self.life = 3

    def draw(self, win):  # drawuing the bullet
        if self.type == "basic_attack":
            food = frames_food[0]
            food_x = self.x - food.get_width() // 2
            food_y = self.y - food.get_height() // 2
            win.blit(food, (food_x, food_y))
        
        elif self.type == "beam":
            end_x = self.x + 1000 * self.facing
            
            pygame.draw.line(win, (40,139,163), (self.x, self.y), (end_x, self.y), 10)
            pygame.draw.line(win, (67,146,165), (self.x, self.y), (end_x, self.y), 6)
            pygame.draw.line(win, (142,196,208), (self.x, self.y), (end_x, self.y), 4)
            pygame.draw.line(win, (33,102,120), (self.x, self.y), (end_x, self.y), 4)
            pygame.draw.line(win, (250,252,253), (self.x, self.y), (end_x, self.y), 4)
