'''
🔫 Strategy
- n 이하 소수구하기
- 소수 3개의 합이 n이 되는 조합찾기
- 카운트

🔐 Method
- n 이하 소수구하기 (에라토스테네스의 체 이용) -> primes list 저장
- 소수 3개의 합이 n이 되는 조합찾기 (조합 combinations 이용)
- 카운트

🐣 TIL
'''
from itertools import combinations

def solution(n):
    answer = 0
    # n이하 소수 구하기
    primes = []
    a = [False, False] + [True]*(n-1)
    for i in range(2,n+1):
        if a[i]:
            primes.append(i)
            for j in range(2*i, n+1, i):
                a[j] = False
    for j in combinations(primes, 3):
        if sum(j) == n:
            answer+=1    
    return answer
