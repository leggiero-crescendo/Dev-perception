'''
🐱 Key Points
1. Progress 순서에 따라 배포가 가능함
2. 작업간의 개발속도가 적힌 speed를 참고 해야함 

🔫 Strategy
queue를 사용해 문제를 해결

🔐 Method

progresses에 대해 첫번째 while문 생성
- cnt : 한번에 배포할 기능의 수 = 0 으로 할당
- 첫번째 progresses가 100이상이거나 progresses 내 요소가 여전히 남아있다면 두번째 while문 반복
    - progresses[0]>=100 -> cnt += 1
    - progress.pop(0)/speeds.pop(0) : 첫번째 요소 제거
- 첫번째 while 문에서 progresses의 각 요소에 각 speeds +
- cnt 값을 answer 할당 

'''

def solution(progresses, speeds):
    answer = []
    while progresses :
        cnt = 0
        while progresses and progresses[0] >= 100:
            cnt+=1
            progresses.pop(0)
            speeds.pop(0)

        progresses = [progresses[i]+speeds[i] for i in range(len(progresses))]

        if cnt:
            answer.append(cnt)
    
    return answer


if __name__ == '__main__':
    progresses = [93, 30, 55]
    speeds = [1, 30, 5]
    result = solution(progresses, speeds)
    print(result)