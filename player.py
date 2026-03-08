import pygame
from image_effects import *
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
            elif self.left:
                flipped_frame = pygame.transform.flip(
                    frames_char[self.walk_count], True, False)
                win.blit(flipped_frame, (self.x, self.y))
            else:
                win.blit(frames_down[self.walk_count], (self.x, self.y))
        self.hitbox = (self.x+10, self.y, 45, 60)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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