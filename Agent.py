import numpy as np
from tqdm import tqdm

class PlayerAgent:
    def __init__(self, color, position, grid):
        self.color = color
        self.position = position
        self.grid = grid

    def SetPosition(self, x, y):
        self.position = [x,y]

    def GetPosition(self):
        return self.position
    
    def MovePlayer(self, dx, dy):
        nx = self.position[0] + dx
        ny = self.position[1] + dy
        if (0 <= nx and nx < self.grid.shape[0] and 0 <= ny and ny < self.grid.shape[1]):
            self.SetPosition(nx, ny)
        else:
            self.SetPosition(self.position[0], self.position[1])


class QLearningAgent:
    def __init__(self, learning_rate, discount_factor, grid_shape):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.grid_shape = grid_shape
        self.num_actions = 4
        self.q_table = np.zeros([grid_shape[0], grid_shape[1], # Number of Grid
                                grid_shape[0], grid_shape[1],  # Number of Food pose
                                grid_shape[0], grid_shape[1],  # Number ofObstacle Pose
                                self.num_actions])             # Number of Action
        self.dx = [-1, 1 ,0 ,0]
        self.dy = [0, 0, -1, 1] # up, down, left, right

    def LearnEpisode(self):
        for grid_x in tqdm(range(self.grid_shape[0]), desc="grid_x", position=1, leave=False):
            for grid_y in tqdm(range(self.grid_shape[1]),desc="grid_y", position=2, leave=False):
                for food_x in tqdm(range(self.grid_shape[0]), desc="food_x", position=3, leave=False):
                    for food_y in tqdm(range(self.grid_shape[1]), desc="food_y", position=4, leave=False):
                        for obs_x in tqdm(range(self.grid_shape[0]), desc="obs_x", position=5, leave=False):
                            for obs_y in tqdm(range(self.grid_shape[1]), desc="obs_y", position=6, leave=False):
                                for action in tqdm(range(self.num_actions), desc="action", position=7, leave=False):
                                    player_pose = (grid_x, grid_y)
                                    food_pose = (food_x, food_y)
                                    obs_pose = (obs_x, obs_y)
                                    self.UpdateQTable(player_pose,
                                                 food_pose,
                                                 obs_pose,
                                                 action)
                                    
    def UpdateQTable(self, player_pose, food_pose, obs_pose, action):
        while (player_pose != food_pose):
            if (np.random.rand() < 0.1):
                action = np.random.choice(self.num_actions)
            else:
                action = np.argmax(self.q_table[player_pose[0], player_pose[1],
                                                food_pose[0], food_pose[1],
                                                obs_pose[0], obs_pose[1]])
            
            new_player_pose = (player_pose[0] + self.dx[action], player_pose[1] + self.dy[action])
            new_player_pose = (max(0, min(self.grid_shape[0] - 1, new_player_pose[0])),
                               max(0, min(self.grid_shape[1] - 1, new_player_pose[1])))
            
            if (new_player_pose == food_pose):
                reward = 1
            elif (new_player_pose == obs_pose):
                reward = -1
            else:
                reward = -0.1

            self.q_table[player_pose[0], player_pose[1],
                         food_pose[0], food_pose[1],
                         obs_pose[0], obs_pose[1], action] = ((1 - self.learning_rate) *
                                                              self.q_table[player_pose[0], player_pose[1], food_pose[0], food_pose[1], obs_pose[0], obs_pose[1], action] +
                                                              self.learning_rate *
                                                              (reward + self.discount_factor * np.max(self.q_table[new_player_pose[0], new_player_pose[1], food_pose[0], food_pose[1], obs_pose[0], obs_pose[1]])))
            player_pose = new_player_pose
    
    def GetQTable(self):
        print(self.q_table)
        return self.q_table