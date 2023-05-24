'''
@기능
    src의 뒤에 dst를 추가하여 하나의 문자열로 만들어준다
@인자
    -src : 합쳐진 문자열의 처음
    -dst : src 뒤에 합쳐질 문자열, list도 가능하다.
@ret
    str :  합쳐진 하나의 문자열 '''
def ConcatStr( src : str , dst : any, seperator :  str = '') -> str :
    ret = []
    ret.append(src)

    if (type(dst) is list) :
        for i in dst : 
            ret.append(str(i))
    else :
        ret.append(str(dst))

    ret = seperator.join(ret)
    return ret
