import sys
import pygame

from pygame.locals import (
    RLEACCEL,
    MOUSEBUTTONDOWN,
    QUIT,
)

pygame.init()

# Game Window
screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption("Tic-Tac-Toe")
pygame.display.set_icon(pygame.image.load("Assets/icon.png"))

# Load Assets
board = pygame.image.load("Assets/board.png").convert()
cross = pygame.image.load("Assets/cross.png").convert()
nought = pygame.image.load("Assets/nought.png").convert()
square = pygame.image.load("Assets/square.png").convert()
font = pygame.font.Font("Assets/font.ttf", 65)

# Constants
GRID_POSITIONS = [(19, 19), (109, 19), (199, 19), (19, 109), (109, 109), (199, 109), (19, 199), (109, 199), (199, 199)]

# Classes
class Cross(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Cross, self).__init__()
        self.image = cross # Cross Image
        self.image.set_colorkey((255, 255, 255), RLEACCEL) # Transparency
        self.rect = self.image.get_rect(topleft = position)

class Nought(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Nought, self).__init__()
        self.image = nought # Nought Image
        self.image.set_colorkey((255, 255, 255), RLEACCEL) # Transparency
        self.rect = self.image.get_rect(topleft = position)

class Square(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Square, self).__init__()
        self.image = square # Square Image
        self.image.set_colorkey((255, 255, 255), RLEACCEL) # Transparency
        self.rect = self.image.get_rect(topleft = position)

grid = pygame.sprite.Group() # Grid Squares Group

for i in range(9):
    grid.add(Square(GRID_POSITIONS[i]))

# Functions
def get_winner(game):

    if game[0] == game[1] == game[2] != "": # Horizontal (Top)
        pygame.draw.line(screen, (0, 205, 205), (19, 61), (281, 61), 5)
        return game[1]

    elif game[3] == game[4] == game[5] != "": # Horizontal (Middle)
        pygame.draw.line(screen, (0, 205, 205), (19, 151), (281, 151), 5)
        return game[4]

    elif game[6] == game[7] == game[8] != "": # Horizontal (Bottom)
        pygame.draw.line(screen, (0, 205, 205), (19, 241), (281, 241), 5)
        return game[7]

    elif game[0] == game[3] == game[6] != "": # Vertical (Left)
        pygame.draw.line(screen, (0, 205, 205), (61, 19), (61, 281), 5)
        return game[3]

    elif game[1] == game[4] == game[7] != "": # Vertical (Middle)
        pygame.draw.line(screen, (0, 205, 205), (151, 19), (151, 281), 5)
        return game[4]

    elif game[2] == game[5] == game[8] != "": # Vertical (Right)
        pygame.draw.line(screen, (0, 205, 205), (241, 19), (241, 281), 5)
        return game[5]

    elif game[0] == game[4] == game[8] != "": # Diagonal (Left-Right)
        pygame.draw.line(screen, (0, 205, 205), (19, 19), (281, 281), 5)
        return game[4]

    elif game[2] == game[4] == game[6] != "": # Diagonal (Right-Left)
        pygame.draw.line(screen, (0, 205, 205), (281, 19), (19, 281), 5)
        return game[4]

    elif "" not in game: # Draw
        return "Nobody"

    else:
        return False

def game_ended(winner):
    text = font.render(f"{winner} Wins!", True, (255, 255, 255)) # Render Text
    rect = text.get_rect(center = (150, 150))
    screen.blit(text, rect)

    pygame.display.update()

    pygame.time.delay(250)
    
    pygame.event.clear() # Clear Queued Events

    idle = True
    while idle:
        for event in pygame.event.get():

            if event.type == QUIT:
                idle = False
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:   
                idle = False

def main():
    turn = "X"
    game_board = ["", "", "", "", "", "", "", "", ""]

    crosses = pygame.sprite.Group() # Crosses Sprite Group
    noughts = pygame.sprite.Group() # Noughts Sprite Group

    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:    
                for i, grid_square in enumerate(grid):
                    if grid_square.rect.collidepoint(pygame.mouse.get_pos()):

                        if game_board[i] == "":
                            if turn == "X":
                                game_board[i] = "X"
                                crosses.add(Cross(grid_square.rect.topleft))
                                turn = "O"
                                        
                            elif turn == "O":
                                game_board[i] = "O"
                                noughts.add(Nought(grid_square.rect.topleft))
                                turn = "X"

        # Draw Sprites
        screen.blit(board, (0, 0))
        
        for cross in crosses:
            screen.blit(cross.image, cross.rect)

        for nought in noughts:
            screen.blit(nought.image, nought.rect)

        # Update Display
        pygame.display.update()

        # Finish Game
        winner = get_winner(game_board)

        if winner:
            running = False

        # Maintain 30 FPS
        clock.tick(30)

    game_ended(winner)
    main()

if __name__ == "__main__":
    main()