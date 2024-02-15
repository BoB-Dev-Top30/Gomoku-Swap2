import random

# 화이트돌을 중심으로 검정돌의 포지션을 정해줌 (최대한 밸런스 있게 하여 상대방의 선택을 어렵게함)
def generate_black_position(white_x, white_y, case_num, random_left_right):
    if(case_num == 1):
        first_black_x = white_x-1
        first_black_y = white_y
        if(random_left_right==0):
            second_black_x = white_x+2
            second_black_y = white_y-1
        elif(random_left_right==1):
            second_black_x = white_x+2
            second_black_y = white_y+1
    elif(case_num == 2):
        first_black_x = white_x
        first_black_y = white_y-1
        if(random_left_right==0):
            second_black_x = white_x-1
            second_black_y = white_y+2
        elif(random_left_right==1):
            second_black_x = white_x+1
            second_black_y = white_y+2
    elif(case_num == 3):
        first_black_x = white_x+1
        first_black_y = white_y
        if(random_left_right==0):
            second_black_x = white_x-2
            second_black_y = white_y-1
        elif(random_left_right==1):
            second_black_x = white_x-2
            second_black_y = white_y+1
    elif(case_num == 4):
        first_black_x = white_x
        first_black_y = white_y+1
        if(random_left_right==0):
            second_black_x = white_x-1
            second_black_y = white_y-2
        elif(random_left_right==1):
            second_black_x = white_x+1
            second_black_y = white_y+2
    return first_black_x, first_black_y, second_black_x, second_black_y

def generate_position(color, count, white_x, white_y , case_num, random_left_right):


    first_black_x, first_black_y, second_black_x, second_black_y = generate_black_position(white_x, white_y, case_num, random_left_right)

    if(color==2 and count==0):
       return first_black_x, first_black_y
    
    elif(color==2 and count==2):
        return second_black_x, second_black_y
