import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from move import Move
from piece import King

class Game:
    
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
    
    #Show methods 
    
    def show_bg(self, surface):
        
        theme = self.config.theme
        
        for row in range(ROW):
            for col in range(COLS):
                
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                    
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)
                
                # row coordinate
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    
                    lbl = self.config.font.render(str(ROW - row), 1, color)
                    lbl_position = (5, 5 + row * SQSIZE)
                    
                    surface.blit(lbl, lbl_position)
                    
                # col coordinate
                if row == 7:
                    color = theme.bg.dark if  (row + col) % 2 == 0 else theme.bg.light
                    
                    lbl = self.config.font.render(str(Square.get_alphacol(col)), 1, color)
                    lbl_position = (col * SQSIZE + SQSIZE - 15, HEIGHT - 24)
                    
                    surface.blit(lbl, lbl_position)
                
                
    def show_pieces(self, surface):
        for row in range(ROW):
            for col in range(COLS):
                # piece?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
                        
    def show_moves(self, surface):
        theme = self.config.theme
        
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            for move in piece.moves:
                color = theme.moves.light if(move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)
                
    # show last move
    def show_last_move(self, surface):
        theme = self.config.theme
        
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                
                color = theme.trace.light if(pos.row + pos.col) % 2 == 0 else theme.trace.dark
                
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)
                
    def show_check(self, color,  surface):
        for row in range(ROW):
            for col in range(COLS):
                # king?
                if self.board.squares[row][col].has_team_piece(color):
                    p = self.board.squares[row][col].piece
                    if isinstance(p, King):
                        color = '#8B0000'

                        rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                        pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
                
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
                
            pygame.draw.rect(surface, color, rect, width=4)
                
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        
    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]
        
    def change_theme(self):
        self.config.change_theme()
        
    def play_sound(self, capture = False, check = False):
        if capture:
            self.config.capture_sound.play()
        elif check:
            self.config.check_sound.play()
        else:
            self.config.move_sound.play()
            
    def reset(self):
        self.__init__()