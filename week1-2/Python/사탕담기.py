'''
🔫 Strategy
경우의 수를 모두 탐색하기 위해 조합으로 문제를 접근하기로 했다.

🔐 Method
1. weights의 길이만큼 for문 반복 (횟수 : i)
2. list weights의 요소를 조합하여 나올 수 있는 경우를 생성(조합 : j)
3. 각 조합에 대하여 합이 m인 조합이 등장하면 return하려고 하는 값 업데이트(반환 : answer)
    
🐣 TIL

'''


from itertools import combinations

def solution(m, weights):
    answer = 0
    for i in range(1, len(weights)):
        for j in combinations(weights, i):
            if sum(j) == m:
                answer+=1

    return answer


def solution_2(m, weights):
    answer = 0
    for i in range(len(weights)):
        com = list(combinations(weights, i+1))
        for j in com:
            if m == sum(j):
                answer += 1
    return answer

if __name__ == '__main__':
    m = 3000
    we = [500, 1500, 2500, 1000, 2000]
    re = solution(m,we)
    print(re)

