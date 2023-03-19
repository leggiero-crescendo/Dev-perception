```bash
# git 로그인 방법 (일시)
git config --global user.name "이름"
git config --global user.email "git에 등록된 이메일"

git config --global user.name "leggiero-crescendo"
git config --global user.email "ktxlee779@gmail.com"

# git 로그인 방법 (자동)
git config credential.helper store
```

```bash
git init #저장소 초기화
git remote add origin https://github.com/prgrms-ad-devcourse/ad-practice-5-assignment.git # git 저장소 주소와 연결
git branch "week1-2/leggiero-crescendo" # branch 생성
git checkout week1-2/leggiero-crescendo
git branch # 확인
git add .
git commit -m "first-up"
git push origin week1-2/leggiero-crescendo

```