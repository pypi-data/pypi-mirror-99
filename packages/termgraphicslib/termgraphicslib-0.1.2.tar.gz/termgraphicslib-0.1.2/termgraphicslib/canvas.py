import math
clear = lambda: print('\033[2J') #do i even use this in the code anywhere? lol
def interpolate(i0,d0,i1,d1):
    if i0 == i1:
        return [d0]
    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0,i1):
        values.append(d)
        d = d + a
    return values
def init_canvas(x,y):
    #this function doesnt work? will look into it
    tmp = []
    canvas = []
    for i in range(0,x):
        tmp.append(' ')
    for i in range(0,y):
        canvas.append(tmp)
    print(canvas)
    return canvas
def init_default_canvas():
    return [[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]]
def putpixel(x,y,color,canvas=init_default_canvas()):
    #TODO: replicate co-ord (and color) system from the book, but this is easier to make for the time being
    '''if color[0] > color[1] and color[0] > color[2]: #red pixel
        char='r'
    elif color[1] > color[0] and color[1] > color[2]: #green pixel
        char='g'
    elif color[2] > color[0] and color[2] > color[1]: #blue pixel
        char = 'b'
    else:
        raise ValueError('Color not found!')
    #print(y,x)'''
    try:
        canvas[y][x] = color
    except:
        print('error in plotting pixel, continuing anyway')
    return canvas

def draw(canvas):
    for y in canvas:
        for i in y:
            if i == ' ':
                print(i,end='')
            else:
                #print(colored('█', '{}'.format(rgb_to_name(tuple(i)))), end='')
                print('\033[38;2;{};{};{}m█'.format(i[0], i[1], i[2]),end='')
        #time.sleep(0.5)
        print('\033[38;2;255;255;255m')
'''def draw_turtle(canvas):
    turtle.goto(0,0)
    turtle.pensize(5)
    yi=0
    for y in canvas:
        turtle.sety(yi)
        turtle.setx(0)
        for i in y:
            turtle.forward(1)
            if i == ' ':
                pass
            else:
                turtle.color(rgb_to_name(tuple(i)))
        yi-=1'''
def drawline(P0, P1, color, canvas=init_default_canvas()):
    #code not from book to define the Ys and Xs
    x1=P0[0]
    y1=P0[1]
    x2=P1[0]
    y2=P1[1]
    dx = (x2 - x1)
    dy = (y2 - y1)
    #print(dx,dy)
    if abs(dx) >= abs(dy):
        step = abs(dx)
    else:
        step = abs(dy)
    print(step)
    dx = dx / step
    dy = dy / step
    x = x1
    y = y1
    i = 1
    while i <= step:
        canvas = putpixel(int(x), int(y), color,canvas=canvas)
        x = x + dx
        y = y + dy
        i = i + 1
    return canvas
def line_coords(P0,P1):
    x1=P0[0]
    y1=P0[1]
    x2=P1[0]
    y2=P1[1]
    dx = (x2 - x1)
    dy = (y2 - y1)
    if abs(dx) >= abs(dy):
        step = abs(dx)
    else:
        step = abs(dy)
    dx = dx / step
    dy = dy / step
    x = x1
    y = y1
    i = 1
    coords=[]
    while i <= step:
        coords.append([int(x),int(y)])
        x = x + dx
        y = y + dy
        i = i + 1
    return coords
def drawtri_wire(p0,p1,p2,color,canvas=init_default_canvas()):
    canvas = drawline(p0,p1,color,canvas=canvas)
    print('1s')
    canvas = drawline(p1,p2,color,canvas=canvas)
    print('2s')
    canvas = drawline(p2,p0,color,canvas=canvas)
    print('3s')
    return canvas
def drawtri_fill(p0,p1,p2,color,canvas=init_default_canvas()):
    x1=p0[0]
    y1=p0[1]
    x2=p1[0]
    y2=p1[1]
    x3=p2[0]
    y3=p2[1]
    line1=line_coords([x1,y1],[x2,y2])
    line2=line_coords([x1,y1],[x3,y3])
    line3=line_coords([x2,y2],[x3,y3])
    print(line1,line2,line3)
    for i in line2:
        canvas = drawline(line1[1],i,color,canvas=canvas)
        canvas = drawline(line3[1],i,color,canvas=canvas)
    for i in line1:
        canvas = drawline(line2[1],i,color,canvas=canvas)
        canvas = drawline(line3[1],i,color,canvas=canvas)
    for i in line3:
        canvas = drawline(line2[1],i,color,canvas=canvas)
        canvas = drawline(line1[1],i,color,canvas=canvas)
    if line2[0] == [0,0] and line1[0] == [0,0]:
        canvas = putpixel(0,0,color,canvas=canvas)
    return canvas
if __name__ == '__main__':
    print("executing test...")
    #put testing code down here
    #srn = drawtri_fill([0,0],[7,15],[7,1],[255,0,0])
    #srn = init_canvas(15,30)
    srn = drawtri_fill([0,0],[7,15],[30,1],[255,0,0])
    srn = drawline([1,1],[24,2],[255,0,255],canvas=srn)
    #print(srn)
    #print('1s')
    #draw(srn)
    srn = drawline([15,13],[3,5],[0,255,255],canvas=srn)
    #print('2s')
    #draw(srn)
    srn = drawline([15,5],[15,9],[255,255,0],canvas=srn)
    #print('3s')
    #draw(srn)
    #srn = drawtri_wire([0,0],[7,15],[30,1],[0,255,0],canvas=srn)
    draw(srn)
    #srn = drawtri_wire([0,0],[7,15],[7,1],[0,255,0],canvas=srn)
    #draw_turtle(srn)
