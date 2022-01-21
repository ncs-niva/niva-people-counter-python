# The following functions are for defining the counting line or ROI, as well as to determined whether the line or ROI
# has been passed.

def get_counting_line(line_orientation, frame_width, frame_height, line_position):
    """
    To return the coords of the counting line by the line position and the frame width and height.
    :param line_orientation: the string of the orientation of the line.need to be top, bottom, left, right. example- if right - the right side it the outside.
    :param frame_width: the width of the frame
    :param frame_height: the height of the frame
    :param line_position: the position of the line in the frame (flout number)
    :return: the coordinates list of the area.
    """
    line_orientations_list = ['top', 'bottom', 'left', 'right']
    if line_orientation not in line_orientations_list:
        raise Exception('Invalid line position specified (options: top, bottom, left, right)')

    if line_orientation == 'top':
        counting_line_y = round(line_position * frame_height)
        return [(0, counting_line_y), (frame_width, counting_line_y)]
    elif line_orientation == 'bottom':
        counting_line_y = round(line_position * frame_height)
        return [(0, counting_line_y), (frame_width, counting_line_y)]
    elif line_orientation == 'left':
        counting_line_x = round(line_position * frame_width)
        return [(counting_line_x, 0), (counting_line_x, frame_height)]
    elif line_orientation == 'right':
        counting_line_x = round(line_position * frame_width)
        return [(counting_line_x, 0), (counting_line_x, frame_height)]


def is_counting_line_passed(point, counting_line, line_orientation):
    """
    To check if the point passed the counting line by the x coord if it left/right or y coord if it bottom/top.
    :param point: the object location.
    :param counting_line: the coordinates list of the area.
    :param line_orientation: the string of the orientation of the line.need to be top, bottom, left, right.
    :return: True if the point passed the line , False if the point didnt pass the line.
    """
    if line_orientation == 'top':
        return point[1] < counting_line[0][1]
    elif line_orientation == 'bottom':
        return point[1] > counting_line[0][1]
    elif line_orientation == 'left':
        return point[0] < counting_line[0][0]
    elif line_orientation == 'right':
        return point[0] > counting_line[0][0]


def is_counting_roi_passed(current_point, first_point, roi_polygon, roi_outside, is_enter):
    """
    To check if the point passed the counting roi.
    If the current location in the roi and the first location not in the roi - it passed
    However, if the current location not in the roi and the first location in the roi - it is not passed.
    :param current_point: the point object for the current location
    :param first_point: the point object for the first detected location.
    :param roi_polygon: the polygon object for the counting roi.
    :param roi_outside: True if the roi if the outside.
    :param is_enter: True if we want to check if the person has entered to the roi,
    and false if we want to check if the person has left the roi.
    :return: True if the point has passed the roi , False if the point has not passed the roi.
    """
    if roi_outside ^ is_enter:
        return roi_polygon.contains(current_point) and not roi_polygon.contains(first_point)
    else:
        return roi_polygon.contains(first_point) and not roi_polygon.contains(current_point)
