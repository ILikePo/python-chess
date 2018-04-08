#!/usr/bin/python3

def select_piece(color):

    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    clicked_sprites = [
        s for s in sprites if s.rect.collidepoint(pos)]

    #only highlight if its the player's color
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color :
        # clicked_sprites[0].highlight(screen)
        #print(clicked_sprites[0])
        clicked_sprites[0].highlight()
        return clicked_sprites[0]

def select_square():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return (y,x)


if __name__ == "__main__":
    import pygame

    # from assets import **

    pygame.init()

    screen = pygame.display.set_mode((800, 60 * 8))
    pygame.display.set_caption('Boss Ass Chess Game')

    from modules.board import *
    from modules.computer import *

    # load background image
    bg = pygame.image.load("assets/chessboard.png").convert()
    # blit like puts the image on there

    # board matrix
    board = Board()

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(piece for row in board.array for piece in row if piece)

    screen.blit(bg, (0, 0))
    all_sprites_list.draw(screen)
    # all_sprites_list = pygame.sprite.LayeredDirty(
    #     piece for row in b.array for piece in row if piece)
    sprites = [piece for row in board.array for piece in row if piece]
    clock = pygame.time.Clock()



    gameover = False
    player = 1 # 'CMP' otherwise

    selected = False #indicates whether a piece is selected yet
    trans_table = dict()

    while not gameover:

        # Human player's turn
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True

                elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                    piece = select_piece("w")
                    print(piece)
                    # a white piece was selected
                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        selected = True

                elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                    square = select_square()
                    if square in player_moves:
                        board.move_piece(piece,square[0],square[1])
                        # see if move puts you in check
                        attacked = move_gen(board,"b",True)
                        if (board.white_king.y,board.white_king.x) not in attacked:
                            #MOVE NOT IN CHECK WE GOOD
                            selected = False
                            player = "AI"
                        else: #THIS MOVE IS IN CHECK
                            pass
                            #TODO: revert the move
                            #TODO: print a message

                    elif (piece.y,piece.x)==square: #CANCEL MOVE
                        #TODO:  unhighlight the square
                        selected = False

                    else: #INVALID MOVE
                        pass
                        #TODO: print a message

        """"
        #AI's turn
        else:
            value, move = minimax(board,5,float("-inf"),float("inf"), True, trans_table)
            if value == float("-inf"):
                #AI IS IN CHECKMATE
                gameover = True
        """

            # elif event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     # get a list of all sprites that are under the mouse cursor
            #     clicked_sprites = [
            #         s for s in sprites if s.rect.collidepoint(pos)]
            #     if len(clicked_sprites) == 1:
            #         # clicked_sprites[0].highlight(screen)
            #         clicked_sprites[0].unhighlight()
            #         # clicked_sprites[0].unhighlight()
            #         # elif:
            #         #     crashed = True
            #         #     print('SOMETHING DEADASS BROKE')

        #print(event)

        #screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)
