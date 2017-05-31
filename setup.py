# To Set Up Camera

import cv2
import easygui
import matplotlib.pyplot as plt
import numpy as np
def onpress(event):
    plt.close(fig)
    A = list()
    B = list()
    for i in range(len(coords)):
        x = coords[i][0]
        y = coords[i][1]
        X = coords[i][2]
        Y = coords[i][3]
        Z = coords[i][4]
        A.append([X,Y,Z,1,0,0,0,0,-x*X,-x*Y,-x*Z])
        A.append([0,0,0,0,X,Y,Z,1,-y*X,-y*Y,-y*Z])
        B.append(x)
        B.append(y)
    AA = np.array(A)
    BB = np.array(B)
    L = np.dot(np.dot(AA.T,AA),np.dot(AA.T,BB))
    print L.shape
    print type(L)
    np.save(fname,L)
def onclick(event):
    global ix, iy,E,N
    ix, iy = event.xdata, event.ydata
    ax.plot(ix, iy, 'r+')
    [E,N,Z]=easygui.multenterbox('Enter Point Coordinates ','Coordinates',['X :','Y :','Z :'],[0,0,0])
    print str(ix)+'  ' +str(iy) +'      '+str(E)+'      '+ str(N) +'     '+str(Z)
    coords.append([ix, iy,float(E),float(N),float(Z)])
    print
    return coords
def cam(name,cn):
    global fname
    fname =name
    global coords
    coords =list()
    cap =cv2.VideoCapture(cn)
    for i in range(20):
        r,img =cap.read()


    global fig
    fig = plt.figure()
    global ax
    ax = fig.add_subplot(111)
    img = img+50;
    ax.imshow(img,cmap='gray')
    fig.show()
    fig.hold()
    for i in xrange(0, 1):
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        cid2 = fig.canvas.mpl_connect('key_press_event', onpress)
    plt.show()

cam('left',0)
cam('right',1)
