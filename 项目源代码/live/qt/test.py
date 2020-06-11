
def get_rtmp_name():
    f = open('prop.txt', 'r',encoding='utf-8')
    a = f.read().split('\n')

    return a[0]

def get_video_name():
    f = open('prop.txt', 'r',encoding='utf-8')
    a = f.read().split('\n')
    return a[1]
def get_audio_name():
    f = open('prop.txt', 'r',encoding='utf-8')
    a = f.read().split('\n')
    return a[2]

print(get_rtmp_name()+get_audio_name()+get_video_name())
print()
print()