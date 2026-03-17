import pygame

text_font = pygame.font.SysFont("Arial", 30, True, False)

class Button():
    def __init__(self, image, x, y, text_input, base_colour, hovering_colour,  font=text_font):
        self.image = image
        self.x = x 
        self.y = y
        self.text_input = text_input
        self.font = font
        self.base_colour = base_colour
        self.hovering_colour = hovering_colour
        self.text = text_font.render("MAIN MENU", True, (255, 0, 0))
        if self.image is not None:
            self.image = self.text
        self.rectangle = self.image.get_rect(center=(self.x, self.y))
        self.text_rectangle = self.text.get_rect(center=(self.x, self.y))
        
    def update(self, win):
        if self.image is not None:
            win.blit(self.image, self.rectangle)
        win.blit(self.text, self.text_rectangle)
        
    def check_for_input(self, mouse_pos):
        if mouse_pos[0] in range(self.rectangle.left, self.rectangle.right) and mouse_pos[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        
    def change_colour(self, mouse_pos):
        if mouse_pos[0] in range(self.rectangle.left, self.rectangle.right) and mouse_pos[1] in range(self.rectangle.top, self.rectangle.bottom):
            self.text = text_font.render(self.text_input, True,self.hovering_colour)
        else:
            self.text = text_font.render(self.text_input, True, self.hovering_colour)
