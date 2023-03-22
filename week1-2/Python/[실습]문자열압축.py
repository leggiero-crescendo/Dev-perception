'''
🐱 Key Points
- 1개 이상 단위로 문자열을 잘라 압축하여 표현하였을 때 가장 짧은 것의 길이를 return 하도록 solution 함수 완성

🔫 Strategy
- 완전탐색과 문자열을 사용해서 해결하는 문제라함.
- 제한사항을 보면 s의 길이가 1이상 1,000이하 -> 완전탐색

🔐 Method
- 1 ~ n/2 문자열 길이만큼 쪼개서 반복 (for / for)
    - tmp에 저장한 첫번째 문자가 뒤에 반복될 경우 cnt +1
    - 같은 단어가 반복된 적 있지만, 더이상 반복되지 않을 경우 -> cnt 값이 1이 아닐 경우 : b = b + str(cnt) + tmp
    - 같은 단어가 반복된 적이 없는 경우 -> b = b + tmp
  - 단위 i 마다 만들어지는 b를 answer에 저장
- answer 중 가장 작은 b의 길이를 return

🐣 TIL
- solution_run으로 하면 runtime error가 뜬다. 나는 반복되는 문자열의 길이가 짧아져서 더 빠르것이라고 예상했는데 왜 일까?
'''
def solution_run(s):
    answer = []
    for i in range(1, (len(s)//2)+1):
        b = ''
        cnt = 1
        tmp = s[:i]

        for j in range(i, len(s)+i, i):
            if tmp == s[j:i+j]:
                cnt+=1
            else:
                if cnt!=1:
                    b = b + str(cnt)+tmp
                else:
                    b = b + tmp
                tmp=s[j:j+i]
                cnt = 1
        # if cnt!=1:
        #     b = b + str(cnt)+tmp
        # else:
        #     b=b+tmp
        answer.append(len(b))
    return min(answer)

def solution(s):
    answer = []
    for i in range(1, (len(s))+1):
        b = ''
        cnt = 1
        tmp = s[:i]

        for j in range(i, len(s)+i, i):
            if tmp == s[j:i+j]:
                cnt+=1
            else:
                if cnt!=1:
                    b = b + str(cnt)+tmp
                else:
                    b = b + tmp
                tmp=s[j:j+i]
                cnt = 1

        answer.append(len(b))
    return min(answer)
