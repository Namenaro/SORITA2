import random
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy as np
import torchvision.datasets as datasets
from random import choice

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other.x == self.x and other.y==self.y:
            return True
        return False

    def __str__(self):
        return "x="+str(self.x) + ",y=" + str(self.y)

    def __hash__(self):
        return hash(str(self))

def get_backward_dir(dir):
    bdir = Point(0,0)
    if dir.x!=0:
        bdir.x=-dir.x
    if dir.y!=0:
        bdir.y=-dir.y
    return bdir

def get_omni():
    ominset = datasets.Omniglot(root='./data_om', download=True, transform=None)
    return ominset

def get_omni_pics():
    ominset = get_omni()
    class_num =32 #F=45, две закорюки и точка = 56, мсамый простой значок = 9, 29 и 32
    res = []
    for i in range(len(ominset)):
        if class_num == ominset[i][1]:
            res.append(ominset[i][0])
    return res

def get_pic(n=0):
    pics = get_omni_pics()
    pic = np.array(pics[n])
    return pic

def sense(point, picture): #hist on omni pic ={255: 0.9264399092970521, 0: 0.07356009070294785}
    xlen=picture.shape[1]
    ylen=picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if val == 0:
            return True
    return False

def sense_1(point, picture):
    xlen=picture.shape[1]
    ylen=picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if val >0:
            return True
    return False


class CoordSelector:
    def __init__(self, image):
        self.image = image
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.points_facts_dict = {}
        self.start_point = None


    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        x = math.ceil(event.xdata)
        y = math.ceil(event.ydata)

        plt.scatter(x, y, s=100, c='red', marker='o', alpha=0.4)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        point = Point(x,y)
        if self.start_point is None:
            self.start_point = point
        self.points_facts_dict[point] = sense(point,self.image)


    def create_device(self):
        plt.imshow(self.image, cmap='gray_r')
        plt.show()
        return self.points_facts_dict, self.start_point


def get_points_facts_dict(pic):
    devcr = CoordSelector(pic)
    abs_points_facts_dict, abs_start_point = devcr.create_device()
    points_facts_dict={}
    for abspoint, fact in abs_points_facts_dict.items():
        point = Point(abspoint.x-abs_start_point.x, abspoint.y-abs_start_point.y)
        points_facts_dict[point]= fact
    return points_facts_dict

def find_start_point(picture):
    Xmax = picture.shape[1]
    Ymax = picture.shape[0]
    while True:
        point = Point(random.randrange(Xmax), random.randrange(Ymax))
        if sense(point, picture):
            print ("start_point = "+ str(point))
            return point