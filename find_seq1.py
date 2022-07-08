from utils import *
from random import choice, randrange
from copy import  deepcopy

def select_direction():
    left = Point(x=1, y=0)
    right = Point(x=-1, y=0)
    top = Point(x=0, y=1)
    down = Point(x=0, y=-1)
    dir = choice([left, right, top, down])
    return dir




def find_1_seq(start_point, pic):
    if sense(start_point, pic) is False:
        return None

    dir_forward = select_direction()
    dir_backward = get_backward_dir(dir_forward)

    #find nearest non-white
    num_steps_to_nearest_tail = 0
    nextp = Point(start_point.x, start_point.y)
    while True:
        nextp.x += dir_forward.x
        nextp.y += dir_forward.y
        if sense(nextp, pic):
            num_steps_to_nearest_tail+=1
        else:
            break
    # меряем длину змейки
    num_steps = 0
    while True:
        nextp.x += dir_backward.x
        nextp.y += dir_backward.y
        if sense(nextp, pic):
            num_steps+=1
        else:
            break
    return num_steps, dir_backward

class RunResult1:
    def __init__(self, name, point):
        self.name = name
        self.point = point
        self.points = [point]
        self.DONE = True

class Seq1:
    def __init__(self, name, num_steps, direct):
        self.name = name
        self.num_steps = num_steps
        self.direct = direct
        self.trivial_p = (0.07**(num_steps))*(1-0.07)

    def _precheck(self, start_point, pic):
        if sense(start_point, pic) is False:
            return False
        backdir = get_backward_dir(self.direct)
        first_point = Point(start_point.x + backdir.x, start_point.y + backdir.y)
        if sense(first_point, pic):
            return False
        return True

    def run(self, start_point, pic):
        if self._precheck(start_point, pic) is False:
            return None
        res = RunResult1(self.name, start_point)

        nextp = deepcopy(start_point)
        for _ in range(self.num_steps-1):
            nextp.x += self.direct.x
            nextp.y += self.direct.y
            if sense(nextp, pic):
                res.points.append(deepcopy(nextp))
            else:
                res.DONE = False
                break
        return res

    def __str__(self):
        return self.name + "["+str(self.direct)+"]x"+str(self.num_steps)+", p="+str(self.trivial_p)

    def print(self):
        st = str(self)
        print(st)


def show_activations_on_pic(pic, seq1, ax):
    for x in range(1, pic.shape[1]-1):
        for y in range(1, pic.shape[0] - 1):
            point = Point(x,y)
            res=seq1.run(point, pic)
            if res is not None:
                if res.DONE:
                    ax.scatter(res.point.x, res.point.y, s=100, c='red', marker='o', alpha=0.4)

def show_seq(pic, seq, ax):
    for x in range(1, pic.shape[1] - 1):
        for y in range(1, pic.shape[0] - 1):
            point = Point(x, y)
            res = seq.run(point, pic)
            if res is None:
                continue
            if res.DONE:
                for point in res.points:
                    ax.scatter(point.x, point.y, s=100, c='green', marker='o', alpha=0.4)
                return

if __name__ == "__main__":
    pic = get_pic()
    start_point = find_start_point(pic)
    num_steps, dir = find_1_seq(start_point, pic)
    seq = Seq1(name="cat", num_steps=num_steps, direct=dir)

    seq.print()

    fig, (ax1, ax2, ax3) = plt.subplots(1,3, sharex=True, sharey=True)
    ax1.imshow(pic, cmap='gray_r')
    ax1.scatter(start_point.x, start_point.y, s=100, c='red', marker='o', alpha=0.4)
    show_seq(pic, seq, ax1)

    ax2.imshow(pic, cmap='gray_r')
    show_activations_on_pic(pic, seq, ax2)

    pic = get_pic(randrange(1,19))
    ax3.imshow(pic, cmap='gray_r')
    show_activations_on_pic(pic, seq, ax3)



    fig.suptitle('find seq')
    plt.show()







