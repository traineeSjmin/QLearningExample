import pygame
import random
import numpy as np
import sys

from Agent import PlayerAgent

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FPS = 0
SCREEN_HEIGHT, SCREEN_WIDTH = 0, 0
CELL_SIZE = 100
FOOD_SIZE = 30
MARGIN = 30
USE_QLEARNING = False

dx = [-1, 1, 0, 0]
dy = [0, 0 ,-1, 1]
grid = []
food_pose = []
score = 0


def Init(grid_shape, fps, use_q_learning):
    global grid, player, food_pose, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, USE_QLEARNING
    SCREEN_HEIGHT = grid_shape[0] * CELL_SIZE
    SCREEN_WIDTH = grid_shape[1] * CELL_SIZE
    FPS = fps
    USE_QLEARNING = use_q_learning
    grid = CreateGrid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
    player = CreatePlayer()
    return


def Run(trained_q_table):
    global score, food_pose
    pygame.init()
    clock = pygame.time.Clock()
    scoreFont = pygame.font.SysFont("arial", 20, True, True)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Game")

    player_pose = CreateRandomPosition(player.GetPosition())
    food_pose = CreateRandomPosition(player.GetPosition())
    obstacle_pose = CreateRandomPosition(player.GetPosition())
    while (obstacle_pose == food_pose):
        obstacle_pose = CreateRandomPosition(player.GetPosition())

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not USE_QLEARNING:
                curr_position = player.GetPosition()
                pose_x = curr_position[0]
                pose_y = curr_position[1]
                if event.key == pygame.K_UP and pose_x > 0:
                    player.MovePlayer(dx[0], dy[0])
                    score -= 0.1
                elif event.key == pygame.K_DOWN and pose_x < SCREEN_HEIGHT//CELL_SIZE-1:
                    player.MovePlayer(dx[1], dy[1])
                    score -= 0.1
                elif event.key == pygame.K_LEFT and pose_y > 0:
                    player.MovePlayer(dx[2], dy[2])
                    score -= 0.1
                elif event.key == pygame.K_RIGHT and pose_y < SCREEN_WIDTH//CELL_SIZE-1:
                    player.MovePlayer(dx[3], dy[3])
                    score -= 0.1

        if (USE_QLEARNING):
            pose_x = player_pose[0]
            pose_y = player_pose[1]
            food_x = food_pose[0]
            food_y = food_pose[1]
            obs_x = obstacle_pose[0]
            obs_y = obstacle_pose[1]
            action = np.argmax(trained_q_table[pose_x,pose_y,food_x,food_y,obs_x,obs_y])
            next_pose_x = pose_x + dx[action]
            next_pose_y = pose_y + dy[action]
            if (0 <= next_pose_x and next_pose_x < SCREEN_WIDTH//CELL_SIZE and
                0 <= next_pose_y and next_pose_y < SCREEN_HEIGHT//CELL_SIZE):
                player.MovePlayer(dx[action], dy[action])
                score -= 0.1

        screen.fill(BLACK)
        player_pose = player.GetPosition()
        if (player_pose == food_pose):
            score += 1
            food_pose = CreateRandomPosition(player.GetPosition())
            obstacle_pose = CreateRandomPosition(player.GetPosition())
            while (obstacle_pose == food_pose):
                obstacle_pose = CreateRandomPosition(player.GetPosition())
        elif (player_pose == obstacle_pose):
            score -= 1
            food_pose = CreateRandomPosition(player.GetPosition())
            obstacle_pose = CreateRandomPosition(player.GetPosition())
            while (obstacle_pose == food_pose):
                obstacle_pose = CreateRandomPosition(player.GetPosition())
                
        screen_player_position = [player_pose[1]*CELL_SIZE,player_pose[0]*CELL_SIZE,CELL_SIZE,CELL_SIZE]
        screen_food_position = [food_pose[1]*CELL_SIZE +CELL_SIZE/2,food_pose[0]*CELL_SIZE+CELL_SIZE/2]
        screen_obstacle_position = [[CELL_SIZE*obstacle_pose[1]+CELL_SIZE/2,CELL_SIZE*obstacle_pose[0]+int(MARGIN/2)],
                                    [CELL_SIZE*obstacle_pose[1]+int(MARGIN/2),CELL_SIZE*obstacle_pose[0]+CELL_SIZE-int(MARGIN/2)],
                                    [CELL_SIZE*obstacle_pose[1]+CELL_SIZE-int(MARGIN/2),CELL_SIZE*obstacle_pose[0]+CELL_SIZE-int(MARGIN/2)]]
        score_text= scoreFont.render("SCORE : " + str(round(score,1)), True, WHITE)
        pygame.draw.rect(screen, RED, screen_player_position)
        pygame.draw.circle(screen, GREEN, screen_food_position, FOOD_SIZE)
        pygame.draw.polygon(screen, YELLOW, screen_obstacle_position)
        screen.blit(score_text, [0, 0])
        pygame.display.update()


def CreateGrid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE):
    if SCREEN_WIDTH%CELL_SIZE != 0 or SCREEN_HEIGHT%CELL_SIZE != 0:
        print("Invalid grid or cell size!")
        return
    column_num = int(SCREEN_WIDTH / CELL_SIZE)
    row_num = int(SCREEN_HEIGHT / CELL_SIZE)
    matrix = [[0 for _ in range(column_num)] for _ in range(row_num)]
    return np.array(matrix)


def CreatePlayer():
    position = [random.randrange(grid.shape[0]), random.randrange(grid.shape[1])]
    player = PlayerAgent(RED, position, grid)
    return player


def CreateRandomPosition(avoid_position):
    while True:
        position = [random.randrange(grid.shape[0]), random.randrange(grid.shape[1])]
        if avoid_position != position:
            return position