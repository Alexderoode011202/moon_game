import pyautogui
import pygame
from pygame import Rect, Surface
from pygame.time import Clock
from sys import path
from os.path import abspath
from os import getcwd
from typing import Tuple, List
from classes import *

print('MAIN GAME STARTED')

""" 
USE xhost + TO DEAL WITH ISSUES REGARDING pyautogui
"""

def cursor_on_rect(cursor_pos: Tuple[int, int], rect: Rect) -> bool:
    """function that checks whether cursor is on the area of a certain rectangle"""    
    return (rect.left < cursor_pos[0] < rect.right) and (rect.height < cursor_pos[1] < rect.bottom)

def main_game(verbose: bool = False):
    pygame.init()

    # graphical preparations
    # -----------------------------------
    WIDTH   : int = pyautogui.size()[0] * 0.8
    HEIGHT  : int = pyautogui.size()[1] * 0.8


    background      : Surface   = pygame.image.load("media/main_game/background.jpg")
    background      : Surface   = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect : Rect      = background.get_rect(center=(WIDTH *0.5, HEIGHT*0.5))

    title_font = pygame.font.Font("media/fonts/Untlang-1G1rB.ttf", 70)

    moon_size: int = int(WIDTH*0.029296875)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    # ///////////////////////////////////

    # logical preparations
    # -----------------------------------
    players: List[Player] = [Player(name="Player 1", card_positions=[(1/4*WIDTH, 4/5*HEIGHT), (1/2*WIDTH, 4/5*HEIGHT), (3/4*WIDTH, 4/5*HEIGHT)]), 
                             Player(name="Player 2", card_positions=[(1/4*WIDTH, 4/5*HEIGHT), (1/2*WIDTH, 4/5*HEIGHT), (3/4*WIDTH, 4/5*HEIGHT)])]
    tiles = [Tile(0, connections=[1], position=(WIDTH*3/8, HEIGHT*1/2), img_path="media/main_game/tile.png"),
             Tile(1, connections=[0], position=(WIDTH*5/8, HEIGHT*1/2), img_path="media/main_game/tile.png")]
    gamestate = GameState(players=players, tiles=tiles, WIDTH=WIDTH, HEIGHT=HEIGHT)
    

    # ///////////////////////////////////

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # basic info
        # -----------------------------------
        cursor_pos  : Tuple[int, int]   = pygame.mouse.get_pos()
        click       : bool              = pygame.mouse.get_pressed()[0]
        # ///////////////////////////////////

        print
        
        # check whether game should end
        # -----------------------------------
        #if gamestate.game_over():
        #    running = False
        # ///////////////////////////////////

        # check whether move can be processed
        # -----------------------------------
        if gamestate.is_ready_for_move():
            gamestate.carry_out_move()
        # ///////////////////////////////////
        
        # check whether card needs to be assigned
        # -----------------------------------
        elif not gamestate.selected_card:
            for card in gamestate.leader.hand:
                if cursor_on_rect(cursor_pos=cursor_pos, rect=card.rect) and click:
                    gamestate.selected_card = card
                    break
            if verbose:
                print(f"selected card: {gamestate.selected_card}")
        # ///////////////////////////////////

            """Following 2 parts have to be turned into a function!"""
        # check whether tile needs to be assigned
        # -----------------------------------
        elif not gamestate.selected_tile:
            for tile in gamestate.board.tile_list:
                if tile.get_card():    # we only want tiles that don't have cards on them
                    continue
                if cursor_on_rect(cursor_pos=cursor_pos, rect=tile.rect) and click:
                    gamestate.selected_tile=tile
                    break
            if verbose:
                print(f"selected card: {gamestate.selected_card}")
        # ///////////////////////////////////

        # updating screen
        # -----------------------------------
        stuff_to_blit = gamestate.provide_to_blit()

        screen.fill("black")
        screen.blit(background, background_rect)

        pygame.draw.rect(screen, (21, 44, 68), Rect(0, 2/3*HEIGHT, WIDTH, HEIGHT))

        for connection in stuff_to_blit[0]:
            pygame.draw.line(screen, (255,255,255), connection[0], connection[1])

        for surf, rect in stuff_to_blit[1]:
            screen.blit(surf, rect)

        if gamestate.leader == players[0]:
            leader_text: Surface = title_font.render(f"leading player: {gamestate.leader.name}", True, (0,255,0))
        else:
            leader_text: Surface = title_font.render(f"leading player: {gamestate.leader.name}", True, (255,0,0))
        
        leader_text_rect: Rect = leader_text.get_rect(center=(WIDTH*0.5, HEIGHT*1/4))

        screen.blit(leader_text, leader_text_rect)
        pygame.display.flip()
        # ///////////////////////////////////

        clock.tick(60)

    pygame.quit()
    return None

if __name__ == "__main__":
    main_game(verbose=True)