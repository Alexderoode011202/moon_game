from typing import Optional, List, Dict, Tuple, Set
import re
from random import shuffle
from pygame import Rect, Surface
import pygame

class Player:
    def __init__(self, name: str = "player 1", card_positions: List[Tuple[int, int]] = [(1/4, 4/5), (1/2, 4/5), (3/4, 4/5)]) -> None:
        self.name           :  str                      = name
        self.card_positions :  List[Tuple[int, int]]    = card_positions
        self.hand           : List["Card"]              = []
        self.rects          : List[Rect]                = []
        self.points = 0
        return None 

    def take_card(self, card: "Card") -> None:
        self.hand.append(card)
        card.update_position(position=self.card_positions[len(self.hand)-1])

    def give_points(self, points: int) -> None:
        self.points += points

    def get_card_graphics(self) -> List[Tuple[Surface, Rect]]:
        card_data: List[Tuple[Surface, Rect]] = []
        # -------------------------------------------- 
        for idx, position in enumerate(self.card_positions):
            card_surf : Surface = self.hand[idx].surf
            card_rect : Rect    = self.hand[idx].surf.get_rect(center=position)
            card_data.append((card_surf, card_rect))
        # -------------------------------------------- 
        return card_data
    
    def __repr__(self) -> str:
        return f"player: {self.name}"

class Tile:
    def __init__(self, tile_id: int, connections: List[int], position: Tuple[int,int], img_path: str) -> None:
        self.id             : int               = tile_id
        self.connections    : List[Tile]        = connections
        self.position       : Tuple[int, int]   = position
        self.surf           : Surface           = pygame.image.load(img_path)
        self.rect           : Rect              = self.surf.get_rect(center=self.position)
        self.taken: Optional[Player] = None
        self.hosting: Optional["Card"] = None
        return None
    
    def add_connection(self, neighbor: "Tile") -> None:
        self.connections.append(neighbor)

    def assign_card(self, card: "Card", player: "Player") -> None:
        self.hosting = card
        card.update_position(self.position)
        self.taken = player
        return None

    def get_side(self) -> Optional[Player]:
        return self.taken
    
    def get_card(self) -> Optional["Card"]:
        return self.hosting
    
    def update_position(self, new_position) -> None:
        self.position = new_position
        self.rect = self.surf.get_rect(center=self.position)
        return None

class Card:
    
    def __init__(self, moon_cycle: str, moon_id: int, position: Tuple[int, int] = None, img_path: str = "") -> None:
        self.moon_cycle : str               = moon_cycle
        self.moon_id    : int               = moon_id
        # -------------------------------------------- 
        self.posession: Optional[Player] = None
        self.position: Optional[Tuple[int, int]] = None
        # --------------------------------------------
        self.position   : Tuple[int, int]   = position
        self.surf       : Surface           = pygame.image.load(img_path)
        self.rect       : Optional[Rect]    = None    
        
        return None
    
    def __str__(self) -> str:
        return f"{self.moon_cycle} card"
    
    def update_position(self, position) -> None:
        self.position = position
        self.rect = self.surf.get_rect(center = self.position)

class Deck:
    paths: List[str] = [
        "media/main_game/moon_types/1_4_left_moon.png",
        "media/main_game/moon_types/half_left_moon.png",
        "media/main_game/moon_types/3_4_left_moon.png",
        "media/main_game/moon_types/full_moon.png",
        "media/main_game/moon_types/3_4_right_moon.png",                            # in total 8 unique cards
        "media/main_game/moon_types/half_right_moon.png",
        "media/main_game/moon_types/1_4_left_moon.png",
        "media/main_game/moon_types/empty_moon.png"
    ]
    
    def __init__(self, n_duplicates: int = 2):
        # Deck Creation
        # -----------------------------------
        self.n_duplicates = n_duplicates
        self.deck: List[Card] = []

        for _ in range(0, n_duplicates+1):
            for idx, path in enumerate(self.paths):

                name: str = re.sub("[0-9]_[0-9]", "quarter", path)
                name: str = re.sub("_", " ", name)
                name = name[:-4]

                self.deck.append(Card(moon_cycle=name, moon_id=idx, img_path=path))
        # ///////////////////////////////////
        shuffle(self.deck)
        return None

    def give_card(self) -> Card:
        return self.deck.pop()
    
    
    

class Board:
    def __init__(self, tiles: List[Tile]) -> None:
        # dict construction
        # -----------------------------------
        self.tile_dict: Dict[List, Tile] = {}
        self.tile_list: List[Tile] = tiles.copy()
        for tile in tiles:
            neighbors = []
            for neighbor_id in tile.connections:
                 neighbors.append(tiles[neighbor_id])
            self.tile_dict[tile] = neighbors
        # ///////////////////////////////////
        return None
    
    def update_board(self):
        pass

    def get_connections(self):
        connections: List[Set[Tile, Tile]] = []
        for start in self.tile_dict:
            for end in self.tile_dict[start]:
                if {start, end} in connections:
                    continue
                else:
                    connections.append([start.position, end.position])
        return connections
    
    def calculate_points(self, tile: Tile) -> int:
        """Still needs to get worked out"""
        return 1
    

class GameState:
    
    def __init__(self, players: List[Player], tiles: List[Tile], WIDTH: int, HEIGHT: int, n_duplicates: int = 2):
        # instantiate all components
        # -----------------------------------
        self.players    : List[Player]  = players
        self.deck       : Deck          = Deck(n_duplicates=n_duplicates)  # create deck
        self.status: str = "starting"
        self.selected_card: Optional[Card] = None
        self.selected_tile: Optional[Tile] = None
        # ///////////////////////////////////

        # save display info
        # -----------------------------------
        self.HEIGHT : int = HEIGHT
        self.WIDTH  : int = WIDTH
        # ///////////////////////////////////
        
        # hand out cards
        # -----------------------------------
        for player in self.players:
            for _ in range(3):
                player.take_card(self.deck.give_card())
        # ///////////////////////////////////

        # create board
        # -----------------------------------
        self.board : Board = Board(tiles=tiles)
        # ///////////////////////////////////

        # let player 1 start
        # -----------------------------------
        self.leader : Player    = self.players[0]
        self.status : str       = f"{self.leader.name} - move"
        # ///////////////////////////////////

        return None
    
    def update_tile_selection(self, tile: Tile) -> None:
        self.selected_tile = tile
        return None

    def update_card_selection(self, card: Card) -> None:
        self.selected_card = card
        return None

    def game_over(self) -> bool:
        for tile in self.board.tile_list:
            if tile.get_side():     # check whether a tile has a card on it
                continue            # if yes, keep looking
            else:
                return False        # if no, there appearantly still is space
        return True                 # if all tiles got cards, we end the game

    def process_move(self) -> None:
        # put card on tile
        # -----------------------------------
        self.selected_tile.assign_card(self.selected_card)
        # ///////////////////////////////////

        # update board
        # -----------------------------------
        #self.board.update()
        # ///////////////////////////////////

        # calculate earned points & assign them to player
        # -----------------------------------
        points = self.board.calculate_points(self.selected_tile)
        self.leader.give_points(points)
        # ///////////////////////////////////

        # let opponent lead & clear card and tile
        self.leader = self.players[1 - self.players.index(self.leader)]
        self.selected_card = None
        self.selected_tile = None
        # ///////////////////////////////////
        return None
    
    def is_ready_for_move(self) -> bool:
        return self.selected_card and self.selected_tile
    
    def carry_out_move(self) -> None:
        # remove the selected card from player's hand and provide new card
        # -----------------------------------
        self.leader.hand.remove(self.selected_card)
        self.leader.take_card(self.deck.give_card())
        # ///////////////////////////////////

        # put selected card on tile and update tile's status
        # -----------------------------------
        self.selected_tile.assign_card(card=self.selected_card, player=self.leader)
        
        # ///////////////////////////////////

        # make new player the leader
        # -----------------------------------
        self.leader = self.players[1-self.players.index(self.leader)]   # this alternates the two
        self.selected_card = None
        self.selected_tile = None
        # ///////////////////////////////////

        return None

    def provide_to_blit(self):

        # get the connections
        # -----------------------------------
        connections: List[Set[Tuple[int, int], Tuple[int, int]]] = self.board.get_connections()
        
        # ///////////////////////////////////
        
        # then get the tiles
        # -----------------------------------
        tiles: List[Tuple[Surface, Rect]] = []
        for tile in self.board.tile_list:
            tiles.append((tile.surf, tile.rect))
        # ///////////////////////////////////
        
        # then get the cards on the tiles
        # -----------------------------------
        cards_on_board: List[Tuple[Surface, Rect]] = []
        for tile in self.board.tile_list:
            if tile.get_card():
                cards_on_board.append((tile.get_card().surf, tile.rect))
        # ///////////////////////////////////

        # get the cards from the leading player
        # -----------------------------------
        player_cards = self.leader.get_card_graphics()
        # ///////////////////////////////////
        
        surf_and_rect: List[Tuple[Surface, Rect]] = tiles
        surf_and_rect.extend(cards_on_board)
        surf_and_rect.extend(player_cards)

        return [connections, surf_and_rect]

        
        


