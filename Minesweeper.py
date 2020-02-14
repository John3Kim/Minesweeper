import random
import sys
from typing import List

'''
Minesweeper
@author: John3Kim
@desc: This is a console-based version of the popular game
Minesweeper.
'''

'''
TODO:
- Make a reveal function that shows whether there is a mine
  or not.  we also need to run a flood algorithm which would 
- Be flexible in terms of the number of mines used in Minesweeper
'''

class Minesweeper:

    def __init__(self, length:int, width:int):
        self.length = length
        self.width = width
        self.board = self.__init_board()
        self.mines = self.__randomize_mines()

    def __init__(self, length:int):
        self.length = length
        self.width = length
        self.board = self.__init_board()
        self.mines = self.__randomize_mines()

    def __init_board(self) -> List[List[int]]:
        arr = [None for i in range(self.length)]

        for i in range(self.length):
            arr[i] = ['#']*self.width

        return arr

    #TODO: Deal with the mines
    def __randomize_mines(self) -> List[List[int]]:
        #max_mines = random.randint(0,(self.length-1)*(self.width-1))
        max_mines = 10

        arr = [None for i in range(self.length)]

        for i in range(self.length):
            arr[i] = [0]*self.width

        while max_mines >= 0:
            rndm_length = random.randint(0,self.length-1)
            rndm_width = random.randint(0,self.width-1)

            if arr[rndm_length][rndm_width] != "X":
                arr[rndm_length][rndm_width] = "X"
                max_mines -= 1

        # Add the numbers in the mine based on vicinity
        # Iterate through all the cells and add number indicating the number of
        # mines present in the vicinity
        
        for i in range(self.length):
            for j in range(self.width):
                if arr[i][j] == "X":

                    if (i < 0 or i > self.length-1) or(j < 0 or j > self.width-1):
                        continue
                    else:
                        for i_mines in range(i-1,i+2):

                            if i_mines > self.length-1 or i_mines < 0:
                                continue
                            
                            for j_mines in range(j-1,j+2):

                                if j_mines > self.width-1 or j_mines < 0:
                                    continue
                                
                                if arr[i_mines][j_mines] != "X":
                                    arr[i_mines][j_mines] += 1

        return arr

    def add_flag(self, i:int, j:int) -> None:
        '''
        Mark potential mines.
        '''
        if self.board[i][j] == "#":
            self.board[i][j] = "F"
        elif self.board[i][j] == "F":
            self.board[i][j] = "#"

    def is_mine(self, i:int, j:int) -> bool:
        
        if self.mines[i][j] == "X":
            return True

        return False

    # TODO fix
    def reveal_tiles(self, i:int, j:int) -> None:
        # implement zero case
        self.board[i][j] = self.mines[i][j]

        if self.board[i][j] == 0:
            self.circular_check(i,j)
            # flood the entire board until we see bordered numbers 
            # Find all zeros from coordinate (i,j) until we see a number other than zero

    # TODO fix
    # we shall check the surroundings
    def circular_check(self,i:int,j:int) -> None: 
        low_bound_i = i - 1 
        upper_bound_i = i + 1
        low_bound_j = j - 1 
        upper_bound_j = j + 1

        while low_bound_i < upper_bound_i: 
            while low_bound_j < upper_bound_j: 

                if self.validate_inputs(low_bound_i,low_bound_j) or (low_bound_i,low_bound_j) == (i,j):
                    continue

                if self.mines[low_bound_i][low_bound_j] == 0:
                    self.board[low_bound_i][low_bound_j] = self.mines[low_bound_i][low_bound_j]

                low_bound_j += 1 
            
            low_bound_i += 1

        
    def validate_inputs(self, i:int, j:int) -> bool:
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

    def __show_mines(self) -> None:
        '''
        Prints the board that shows all the mines. 
        This is used only for debugging purposes 
        '''
        for row in self.mines:
            print(row)
        
        
if __name__ == "__main__":
    minesweeper = Minesweeper(10)
    
    while True:

        minesweeper.show_board()

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

        if minesweeper.validate_inputs(height,width):
            print("Numbers out of bounds.")
            continue

        if mode == 'F':
            minesweeper.add_flag(height,width)
            continue
        else:
            minesweeper.reveal_tiles(height,width)
            
            if minesweeper.is_mine(height,width):
                minesweeper.show_board()
                print("Game over")
                break
            
        
        
    
    
    
