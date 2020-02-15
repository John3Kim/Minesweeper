import random
import sys
from typing import List

'''
Minesweeper
@author: John3Kim
@desc: This is a console-based version of the popular game
Minesweeper.
'''

class Minesweeper:

    def __init__(self):
        self.length = None
        self.width = None
        self.num_mines = None
        self.num_revealed = 0
        self.board = None
        self.mines_board = None

    def __init_board(self) -> List[List[int]]:
        '''
        Builds the board for Minesweeper. 
        '''
        game_board = [None for l in range(self.length)]

        for l in range(self.length):
            game_board[l] = ['#']*self.width

        return game_board
    
    def board_settings(self): 
    
        while True:
            try:
                length = int(input("Please set length of the board.  "))
                width = int(input("Please set width of the board. "))
                
                if length < 1 or width < 1: 
                    print("Please enter positive whole numbers!")
                
                break

            except: 
                print("Please input whole numbers!")
                continue
            
        self.length = length 
        self.width = width
        self.board = self.__init_board()

    
    def mines_settings(self,is_random:bool=False)-> None:
        
        size_board = self.length*self.width

        if is_random: 
            self.num_mines = random.randint(0,(self.length-1)*(self.width-1)) 
            self.mines_board = self.__randomize_mines(self.num_mines)
            return 
        
        while True: 
            
            num_mines_input = input("How many mines do you want? Choose between 1 and {highest}.  Quit with (Q/q).".format(highest = size_board)).upper()
            
            if num_mines_input == 'Q': 
                sys.exit()

            try:
                num_mines_input = int(num_mines_input)
            except: 
                print("Input whole numbers!")
                continue

            if 1 <= num_mines_input <= size_board: 
                break 
            else: 
                print("Not within bounds! Input again!")

        
        self.num_mines = num_mines_input
        self.mines_board = self.__randomize_mines(self.num_mines)

    def __randomize_mines(self,number_mines:int) -> List[List[int]]:
        '''
        Adds mines in the board. 
        '''

        #max_mines = random.randint(0,(self.length-1)*(self.width-1))
        max_mines = number_mines

        mines_board = [None for i in range(self.length)]

        for i in range(self.length):
            mines_board[i] = [0]*self.width

        while max_mines > 0:
            rndm_length = random.randint(0,self.length-1)
            rndm_width = random.randint(0,self.width-1)

            if mines_board[rndm_length][rndm_width] != "X":
                mines_board[rndm_length][rndm_width] = "X"
                max_mines -= 1

        # Add the numbers in the mine based on vicinity
        # Iterate through all the cells and add number indicating the number of
        # mines present in the vicinity
        
        for i in range(self.length):
            for j in range(self.width):
                if mines_board[i][j] == "X":

                    if (i < 0 or i > self.length-1) or(j < 0 or j > self.width-1):
                        continue
                    else:

                        for i_mines in range(i-1,i+2):

                            if i_mines > self.length-1 or i_mines < 0:
                                continue
                            
                            for j_mines in range(j-1,j+2):

                                if j_mines > self.width-1 or j_mines < 0:
                                    continue
                                
                                if mines_board[i_mines][j_mines] != "X":
                                    mines_board[i_mines][j_mines] += 1

        return mines_board
    
    def already_revealed(self, i:int, j:int) -> None: 
        '''
        Checks to see if a player has already revealed the tile
        '''
        return True if self.board[i][j] not in {'#','F'} else False

    def is_victory(self) -> bool: 
        num_hashes = self.length*self.width

        # Count the number of hashes removed 
        for i in range(self.length): 
            for j in range(self.width): 
                if self.board[i][j] not in {"#","F"}: 
                    num_hashes -= 1
                

        return True if (num_hashes == self.num_mines) else False

    def add_flag(self, i:int, j:int) -> None:
        '''
        Mark potential mines.
        '''
        if self.board[i][j] == "#":
            self.board[i][j] = "F"
        elif self.board[i][j] == "F":
            self.board[i][j] = "#"

    def is_mine(self, i:int, j:int) -> bool:
        '''
        Checks if a tile contains a mine.
        '''
        return True if self.mines_board[i][j] == "X" else False

    def reveal_tiles(self, i:int, j:int) -> None:
        ''' 
        Reveals board tiles.  
        '''
        number_set = {i for i in range(9)}
        
        self.board[i][j] = self.mines_board[i][j]

        # if we spot a zero, run the algorithm on the surrounding tiles
        # flood the entire board until we see bordered numbers 
        # Find all zeros from coordinate (i,j) until we see a number other than zero
        if self.board[i][j] == 0:
            
            for i_mines in range(i-1,i+2):

                if i_mines > self.length-1 or i_mines < 0:
                    continue
                                
                for j_mines in range(j-1,j+2):

                    if j_mines > self.width-1 or j_mines < 0:
                        continue
                    
                    if self.board[i_mines][j_mines] in number_set:
                        self.board[i][j] = self.mines_board[i][j]
                    else:
                        self.reveal_tiles(i_mines,j_mines)
       
    def input_out_of_bounds(self, i:int, j:int) -> bool:
        '''
        Check to see if the index i or j are out of bounds
        '''
        height_bound = i < 0 or i > self.length-1
        width_bound = i < 0 or i > self.width-1

        return True if height_bound or width_bound else False
    
    def show_board(self) -> None:
        print("   " + str([i for i in range(len(self.board[0]))]))

        for i,row in enumerate(self.board):
            print(str(i) + ": " + str(row))

    def show_mines(self) -> None:
        '''
        Prints the board that shows all the mines. 
        This is used only for debugging purposes 
        '''
        for row in self.mines_board:
            print(row)
        
        
if __name__ == "__main__":
    minesweeper = Minesweeper()

    minesweeper.board_settings()
    minesweeper.mines_settings()

    while True:

        minesweeper.show_board()

        if minesweeper.is_victory(): 
            print("Congrats! You've managed to clear the field!")
            break

        mode = input("Enter (F/f) for flag mode or enter (Q/q) to quit. Press Enter or input any other key to reveal tiles.   ").upper()

        if mode == 'Q': 
            print("Exiting game... Good bye!")
            sys.exit()
        elif mode == 'F':
            print("Flag mode")
        else: 
            print("Reveal tiles mode")
        
        try:
            height = int(input("Input height. "))
            width = int(input("Input width. "))
        except:
            print("Please input valid numbers...")
            continue

        if minesweeper.input_out_of_bounds(height,width):
            print("Numbers out of bounds.")
            continue

        if mode == 'F':
            minesweeper.add_flag(height,width)
            continue
        else:
            
            if minesweeper.already_revealed(height,width): 
                print("Already chose this plot.")
                continue

            minesweeper.reveal_tiles(height,width)

            if minesweeper.is_mine(height,width):
                minesweeper.show_board()
                print("Game over")
                break
        
        
    
    
    
