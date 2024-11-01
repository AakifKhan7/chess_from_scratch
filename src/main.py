import pygame
import sys
from game import Game
from square import Square
from const import *
from move import Move
import time

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
    
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_hover(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # check valid piece(color)?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool= True)

                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                                    
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    try:
                        game.set_hover(motion_row, motion_col)
                    except IndexError:
                        continue
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        
                        move = Move(initial, final)
                        
                        
                        # valid move?
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            
                            board.set_true_en_passant(dragger.piece)
                            
                            #sounds
                            game.play_sound(captured)
                            
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                            
                        if board.in_check(dragger.piece, move):
                            game.play_sound(check=True)
                            game.show_check(piece.color, screen)
                            
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing in theme
                    if event.key == pygame.K_t:
                        game.change_theme()
                        
                    if event.key == pygame.K_r:
                        game.reset()
                        
                        game = self.game
                        screen = self.screen
                        board = self.game.board
                        dragger = self.game.dragger
                
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            
            pygame.display.update()
    
main = Main()
main.mainloop()