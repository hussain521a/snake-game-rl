import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('arial', 30)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

#Colors
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 1000

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        #init starting game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1
        #Check if input is recieved
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        #Move based on action
        self._move(action)
        self.snake.insert(0, self.head)
        
        #Check if action ended game
        reward = 0
        game_over = False
        #End if collision or game continues too long
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        #Either place new food or move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop() #removes last part of snake as movement occurs
        
        #Update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        #Return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        #Using pt to represent self.head 
        if pt is None:
            pt = self.head
        #Hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        #Hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        #Snake
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))            
        #Food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        #Score display
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    #Action will update the head
    def _move(self, action): 
        #Action will be [0,0,0] <- [straight, turn right, turn left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)
        if np.array_equal(action, [1,0,0]):#straight
            new_direction = clock_wise[index]#No direction change
        elif np.array_equal(action, [0,1,0]):#Right turn
            next_index = (index +1) % 4#Increment/Loop index around to 0
            new_direction = clock_wise[next_index]#Next direction in clockwise list
        else:
            np.array_equal(action, [0,0,1])#Left turn
            next_index = (index -1) % 4#Decrement/Loop index around to 3
            new_direction = clock_wise[next_index]#Previous direction in clockwise list
        
        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            
#Old game loop
# if __name__ == '__main__':
#     game = SnakeGameAI()
    
#     # game loop
#     while True:
#         game_over, score = game.play_step()
        
#         if game_over == True:
#             break
        
#     print('Final Score', score)
        
        
#     pygame.quit()