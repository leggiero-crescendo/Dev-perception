'''
🐱 Key Points
- 남은 작업량 계산을 통한 배상비용 최소화

🔫 Strategy
- 자료구조 heap 활용, 우선순위 큐

🔐 Method

🐣 TIL
other 1) lambda 사용한 코드를 보면 reverse를 하지 않고 -1 가장 끝을 확인하기 위해 -1과 breack를 사용하지 않는 방법을 씀 
    - 또한 lambda를 이용해서 work의 요소 x에 대하여 x**2를 한 후 for 문 대신 map을 사용하고 sum을 진행함
    => map은 메모리 관리에 효율적임 [https://wikidocs.net/21057]
other 2) heapq module 사용
    - heap 완전 이진트리의 일종 우선순위 큐를 위하여 만들어진 자료구조 
    - 최댓값 , 최솟값을 빠르게 찾아내도록 만들어진 자료구조
    - 힙은 일종의 반정렬 상태(느슨한 정렬 상태) 를 유지한다.
        - 큰 값이 상위 레벨에 있고 작은 값이 하위 레벨에 있다는 정도 간단히 말하면 부모 노드의 키 값이 자식 노드의 키 값보다 항상 큰(작은) 이진 트리를 말한다.
    - 힙 트리에서는 중복된 값을 허용한다. (이진 탐색 트리에서는 중복된 값을 허용하지 않는다.)
    [참고](https://gmlwjd9405.github.io/2018/05/10/data-structure-heap.html)
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



import heapq

def solution_heapq(no, works):
    MaxHeap = []

    if no >= sum(works):
        return 0

    for work in works:
        heapq.heappush(MaxHeap, (-work, work))

    for _ in range(no):
        work = heapq.heappop(MaxHeap)[1] - 1 
        heapq.heappush(MaxHeap, (-work, work))

    return sum([i[1] ** 2 for i in MaxHeap])
