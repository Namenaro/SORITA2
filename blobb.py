from utils import *

class Blob:
    def __init__(self, name):
        self.name=name
        self.points_facts_dict = {}


    def check(self, pic, abs_point):
        # в данной точке изображения смотрим, имеется ли такой-то блоб
        for point, fact in self.points_facts_dict.items():
            abs_p = Point(point.x+abs_point.x, point.y+abs_point.y)
            res = sense(abs_p, pic)
            if res != fact:
                return False
        return True

    def init_handly(self, pic):
         self.points_facts_dict = get_points_facts_dict(pic)

    def show_on_pic(self, pic):
        fig, ax = plt.subplots()
        plt.imshow(pic, cmap='gray_r')
        for x in range(pic.shape[1]):
            for y in range(pic.shape[0]):
                point = Point(x, y)
                res = self.check(pic, point)
                if res:
                    ax.plot(point.x, point.y, marker='o', markerfacecolor='green', color='green',
                        linewidth=4, alpha=0.3)
        plt.show()



if __name__ == "__main__":
    pic = get_pic()
    bl = Blob('test')
    bl.init_handly(pic)
    bl.show_on_pic(pic)
