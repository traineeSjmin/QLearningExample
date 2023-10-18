import pygame
import random
import numpy as np
import sys
import time

from Player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BRUE = (0, 0, 255)
FPS = 10
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
CELL_SIZE = 100

dx = [0, 0, -1, 1]
dy = [-1, 1 ,0 ,0]
grid = []
food_pose = []
score = 0


def Init():
    global grid, player, food_pose
    grid = CreateGrid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
    player = CreatePlayer()
    return


def Run():
    global score, food_pose
    pygame.init()
    clock = pygame.time.Clock()
    scoreFont = pygame.font.SysFont("arial", 30, True, True)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Game")

    food_pose = CreateFood()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            elif event.type == pygame.KEYDOWN:
                curr_position = player.GetPosition()
                pose_x = curr_position[0]
                pose_y = curr_position[1]
                if event.key == pygame.K_UP and pose_y > 0:
                    player.MovePlayer(dx[0], dy[0])
                elif event.key == pygame.K_DOWN and pose_y < SCREEN_HEIGHT//CELL_SIZE-1:
                    player.MovePlayer(dx[1], dy[1])
                elif event.key == pygame.K_LEFT and pose_x > 0:
                    player.MovePlayer(dx[2], dy[2])
                elif event.key == pygame.K_RIGHT and pose_x < SCREEN_WIDTH//CELL_SIZE-1:
                    player.MovePlayer(dx[3], dy[3])

        screen.fill(BLACK)
        player_pose = player.GetPosition()
        if (player_pose == food_pose):
            score += 1
            while True:
                food_pose = CreateFood()
                if (player_pose != food_pose): break

        screen_player_position = [player_pose[0]*CELL_SIZE,player_pose[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE]
        screen_food_position = [food_pose[0]*CELL_SIZE,food_pose[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE]
        score_text= scoreFont.render("SCORE : " + str(score), True, WHITE)
        pygame.draw.rect(screen, RED, screen_player_position)
        pygame.draw.rect(screen, GREEN, screen_food_position)
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
    player = Player(RED, position)
    return player


def CreateFood():
    position = [random.randrange(grid.shape[0]), random.randrange(grid.shape[1])]
    return position


# TODO :: Check the index of state
def StateToIndex(state):
    return state[1] * grid.shape[1] + state[0]