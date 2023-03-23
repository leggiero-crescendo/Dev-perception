'''
🔫 Strategy
- 스킬트리에서 선행스킬 순서에 존재하는 것들만 확인함
- check를 통해서 각 문자열의 요소확인

🔐 Method
- skill_trees 의 문자열 하나씩 확인
- 각 문자열의 문자 요소 하나씩 확인
- 문자열의 문자요소가 skill에 포함된다면
    - 그 s가 skill_list 중 첫번째가 아니라면 False 반환
    
🐣 TIL
- 문자열 검증방식으로 접근했었는데, 다른 사람 코드를 보니 문자열을 새로 s로 만들어서 skill 값과 비교해보는 식으로 접근하는 것이 훨씬 간결하게 코드를 짤 수 있는 것 같다.
'''
def solution_my(skill, skill_trees):
    answer = 0
    
    for skills in skill_trees: #skill_trees 의 문자열 하나씩 확인
        skill_list = list(skill)
        check = False
        for s in skills: # 각 문자열의 문자 요소 하나씩 확인
            if s in skill: # 문자열의 문자요소가 skill에 포함된다면
                if s !=skill_list[0]: # 그 s가 skill_list 중 첫번째가 아니라면
                    check = False
                    break
                else:
                    skill_list.pop(0)
                    check = True
            else:
                check = True
        if check:
            answer += 1
                
    return answer

def solution(skill, skill_trees):
    count = 0
    for skill_tree in skill_trees:
        s = ""                      # 하나의 스킬트리를 뽑을 때마다 s 초기화
        for ch in skill_tree:       
            if ch in skill:         # 스킬트리 중에 skill이 있다면 s에 추가
                s += ch
        
        if skill[:len(s)] == s:     # 만든 s를 기준으로 skill과 같다면 count += 1
            count += 1
    
    return count
