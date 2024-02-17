import hydra
from omegaconf import DictConfig, OmegaConf
from gomoku_rl import CONFIG_PATH
from gomoku_rl.policy import get_policy, Policy
from gomoku_rl.utils.policy import uniform_policy, _policy_t
from torchrl.data.tensor_specs import (
    DiscreteTensorSpec,
    CompositeSpec,
    UnboundedContinuousTensorSpec,
    BinaryDiscreteTensorSpec,
)
import torch
import logging

from gomoku_rl.core import Gomoku
import torch
from tensordict import TensorDict

board_size = 15
num_actions = board_size * board_size

ai_x = 0
ai_y = 0

ai_color = 0

def make_model(cfg: DictConfig):
    board_size = cfg.board_size
    device = cfg.device
    action_spec = DiscreteTensorSpec(
        board_size * board_size,
        shape=[
            1,
        ],
        device=device,
    )
    # when using PPO, setting num_envs=1 will cause an error in critic
    observation_spec = CompositeSpec(
        {
            "observation": UnboundedContinuousTensorSpec(
                device=cfg.device,
                shape=[2, 3, board_size, board_size],
            ),
            "action_mask": BinaryDiscreteTensorSpec(
                n=board_size * board_size,
                device=device,
                shape=[2, board_size * board_size],
                dtype=torch.bool,
            ),
        },
        shape=[
            2,
        ],
        device=device,
    )
    model = get_policy(
        name=cfg.algo.name,
        cfg=cfg.algo,
        action_spec=action_spec,
        observation_spec=observation_spec,
        device=cfg.device,
    )
    return model

@hydra.main(version_base=None, config_path=CONFIG_PATH, config_name="demo")
def main(cfg:DictConfig):
    global tensordict
    global ai_x
    global ai_y
    global ai_color

    if not OmegaConf.has_resolver("eval"):
        OmegaConf.register_new_resolver("eval", eval)
    
    OmegaConf.resolve(cfg)

    if(ai_color==2):
        print("흑돌에 특화된 ai를 불러옵니다.")
        model_ckpt_path = "pretrained_models/15_15/ppo/0.pt"
    
    elif(ai_color==1):
        print("백돌에 특화된 ai를 불러옵니다.")
        model_ckpt_path = "pretrained_models/15_15/ppo/1.pt"

    if model_ckpt_path:
        model = make_model(cfg)
        model.load_state_dict(torch.load(model_ckpt_path, map_location=cfg.device))
        model.eval()
    else:
        model = uniform_policy

    # AI 모델을 사용하여 다음 움직임 예측
    with torch.no_grad():
        tensordict = model(tensordict).cpu()

    # 모델이 예측한 다음 움직임의 인덱스
    action: int = tensordict["action"].item()

    print(action)
    # 인덱스를 (x, y) 좌표로 변환
    board_size = 15  # 예시에서는 15x15 보드를 사용
    x = action // board_size
    y = action % board_size

    ai_x = x
    ai_y = y

def gomoku_rl(input_tensor, my_colour):
    global tensordict  # 전역 변수 tensordict를 사용하겠다고 선언
    global ai_x
    global ai_y
    global ai_color

    ai_color = my_colour # 내 칼라(ai) 전달받음
    tensordict = input_tensor  # 이제 전역 변수에 값을 할당
    main()  # main 함수 호출


    print(f"AI move: ({ai_x}, {ai_y})")

    return ai_x, ai_y