'''
🐱 Key Points

🔫 Strategy

🔐 Method

🐣 TIL
- lambda 사용한 코드를 보면 reverse를 하지 않고 -1 가장 끝을 확인하기 위해 -1과 breack를 사용하지 않는 방법을 씀 
- 또한 lambda를 이용해서 work의 요소 x에 대하여 x**2를 한 후 for 문 대신 map을 사용하고 sum을 진행함
=> map은 메모리 관리에 효율적임 [https://wikidocs.net/21057]
'''

def solution(no, works):
    result = 0
    for num in range(1,no+1):
        works.sort(reverse=True)
        if works[0] == 0: 
            break
        works[0] -= 1
    for i in works:
        result += i**2
    return result

def solution_lambda(no, works):
    for i in range(no):
        works.sort()
        if works[-1] != 0:
            works[-1] -= 1
    return sum(map(lambda x : x**2, works))
