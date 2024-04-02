

import polarAC_utils as pAC

def sort_CW(points):
    """
    Takes a pointcloud and sorts it in clockwise order, starting with a top point
    Input: a list of points where each point is a tuple
    Output: The same list of points, sorted in CCW order
    """
    points_copy = points
    x_only, y_only = [x for x, y in points], [y for x, y in points]
    sorta = []
    max_y = max(y_only)
    # select point at top of point cloud
    sorta.append([x for x in points if x[1] == max_y][0]) # add point with maximum y coordinate, as tuple, to sorta
    points_copy.remove(sorta[0]) # remove max y point from points list
    p1, p2 = pAC.return_two_closest(sorta[0], points_copy)
    if p1[0]<p2[0]:   # if p1 is the leftmost point
        sorta.append(p1) # add it to sorta
        sorta.append(p2)
    else:
        sorta.append(p2)
        sorta.append(p1)
    points_copy.remove(p1)
    points_copy.remove(p2)
    # Iterate through each point
    while len(points_copy) > 0:
        p1 = pAC.return_closest(sorta[len(sorta)-1], points_copy)
        sorta.append(p1)
        points_copy.remove(p1)
    return sorta