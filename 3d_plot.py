# Plot 3D
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

cameraLeft = 'left.npy'
CamerRight = 'right.npy'
cnl = 0
cnr = 1
"""
% Define thresholds for channel 1 based on histogram settings
channel1Min = 0.000;
channel1Max = 18.000; R

% Define thresholds for channel 2 based on histogram settings
channel2Min = 7.000;
channel2Max = 65.000; G

% Define thresholds for channel 3 based on histogram settings
channel3Min = 103.000;
channel3Max = 255.000; B

"""
# cmin = np.array([32,102,4])
# cmax = np.array([73,127,26])
cmin = np.array([103, 7, 0])
cmax = np.array([255, 65, 18])

capl = cv2.VideoCapture(cnl)
capr = cv2.VideoCapture(cnr)


def p3d(x1, y1, x2, y2):
    A = list()
    B = list()
    LL = np.load(cameraLeft).tolist()
    LR = np.load(CamerRight).tolist()
    A.append([(LL[0] - x1 * LL[8]), (LL[1] - x1 * LL[9]), (LL[2] - x1 * LL[10])])
    A.append([(LL[4] - y1 * LL[8]), (LL[5] - y1 * LL[9]), (LL[6] - y1 * LL[10])])
    B.append(x1 - LL[3])
    B.append(y1 - LL[7])
    A.append([(LR[0] - x2 * LR[8]), (LR[1] - x2 * LR[9]), (LR[2] - x2 * LR[10])])
    A.append([(LR[4] - y2 * LR[8]), (LR[5] - y2 * LR[9]), (LR[6] - y2 * LR[10])])
    B.append(x2 - LR[3])
    B.append(y2 - LR[7])
    A = np.array(A)
    B = np.array(B)
    X, Y, Z = np.dot(np.dot(A.T, A), np.dot(A.T, B)).flatten()
    print X, Y, Z
    return (X, Y, Z)




fig = plt.figure()
ax = Axes3D(fig)
plt.show(block=False)
X = list()
Y = list()
Z = list()

time =int(raw_input('Enter Time To Record :')*10)
t=0
tt=0
while tt<time:
    t+=1
    tt =t/10
    print 'Time is ' + str(t/10)
    r, imgl = capl.read()
    r, imgr = capr.read()
    r, imgl = capl.read()
    r, imgr = capr.read()
    ok = 0
    thl = cv2.inRange(imgl, cmin, cmax)
    thr = cv2.inRange(imgr, cmin, cmax)
    xyt = cv2.findNonZero(thl)
    sxy = np.sum(xyt, 0);
    nxy = np.size(xyt)
    if nxy > 20:
        yl = round((sxy[0][1] / (nxy / 2)))
        xl = round((sxy[0][0] / (nxy / 2)))
        print 'Left Camera'
        print 'X : ' + str(xl)
        print 'Y : ' + str(yl)
        ok += 1
    xyt = cv2.findNonZero(thr)
    sxy = np.sum(xyt, 0);
    nxy = np.size(xyt)
    if nxy > 20:
        yr = round((sxy[0][1] / (nxy / 2)))
        xr = round((sxy[0][0] / (nxy / 2)))
        print 'Right Camera'
        print 'X : ' + str(xr)
        print 'Y : ' + str(yr)
        ok += 1

        if ok == 2:
            Xi, Yi, Zi = p3d(xl, yl, xr, yr)
            X.append(Xi)
            Y.append(Yi)
            Z.append(Zi)
            ax.scatter3D(np.array(X), np.array(Y), np.array(Z))
            plt.hold()
            plt.pause(0.1)
plt.close(fig)
XX =np.array(X)
YY =np.array(Y)
ZZ =np.array(Z)
np.save('x',XX)
np.save('y',YY)
np.save('z',ZZ)
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter3D(XX,YY,ZZ)
plt.show(block=False)
while True:
    pass
