def coordgen(x,y):
    for a in range(x):
        for b in range(y):
            yield a,b


def countergen():
    i = 0
    while True:
        yield i
        i += 1


def adjacentpixels(x,y,t=1):
    for a in range(y-t,y+t+1):
        for b in range(x-abs(a), x+abs(a)+1):
            yield a,b
