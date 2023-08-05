import re

def type_extraction(targettxt, n=1):
    p = re.compile('^(.+)[.](.+)')
    m = p.match(targettxt)

    if(m !=None):
        targettxt = m.group(2)
    else :
        targettxt = 'unknown'

    #print(m.pos)

    #targettxt = m.group(2)

    return targettxt





#print(type_extraction('테스트파일의이름이다.mp4'))
print(type_extraction('쏜애플 (THORNAPPLE) - 행복한 나를 (Happy Me) (Prod. by 박근태 (Park Keuntae)) MV.m4a'))
#youtube_url = 'https://www.youtube.com/watch?v=k5nLRFoZQTY'

def to_any():
    youtube_url='http://youtu.be/5Y6HSHwhVlY'

    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(youtube_url)

    if not match:
        print('no match')
    print(match.group('id'))


