import pygame
import solver
import csv
import os
import random


class Square:
    # an individual sudoku square
    def __init__(self, value, row, col, board_size):
        self.value = value
        self.value_color = (0, 0, 0)
        self.row = row
        self.col = col
        self.board_size = board_size
        self.selected = False
        self.immutable = False
        if value != 0:
            self.immutable = True
        self.square_size = self.board_size / 9
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size

    # displays assigned value
    def drawText(self, display):
        # display value
        font = pygame.font.SysFont('Verdana', 35)
        if self.immutable:
            font = pygame.font.SysFont('Verdana', 35, True, True)
        if self.value != 0:
            text = font.render(str(self.value), 1, self.value_color)
            display.blit(text, (self.x + (self.square_size / 2 - text.get_width() / 2),
                                self.y + (self.square_size / 2 - text.get_height() / 2)))
    
    # highlights selected square
    def drawBorder(self, display):
        square_size = self.board_size / 9
        x = self.row * square_size
        y = self.col * square_size
        border_color = (0, 0, 255)
        
        if self.selected:
            pygame.draw.rect(display, border_color, (x, y, square_size, square_size), 3)

    # draws both text and border
    def draw(self, display):
        self.drawBorder(display)
        self.drawText(display)

    def setSelected(self, value):
        self.selected = value
    
    def setValue(self, value):
        self.value = value
        self.value_color = (0, 0, 0)
    

class GameBoard:
    def __init__(self, board, board_width=600, board_height=700):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.board_width = board_width
        self.board_height = board_height
        self.selected = None
        self.squares = [[Square(self.board[r][c], r, c, self.board_width)
                        for c in range(self.cols)] for r in range(self.rows)]
        self.solution = solver.solve(board)

    def draw(self, display):
        square = self.board_width / 9

        # draw starting grid
        for line in range(0, 10):
            if line % 3 == 0:
                thickness = 5
            else:
                thickness = 1
            pygame.draw.line(display, (0, 0, 0), (0, line*square), (self.board_width, line*square), thickness)
            pygame.draw.line(display, (0, 0, 0), (line*square, 0), (line*square, self.board_width), thickness)

        # populate squares and show selected on display
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[r][c].draw(display)

    def selectSquare(self, row, col):
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[r][c].setSelected(False)
        
        self.squares[row][col].setSelected(True)
        self.selected = (row, col)

    def clicked(self, position):
        # convert mouse click position to square position
        # only captures mouse clicks in game board, not on bottom menu
        if position[0] < self.board_width and position[1] < self.board_width:
            square_size = self.board_width / 9
            x = position[0] // square_size
            y = position[1] // square_size
            return int(x), int(y)
        else:
            return None

    def setValue(self, value):
        r = self.selected[0]
        c = self.selected[1]
        if not self.squares[r][c].immutable:
            self.squares[r][c].setValue(value)
    
    def clear(self):
        temp = self.selected
        for r in range(self.rows):
            for c in range(self.cols):
                self.selected = (r, c)
                self.setValue(0)
        self.selected = temp
    
    def check(self):
        # checks user inputs if they are correct
        # changes text to red if incorrect
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.squares[r][c].immutable and self.squares[r][c].value != 0 and \
                        self.squares[r][c].value != self.solution[r][c]:
                    self.squares[r][c].value_color = (255, 0, 0)

    def fillSolution(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[r][c].setValue(self.solution[r][c])


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x          # top left corner
        self.y = y          # top left corner
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, display):
        black = (0, 0, 0)
        pygame.draw.rect(display, black, self.rect, 2)
        font = pygame.font.SysFont('Verdana', 20)
        text = font.render(self.text, 1, black)
        display.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def clicked(self, position):
        if (self.x < position[0] < (self.x + self.width)) and (self.y < position[1] < (self.y + self.height)):
            return True
        else:
            return False


def updateDisplay(display, buttons, game=None):
    display.fill((255, 255, 255))
    for button in buttons:
        button.draw(display)
    if game is not None:
        game.draw(display)


def main():
    # initialize the game and display
    pygame.init()
    display_width = 600
    display_height = 700
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Sudoku")

    def main_menu():
        # main menu items
        padding_width = display_width * .1
        padding_height = display_height * .1
        button_width = display_width - padding_width * 2
        button_height = (display_height - padding_height * 4) * .3
        easy_game_button = Button(padding_width, padding_height, button_width, button_height, "Easy")
        medium_game_button = Button(padding_width, easy_game_button.y + button_height + padding_height,
                                    button_width, button_height, "Medium")
        hard_game_button = Button(padding_width, medium_game_button.y + button_height + padding_height,
                                  button_width, button_height, "Hard")
        buttons = [easy_game_button, medium_game_button, hard_game_button]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.clicked(position):
                            if button == easy_game_button:
                                path = 'puzzles/easy/'
                            elif button == medium_game_button:
                                path = 'puzzles/medium/'
                            else:
                                path = 'puzzles/hard/'
                            random_puzzle = random.choice(os.listdir(path))
                            with open(path + random_puzzle, newline='') as f:
                                reader = csv.reader(f)
                                b = list(reader)
                            for r in range(len(b)):
                                for c in range(len(b[r])):
                                    b[r][c] = int(b[r][c])
                            return b

            updateDisplay(display, buttons)
            pygame.display.update()

    def play_game(b):
        # initialize game elements
        game = GameBoard(b)
        # padding width: 1% each, 5% total
        # buttons: back, clear, check, solve
        # back_button width: 10% (after padding)
        # clear, check, solve button width: 30% each (after padding)
        padding = display_width * .01
        y = display_width + padding
        back_button_width = (display_width - (padding * 5)) * .1
        button_width = (display_width - (padding * 5)) * .3
        button_height = display_height - (display_width + padding * 2)
        back_button = Button(padding, y,
                             back_button_width, button_height, '<<')
        clear_button = Button(back_button.width + padding * 2, y,
                              button_width, button_height, 'Clear all (Space)')
        check_button = Button(clear_button.x + button_width + padding, y,
                              button_width, button_height, 'Check (?)')
        solve_button = Button(check_button.x + button_width + padding, y,
                              button_width, button_height, 'Solve (Enter)')
        buttons = [back_button, clear_button, check_button, solve_button]

        # variables
        key_pressed = None
        run = True
        return_to_menu = False

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    clicked = game.clicked(position)
                    if clicked:
                        game.selectSquare(clicked[0], clicked[1])
                    else:
                        for button in buttons:
                            if button.clicked(position):
                                if button == back_button:
                                    return_to_menu = True
                                    run = False
                                elif button == clear_button:
                                    game.clear()
                                elif button == check_button:
                                    game.check()
                                else:
                                    game.fillSolution()
                    key_pressed = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        key_pressed = 1
                    elif event.key == pygame.K_2:
                        key_pressed = 2
                    elif event.key == pygame.K_3:
                        key_pressed = 3
                    elif event.key == pygame.K_4:
                        key_pressed = 4
                    elif event.key == pygame.K_5:
                        key_pressed = 5
                    elif event.key == pygame.K_6:
                        key_pressed = 6
                    elif event.key == pygame.K_7:
                        key_pressed = 7
                    elif event.key == pygame.K_8:
                        key_pressed = 8
                    elif event.key == pygame.K_9:
                        key_pressed = 9
                    elif event.key == pygame.K_BACKSPACE:
                        key_pressed = 0
                    elif (event.mod & pygame.KMOD_SHIFT) and event.key == pygame.K_SLASH:
                        game.check()
                        key_pressed = None
                    elif event.key == pygame.K_RETURN:
                        game.fillSolution()
                        key_pressed = None
                    elif event.key == pygame.K_SPACE:
                        game.clear()
                        key_pressed = None

            if game.selected and key_pressed is not None:
                game.setValue(key_pressed)

            updateDisplay(display, buttons, game)
            pygame.display.update()
        return return_to_menu

    board = main_menu()
    while True:
        if play_game(board):    # return to main menu if true
            board = main_menu()
        else:
            break


if __name__ == '__main__':
    main()
