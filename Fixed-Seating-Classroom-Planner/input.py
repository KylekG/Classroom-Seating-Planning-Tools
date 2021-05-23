import cv2
import general as cpg
import instructions_drawer as instruct
import numpy as np
from skimage.feature import match_template, peak_local_max
from shapely.geometry import Polygon, Point
import math, itertools, os, shapely
from ortools.linear_solver import pywraplp as OR
import matplotlib.pyplot as plt

DOT_SIZE = 1

class TempData():
    """A class used to pass information to the click callbacks used by the
    input functions to get information from user interactions with the cv2
    windows.


    Instance Variables:

    ref -- A list used to store data on clicked points in the form of
    (int, int) tuples.

    ref_temp -- A list used to store data on the location of the mouse in the
    form of (int, int) tuples.

    refresh -- A list used to keep track of whether or not to rfresh the cv2
    window's image.

    chair_scale -- An int used to keep track of how much a chair orientation
    has been scaled up.

    window_name -- The name of the cv2 window the input function is interacting
    with.

    chair_selection -- An int used to keep track of the currently selected
    chair orientation for placement.


    Public Methods:

    set_window_name -- Sets the instance variable window_name to the string
    provided.

    set_chair_scale -- Sets the instance variable window_name to int value
    provided.
    """

    def __init__(self):
        """Initializes an instance of the TempData class.
        """
        self.ref = []
        self.ref_temp = []
        self.refresh = []
        self.chair_scale = None
        self.window_name = None
        self.chair_selection = 0

    def set_window_name(self, window_name):
        """Sets the instance variable window_name to the provided value.


        Keyword Argument:

        window_name -- The string to set the instance variable window_name to.
        """
        assert(isinstance(window_name, str)), "window_name must be a string."
        self.window_name = window_name

    def set_chair_scale(self, chair_scale):
        """Sets the instance variable chair_scale to the provided value.


        Keyword Argument:

        chair_scale -- The int to set the instance variable chair_scale to.
        """
        assert(isinstance(chair_scale, int)), "chair_scale must be an int."
        self.chair_scale = chair_scale


def __trackbar_change(integer):
    """The callback for trackbar change. Currently does nothing."""
    return

def __get_scale_selection_click_coords(event, x, y, flags, temp_dat):
    """The private callback for mouse events in the cv2 window during the Scale
    Selection input section. Adds coords to temp_dat.ref on left mouse click if
    there are less than 2 coords in it. Deletes the latest coord from
    temp_dat.ref on right click. Tracks mouse position on mouse move by adding
    its coords to temp_dat.ref_temp.
    """

    if event == cv2.EVENT_MOUSEMOVE:
        for item in range(len(temp_dat.ref_temp)):
            del temp_dat.ref_temp[-1]
        temp_dat.ref_temp.append((x + cv2.getTrackbarPos("Wscroll",
                                                         temp_dat.window_name),
                                  y + cv2.getTrackbarPos("Hscroll",
                                                         temp_dat.window_name)))
        temp_dat.refresh.append('r')
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(temp_dat.ref) < 2:
            temp_dat.ref.append((x + cv2.getTrackbarPos("Wscroll",
                                                        temp_dat.window_name),
                                 y + cv2.getTrackbarPos("Hscroll",
                                                        temp_dat.window_name)))
            temp_dat.refresh.append('r')
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(temp_dat.ref) > 0:
            del temp_dat.ref[-1]
            temp_dat.refresh.append('r')
def scale_selection(non_writable_img, menu_refresh, window_name,
                    room_info):
    """scale_selection handles the scale selection input section of the room
    solving process. This function provides the user with an easy way of having
    the tool calculate distances within a diagram based off of mouse clicks on
    the provided room diagram. After running the function, the provided window
    will update to show the diagram, and the tool will update room_info._scale
    upon successful completion of the user clicking 2 diagonal corners of the
    room diagram's scale.


    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    window_name -- The name (string) of the cv2 window for the function to use.

    room_info -- The RoomInfo instance being used to keep track of input
    information.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    selected_color = cpg.PURPLE
    temp_color = cpg.GREEN
    orientation = room_info.parameters_dict["scale_orientation"]
    scale_units = room_info.parameters_dict["scale_length_units"]
    distance_units = room_info.parameters_dict["units_to_distance"]

    if show_instr:
        instruct.scale_selection_explanation(window_name, screen_height,
                                             screen_width)

    scroll_height = 0
    scroll_width = 0
    writable_clone = non_writable_img.copy()
    temp_dat = TempData()
    temp_dat.set_window_name(window_name)

    cv2.createTrackbar("Hscroll", window_name, scroll_height,
                       (height - screen_height), __trackbar_change)
    cv2.createTrackbar("Wscroll", window_name, scroll_width,
                       (width - screen_width), __trackbar_change)

    cv2.setMouseCallback(window_name, __get_scale_selection_click_coords,
                         temp_dat)

    while True:
        #These lines are what allow the scrolling
        scroll_height = cv2.getTrackbarPos("Hscroll", window_name)
        scroll_width = cv2.getTrackbarPos("Wscroll", window_name)
        shown_img = np.array([(scroll_width, scroll_height),
                               (scroll_width + width, scroll_height),
                               (scroll_width + width, scroll_height + height),
                               (scroll_width, scroll_height + height)])
        cds = cpg.get_coords(shown_img)
        img = writable_clone[cds[2]:cds[3], cds[0]:cds[1]]
        cv2.imshow(window_name, img)

        #Refreshes the image if there has been an update to it
        if len(temp_dat.refresh) >= 1:
            writable_clone = non_writable_img.copy()
            if len(temp_dat.ref) >= 2:
                for i in range((len(temp_dat.ref)
                                - (len(temp_dat.ref) % 2)) // 2):
                    cv2.rectangle(writable_clone, temp_dat.ref[i * 2],
                                  temp_dat.ref[i * 2 + 1],
                                  selected_color, 1)
            if len(temp_dat.ref) % 2 == 1:
                cv2.rectangle(writable_clone, temp_dat.ref[-1],
                              temp_dat.ref_temp[0], temp_color, 1)
            temp_dat.refresh=[]

        #Listen for key presses
        key = cv2.waitKey(1) & 0xFF

        # if the 'e' key is pressed, break from the loop
        if key == ord("e"):
            if (len(temp_dat.ref) == 2):
                menu_refresh.append('r')
                room_info.set_new_scale(temp_dat.ref[0], temp_dat.ref[1],
                                        distance_units, orientation,
                                        scale_units)
                break

def __get_chair_type_selection_click_coords(event, x, y, flags, temp_dat):
    """The private callback for mouse events in the cv2 window during the Chair
    Type Selection input section. Adds coords to temp_dat.ref on left mouse
    click. Deletes the latest coord from temp_dat.ref on right click.
    Tracks mouse position on mouse move by adding its coords to
    temp_dat.ref_temp.
    """
    if event == cv2.EVENT_MOUSEMOVE:
        for item in range(len(temp_dat.ref_temp)):
            del temp_dat.ref_temp[-1]
        temp_dat.ref_temp.append((x + cv2.getTrackbarPos("Wscroll",
                                                         temp_dat.window_name),
                                  y + cv2.getTrackbarPos("Hscroll",
                                                         temp_dat.window_name)))
        temp_dat.refresh.append('r')
    if event == cv2.EVENT_LBUTTONDOWN:
        temp_dat.ref.append((x + cv2.getTrackbarPos("Wscroll",
                                                    temp_dat.window_name),
                             y + cv2.getTrackbarPos("Hscroll",
                                                    temp_dat.window_name)))
        temp_dat.refresh.append('r')
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(temp_dat.ref) > 0:
            del temp_dat.ref[-1]
            temp_dat.refresh.append('r')
def chair_type_selection(non_writable_img, menu_refresh, window_name,
                         room_info):
    """chair_type_selection handles the chair type selection input section of
    the room solving process. This function provides the user with an easy way
    of supplying the tool  with information on the different chair orientations
    within a diagram based off of mouse clicks on the provided room diagram.
    After running the function, the provided window will update to show the
    room diagram, and the tool will update room_info._chair_types upon
    successful completion of the user clicking 2 diagonal corners of a bounding
    rectangle of each chair orientation within the diagram.


    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    window_name -- The name (string) of the cv2 window for the function to use.

    room_info -- The RoomInfo instance being used to keep track of input
    information.
    """

    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    selected_color = cpg.PURPLE
    temp_color = cpg.GREEN

    if show_instr:
        instruct.chair_type_selection_explanation(window_name, screen_height,
                                                  screen_width)

    scroll_height = 0
    scroll_width = 0
    writable_clone = non_writable_img.copy()
    temp_dat = TempData()
    temp_dat.set_window_name(window_name)

    cv2.createTrackbar("Hscroll", window_name, scroll_height,
                       (height - screen_height), __trackbar_change)
    cv2.createTrackbar("Wscroll", window_name, scroll_width,
                       (width - screen_width), __trackbar_change)

    cv2.setMouseCallback(window_name, __get_chair_type_selection_click_coords,
                         temp_dat)

    while True:

        #These lines are what allow the scrolling
        scroll_height = cv2.getTrackbarPos("Hscroll", window_name)
        scroll_width = cv2.getTrackbarPos("Wscroll", window_name)
        shown_img = np.array([(scroll_width, scroll_height),
                              (scroll_width + width, scroll_height),
                              (scroll_width + width, scroll_height + height),
                              (scroll_width, scroll_height + height)])
        cds = cpg.get_coords(shown_img)
        img = writable_clone[cds[2] : cds[3], cds[0] : cds[1]]
        cv2.imshow(window_name, img)

        #Refreshes the image if there has been an update to it
        if len(temp_dat.refresh) >= 1:
            writable_clone=non_writable_img.copy()
            if len(temp_dat.ref) >= 2:
                for i in range((len(temp_dat.ref) - (len(temp_dat.ref) % 2))
                               // 2):
                    cv2.rectangle(writable_clone, temp_dat.ref[i * 2],
                                  temp_dat.ref[i * 2 + 1],
                                  selected_color, 1)
            if len(temp_dat.ref) % 2 == 1:
                cv2.rectangle(writable_clone, temp_dat.ref[-1],
                              temp_dat.ref_temp[0], temp_color, 1)
            temp_dat.refresh = []

        #Listen for key presses
        key = cv2.waitKey(1) & 0xFF

        # if the 'e' key is pressed, break from the loop
        if key == ord("e"):
            if (len(temp_dat.ref) % 2 == 0):
                menu_refresh.append('r')
                room_info.set_new_chair_types(temp_dat.ref, non_writable_img)
                break

def __polygon_creation_click_coords(event, x, y, flags, temp_dat):
    """The private callback for mouse events in the cv2 window during the
    polygon creation input section. Adds coords to temp_dat.ref on left mouse
    click. Deletes the latest coord from temp_dat.ref on right click. Coords
    added are adapted to match what the coords would be relative to the cut
    section within the original room diagram. This means that the callback
    scales down coords to counteract the scaling up done in polygon_creation.
    """
    if event == cv2.EVENT_LBUTTONDOWN:#If the left mouse button is clicked, add the point (scaled down to the chair's original size) to ref[].
        temp_dat.ref.append((int(x / temp_dat.chair_scale),
                             int(y / temp_dat.chair_scale)))
        temp_dat.refresh.append('r')
    elif event == cv2.EVENT_RBUTTONDOWN:   # right-click to delete the latest point added to ref from the polygon
        del temp_dat.ref[-1]
        temp_dat.refresh.append('r')

def polygon_creation(non_writable_img, menu_refresh, window_name, room_info):
    """polygon_creation handles the polygon creation input section of the room
    solving process. This function provides the user with an easy way
    of defining the physical shape of the chair within each previously
    designated chair orientation. After running the function, the provided
    window will update to show a selected chair orientation. Upon completion of
    the input for the inputs for that orientation, the window will update to
    show the next selected chair orientation. When this is done for all chair
    orientations, the function will set room_info._chair_polys to a list
    containing all of them.


    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    room_info -- The RoomInfo instance being used to keep track of input
    information. Must already have _ChairType instances contained within
    room_info._chair_types.

    window_name -- The name (string) of the cv2 window for the function to use.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    line_color = cpg.RED
    chair_scale = room_info.parameters_dict["chair_scale"]
    dot_size = cpg.DOT_SIZE

    if show_instr:
        instruct.polygon_creation_explanation(window_name, screen_height,
                                              screen_width)
    chair_types = room_info.get_chair_types()
    list_of_chair_polys = []

    for i in range(len(chair_types)):
        chair_type = chair_types[i]
        cds = cpg.get_coords(np.array(chair_type.points))
        template = chair_type.template #template is the subsection of img that contains the chair
        height = len(template) #gets the height of the subsection
        width = len(template[0]) #gets the width of the subsection
        temp_dat = TempData()
        temp_dat.set_chair_scale(chair_scale)
        template = cv2.resize(template, (chair_scale * width,
                                         chair_scale * height))#resizes the image to be 4 times the original size
        template_copy = template.copy()

        cv2.setMouseCallback(window_name, __polygon_creation_click_coords,
                             temp_dat)

        while True:
            cv2.imshow(window_name, template_copy)
            if len(temp_dat.refresh) >= 1:
                template_copy = template.copy()
                points = len(temp_dat.ref)
                if points >= 2:#if there are at least 2 points, adds a line between the latest created point and the previous point.
                #this allows the polygon to be drawn by the user on the window as they are marking it out
                    for poly_point in range(points):
                        line = cv2.line(template_copy,
                                        (temp_dat.ref[poly_point][0]
                                         * chair_scale,
                                         temp_dat.ref[poly_point][1]
                                         * chair_scale),
                                        (temp_dat.ref[poly_point-1][0]
                                         * chair_scale,
                                         temp_dat.ref[poly_point-1][1]
                                         * chair_scale),
                                        line_color, 1)
                for poly_point in range(points):
                    dot = cv2.circle(template_copy,
                                     (temp_dat.ref[poly_point][0]
                                      * chair_scale,
                                      temp_dat.ref[poly_point][1]
                                      * chair_scale),
                                     int(dot_size * chair_scale / 2),
                                     line_color, -1)
                cv2.imshow(window_name, template_copy)#show template in the window
                refresh = []
            key = cv2.waitKey(1) & 0xFF
            if key == ord('e'):#close the window if 'e' is pressed
                if len(temp_dat.ref) >= 3:
                    break
        # centroid_offset = Polygon(np.array(temp_dat.ref)).centroid
        polygon = room_info.create_new_chair_poly(chair_type, temp_dat.ref)
        list_of_chair_polys.append(polygon)
    room_info.set_chair_polys(list_of_chair_polys)
    menu_refresh.append('r')

def chair_recognition(non_writable_img, menu_refresh, window_name, room_info):
    """chair_recognition handles the chair recognition input section of the
    room solving progress. This function identifies chairs within the room
    based off of the previously selected chair orientations and provided
    finding_threshold. Upon completion, this function will draw a version of
    the room diagram with all identified chairs marked in color line_color, and
    will set room_info._chairs to a list containing _Chair instances
    representing them.


    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    room_info -- The RoomInfo instance being used to keep track of input
    information. Must already have _ChairType instances contained within
    room_info._chair_types and _ChairPoly instances contained within
    room_info._chair_polys.

    window_name -- The name (string) of the cv2 window for the function to use.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    line_color = cpg.RED
    finding_threshold = room_info.parameters_dict["finding_threshold"]

    if show_instr:
        instruct.chair_recognition_explanation(window_name, screen_height,
                                               screen_width)

    scroll_height = 0
    scroll_width = 0

    cv2.createTrackbar("Hscroll", window_name, scroll_height,
                       (height - screen_height), __trackbar_change)
    cv2.createTrackbar("Wscroll", window_name, scroll_width,
                       (width - screen_width), __trackbar_change)
    list_of_chairs = []
    # initialize empty array
    x = np.array([])
    y = np.array([])
    ctype = np.array([])

    room_info_chair_types = room_info.get_chair_types()
    room_info_chair_polys = room_info.get_chair_polys()
    writable_clone = non_writable_img.copy()
    # extract all types of chairs
    for chair_type in room_info_chair_types:
        chair_template = chair_type.template
        # run matching function (may take a minute or two)
        result = match_template(non_writable_img, chair_template,
                                pad_input = True)
        points = peak_local_max(result, min_distance = 1,
                                threshold_rel = finding_threshold) # find our peaks (our location points)
        for poly in room_info_chair_polys:
            if poly.chair_type == chair_type:
                type_poly = poly
        for point in range(len(points)):
            center_coordinates = (points[point, 1].item(),
                                  points[point, 0].item())
            chair = room_info.create_new_chair(chair_type, type_poly,
                                               center_coordinates)
            list_of_chairs.append(chair)
    for chair in list_of_chairs:
        chair.draw(writable_clone, line_color, 1)
    while True:
    #These lines are what allow the scrolling
        scroll_height = cv2.getTrackbarPos("Hscroll", window_name)
        scroll_width = cv2.getTrackbarPos("Wscroll", window_name)
        shown_img = np.array([(scroll_width, scroll_height),
                              (scroll_width + width, scroll_height),
                              (scroll_width + width, scroll_height + height),
                              (scroll_width, scroll_height + height)])
        cds = cpg.get_coords(shown_img)
        img = writable_clone[cds[2] : cds[3], cds[0] : cds[1]]
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):#close the window if 'e' is pressed
            room_info.set_chairs(list_of_chairs)
            break
    # store output in room_info
    menu_refresh.append('r')


def __place_Chair(event, x, y, flags, temp_dat):
    """The private callback for mouse events in the cv2 window during the
    chair addition input section. Adds coords to temp_dat.ref on left mouse
    click. Deletes the latest coord from temp_dat.ref on right click. Keeps
    track of mouse position by adding current coords on mouse movement to
    temp_dat.ref_temp.
    """
    if event == cv2.EVENT_MOUSEMOVE:
        for item in range(len(temp_dat.ref_temp)):
            del temp_dat.ref_temp[-1]
        temp_dat.ref_temp.append([x + cv2.getTrackbarPos("Wscroll",
                                                         temp_dat.window_name),
                                  y + cv2.getTrackbarPos("Hscroll",
                                                          temp_dat.window_name),
                                  temp_dat.chair_selection])
        temp_dat.refresh.append('r')
    if event == cv2.EVENT_LBUTTONDOWN:
        temp_dat.ref.append([x + cv2.getTrackbarPos("Wscroll",
                                                    temp_dat.window_name),
                             y + cv2.getTrackbarPos("Hscroll",
                                                    temp_dat.window_name),
                             temp_dat.chair_selection])
        temp_dat.refresh.append('r')
    if event == cv2.EVENT_RBUTTONDOWN:
        del temp_dat.ref[-1]
        temp_dat.refresh.append('r')
def chair_addition(non_writable_img, menu_refresh, window_name, room_info):
    """chair_addition handles the chair addition input section of the
    room solving progress. This function allows users to designate chairs
    within the room based off of the previously selected chair orientations.
    This function displays the provided room diagram with all identified chairs
    drawn onto it. It will also show a preview of the currently selected chair
    orientation in color temp_color around the location of the cursor. Clicking
    within the window will add the preview chair as an actual chair and show it
    in color selected_color. Users can undo added chairs by right clicking.
    Upon completion, the function will add _Chair instances representing the
    added chairs to room_info._chairs


    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    room_info -- The RoomInfo instance being used to keep track of input
    information. Must already have _ChairType instances contained within
    room_info._chair_types and _ChairPoly instances contained within
    room_info._chair_polys. Also requires room_info._chairs to already have
    been set to a list of _Chair instances.

    window_name -- The name (string) of the cv2 window for the function to use.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    line_color = cpg.RED
    selected_color = cpg.PURPLE
    temp_color = cpg.GREEN

    if show_instr:
        instruct.chair_addition_explanation(window_name, screen_height,
                                            screen_width)
    scroll_height = 0
    scroll_width = 0

    cv2.createTrackbar("Hscroll", window_name, scroll_height,
                       (height - screen_height), __trackbar_change)
    cv2.createTrackbar("Wscroll", window_name, scroll_width,
                       (width - screen_width), __trackbar_change)

    temp_dat = TempData()
    temp_dat.set_window_name(window_name)
    temp_dat.refresh = ['r']
    chair_poly_types = room_info.get_chair_polys()
    total_chair_types = len(chair_poly_types) - 1
    writable_clone = non_writable_img.copy()

    cv2.setMouseCallback(window_name, __place_Chair, temp_dat)

    while True:
        scroll_height = cv2.getTrackbarPos("Hscroll", window_name)
        scroll_width = cv2.getTrackbarPos("Wscroll", window_name)
        shown_img = np.array([(scroll_width, scroll_height),
                             (scroll_width + width, scroll_height),
                             (scroll_width + width, scroll_height + height),
                             (scroll_width, scroll_height + height)])
        cds = cpg.get_coords(shown_img)
        img = writable_clone[cds[2] : cds[3], cds[0] : cds[1]]
        cv2.imshow(window_name, img)
        if len(temp_dat.refresh) >= 1:
            writable_clone = non_writable_img.copy()
            for chair in room_info.get_chairs():
                chair.draw(writable_clone, line_color, 1)
            #Draw Temp chair
            if len(temp_dat.ref_temp) >= 1:
                temp_chair_poly = chair_poly_types[temp_dat.ref_temp[0][2]]
                temp_chair_type = temp_chair_poly.chair_type
                temp_chair_coords = (temp_dat.ref_temp[0][0],
                                     temp_dat.ref_temp[0][1])
                temp_chair = room_info.create_new_chair(temp_chair_type,
                                                        temp_chair_poly,
                                                        temp_chair_coords)
                temp_chair.draw(writable_clone, temp_color, 1)
            #Draw added chairs
            for added_chair_ref in temp_dat.ref:
                added_chair_poly = chair_poly_types[added_chair_ref[2]]
                added_chair_type = added_chair_poly.chair_type
                added_chair_coords = (added_chair_ref[0], added_chair_ref[1])
                added_chair = room_info.create_new_chair(added_chair_type,
                                                         added_chair_poly,
                                                         added_chair_coords)
                added_chair.draw(writable_clone, selected_color, 1)
            refresh = []

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'): #close the window if 'e' is pressed
            break
        elif key == ord('d'): #shift to the next chair type if key 'a' is pressed
            if temp_dat.chair_selection < total_chair_types:
                temp_dat.chair_selection = temp_dat.chair_selection + 1
            else:
                temp_dat.chair_selection = 0
            temp_dat.refresh = ['r']
        elif key == ord('a'): #shift to the previous chair type if key 'd' is pressed
            if temp_dat.chair_selection > 0:
                temp_dat.chair_selection = temp_dat.chair_selection - 1
            else:
                temp_dat.chair_selection = total_chair_types
            temp_dat.refresh = ['r']
        elif key == ord('s'):
            for added_chair_ref in temp_dat.ref:
                print(added_chair_ref)
    for added_chair_ref in temp_dat.ref:
        added_chair_poly = chair_poly_types[added_chair_ref[2]]
        added_chair_type = added_chair_poly.chair_type
        added_chair = room_info.create_new_chair(added_chair_type,
                                                 added_chair_poly,
                                                 (added_chair_ref[0],
                                                  added_chair_ref[1]))
        room_info.add_chair(added_chair)
    menu_refresh.append('r')

def __delete_chairs(event, x, y, flags, temp_dat):
    """The private callback for mouse events in the cv2 window during the
    chair deletion input section. Adds coords to temp_dat.ref on left mouse
    click. Deletes the latest coord from temp_dat.ref on right click. Keeps
    track of mouse position by adding current coords on mouse movement to
    temp_dat.ref_temp.
    """
    if event == cv2.EVENT_MOUSEMOVE:
        for item in range(len(temp_dat.ref_temp)):
            del temp_dat.ref_temp[-1]
        temp_dat.ref_temp.append((x + cv2.getTrackbarPos("Wscroll",
                                                         temp_dat.window_name),
                                  y + cv2.getTrackbarPos("Hscroll",
                                                         temp_dat.window_name)))
        temp_dat.refresh.append('r')
    if event == cv2.EVENT_LBUTTONDOWN:
        temp_dat.ref.append((x + cv2.getTrackbarPos("Wscroll",
                                                    temp_dat.window_name),
                             y + cv2.getTrackbarPos("Hscroll",
                                                    temp_dat.window_name)))
        temp_dat.refresh.append('r')
    if event == cv2.EVENT_RBUTTONDOWN:
        del temp_dat.ref[-1]
        temp_dat.refresh.append('r')
def chair_deletion(non_writable_img, menu_refresh, window_name, room_info):
    """chair_deletion handles the chair deletion input section of the
    room solving progress. This function allows users to delete identified
    chairs from room_info._chairs. This function displays the provided room
    diagram with all identified chairs drawn onto it. The user is able to
    designate rectangles on the diagram by clicking on the locations for a
    diagonal pair of its corners. Upon completion, all chairs within the
    rectangles are removed from room_info._chairs.


    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    window_name -- The name (string) of the cv2 window for the function to use.

    room_info -- The RoomInfo instance being used to keep track of input
    information. Must already have _ChairType instances contained within
    room_info._chair_types and _ChairPoly instances contained within
    room_info._chair_polys. Also requires room_info._chairs to already have
    been set to a list of _Chair instances.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    line_color = cpg.RED
    selected_color = cpg.PURPLE
    temp_color = cpg.GREEN

    if show_instr:
        instruct.chair_deletion_explanation(window_name, screen_height,
                                            screen_width)

    scroll_height = 0
    scroll_width = 0

    cv2.createTrackbar("Hscroll", window_name, scroll_height,
                       (height - screen_height), __trackbar_change)
    cv2.createTrackbar("Wscroll", window_name, scroll_width,
                       (width - screen_width), __trackbar_change)

    writable_clone = non_writable_img.copy()
    writable_clone_backup = writable_clone.copy()
    temp_dat = TempData()
    temp_dat.set_window_name(window_name)
    temp_dat.refresh.append('r')

    room_info_chairs = room_info.get_chairs()
    #Draw all chairs on a fresh room
    for chair in room_info_chairs:
        chair.draw(writable_clone, line_color, 1)
    #Take a copy of the current drawing state
    writable_clone_backup = writable_clone.copy()

    cv2.setMouseCallback(window_name, __delete_chairs, temp_dat)

    while True:
        scroll_height = cv2.getTrackbarPos("Hscroll", window_name)
        scroll_width = cv2.getTrackbarPos("Wscroll", window_name)
        shown_img = np.array([(scroll_width, scroll_height),
                              (scroll_width + width, scroll_height),
                              (scroll_width + width, scroll_height + height),
                              (scroll_width, scroll_height + height)])
        cds = cpg.get_coords(shown_img)
        img = writable_clone[cds[2] : cds[3], cds[0] : cds[1]]
        cv2.imshow(window_name, img)

        #Refreshes the image
        if len(temp_dat.refresh) >= 1:
            #Reverts to the previous drawing state copy with chairs drawn in.
            writable_clone = writable_clone_backup.copy()
            #Draws selection Rectangles
            if len(temp_dat.ref) >= 2:
                for i in range((len(temp_dat.ref)
                                - (len(temp_dat.ref) % 2)) // 2):
                    cv2.rectangle(writable_clone, temp_dat.ref[i * 2],
                                  temp_dat.ref[i * 2 + 1], selected_color,
                                  1)
            if len(temp_dat.ref) % 2 == 1:
                cv2.rectangle(writable_clone, temp_dat.ref[-1],
                              temp_dat.ref_temp[0], temp_color, 1)
            temp_dat.refresh=[]

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            if len(temp_dat.ref) % 2 == 0:
                break

    rectangles = []
    if len(temp_dat.ref) >= 2:
        for i in range((len(temp_dat.ref) - len(temp_dat.ref) % 2)
                        // 2):
            x_coord1 = temp_dat.ref[i * 2][0]
            y_coord1 = temp_dat.ref[i * 2][1]
            x_coord2 = temp_dat.ref[i * 2 + 1][0]
            y_coord2 = temp_dat.ref[i * 2 + 1][1]

            if x_coord1 > x_coord2:
                x_temp = x_coord1
                x_coord1 = x_coord2
                x_coord2 = x_temp

            if y_coord1 > y_coord2:
                y_temp = y_coord1
                y_coord1 = y_coord2
                y_coord2 = y_temp

            rectangles.append([(x_coord1, y_coord1), (x_coord2, y_coord2)])

    for rectangle in rectangles:
        remove_these = []
        for chair in room_info_chairs:
            if (chair.coords[0] > rectangle[0][0]
                and chair.coords[0] < rectangle[1][0]):
                if (chair.coords[1] > rectangle[0][1]
                    and chair.coords[1] < rectangle[1][1]):
                    remove_these.append(chair)

        while len(remove_these) >= 1:
            room_info.remove_chair(remove_these[0])
            del remove_these[0]
    menu_refresh.append('r')

def input_preview(non_writable_img, menu_refresh, window_name, room_info):
    """input_preview allows the user to preview all of their inputs by making
    the window display the diagram with all of their inputs.

    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    window_name -- The name (string) of the cv2 window for the function to use.

    room_info -- The RoomInfo instance being used to keep track of input
    information. Must already have _ChairType instances contained within
    room_info._chair_types and _ChairPoly instances contained within
    room_info._chair_polys. Also requires room_info._chairs to already have
    been set to a list of _Chair instances.

    show_instr -- A bool that tells the function whether or not to show
    instructions to the user.

    height -- The height (int) to make the window.

    width -- The width (int) to make the window.

    line_color -- The color to use (in BGR Tuple form) when drawing the
    identified chairs.

    selected_color -- The color to use (in BGR Tuple form) when drawing the
    selected chair types (chair orientations).

    save_to_json -- Whether or not to save data to json
    (currently not functioning).

    json_save_name -- The filename to use when saving the data to json.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    height = room_info.window_info_dict["height"]
    width = room_info.window_info_dict["width"]
    line_color = cpg.RED
    selected_color = cpg.PURPLE
    save_to_json = room_info.parameters_dict["save_to_json"]
    json_save_name = room_info.parameters_dict["json_save_name"]
    if show_instr:
        instruct.input_preview_explanation(window_name, screen_height,
                                           screen_width)

    scroll_height = 0
    scroll_width = 0

    cv2.createTrackbar("Hscroll", window_name, scroll_height,
                       (height - screen_height), __trackbar_change)
    cv2.createTrackbar("Wscroll", window_name, scroll_width,
                       (width - screen_width), __trackbar_change)

    writable_clone = non_writable_img.copy()
    writable_clone_backup = writable_clone.copy()

    for chair_type in room_info.get_chair_types():
        chair_type.draw(writable_clone, selected_color, 2)
    for chair in room_info.get_chairs():
        chair.draw(writable_clone, line_color, 2)
    room_info.get_scale().draw(writable_clone, line_color, 2)
    while True:
        scroll_height = cv2.getTrackbarPos("Hscroll", window_name)
        scroll_width = cv2.getTrackbarPos("Wscroll", window_name)
        shown_img = np.array([(scroll_width, scroll_height),
                              (scroll_width + width, scroll_height),
                              (scroll_width + width, scroll_height + height),
                              (scroll_width, scroll_height + height)])
        cds = cpg.get_coords(shown_img)
        img = writable_clone[cds[2] : cds[3], cds[0] : cds[1]]
        cv2.imshow(window_name, img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            # if save_to_json:
            #     with open(json_save_name, 'w') as json_file:
            #         json.dump(room_info, json_file)
            break
    menu_refresh.append('r')

def __miset(nodes, edges, solver):
    """This is a helper function that solves the graph provided subject to the
    constraints on the social distancing seat assignment problem.
    """
    NODES = []
    NODES.extend(nodes)    # these four lines are not necessary
    EDGES = []             # made a copy in case the lists will be modified
    EDGES.extend(edges)

    # define model
    m = OR.Solver('maxIndSet', solver)

    # decision variables
    x = {} # node i is in the maximal independent set is 1, else 0
    for i in NODES:
        x[i] = m.IntVar(0, 1, ('%s' % (i)))

    # objective function
    m.Maximize(sum(x[i] for i in NODES))

    # subject to: no more than 1 node from an edge
    for edge in EDGES:
        m.Add(x[edge[0]] + x[edge[1]] <= 1)

    m.Solve()

    sol = {}
    for i in NODES:
        sol.update( {x[i].name() : x[i].solution_value()} )

    return(sol)

def solve_room(non_writable_img, menu_refresh, window_name, room_info):
    """solve_room converts the input into a graph representation of the room
    and solves it for maximum occupancy under the social distancing
    constraints. Upon completion, it saves a diagram clearly displaying the
    solution under the name solution_name. The diagram will show seats that
    should be used in orange, and seats that should not be used in blue. Around
    each orange seat, a radius is drawn to display the distance required for
    social distancing.

    Keyword arguments:

    non_writable_img -- A cv2 image of the room diagram. Not meant to be
    written on by the code.

    menu_refresh -- A list that will be appended to upon completion of the
    function.

    window_name -- The name (string) of the cv2 window for the function to use.

    room_info -- The RoomInfo instance being used to keep track of input
    information. Must already have _ChairType instances contained within
    room_info._chair_types and _ChairPoly instances contained within
    room_info._chair_polys. Also requires room_info._chairs to already have
    been set to a list of _Chair instances.

    solution_dpi -- The dpi (int) to use when writing the solution diagram.

    solution_name -- The filename (string) to use when writing the solution
    diagram.
    """
    show_instr = room_info.parameters_dict["show_instructions"]
    screen_height = room_info.parameters_dict["screen_height"]
    screen_width = room_info.parameters_dict["screen_width"]
    solution_dpi = room_info.parameters_dict["solution_dpi"]
    solution_name = room_info.parameters_dict["solution_name"]

    if show_instr:
         instruct.solve_room_explanation(window_name, screen_height,
                                         screen_width)
    coords = []
    polygons = []
    middles = []

    room_info_chairs = room_info.get_chairs()
    for chair in room_info_chairs:
        coords.append(Point(chair.coords))
        chair_poly = chair.chair_poly
        polygon = Polygon(np.array(chair_poly.points))
        polygon = shapely.affinity.translate(polygon,
                                             xoff = chair.coords[0],
                                             yoff = chair.coords[1])
        polygon = shapely.affinity.translate(polygon,
                                             xoff = chair_poly.offsets[0],
                                             yoff = chair_poly.offsets[1])
        polygons.append(polygon)
        middles.append(polygon.centroid)
    # set axis tick size
    plt.rc('xtick', labelsize = 4)
    plt.rc('ytick', labelsize = 4)
    fig, ax = plt.subplots(dpi = solution_dpi)
    plt.axis('off')

    # set axis line size
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(0.5)

    # plot points
    xs = []
    ys = []
    for chair in middles:
        xs.append(chair.x)
        ys.append(chair.y)
    # generate edges from distances
    edgelist = list()      # overall list of (directed) edges

    for i in range(len(coords)):
        for j in range(len(coords)):
            if (i != j):
                dist = polygons[j].distance(middles[i])
                if (dist <= room_info.get_scale().pixels_to_distance):
                    edgelist.append((i, j)) # add edge if seat is too close


    nodes = []
    for i in range(len(coords)):
        nodes.append(i)

    # solve problem
    sol = __miset(nodes, edgelist, OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    in_solution = list(sol.values())
    total_chairs = 0
    chairs_in_solution = []
    for i in in_solution:
        if i == 1.0:
            total_chairs += 1

    for i in range(len(in_solution)):
        if in_solution[i] == 0:
            xz, yz = polygons[i].exterior.xy
            ax.plot(xz, yz, color = 'blue', alpha = 1, linewidth = 0.2,
                    solid_capstyle = 'round', zorder = 2)
            ax.fill(xz, yz, alpha = 0.6, fc = 'lightblue', ec = 'darkblue',
                    linewidth = 0.15, zorder = 2)
        else:
            xz, yz = polygons[i].exterior.xy
            ax.plot(xz, yz, color = 'orange', alpha = 1, linewidth = 0.2,
                    solid_capstyle = 'round', zorder = 3)
            ax.fill(xz, yz, alpha = 0.6, fc = 'orange', ec = 'darkred',
                    linewidth = 0.15, zorder = 3)
            draw_circle = plt.Circle((middles[i].x, middles[i].y),
                                     room_info.get_scale().pixels_to_distance,
                                     fill = False, ec = 'darkblue', ls = '--',
                                     lw = 0.2, zorder = 4)
            ax.add_artist(draw_circle)
            chairs_in_solution.append(room_info_chairs[i])

    plt.text(10, 10, str(int(total_chairs)) + " seats",
             fontsize = 6, color = 'red',
             horizontalalignment = 'left',
             verticalalignment = 'top')
    room_info.set_chairs_in_sol(chairs_in_solution)
    print("generating image")
    ax.imshow(non_writable_img)
    plt.savefig(solution_name + ".jpg", orientation = 'portrait',
                format = 'jpg',
                dpi = solution_dpi)
    menu_refresh.append('r')
    return
