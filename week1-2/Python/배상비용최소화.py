'''
🐱 Key Points

🔫 Strategy

🔐 Method

🐣 TIL

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
