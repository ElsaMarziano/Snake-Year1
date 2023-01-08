from typing import Optional
from game_display import GameDisplay
import math
from board import  Board
from snake import Snake
from game_utils import get_random_apple_data
from wall import Wall
from game_utils import get_random_wall_data
from constants import COLORS, MOVES
from helper import check_direction
from helper import make_something_move
from helper import check_location




class SnakeGame:
    #TODO Code review!!!!!!! + add comments
    #TODO upload score when apple eaten
    #TODO dont commit suicide
    #TODO We're not using self.__key_clicked, check if it's needed to pass tests
    #TODO Default to all parameters
    #TODO Update round, stop when round is at the maximum
    #TODO check what is needed to be in the first round



    def __init__(self, args) -> None:
        WIDTH_SNAKE = args.width // 2
        HEIGHT_SNAKE = args.height // 2
        self.__key_clicked = None
        self.score = 0
        self.__debug = args.debug
        self.__snake = Snake([(WIDTH_SNAKE,HEIGHT_SNAKE - 2),(WIDTH_SNAKE,HEIGHT_SNAKE - 1), (WIDTH_SNAKE,HEIGHT_SNAKE)], args.debug)
        self.__board = Board(self.__snake.get_location(),args.width, args.height, args.apples, args.walls)
        self.__round = args.rounds
        self.__is_over = False
        self.__round_current = 0


    def read_key(self, key_clicked: Optional[str])-> None:
        self.__key_clicked = key_clicked


    def update_objects(self, move)-> None:
        """ This function updates every object on the board at each turn """
        # Moves snake and check if he's dead
        if self.__is_over and self.__round_current != 0 : return
        if not self.__debug:
            snake_head_after_move = make_something_move(self.__snake.get_head(), MOVES[move]) # Get head after move
        # Check if snake is still inside the board
        # ? @amitai Why do we need this?
            need_to_grow = 0
            if check_location(self.__board.height, self.__board.width, snake_head_after_move): 
                need_to_grow = self.__board.board[snake_head_after_move[1]][snake_head_after_move[0]] == "A" # Check if head is on apple

            snake_status:  dict = self.__snake.move_snake(move) #move first before tell him to grow if needed
        # Update snake location on board, check if snake is dead
            if self.__board.place_snake([snake_status["old_loc"]], snake_status["new_loc"]) == "DEAD" or snake_status["is_dead"]:
                self.__is_over = True
        # Check if snake needs to grow and updates score
            if not self.__is_over and need_to_grow:
                self.__snake.growing()
                self.__board.apples_on_board -= 1
                self.add_score()
        # Add aples, move walls and stuff
        if self.__round_current <= 1:
            wall_to_place = self.__board.place_walls()
        else:
            self.__board.move_walls_in_board()  # advance wall
            wall_to_place = self.__board.place_walls()



        if self.__board.snake_hits_wall(self.__snake) and not self.__is_over:
            self.__is_over = True
            

        if self.__round % 2 == 0:
            self.__board.add_wall(Wall())
        if wall_to_place != 0:
            for wall in range(wall_to_place):
                self.__board.add_wall(Wall())
        self.__board.place_walls()
        self.__board.add_apple(get_random_apple_data())
        
        
    def add_score(self):
        self.score += int(math.sqrt(self.__snake.get_size()))


    


    def draw_board(self, gd: GameDisplay) -> None:
        for height, _ in enumerate(self.__board.board):
            for width, _ in enumerate(self.__board.board[0]):
                color = self.__board.board[height][width]
                if color != "_":
                    gd.draw_cell(width, height, COLORS[color])

    def end_round(self) -> None:
        self.__round_current += 1
        if self.__round <= -1:
            self.__round -= 1
            return
        if self.__round == 0:
            self.__is_over = True
        else:
            self.__round -= 1


    def is_over(self) -> bool:
        return self.__is_over
