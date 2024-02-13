import torch
from tensordict import TensorDict
# 모델에 전달할 데이터 텐서형태로 변환

def preprocess_tensor(my_map, before_x, before_y, original_color, enemy_color):

    ai_data = [[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15]
    enemy_data = [[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15]
    enemy_before_data = [[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15,[0.]*15]

    # 순회 하면서 ai와 적의 데이터를 각각 테이블에 반영
    for i in range(0, 15):
        for j in range(0, 15):
            if my_map[i][j]==original_color:
                ai_data[i][j] = 1
            elif my_map[i][j]==enemy_color:
                enemy_data[i][j] = 1
    
    # 그 전의 데이터 반영
    enemy_before_data[before_x][before_y]=1

    data_package=[ai_data, enemy_data, enemy_before_data]

    # 패키지화 + 완성
    current_state= torch.tensor([data_package])
    
    ##########################################

    board_size = 15
    num_actions = board_size * board_size
    action_mask = torch.ones(num_actions, dtype=torch.bool)

    false_indices = []

    # 해당 x * 15 + y
    for i in range(0, 15):
        for j in range(0, 15):
            if (my_map[i][j]==1) or (my_map[i][j]==2):
                false_indices.append(i*15 + j)

    for index in false_indices:
        action_mask[index] = False

    action_mask = action_mask.view(1, -1)  # 배치 차원을 추가


    # 모델에 전달할 TensorDict 생성
    tensordict = TensorDict({
        "observation": current_state.unsqueeze(0),
        "action_mask": action_mask,
    }, batch_size=1)

    return tensordict