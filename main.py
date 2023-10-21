import GridGame as gg
from Agent import QLearningAgent

from tqdm import tqdm
import numpy as np
import os


FPS = 5
USE_QLEARNING = True
SAVE_TRAINED_FILE = True
LOAD_TRAINED_FILE = True

learning_rate = 0.1
discount_factor = 0.9
num_episodes = 30
grid_shape = (4,4)
eplilon = 0.1

absolute_path = os.getcwd()
save_path = absolute_path + "\\pretrained_q_learning"
load_path = absolute_path + "\\pretrained_q_learning"


def TrainQLearningAgent():
    learning_agent = QLearningAgent(learning_rate,
                                    discount_factor,
                                    grid_shape,
                                    eplilon)
    for _ in tqdm(range(num_episodes), desc="EPISODE", position=0):
        learning_agent.LearnEpisode()
    q_table = learning_agent.GetQTable()
    return q_table


def SaveTrainedFile(q_table):
    np.save(save_path + "\\" + str(grid_shape[0]) + "x" + str(grid_shape[1]), q_table)


def LoadTraindFile(file_name):
    q_table = np.load(load_path + "\\" + file_name)
    return q_table


if __name__ == "__main__":
    if (USE_QLEARNING):
        trained_q_table = TrainQLearningAgent()
    else:
        trained_q_table = None

    if (SAVE_TRAINED_FILE):
        SaveTrainedFile(trained_q_table)

    if (LOAD_TRAINED_FILE):
        file_name = str(grid_shape[0]) + "x" + str(grid_shape[1]) + ".npy"
        trained_q_table = LoadTraindFile(file_name)
    gg.Init(grid_shape, FPS, USE_QLEARNING)
    gg.Run(trained_q_table)