import pygame
from image_effects import *
from button import Button


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.height = screen_height
        self.width = screen_width

    def main_menu(self, win):
        pygame.display.set_caption("Menu")

        MENU_FONT = pygame.font.SysFont("Arial", 30, True, False)
        MENU_RECT = MENU_FONT.render("Cat Adventure", True, (255, 0, 0))
        PLAY_BTN = Button(image=default_button,
                          x=self.width / 2,
                          y=0 + 40,
                          text_input="Play",
                          base_colour=(255, 0, 0),
                          hovering_colour=(255, 0, 100))
        
        OPTION_BTN = Button(image=default_button,
                          x=self.width / 2,
                          y=0 + 80,
                          text_input="Option",
                          base_colour=(255, 0, 0),
                          hovering_colour=(255, 0, 100))
        
        QUIT_BTN = Button(image=default_button,
                          x=self.width / 2,
                          y=0 + 120,
                          text_input="Quit",
                          base_colour=(255, 0, 0),
                          hovering_colour=(255, 0, 100))

        while True:
            win.blit(main_menu_bg, (0, 0))
            MOUSE_POS = pygame.mouse.get_pos()

            win.blit(MENU_RECT, (self.width / 2 - MENU_RECT.get_width() / 2, 0))

            for button in [PLAY_BTN, OPTION_BTN, QUIT_BTN]:
                button.change_colour(MOUSE_POS)
                button.update(win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BTN.check_for_input(MOUSE_POS):
                        return "play"
                    if OPTION_BTN.check_for_input(MOUSE_POS):
                        return "option"
                    if QUIT_BTN.check_for_input(MOUSE_POS):
                        return "quit"

            pygame.display.update()
            
    def play(self):
        pass
    
    
    def option(self):
        pass
