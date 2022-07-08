import matplotlib.pyplot as plt

from utils import *
from find_seq1 import *
from seq_utils import *

class Seq2:
    def __init__(self, name, seq1, num_steps, mean_u, u_err_max):
        self.seq1 = seq1
        self.name = name
        self.num_steps = num_steps
        self.mean_u = mean_u
        self.u_err_max = u_err_max

    def print(self):
        st = str(self)
        print(st)

    def _get_u(self):
        return Point(int(self.mean_u.x), int(self.mean_u.y))

    def __str__(self):
        st = self.name + "["+ str(self.seq1) +"]x"+str(self.num_steps) + " by u="+str(self.mean_u)
        return st

class RunResult2:
    def __init__(self, name, point):
        self.name = name
        self.point = point
        self.points_1 = []
        self.points_2 = []
        self.errors = []

def list_of_points_to_seq_obj(name, seq1, points_list):
    mean_u = get_mean_u(points_list)
    u_err_max = mean_u.x + mean_u.y
    seq2 = Seq2(name=name, seq1=seq1, num_steps=len(points_list), mean_u=mean_u, u_err_max=u_err_max)
    return seq2

def find_seq2_on_pic(pic, seq2):
    seq2rezs = []
    # создать бинарную картинку сек1
    # -----создать рез

    # выбираем слусайную точку 1
    # из нее в обе стороны растим сек 2, заполняя рез с ошибками
    # когда она выращена, удяляем с карты все точки типа 2, вошедшие в змейку
    # и повторяем код -----
    return seq2rezs

def show_rezs2_on_pic(pic, seq2rezs , ax):
    pass

def GROW_2SEQ():
    pic = get_pic()
    seq1 = Seq1(name="ver", num_steps=5, direct=Point(x=0, y=-1))

    new_img = apply_seq1_to_pic(pic, seq1)
    plt.figure()
    cm = plt.get_cmap('seismic')
    plt.imshow(new_img, cmap=cm, vmin=0, vmax=1)
    plt.show()

    start_point = get_random_event_coord(new_img)
    points_list = try_grow_seq_of_points(start_point, new_img, max_rad=4)
    print(points_list)
    if len(points_list) < 3:
        print("too short!")
        return None

    seq2 = list_of_points_to_seq_obj("cat2", seq1, points_list)
    seq2.print()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, sharey=True)
    ax1.imshow(pic, cmap='gray_r')
    for point in points_list:
        ax1.scatter(point.x, point.y, s=100, c='green', marker='o', alpha=0.4)

    pic = get_pic(randrange(1, 19))
    ax2.imshow(pic, cmap='gray_r')
    seq2rezs = find_seq2_on_pic(pic, seq2)
    show_rezs2_on_pic(pic, seq2rezs, ax2)


    pic = get_pic(randrange(1, 19))
    ax3.imshow(pic, cmap='gray_r')
    seq2rezs = find_seq2_on_pic(pic, seq2)
    show_rezs2_on_pic(pic, seq2rezs, ax3)

    plt.show()

if __name__ == "__main__":
    GROW_2SEQ()




