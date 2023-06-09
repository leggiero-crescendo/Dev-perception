# DEV-Perception
- [프로그래머스 자율주행인지과정 5기](https://school.programmers.co.kr/learn/courses/16305/16305-5%EA%B8%B0-k-digital-training-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-%EC%9E%90%EC%9C%A8%EC%A3%BC%ED%96%89-%EB%8D%B0%EB%B8%8C%EC%BD%94%EC%8A%A4-perception)
- [알고리즘 연습 기록](https://github.com/leggiero-crescendo/coding-test.git)

## 🗂 Doc
<details>
<summary>Xycar</summary>
<div markdown="1"> 

- [Xycar 모음](xycar.md)
</div>
</details>
<details>
<summary>OpenCV C++ 예시 모음</summary>
<div markdown="1"> 

  
| Basic | Intermediate |
| --- | --- |
| [OpenCV 영상 입출력](https://github.com/leggiero-crescendo/Dev-perception/issues/3) | [이동변환](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issue-1680446525), [전단변환](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issuecomment-1519784000)|
| [cv::Mat](https://github.com/leggiero-crescendo/Dev-perception/issues/3#issuecomment-1516305225) | [크기변환 보간법](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issuecomment-1519894023) |
|[동영상 입출력](https://github.com/leggiero-crescendo/Dev-perception/issues/3#issuecomment-1517192260) | 회전변환, 기하변한 |
| [그리기 함수](https://github.com/leggiero-crescendo/Dev-perception/issues/3#issuecomment-1517194703) | 어파인변환 투시변환 |
|  [이벤트 처리](https://github.com/leggiero-crescendo/Dev-perception/issues/3#issuecomment-1517194889) | 리맵핑 |
||[컬러영상의 기초](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issuecomment-1522810850)|
||[색공간](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issuecomment-1522810911)|
||[컬러영상처리](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issuecomment-1522810970)|
||[특정색상영역추출](https://github.com/leggiero-crescendo/Dev-perception/issues/4#issuecomment-1522811035)|

</div>
</details>


## 👻 TIL

<details>
<summary>Week 1 (3/17)</summary>
<div markdown="1">   

- [Github 사용법 , 문제유형 파악법](./week1-1/)

- [알고리즘 문제 8개 과제](./week1-2/)

|  | Python | CPP |
| --- | --- | --- |
| Lv2. 사탕 담기 | ✅ |  |
| Lv2. 올바른 괄호 | ✅ |  |
| Lv2. 기능 개발 | ✅ |  |
| Lv2. 배상 비용 최소화 | ✅ |  |
| Lv1. 세 소수의 합 | ✅ |  |
| Lv2. 주사위 게임 |  |  |
| Lv2. 문자열 압축 | ✅ |  |
| Lv2. 스킬 트리 | ✅ |  |

</div>
</details>
<details>
<summary>Week 2 : Linux Basic (3/20 ~ 3/24)</summary>
<div markdown="1">       

- [리눅스 기초1](./week2/230320.md)
- [리눅스 기초2](./week2/230321.md)
- [리눅스 기초3](./week2/230322.md)
- [리눅스 기초4](./week2/230323.md)
- [리눅스 기초5](./week2/230324.md)

</div>
</details>
<details>
<summary>Week 3 : ROS1 (3/27 ~ 3/31)</summary>
<div markdown="1">       

- [ROS 기초](./week3/230327.md)
- [ROS 프로그래밍](./week3/230328.md)
  - [과제 1 Turtlesim 8자주행 변형](./week3/230328_실습.md) : turtlesim 이 turn 하는 횟수를 파라미터로 지정할 수 있도록 코드수정
  - [과제 2 예제코드 분석](./week3/230328_실습.md)
- ROS 노드 통신프로그래밍
  - [과제 1 ROS 노드통신프로그래밍](./week3/230329_homework1.md) 
  - [과제 2 토픽 가공해서 보내기](./week3/230329_homework2.md)
  - [ROS 노드 원격통신](./week3/230329.md)
- [자이카 소개](./week3/230330.md)
- [RVIZ 기반 차량 3D 모델링, 3D자동차](./week3/230331.md)
  - [과제 1 자이카 실습과제](./week3/230331_자이카실습과제1.md)

</div>
</details>
<details>
<summary>Week 4 : ROS1 with Sensor & RVIZ (4/3 ~ 4/7)</summary>
<div markdown="1">       

- [센서장치 기초, 데이터시각화](./week4/230403.md)
  - [과제 1 RVIZ 기반 IMU 뷰어제작](./week4/week4-1/230403실습.md)
- [라이다, 초음파 센서 활용](./week4/230404.md)
  - [과제 1 RVIZ 기반 라이다 뷰어제작](./week4/week4-2/230404실습.md)
- [센서를 활용한 자율주행](./week4/230405.md)
- [실습 DAY (목,금)](./week4/230406-07.md)
  - [실습 소스 파일](./week4/week4-4,5)

</div>
</details>
<details>
<summary>Week 5 : Lane detection (4/10 ~ 4/14)</summary>
<div markdown="1">       

- [자이카 차선인식](./week5/230410.md)
  - [git 특강:김동영강사님](./week5/Github특강.md)
- [차선인식 기법](./week5/230411.md)
- [조향각 제어](./week5/230412.md)
- [실습](./week5/230413-14.md)
</div>
</details>
<details>
<summary>Week 6 : OpenCV with C++ Basic (4/17 ~ 4/21)</summary>
<div markdown="1">       

- [로보틱스 기초 지식 및 컴퓨터비전, OPENCV](./week6/230417.md)
  - [CMake이용하여 build하기 예시 정리](https://leggiero-crescendo.tistory.com/95)
  - [CMakeLists 를 작성할 때 도움이 될 수 있도록 정리](https://github.com/leggiero-crescendo/Dev-perception/issues/2)
- [OpenCV 기초사용법 1](./week6/230418.md)
  - [실습 1 영상 입출력 : 커맨드로 args 받기(feet, clion으로 args받기)](https://leggiero-crescendo.tistory.com/96)
- [OpenCV 기초사용법 2](./week6/230419.md)
- [영상의 밝기와 명암비 조절](./week6/230420.md)
- [필터링](./week6/230421.md)
  - [과제 1 히스토그램 스트레칭 개선](./week6/week6-5)

</div>
</details>

<details>
<summary>Week 7: OpenCV with C++ Intermediate (4/24 ~ 4/28)</summary>
<div markdown="1">       

- [영상의 기하학적 변환](./week7/230424.md)
- [컬러 영상 처리](./week7/230425.md)
- [영상의 특징 추출](./week7/230426.md)
- [이진 영상 처리](./week7/230427.md)
- [영상분활과 객체검출](./week7/230428.md)
  - [황성규강사님 Seession](./week7/230428_1.md)
  - [과제 1 서브픽셀](./week7/230428_과제.md)

</div>
</details>


<details>
<summary>Week 8: OpenCV with C++ Advanced (5/1 ~ 5/5)</summary>
<div markdown="1">       

- [특징점 검출과 매칭](./week8/230501.md)
- [머신러닝과 딥러닝 1](./week8/230502.md)
- [머신러닝과 딥러닝 2](./week8/230503.md)
- [차선인식 온라인 프로젝트](./week8/230504-05.md)

</div>
</details>

<details>
<summary>Week 9: Offline Lane keeping project (5/8 ~ 5/12)</summary>
<div markdown="1">       

- [lane keeping](./Project/1.LaneKeeping/)

</div>
</details>
<details>
<summary>Week 10: 인공지능 수학</summary>
<div markdown="1">       

</div>
</details>

<details>
<summary>Week 11: 인공지능개요 (5/22 ~ 5/26)</summary>
<div markdown="1">       
  
- [Docker](./week11/230522.md)
- [인공신경망 개요](./week11/230523.md)
- [신경망 개요](./week11/230524.md)
- [Perception in self driving car](./week11/230525.md)
  - [pytorch tensor ](./week11/week11-4/pytorch_tensor.py)
- [CNN](./week11/230526.md)

</div>
</details>

<details>
<summary>Week 12: Deep Learning (5/29 ~ 6/2)</summary>
<div markdown="1">       
  
- [Object detection](./week12/230529.md)
- [Yolo](./week12/230530.md)
- [Yolo v3](./week12/230531.md)
- [Yolo v3 Load model](./week12/230601.md)

</div>
</details>

<details>
<summary>Week 13: 자율주행 perception 기술 (6/5 ~ 6/9)</summary>
<div markdown="1">       
  
- [자율주행 perception 기술](./week13/230605.md)
- [Open Dataset](./week13/230606.md)
- [Data labeling](./week13/230607.md)
- [Perception Application1](./week13/230608.md)
- [Perception Application2](./week13/230609.md)

</div>
</details>
