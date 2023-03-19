'''
🔫 Strategy
괄호의 짝을 확인한다. 

🔐 Method
1. ()를 확인하기 위하여 (일 경우 w+1 ,)일 경우 w-1로 구성
2. ) 중 가장 처음이 )로 시작된다면 False 반환
3. for 문을 다 돈 후 w를 확인하여 0일 경우 True , 아닐 경우 False
    
🐣 TIL
other 1 ) stack으로 접근 하면 다음과 같다.
other 2 ) 전략은 같지만 조금 더 간략하게 코드를 구성하는 방법인 것 같다.

[other code reference]
(https://velog.io/@ssongplay/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-%EC%98%AC%EB%B0%94%EB%A5%B8-%EA%B4%84%ED%98%B8-Python)

'''

def solution_my(s):
    w = 0
    for i, c in enumerate(s):
        if c == "(":
            w+=1
        else:
            if i == 0:
                return False
            else:
                w-=1
    if w == 0:
        return True
    else:
        return False


def solution_other1(s):
    stack = []
    for c in s:
        if c == "(":
            stack.append(c)
        else:
            if stack:
                stack.pop()
            else:
                return False
    if stack:
        return False
    return True


def solution_other2(s):
    x = 0
    for w in s:
        if x < 0:
            break
        x = x+1 if w=="(" else x-1 if w==")" else x
    return x==0

if __name__ == '__main__':
    s = "()()"
    result = solution_my(s)
    print(result)