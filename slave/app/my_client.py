# -*- coding: utf-8 -*

# my_client.py

# Constants; Do not edit
import time
from algo.eval_color import *
from algo.generate_position import *
from algo.preprocess_tensor import *
from scripts.demo import *
import random

NONE = 0
WHITE = 1
BLACK = 2

COLOUR = 0
COORD = 1

original_color=0
enemy_color=0

my_map = [[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15]
my_colour = NONE

p1_count=0
p2_count=0

before_enemy_x = 0
before_enemy_y = 0


# 중점이 되는 흰돌의 위치
white_x = random.randrange(6,10)
white_y = random.randrange(6,10)

# 첫 3점을 정하는 랜덤값
case_num = random.randrange(1,5)
random_left_right = random.randrange(0,2)

# 전략:
# Player 1이 걸리면 밸런스 있는 3수를 두고 상대방의 선택을 어렵게 한 후, 최적의 조건칼라를 고른다.
# Player 2가 걸리면 무조건 색깔을 바로 골라서 알고리즘 보다 AI 모델이 두는 수를 늘린다.

def view_map():
    for y in range(15):
        for x in range(15):
            if my_map[x][y] == WHITE:
                print('o', end='')
            elif my_map[x][y] == BLACK:
                print('x', end='')
            else:
                print(' ', end='')
        print('')


def set_colour(colour):
    print("set_colour:", colour)

    global my_colour
    my_colour = colour


def set_stone(x, y, colour):
    print("set_stone:", x, y, colour)

    global my_map
    global before_enemy_x
    global before_enemy_y
    
    # set 할때 들어온 colour이 내 칼라랑 다르면 상대방의 직전 x, y좌표값에 저장된다.
    if(colour != my_colour):
        before_enemy_x = x
        before_enemy_y = y
        print("상대방이 직전에 둔 좌표는", x, y)

    my_map[x][y] = colour
    view_map()

def choose_colour():
    global my_colour
    global p1_count
    global p2_count
    global original_color
    global enemy_color

    print("select_colour")

    ## Player1 + 첫번째 턴 (색깔바로선택)
    if((my_colour==1) and (p1_count==3)):
        print("Player1의 선택 단계입니다.", p1_count)
        my_colour= eval_color(my_map)
        original_color = my_colour
        p1_count+=1
    
    ## Player2 두번째 턴(색깔바로선택)
    # 흑을 선택 or 백을 선택
        # 백을 선택하면 (내차례) -> 진짜 돌두기
        # 흑을 선택하면 (상대방차례) -> 진짜 돌두기
    elif((my_colour==1) and (p2_count==0)):
        print("Player2의 선택 단계입니다.", p2_count)
        my_colour = eval_color(my_map)
        original_color = my_colour
        p2_count+=1
    
    return my_colour


def place_stone():
    global my_colour
    global p1_count
    global p2_count
    global original_color
    global enemy_color
    global before_enemy_x
    global before_enemy_y
    

    # 미리 정해둔 white값
    global white_x
    global white_y

    # 미리 정해둔 랜덤값
    global case_num
    global random_left_right

    print("place_stone")
    
    ## Player1 + 첫번째턴 (연속)
    if((my_colour==2) and p1_count==0):
        print("중점이 되는 흰돌의 위치는", white_x, white_y)
        x, y = generate_position(my_colour, p1_count, white_x, white_y, case_num, random_left_right)
        p1_count+=1
        time.sleep(1)
        return x, y
    
    ## Player1 + 두번째턴(연속)
    elif((my_colour==1) and (p1_count==1)):
        print("중점이 되는 흰돌의 위치는", white_x, white_y)
        print("my_colour", my_colour)
        print("count는", p1_count)
        p1_count+=1
        time.sleep(1)
        return white_x, white_y
    
    ## Player1 + 3번째턴(연속)
    elif((my_colour==2) and (p1_count==2)):
        print("중점이 되는 흰돌의 위치는", white_x, white_y)
        print("my_colour", my_colour)
        print("count는", p1_count)
        x, y = generate_position(my_colour, p1_count, white_x, white_y , case_num, random_left_right)
        p1_count+=1
        time.sleep(1)
        return x, y

    ## Model 소환 (내 차례일때 둔다.)
    else:
        print("이제 돌을 둡니다.")
        my_tensor = preprocess_tensor(my_map, before_enemy_x, before_enemy_y, my_colour)
        x, y = gomoku_rl(my_tensor, my_colour)
        # next_move = find_best_move(my_map, my_colour)
        print(x,y,"위치에 돌을 둡니다.")
        time.sleep(1)
        return x, y

def make_decision():
    print("make_decision")

    # 걍 고정(move 절대 안함, 모델에게 빨리넘기기 위한 전략)
    return COLOUR

def victory():
    print("victory")


def defeat():
    print("defeat")

