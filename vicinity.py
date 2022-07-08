from utils import *

def get_coords_for_radius(center, radius):
    #|x|+|y|=radius ->  |y|=radius-|x|
    # x>0  -> y1 = radius-|x|
    if radius == 0:
        return [Point(center.x, center.y)]

    points = []
    for modx in range(0, radius+1):
        mody = radius - modx
        # x>0
        if modx != 0 and mody != 0:
            points.append(Point(modx + center.x, mody + center.y))
            points.append(Point(-modx + center.x, mody + center.y))
            points.append(Point(modx + center.x, -mody + center.y))
            points.append(Point(-modx + center.x, -mody + center.y))

        if modx == 0 and mody != 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(modx + center.x, -mody + center.y))

        if modx != 0 and mody == 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(-modx + center.x, mody + center.y))
    return points


def get_coords_less_or_eq_raduis(center, radius):
    points = []
    for r in range(0, radius+1):
        r_points = get_coords_for_radius(center.x, center.y, r)
        points = points + r_points
    return points