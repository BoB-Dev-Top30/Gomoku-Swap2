def eval_color(board):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 가로, 세로, 대각선
    color_weights = {1: 0, 2: 0}  # 각 색의 가중치를 저장할 딕셔너리

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != 0:  # 돌이 있는 경우
                for dx, dy in directions:  # 모든 방향에 대해 탐색
                    for gap in range(4):  # 최대 3칸 띄어질 수 있으므로
                        nx, ny = x + dx*(gap+1), y + dy*(gap+1)
                        if 0 <= nx < len(board[0]) and 0 <= ny < len(board):  # 보드 범위 내에 있는지 확인
                            if board[ny][nx] == board[y][x]:  # 같은 색 돌이면
                                if gap == 0:
                                    color_weights[board[y][x]] += 1**2  # 1칸 띄어져 있으면 제곱의 가중치 부여
                                elif gap == 2:
                                    color_weights[board[y][x]] += 10  # 2칸 띄어져 있으면 +10 가중치 부여
                                elif gap == 3:
                                    color_weights[board[y][x]] += 5  # 3칸 띄어져 있으면 +5 가중치 부여

    # 가중치가 높은 색 반환, 동일하면 1(백돌) 반환
    return 1 if color_weights[1] >= color_weights[2] else 2
