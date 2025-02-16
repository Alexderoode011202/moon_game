import pyautogui
import pygame
from pygame import Rect, Surface
from pygame.time import Clock
from typing import Tuple
from main_game import main_game

def cursor_on_surface(rect: Rect, mouse_pos: Tuple[int, int]) -> bool:
    "checks whether the mouse is on a particular rectangle's surface"
    if rect.left < mouse_pos[0] < rect.right and rect.top < mouse_pos[1] < rect.bottom:
        return True
    return False

# 1. get dimensions of screen
# -----------------------------------
# subprocess.run(["xhost", "+"])
WIDTH   : int = pyautogui.size()[0] * 0.8
HEIGHT  : int = pyautogui.size()[1] * 0.8
# ///////////////////////////////////


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = Clock()

# font
# -----------------------------------
title_font = pygame.font.Font("media/fonts/Untlang-1G1rB.ttf", 70)
# ///////////////////////////////////

# images 
# -----------------------------------
background      : Surface   = pygame.image.load("media/start/background/background.jpg")
background      : Surface   = pygame.transform.scale_by(background, HEIGHT/background.get_size()[1])
background_rect : Rect      = background.get_rect(center=(WIDTH *0.5, HEIGHT*0.5))

title       : Surface = title_font.render("Rise of the Moon", True, (255,255,255))
title_rect  : Surface = title.get_rect(center=(WIDTH*0.5, HEIGHT*1/6))

sp_text         : Surface   = title_font.render("single-player", True, (255,255,255), (255,0,0))
sp_text_rect    : Rect      = sp_text.get_rect(center=(WIDTH*1/5, HEIGHT*2/3))

mp_text         : Surface   = title_font.render("multi-player", True, (255,255,255), (0,255,0))
mp_text_rect    : Rect      = sp_text.get_rect(center=(WIDTH*4/5, HEIGHT*2/3))
# ///////////////////////////////////

running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0] and cursor_on_surface(rect=sp_text_rect, mouse_pos=pygame.mouse.get_pos()):
        print("SINGLE PLAYER")

    if pygame.mouse.get_pressed()[0] and cursor_on_surface(rect=mp_text_rect, mouse_pos=pygame.mouse.get_pos()):
        print("MULTI PLAYER")
        #subprocess.run(["python", "main_game.py"])
        main_game()
        running = False

            
    # updating screen
    # -----------------------------------
    screen.fill("black")
    screen.blit(background, background_rect)
    screen.blit(title, title_rect)
    screen.blit(sp_text, sp_text_rect)
    screen.blit(mp_text, mp_text_rect)

    pygame.display.flip()
    # ///////////////////////////////////

    clock.tick(60)

pygame.quit()