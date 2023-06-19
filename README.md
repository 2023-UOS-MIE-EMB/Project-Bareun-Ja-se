# Project-Bareun-Ja-se
University of Seoul, Mechanical Information Engineering, Embeded System Final Project
==========================
# 1. 프로젝트 소개

## 1.1. 프로젝트 명
###  **바른자세**<br>
[Capstone UOS 사이트](https://capstone.uos.ac.kr/mie/index.php/%EB%B0%94%EB%A5%B8_%EC%83%9D%EA%B0%81_-_%EB%B0%94%EB%A5%B8_%EC%9E%90%EC%84%B8)<br>

## 1.2. 프로젝트 기간
📅 2023.03.31 ~ 2023.06.15 

## 1.3. 팀 소개
### 팀명 : 바른생각
| 학교 | 학과 | 학번 | 이름 | 역할 |
|:---:|:---:|:---:|:---:|:---:|
| 서울시립대 | 기계정보공학과 | 20174300** | 정* (팀장) | 서버 |
| 서울시립대 | 기계정보공학과 | 20184300** | 김*준 | 서버 |
| 서울시립대 | 기계정보공학과 | 20184300** | 김*현 | 클라이언트 | 
| 서울시립대 | 기계정보공학과 | 20184300** | 권*표 | 클라이언트 | 

<img src="https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/e2c7619a-f202-4725-a778-65f0a5774f90" alt="단체사진" width="450px"><br>
--------------------------
서버 & 클라이언트 설계 설명 링크:arrow_lower_left:<br>
:computer: [RaspberryPi Server]((#4-서버-설계-및-구현))<br> 
&nbsp;:iphone:   [Android App Client](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/blob/APP_Client/README.md)

--------------------------
# 2.	프로젝트 개요
## 2.1	프로젝트 설명
&nbsp;본 프로젝트는 장시간의 집중시간을 편안한 자세로서 사용자에게 제공하는 것을 목표로 한다. 프로젝트는 모터를 통해 높이가 조절 되는 거치대를 기본으로 구성이 되어 있다. 이를 통해 사용자의 목과 팔꿈치의 부담을 줄이도록 해준다. 카메라를 통한 얼굴인식과 이를 이용한 알람 기능으로 사용자의 비집중 시간을 감지하여 알림을 제공한다. 프로젝트는 하드웨어를 제어하는 라즈베리파이 서버와 사용자의 입력을 기반으로 요청을 보내는 안드로이드 앱(클라이언트)으로 구성되어 있다. 서버와 클라이언트는 WiFi를 통해 1:1 TCP/IP통신을 한다.
 사용자는 안드로이드 앱을 통해 높이 조절, 알람 시간 설정, 알람 모드 설정, 현재 촬영되는 영상 확인의 기능을 서버에게 요청할 수 있다. 또한 자신이 주로 사용하는 설정을 프로필을 만들어 저장하고, 불러올 수 있다.
 서버는 클라이언트로부터 받은 요청을 바탕으로 하드웨어 제어를 하며 기능을 수행한다. 높이 조절 기능은 사용자가 요청한 높이로 모터를 제어하여 사용자가 요청한 높이로 거치대를 조절한다. 알람 기능을 사용자가 설정한 경우에는 카메라를 통해 사용자의 얼굴을 인식한다. 이 때 사용자의 얼굴이 인식되지 않으면, 사용자가 현재 집중을 하지 않고 있다고 판단하여, 시간을 측정한다. 측정한 시간이 알람 설정 시간이상이 되면 사용자가 요청한 알람 모드(소리, 진동)에 따라 알람을 제공한다. 사용자의 얼굴이 측정되지 않을 때는 LED 인디케이터를 통해 사용자에게 시작적인 알람을 제공한다. 이 때 사용자는 실제로 집중하고 있음에도 얼굴 인식이 되지 않고 있는 경우에는 자세를 바르게 하거나, 카메라 각도를 조절할 수 있게 된다. 서버는 사용자가 추가적인 요청을 보내면 현재 촬영 영상을 특정 웹주소를 통해 스트리밍한다.

## 2.2	배경 및 기대효과
&nbsp;현대에 이르러서는 근무 시간, 여가시간 등 다양한 이유로 장시간 책상을 이용하는 인원들이 증가하고 있다. 현재의 책상 이용 자세의 경우 머리와 목의 각도, 상완 외전 및 들어올림, 손목의 구부러짐과 신전 등 신체의 기능 구현에 있어 인체에 부담을 주고 있다. 그로 인해 VDT(Video Display Terminal)라 불리는 근골격계 질환을 겪는 현대인이 증가하고 있다.
 책상에 앉아 장시간 업무를 진행 할 때 신체에 부담을 주는 자세를 개선하고 높은 집중 시간을 유지하는 데 도움이 되는 기구를 개발한다. 앱으로 사용자가 원하는 각도를 세밀하게 조정할 수 있고, 졸음 인식 기능과 알람 기능을 삽입하여 신체의 부담을 줄이고 효율성을 높인다.

## 2.3  사용자 시나리오
 ![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/b78ae144-5aee-4338-a127-c53465e15b04)


# 3. 시스템 구성

![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/b7fa33be-ea2b-4e97-a2c8-6969fecbf431)
<br>
&nbsp;본 시스템의 설계 구성도는 위와 같다. 클라이언트와 서버는 WiFi환경을 기반으로 TCP/IP 통신을 진행한다. 클라이언트의 요청을 서버는 연결된 기기를 제어하여 처리한다. 카메라를 통해 사용자 얼굴을 인식하여 비집중 감지, 영상 스트리밍 등의 기능을 수행한다. 사용자의 요청을 처리함에 따라 필요한 하드웨어 출력 장치를 선택하여 제어한다. 

==============================
# 4. 서버(RaspberryPi) 설계 및 구현 
![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/2227daba-5428-4a44-a270-adb3db47703a)<br>
 서버 시스템은 WiFi연결과 Listening Socket 생성을 하는  ‘서버 Listen' 단계와 클라이언트의 요청을 처리하는 ’요청 처리‘ 두 부분으로 나뉜다.
## 4.1 서버 Listen
 Ubuntu NetworkManger 패키지를 이용하여 사전에 정의된 WiFi에 연결한다. 이후 TCP 서버 소켓을 만들고 클라이언트의 접속을 기다린다.
## 4.2 요청 처리
클라이언트의 요청이 담긴 패킷을 받고, 이를 파싱하여 그에 따른 동작을 하는 과정이다. 서버는 클라이언트에게 이하 4가지 (모터 제어/비집중 시간 감지 및 알람/영상 스트리밍/전원 제어)기능을 제공한다.
## 4.3 모터 제어 프로세스
![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/e53b66e5-a5e9-4747-9529-8ca6c05e36a8)<br>
 모터 제어 프로세스는 사용자의 목표 단계가 담긴 queue를 받아, 이를 비울 때까지 모터를 제어하여 처리하는 동작을 한다. 서버는 사용자의 요청을 즉시 실행할 수 없을 때는 queue에 담고, 실행 가능할 때 queue를 복사하여 위의 모터 제어 동작을 하는 프로세스를 생성한다. 
 그러나 서버의 패킷 파싱 이후 모터 제어 프로세스 생성 유무를 결정하기 때문에, 기존의 모터 제어 프로세스가 종료 후, 새로운 요청이 도착해야만 queue에 담긴 요청이 실행되는 문제가 있다.
## 4.4 비집중 감지 프로세스
![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/12ba95ad-21be-4123-ba2c-0260b02464b8)<br>
 서버는 사용자가 알람 관련 기능을 설정하면, 비집중 감지 프로세스를 생성한다. 감지 프로세스는 사용자가 얼굴이 인식되지 않는 상황을 비집중 시간이라고 판단한다. 비집중이 인식되면 LED를 통해 경고한다. 측정 결과에 따라 ’집중‘, ’비집중‘ 두가지 상태로 구분한다. 바로 전 프레임의 상태를 저장하고, 이를 현 프레임과 비교한다. 만약 상태가 달라지면 달라지는 시점을 저장한다. 이후 가장 최근에 기록한 시점으로부터 경과한 시간이 알람 시간보다 크고, 현재 상태가 ’비집중 상태‘라면 알람 모드에 따라 알람을 울린다.  	

![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/1838469e-7740-4536-93b7-c792cde87afe)<br>
 비집중 감지 프로세서는 LED, 스피커, 부저 의 제어가 필요하다. 해당 하드웨어는 라즈베리 파이의 GPIO제어를 이용해 울리게 된다. 각 제어는 ON/OFF를 설정하는 방식이다.

## 4.5 영상 스트리밍
![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/622daaae-b9ca-4052-aa10-68e7d80c69bc)<br>
사용자의 얼굴 인식 결과 영상을 특정 웹주소를 통해 Mjpeg over HTTP 방식으로 계속해서 스트리밍 한다. Flask 프레임 워크를 이용하여 구현했다. 해당 기능을 python을 통해 실행하는데, 이때 rasberry Pi 프로세스에게 큰 부하가 발생한다. 따라서 10분 이상 동작하면 프로세스의 쓰로틀링을 유발하고, 서버의 처리 속도가 매우 늦어지거나 혹은 라즈베리 파이가 종료 될 수 있는 문제점이 있다.
## 	4.6 전원 제어
![image](https://github.com/2023-UOS-MIE-EMB/Project-Bareun-Ja-se/assets/83463280/68acda19-b587-4f55-962c-03970bf44f5e)<br>
 자원 회수 이후 OS의 종료기능을 이용하여 라즈베리 파이를 종료시킨다. 처음으로 소켓을 모두 닫는다. 이후 모터 제어를 통해 기기 상태를 초기화 한다. 이후 초기화가 끝나면 프로세스를 차례로 종료 시킨 후, Process 객체를 반환한다. 이후 공유 메모리 공간을 반환한다. 자원회수가 끝난 후에는 OS 명령어를 이용해 라즈베리파이를 종료시킨다. 따라서 라즈베리파이가 아닌 독립적으로 전력을 공급받는 모터와 모터 드라이버는 종료하지 못한다는 문제점이 있다.
