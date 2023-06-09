# 230329 - ROS 노드 실습
## Q1) 누락 없이 데이터가 모두 잘 도착하는가?
---
0. 과제설명
- rosrun을 통하여 pub -> sub python 파일을 순차적으로 실행시켰을 경우

1. 현상확인

- 아래 그림과 같이 초기 데이터의 누락 발생

![Image](./img/1-1.png)

2. 원인분석
- subscriber가 준비되어있지 않은 상태에서 데이터를 먼저 전송했기 떄문이다.

3. 해결책 적용결과 정리
- get_num_connections() [Documents](http://docs.ros.org/en/lunar/api/rospy/html/rospy.topics.Topic-class.html#get_num_connections)
- Method : To check Subscriber connectiton 
```python
while ( pub.get_num_connections() == 0):
    cnt += 1

while not rospy.is_shutdown():
    ...
```
![Result](./img/1-2.png)

## Q2) 데이터 크기에 따른 전송속도는 어떻게 되는가?
0. 과제설명
1) sender
- sender_speed.py -> receiver_spped.py : sr_speed.launch
- sender 노드 생성 -> Topic : long_string (#으로 가득채움) -> 초당 1회 다양한 용량의 long_string 생성 
- 사이즈를 바꾸어서 1Mbyte, 5Mbyte, 10Mbyte, 20Mbyte, 50Mbyte 전송
2) receiver
- receiver 라는 이름으로 노드생성
- 다양한 용량의 long string을 수신해서, long_string 1개를 다 받으면 소요시간을 화면에 출력함 
- 가능한 속도도 출력하기 단위는 bps(byte/second)

1. 현상확인을 위한 코드 구현
#### sender_speed.py
```python
#!/usr/bin/env python
#-*- coding: utf-8-*-

import rospy 
from std_msgs.msg import String

rospy.init_node('sender', anonymous=True)

pub = rospy.Publisher('long_string', String) 
size = rospy.get_param('~size')
hash = '#'* 1000000 * size#size_dic[size]


rate = rospy.Rate(1) #초당 1회

while not rospy.is_shutdown():
    print size 

    hash_time = hash + ":" + str(rospy.get_time())
    print hash_time
    pub.publish(hash_time) 
    rate.sleep() 
```
#### receiver_speed.py
```python
#!/usr/bin/env python
#-*- coding: utf-8-*-
# Sheband(#!)
import sys
import rospy # rospy module
from std_msgs.msg import String

name = 'receiver'
sub_topic = 'long_string'

def callback(data):
    msgs = data.data.split(":")
    time_data = float(rospy.get_time()) - float(msgs[1])
    str_size = sys.getsizeof(msgs[0])
    rospy.loginfo(str(str_size)+"byte :"+str(time_data)+"s")
    rospy.loginfo("speed:"+str(float(str_size)/max(time_data, 1e-9))+"byte/s")
    
rospy.init_node(name, anonymous=True) 
sub = rospy.Subscriber(sub_topic, String, callback) 

rospy.spin() 

```
#### sr.launch
```python
<launch>
    <arg name="size_m" default="1"/>
	<node pkg="msg_send" type="sender_speed.py" name="sender">
        <param name="size" type="int" value="$(arg size_m)"/>
    </node>
	<node pkg="msg_send" type="receiver_speed.py" name="receiver" output="screen"/>
</launch>
```

2. 결과

![1M](./img/2-1.png)
![5M](./img/2-5.png)
![10M](./img/2-10.png)
![20M](./img/2-20.png)
![50M](./img/2-50.png)

3. 분석
- 1M : 0.005s 이하 
- 5M : 0.04s 
- 10M : 0.05s 
- 20M : 0.06s 
- 50M : 0.2s 
- 용량이 커지게 되면 도착시간에 차이는 있으나 속도에는 큰차이가 없는 것을 확인함 

## Q3) 도착하는 데이터를 미처 처리하지 못하면 어떻게 되는가?

1. 과제설명
    - sender_overflow.py receiver_overflow.py sr_overflow.launch
    - 도착하는 데이터를 미처 처리하지 못하면 어떻게 되는지 알아본다. 늦더라도 다 처리하는지, 순서가 뒤섞이는지, 몇몇은 버리는지 확인한다.
    - 받는쪽이 버벅되게 만들어놓고 데이터를 왕창보낸다.
        - 구독자의 콜백함수 안에 시간 많이 걸리는 코드 넣어서 토픽 처리에 시간이 걸리도록 만들어라
    - **콜백함수가 끝나지 않았는데 토픽이 새로 도착하면 어떻게 되나.**
        - 도착한 토픽은 임시로 어딘가에 쌓이는가? 나중에 꺼내서 처리할 수 있는가?
        - 그냥 없어지는가? 한 번 못받은 토픽은 영영 못받는 것인가
        - 발행자는 이 사실을 아는가? 알려줄 수 있는 방법이 있나
    - sender_overflow.py
        - sender이라는 이름으로 노드 생성
        - 발행하는 토픽 이름은 my_topic, 타입은 int32
        - 1초에 1000번씩 숫자를 1씩 증가해서 토픽을 발행
    - receiver_overflow.py
        - receiver이름으로 노드 생성
        - sender로부터 my_topic을 화면에 출력하여 토픽의 누락 여부를 확인
        - 1씩 숫자가 증가하지 않으면 뭔가 문제가 있다는 것을 확인할 수 있다.
    
2. 현상확인을 위한 코드 구현
    
    msg_overflow.launch
    
    ```xml
    <launch>
    	<node pkg='msg_send' type='sender_overflow.py' name='sender' />
    	<node pkg='msg_send' type='receiver_overflow.py' name='receiver' output='screen' />
    </launch>
    ```
    
    sender_overflow.py
    
    ```python
    #!/usr/bin/env python
    
    import rospy
    from std_msgs.msg import Int32
    
    rospy.init_node('sender', anonymous=True)
    
    pub = rospy.Publisher('my_topic', Int32)
    
    rate = rospy.Rate(100000)
    count = 1
    
    while (pub.get_num_connections() == 0):
        continue
    
    while not rospy.is_shutdown():
        pub.publish(count)
        count = count + 1
        rate.sleep()
    ```
    
    receiver_overflow.py
    
    ```python
    #!/usr/bin/env python
    #-*- coding: utf-8-*-
    
    import sys
    import rospy # rospy module
    from std_msgs.msg import Int32
    
    name = 'receiver'
    sub_topic = 'my_topic'
    
    def callback(msg):
    	rospy.loginfo('callback')
    	rospy.sleep(5)
    	print msg.data
        
    rospy.init_node(name, anonymous=True) 
    sub = rospy.Subscriber(sub_topic, Int32, callback) 
    
    rospy.spin()
    ```
    
3. 결과
    - callback 시 데이터가 누락되는 경우가 발생했다.
    
    ![png](./img/3-1.png)
    

## Q4) 주기적 발송에서 타임슬롯을 오버하면 어떻게 되는가?


1. 과제설명
    - 주기적 발송에서 타임슬롯을 오버하면 어떻게 되는가
    - 1초에 5번, rate(5)로 셋팅하고 작업시간이 0.2초가 넘도록 만들자. sleep앞에 들어간 작업코드의 수행시간을 늘려본다.
    - 늘렸다 줄였다를 반복해서 해보자. 입력값을 받아서 이걸 조정할 수 있게 만들면 된다. input을 통해 사용자가 직접 느리게 하든지, 양을 크게 해서 시간을 늘리든지 그 후 중요한 것은 걸린 시간을 출력하는 것이다.
    - 1초에 5번을 지킬 수 없으면 어떻게 작동하는지 보아라
        - 앞에서부터 쭉 밀리는 식으로 일하는지
        - 쉬는 시간을 조정하는지
        - 3번만하고 다음으로 넘어가는지
    - 입력받은 카운트만큼 반복을 진행해서 시간을 계속 늘리도록 한다.
    - 각각의 시작, 끝, 쉬는 시간을 리스트로 묶는다.
2. 현상확인을 위한 코드구현
    
    msg_time.launch
    
    ```jsx
    <launch>
    	<node pkg="msg_send" type="teacher_int32_job.py" name="teacher" output="screen"/>
    	<node pkg="msg_send" type="student_int32.py" name="student" output="screen"/>
    </launch>
    ```
    
    teacher_int32_job.py
    
    ```python
    #!/usr/bin/env python
    
    import rospy
    import timeit
    from std_msgs.msg import Int32
    
    rospy.init_node('teacher')
    pub = rospy.Publisher('msg_to_students', Int32, queue_size = 0)
    
    rate = rospy.Rate(5)
    time = input('input epoch : ')
    
    def do_job(time):
    	for i in range(0,time):
    		i += 1
    		pub.publish(i)
    
    while not rospy.is_shutdown():
    	start_time = timeit.default_timer()	
    	do_job(time)
    	end_time = timeit.default_timer()
    	print 'send time : %.4f sec'%(end_time - start_time)
    	rate.sleep()
    	end_sleeptime = timeit.default_timer()
    	print 'sleep time : %.4f sec'%(end_sleeptime-end_time)
    	total = end_sleeptime - start_time
    	print 'total time : %.4f sec'%(total)
    	print '\n'
    ```
    
    student_int.py
    
3. 결과
    
    time slot의 크기에 작업시간을 모두 완료 하고 남은 slot 만큼 sleep 하는 모습을 볼 수 있었다. 작업시간이 time slot 의 크기보다 크다면 쉬는 시간 없이 일을 지속하는 것으로 보인다.
    
    ![img](./img/4-1.png)
    
    ```jsx
    rate time과 input 횟수를 변경해서 주었다.
    input rate_num : 60
    input time : 10000
    do job time :0.2570 sec
    sleep time:0.0001 sec
    do job time :0.2463 sec
    sleep time:0.0000 sec
    do job time :0.2489 sec
    sleep time:0.0000 sec
    do job time :0.2462 sec
    sleep time:0.0000 sec
    do job time :0.2439 sec
    sleep time:0.0000 sec
    do job time :0.2401 sec
    sleep time:0.0001 sec
    ...
    ...
    ----------------------------
    total time : 15.4424 sec
    ----------------------------
    ```
    

## Q5) 협업 상황에서 노드를 순서대로 기동할 수 있는가?

1. 과제설명
    - 협업해야 하는 노드를 순서대로 가동시킬 수 있나
    - roslaunch로 구현해보고 정 안되면 rosrun으로 진행해보아라
    - first.py second.py third.py fourth.py receiver.py sr_order.launch
    - 순서대로 receiver에 메시지를 보내도록 만든다.
        - receiver는 도착한 순서대로 출력해야 하는데, 이때 first→second→third→fourth가 되어야 한다.
        - 앞에 노드가 움직이기 전에는 절대 토픽을 먼저 보내면 안된다.
    - 어떻게 동기를 맞추고 순서를 맞추는가
        - Launch파일을 이용해서 할 수 있는가, 이게 가장 편리할 듯하다. 이것을 먼저 고민해보라
        - ros의 도움으로 할 수 있나
        - 아니면 내가 프로그래밍 해야 하는가
    - receiver.py 작성
        - 구독해야할 토픽의 이름은 “msg_to_receiver”, 내용은 string,
        - my name is first, my name is second, my name is third, my name is fourth
        - 테스트를 위해 받은 토픽이 순차적으로 오는지 화면에 출력
    - first.py/second.py/third.py/fourth.py
        - 자기 이름에 맞춰서 first, second, third, fourth
        - first노드가 receiver 노드로 최소한 첫 토픽을 보내는 시점 이후에 전송을 시작해야 한다.


2. 현상확인을 위한 코드 구현

```jsx
$ cd ~/xycar_ws/src
$ catkin_create_pkg order_msg std_msgs rospy
```

```
<!-- sr_order.launch --><launch>
	<node name="receiver" pkg="order_test" type="receiver.py" output="screen" />
	<node name="first" pkg="order_test" type="first.py" output="screen" />
	<node name="second" pkg="order_test" type="second.py" output="screen" />
	<node name="third" pkg="order_test" type="third.py" output="screen" />
	<node name="fourth" pkg="order_test" type="fourth.py" output="screen" />
</launch>
```

```
#!/usr/bin/env python

import rospy
from std_msgs.msg import String

name = 'first'

OK = None

def ctl_callback(data):
    global OK
    OK = str(data.data)

rospy.init_node(name)
rospy.Subscriber("start_ctl", String, ctl_callback)

while True:
    if not OK: continue
    d = OK.split(":")
    if (len(d) == 2) and (d[0] == name) and (d[1] == "go"):
        break

pub = rospy.Publisher("msg_to_receiver", String, queue_size=1)

rate = rospy.Rate(2)
hello_str = String()

while not rospy.is_shutdown():
    hello_str.data = "my name is " + name
    pub.publish(hello_str)
    rate.sleep()
```

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import String

name = 'second'

OK = None

def ctl_callback(data):
    global OK
    OK = str(data.data)

rospy.init_node(name)
rospy.Subscriber("start_ctl", String, ctl_callback)

while True:
    if not OK: continue
    d = OK.split(":")
    if (len(d) == 2) and (d[0] == name) and (d[1] == "go"):
        break

pub = rospy.Publisher("msg_to_receiver", String, queue_size=1)

rate = rospy.Rate(2)
hello_str = String()

while not rospy.is_shutdown():
    hello_str.data = "my name is " + name
    pub.publish(hello_str)
    rate.sleep()
```

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import String

name = 'third'

OK = None

def ctl_callback(data):
    global OK
    OK = str(data.data)

rospy.init_node(name)
rospy.Subscriber("start_ctl", String, ctl_callback)

while True:
    if not OK: continue
    d = OK.split(":")
    if (len(d) == 2) and (d[0] == name) and (d[1] == "go"):
        break

pub = rospy.Publisher("msg_to_receiver", String, queue_size=1)

rate = rospy.Rate(2)
hello_str = String()

while not rospy.is_shutdown():
    hello_str.data = "my name is " + name
    pub.publish(hello_str)
    rate.sleep()
```

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import String

name = 'fourth'

OK = None

def ctl_callback(data):
    global OK
    OK = str(data.data)

rospy.init_node(name)
rospy.Subscriber("start_ctl", String, ctl_callback)

while True:
    if not OK: continue
    d = OK.split(":")
    if (len(d) == 2) and (d[0] == name) and (d[1] == "go"):
        break

pub = rospy.Publisher("msg_to_receiver", String, queue_size=1)

rate = rospy.Rate(2)
hello_str = String()

while not rospy.is_shutdown():
    hello_str.data = "my name is " + name
    pub.publish(hello_str)
    rate.sleep()
```

```python
#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(msg):
	rospy.loginfo("I heard %s", msg.data)

rospy.init_node('receiver')
rospy.Subscriber('msg_to_receiver',String, callback)
pub = rospy.Publisher('start_ctl',String,queue_size=1)

rate = rospy.Rate(10)
hello_str = String()

rospy.sleep(1)

sq = ['first','second','third','fourth']
pub_msg = String()

for i in sq:
	pub_msg.data = i+":go"
	pub.publish(pub_msg)
	rospy.sleep(3)

rospy.spin()
```

3. 해결책 적용결과 정리


![png](./img/5-1.png)
![png](./img/5-2.png)

