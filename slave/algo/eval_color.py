def eval_color(board):
    # 돌의 개수와 연속성을 평가하여 점수를 계산하는 함수
    def score_line(line):
        scores = {1: 0, 2: 0}
        current_stone = 0
        count = 0
        for stone in line:
            if stone == current_stone:
                count += 1
            else:
                if current_stone != 0 and count > 1:
                    scores[current_stone] += count * count  # 연속된 돌의 개수에 비례하여 점수 부여
                current_stone = stone
                count = 1
        if current_stone != 0 and count > 1:
            scores[current_stone] += count * count
        return scores

    total_scores = {1: 0, 2: 0}

    # 가로, 세로, 대각선 방향으로 점수 계산
    for i in range(15):
        total_scores[1] += score_line(board[i])[1]
        total_scores[2] += score_line(board[i])[2]
        total_scores[1] += score_line([board[j][i] for j in range(15)])[1]
        total_scores[2] += score_line([board[j][i] for j in range(15)])[2]

    # 대각선 검사
    for d in range(-14, 15):
        total_scores[1] += score_line([board[i][i+d] for i in range(15) if 0 <= i+d < 15])[1]
        total_scores[2] += score_line([board[i][i+d] for i in range(15) if 0 <= i+d < 15])[2]
        total_scores[1] += score_line([board[i+d][i] for i in range(15) if 0 <= i+d < 15])[1]
        total_scores[2] += score_line([board[i+d][i] for i in range(15) if 0 <= i+d < 15])[2]

    # 더 높은 점수를 가진 돌의 색을 반환
    if total_scores[1] > total_scores[2]:
        return 1  # 백돌이 더 유리
    elif total_scores[2] > total_scores[1]:
        return 2  # 흑돌이 더 유리
    else:
        return 1  # 동일한 점수, 동등한 위치, 다음 수를 두는 선택권에 우선순위 부여