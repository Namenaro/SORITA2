from utils import *
from vicinity import *

import numpy as np

def apply_seq1_to_pic(pic, seq1):
    new_pic = np.zeros(pic.shape)
    for x in range(1, pic.shape[1] - 1):
        for y in range(1, pic.shape[0] - 1):
            point = Point(x, y)
            res = seq1.run(point, pic)
            new_pic[y, x] = 0
            if res is not None:
                if res.DONE:
                    new_pic[y, x] = 1
    return new_pic


def get_random_event_coord(event_map):
    Xmax = event_map.shape[1]
    Ymax = event_map.shape[0]
    while True:
        point = Point(random.randrange(Xmax), random.randrange(Ymax))
        if sense_1(point, event_map):
            return point

def _dist(point1, point2):
    dx = abs(point1.x - point2.x)
    dy = abs(point1.y - point2.y)
    return dx+dy

def _find_nearest_1(start_point, new_img, max_rad):
    for r in range(1, max_rad):
        r_points = get_coords_for_radius(start_point, r)
        for point in r_points:
            if sense_1(picture=new_img, point=point):
                return point
    return None


def is_allowed_by_exclusions(prev_point, candidate_point,  exclusions):
    dist = _dist(prev_point, candidate_point)
    for exclusion in exclusions:
        if _dist(exclusion, candidate_point)<dist:
            return False
    return True

def _find_nearest_1_with_exclusions(start_point, new_img, max_rad, exclusions):
    for r in range(0, max_rad):
        r_points = get_coords_for_radius(start_point, r)
        for point in r_points:
            if sense_1(picture=new_img, point=point):
                if is_allowed_by_exclusions(start_point, point, exclusions):
                    return point
    return None

def try_grow_seq_of_points(start_point, new_img, max_rad):
    # возвращает список точек, образующих на карте нечеткую последовательность
    points_found = [start_point]
    print ("strated at: ")
    print (start_point)
    second_p = _find_nearest_1(start_point, new_img, max_rad=max_rad)
    print ("second is:")
    print(second_p)
    if second_p is None:
        print ("grouth failed! max_rad = "+ str(max_rad))
        return None
    u = Point(second_p.x - start_point.x, second_p.y - start_point.y)
    print ("u is:")
    print (u)
    points_found.append(second_p)
    lust_point = second_p
    while True:
        next_expected_point = Point(x=lust_point.x + u.x, y=lust_point.y + u.y)
        next_real_point = _find_nearest_1_with_exclusions(next_expected_point, new_img, max_rad, points_found)
        if next_real_point is None:
            break
        points_found.append(next_real_point)
        lust_point = next_real_point
    #обратный проход
    u = get_backward_dir(u)
    lust_point = points_found[0]
    while True:
        next_expected_point = Point(x=lust_point.x + u.x, y=lust_point.y + u.y)
        next_real_point = _find_nearest_1_with_exclusions(next_expected_point, new_img, max_rad, points_found)
        if next_real_point is None:
            break
        points_found.append(next_real_point)
        lust_point = next_real_point
    return points_found


def get_mean_u(points_list):
    n = len(points_list)
    dx = 0
    dy = 0
    prev_point = points_list[0]
    for i in range(1, len(points_list)):
        dx += abs(points_list[i].x - prev_point.x)
        dy += abs(points_list[i].y - prev_point.y)
        prev_point = points_list[i]

    return Point(x=dx/n, y=dy/n)


