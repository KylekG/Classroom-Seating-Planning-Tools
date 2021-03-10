import cv2
import json
import menu_drawer as cpmenu
import general as cpg
from shapely.geometry import Polygon, Point

WINDOW_NAME = "Seating Planner"
DOT_SIZE = 1

NOT_SET = False

def __set_window_size_properties(floor_img, screen_height, screen_width):
    """A helper function used to set some properties of the window based off of
    the size provided through screen_height and screen_width when compared to
    the size of the image.


    Keyword arguments:

    floor_img -- The image of the room diagram (loaded through cv2).

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    if floor_img.shape[0] > screen_height:
        height = floor_img.shape[0]
        window_height = screen_height
    else:
        height = screen_height
        window_height = floor_img.shape[0] - 1
    if floor_img.shape[1] > screen_width:
        width = floor_img.shape[1]
        window_width = screen_width
    else:
        width = screen_width
        window_width = floor_img.shape[1] - 1
    return height, window_height, width, window_width

def launch_classroom_planner(screen_height, screen_width, room_type, floor,
                             json_load_name, load_from_json, save_to_json,
                             json_save_name, scale_units_length,
                             units_to_distance, scale_orientation, chair_scale,
                             solution_name, sol_dpi, finding_threshold,
                             show_instr):
    """The launching function for the classroom planning tool. Launches the
    classroom planner configured around the keyword arguments provided.


    Keyword Arguments:

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    room_type -- The type of room being solved. (Currently not functional.)

    floor -- The name of the image file containing the room diagram.

    save_to_json -- Whether or not to save data to json (currently not
    functional).

    json_save_name -- The filename to use when saving the data to json.

    scale_units_length -- How many units (feet meters e.t.c.) long the room
    diagram's scale is. Must be an int or a float.

    units_to_distance -- How many units (same units as scale_units_length) to
    distance seats within the room by. Must be an int or float.

    scale_orientation -- the orientation of the room diagram's scale. Must be
    either the string value "Horizontal" or "Vertical".

    chair_scale -- The amount (int) to scale each chair orientation up by when
    making the chair shape inputs.

    solution_name -- The filename (string) to use when writing the solution
    diagram.

    solution_dpi -- The dpi (int) to use when writing the solution diagram.

    finding_threshold -- The finding_threshold for the recognition process.
    A float with a minimum of 0 and maximum of 1. Higher values will result in
    less chairs  being placed. At 1, no chairs will be identified, but
    finding_threshold that are too low will result in erroneous chair
    placements.

    show_instr -- A bool representing whether or not to show instructions.
    """
    floor_img = cv2.imread(floor, cv2.IMREAD_UNCHANGED)
    room_info = cpg.RoomInfo()

    (height, window_height,
     width, window_width) = __set_window_size_properties(floor_img,
                                                         screen_height,
                                                         screen_width)

    non_writable_img = cv2.imread(floor)

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(WINDOW_NAME, window_width, window_height)

    cpmenu.main_menu(screen_height, screen_width, room_type, room_info,
                     save_to_json, json_save_name, scale_units_length,
                     units_to_distance, scale_orientation, chair_scale,
                     solution_name, sol_dpi, finding_threshold, show_instr,
                     WINDOW_NAME, DOT_SIZE, height, width, non_writable_img)
