import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
Learning_Rate = 0.001

class Agent:

    def __init__(self):
        self.num_games = 0
        self.epsilon = 0 #Randomness
        self.gamma = 0.9 #Discount Rate - value smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)#Automatically call popleft() on limit
        self.model = Linear_QNet(11, 256, 3) # 11 is state inputs, 256 is hidden layer, 3 is output moves
        self.trainer = QTrainer(self.model, Learning_Rate, self.gamma)

    def get_state(self, game):
        #Get information from game
        head = game.snake[0]

        #Point values
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        #Boolean values
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        #Updating state information
        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            #Current move direction booleans
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            #Relative food location, multiple can be true
            game.food.x < game.head.x,  #Food left
            game.food.x > game.head.x,  #Food right
            game.food.y < game.head.y,  #Food up
            game.food.y > game.head.y  #Food down
            ]

        return np.array(state, dtype=int) #Converts booleans to 0/1


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))#Pop left if MAX_MEMORY reached

    def train_long_memory(self):
        if len(self.memory) >  BATCH_SIZE:\
            #Return list of tuples
            sample = random.sample(self.memory, BATCH_SIZE)#List of multiple tuples
        else:
            sample = self.memory

        #Manually loop to train from sample data
        # for state, action, reward, next_state, done in sample:
        #     self.trainer.train_step(state, action, reward, next_state, done)

        #Python zip() to train from sample data
        states, actions, rewards, next_states, done = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #Tradeoff exploration (early) /  exploitation (after experience)
        self.epsilon = 80 - self.num_games #More games decreases epsilon
        final_move = [0,0,0]
        #Random move
        if random.randint(0, 200) < self.epsilon: #If epsilon is low, less random moves
            move_index = random.randint(0,2) # 0, 1, or 2
            final_move[move_index] = 1
        #Predicted move
        else:
            state0 = torch.tensor(state, dtype=torch.float32)#Create tensor to hold state data
            prediction = self.model(state0)#Use state data held in tensor to predict in model
            move_index = torch.argmax(prediction).item()#Get max value's index from tensor after prediction
            final_move[move_index] = 1
        
        return final_move
    

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        #Get old state
        old_state = agent.get_state(game)

        #Get new move
        new_move = agent.get_action(old_state)

        reward, done, score = game.play_step(new_move)
        new_state = agent.get_state(game)

        #Train short memory
        agent.train_short_memory(old_state, new_move, reward, new_state, done)

        #Remember
        agent.remember(old_state, new_move, reward, new_state, done)

        ##Train long memory and plot results
        if done:
            #
            game.reset()
            agent.num_games += 1
            agent.train_long_memory

            if score > record:
                record = score
                agent.model.save()
            
            print('Game: ', agent.num_games, 'Score: ', score, 'Record: ', record)

            #Show progress using MatPlotlib
            plot_scores.append(score)
            total_score += score
            avg_score = total_score/agent.num_games
            plot_mean_scores.append(avg_score)
            plot(plot_scores, plot_mean_scores)



if __name__ == '__main__':
    train()