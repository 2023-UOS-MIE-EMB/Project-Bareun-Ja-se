
'''
@기능
    모터를 일정시간동안 회전시킴. 인자의 부호에 따라 방향을 선택한다.
@변수
    time : 모터를 동작시킬 시간
@리턴
    bool : 성공적인 동작이면 true, 아니면 false
'''
def ControllingMotorWithTime( time : int  ) -> bool :
    print("Motor Worked during : " , time)
    return True
