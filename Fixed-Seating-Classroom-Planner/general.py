from shapely.geometry import Polygon, Point
import numpy as np
import cv2

NOT_SET = False
DOT_SIZE = 1

GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (0, 0, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

def get_coords(rect):
    """Takes an np.array with coords of rectangle.

    Returns max / min height / width
    """
    lw = min(rect[:,0])
    uw = max(rect[:,0])
    lh = min(rect[:,1])
    uh = max(rect[:,1])

    return(lw, uw, lh, uh)


class _RoomScale():
    """_RoomScale is a private class used by the RoomInfo class to store
    information about the scale of a room. User's should not directly
    instantiate objects of the _RoomScale class, but are able to create, set
    and use _RoomScale objects through the RoomInfo class.


    Instance variables:

    points -- A list of (int, int) pair tuples representing the coordinates
    of the four corners of the room diagram's scale.

    scale_length_pixels -- An int representing the length in pixels of the
    room diagram's scale.

    unit_length_pixels -- A float representing the length in pixels of a
    single unit (same unit used by the user in units_to_distance and
    scale_length_units).

    pixels_to_distance -- A float representing the length ini pixels to
    distance seats within the room by.

    scale_length_units -- scale_length_units from the keyword arguments.

    units_to_distance -- units_to_distance from the keyword arguments.

    scale_orientation -- scale_orientation from the keyword arguments.


    Public Methods:

    redefine_points -- Allows changes to be made to the points instance
    variable. Recalculates the other instance variables to match this.

    redefine_scale_orientation -- Allows the scale_orientation instance
    variable to be changed. Recalculates the other instance variables to match
    this.

    redefine_scale_length_units -- Allows the scale_length_units Instance
    variable to be changed. Recalculates the other instance variables to match
    this.

    redefine_units_to_distance -- Allows the units_to_distance instance
    variable to be changed. Recalculates the other instance variables to match
    this.

    draw -- Draws the instance in the provided image with the provided color
    and line width.
    """

    def __init__(self, point1, point2, units_to_distance, scale_orientation,
                 scale_length_units):
        """Initializes an instance of the _RoomScale class. This should never
        be done directly; Users should work with _RoomScale through an instance
        of the RoomInfo class.


        Keyword arguments:

        point1 -- A tuple of length 2 containing integers to represent the
        coordinates of a corner of the room diagram's scale.

        point2 -- A tuple of length 2 containing integers to represent the
        coordinates of the corner of the room diagram's scale opposite to
        point1.

        units_to_distance -- An int or float representing how many units (feet,
        meters, inches, e.t.c.) to distance seats within the room by.

        scale_orientation -- A string that is either "Horizontal" or
        "Vertical" (case sensitive) indicating the orientation of the room
        diagram's scale.

        scale_length_units -- An int or float representing how many units
        (feet, meters, inches, e.t.c. must be the same unit as the
        units_to_distance keyword argument) long the scale is.
        """
        #Define the points of the scale based off the given points
        x1 = point1[0]
        x2 = point2[0]
        y1 = point1[1]
        y2 = point2[1]
        if x1 > x2:
            x1_temp = x1
            x1 = x2
            x2 = x1_temp
        if y1 > y2:
            y1_temp = y1
            y1 = y2
            y2 = y1_temp
        self.points = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
        #Define the length of the scale in pixels based off its points and orientation
        if scale_orientation == "Horizontal":
            self.scale_length_pixels = int(x2 - x1)
        else:
            self.scale_length_pixels = int(y2 - y1)
        #Define the unit length in pixels based off the scale length in pixels and units
        self.unit_length_pixels = float(self.scale_length_pixels
                                        / scale_length_units)
        #Define the distancing length in pixels based off the unit length and the length in units to distance by
        self.pixels_to_distance = float(self.unit_length_pixels
                                        * units_to_distance)
        #Stores the creation parameters to the scale so that later editing can be done
        self.scale_length_units = scale_length_units
        self.units_to_distance = units_to_distance
        self.scale_orientation = scale_orientation

    def redefine_points(self, point1, point2):
        """Changes the values of the instance variables of the _RoomScale
        object to match those of point1 and point2.


        Keyword arguments:

        point1 -- A tuple of length 2 containing integers to represent the
        coordinates of a corner of the room diagram's scale.

        point2 -- A tuple of length 2 containing integers to represent the
        coordinates of the corner of the room diagram's scale opposite to
        point1.
        """
        #Assert validity of point1 and point2
        assert(isinstance(point1, tuple)), "point1 is not a valid tuple"
        assert(isinstance(point2, tuple)), "point2 is not a valid tuple"
        assert(len(point1) == 2), "point1 is not a valid tuple"
        assert(len(point2) == 2), "point2 is not a valid tuple"
        for item in point1:
            assert(isinstance(item, int)), "point1 is not a valid tuple"
        for item in point2:
            assert(isinstance(item, int)), "point2 is not a valid tuple"

        x1 = point1[0]
        x2 = point2[0]
        y1 = point1[1]
        y2 = point2[1]
        if x1 > x2:
            x1_temp = x1
            x1 = x2
            x2 = x1_temp
        if y1 > y2:
            y1_temp = y1
            y1 = y2
            y2 = y1_temp
        self.points = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
        #Define the length of the scale in pixels based off its points and orientation
        if self.scale_orientation == "Horizontal":
            self.scale_length_pixels = x2 - x1
        else:
            self.scale_length_pixels = y2 - y1
        #Define the unit length in pixels based off the scale length in pixels and units
        self.unit_length_pixels = (self.scale_length_pixels
                                   / self.scale_length_units)
        #Define the distancing length in pixels based off the unit length and the length in units to distance by
        self.pixels_to_distance = (self.unit_length_pixels
                                   * self.units_to_distance)

    def redefine_scale_orientation(self, scale_orientation):
        """Changes the values of the instance variables of the _RoomScale
        object to match that of scale_orientation.


        Keyword argument:

        scale_orientation -- A string that is either "Horizontal" or
        "Vertical" (case sensitive) indicating the orientation of the room
        diagram's scale.
        """
        assert(scale_orientation == "Vertical"
               or scale_orientation == "Horizontal"), ("scale_orientation must"
                                                       ' be either "Vertical"'
                                                       ' or "Horizontal"')
        self.scale_orientation = scale_orientation

        if self.scale_orientation == "Horizontal":
            self.scale_length_pixels = x2 - x1
        else:
            self.scale_length_pixels = y2 - y1
        #Define the unit length in pixels based off the scale length in pixels and units
        self.unit_length_pixels = (self.scale_length_pixels
                                   / self.scale_length_units)
        #Define the distancing length in pixels based off the unit length and the length in units to distance by
        self.pixels_to_distance = (self.unit_length_pixels
                                   * self.units_to_distance)

    def redefine_scale_length_units(self, scale_length_units):
        """Changes the values of the instance variables of the _RoomScale
        object to match that of scale_length_units.


        Keyword argument:

        scale_length_units -- An int or float representing how many units
        (feet, meters, inches, e.t.c. must be the same unit as the
        units_to_distance keyword argument) long the scale is.
        """
        #Assert validity of scale_units_length
        assert(isinstance(scale_length_units, (int, float))), ("scale_units_"
                                                               "length must "
                                                               "be an int or "
                                                               "a float")
        self.scale_length_units = scale_length_units
        self.unit_length_pixels = (self.scale_length_pixels
                                   / self.scale_length_units)
        self.pixels_to_distance = (self.unit_length_pixels
                                   * self.units_to_distance)

    def redefine_units_to_distance(self, units_to_distance):
        """Changes the values of the instance variables of the _RoomScale
        object to match that of units_to_distance.


        Keyword argument:

        units_to_distance -- An int or float representing how many units (feet,
        meters, inches, e.t.c.) to distance seats within the room by.
        """
        assert(isinstance(units_to_distance, (int, float))), ("units_to_"
                                                               "distance "
                                                               "must be an int"
                                                               " or a float")
        self.units_to_distance = units_to_distance
        self.pixels_to_distance = (self.unit_length_pixels
                                   * self.units_to_distance)

    def draw(self, img, line_color, line_width):
        """Draws the _RoomScale object in img with color line_color and line
        width line_width.


        Keyword arguments:

        img -- The image to draw on.

        line_color -- The color to draw the _RoomScale object in. Must be a
        BGR color tuple.

        line_width -- The line width to use when drawing the _RoomScale object.
        Must be an int.
        """
        #TODO: STILL NEEDS ASSERT STATEMENTS
        rect = cv2.rectangle(img, self.points[0], self.points[2], line_color,
                             line_width)


class _ChairType():
    """_ChairType is a private class used by the RoomInfo class to store
    information on a chair orientation within the room's diagram. User's should
    not directly instantiate objects of the _ChairType class, but are able to
    create, set and use _ChairType objects through the RoomInfo class.


    Instance variables:

    points -- A list of (int, int) pair tuples representing the coordinates
    of the four corners of the chair orientation's highlighted section.

    template -- A cut section of the image the _ChairType object was
    instantiated from that contains the chair orientation within the
    coordinates in the instance variable "points".


    Public Method:

    draw -- Draws the instance in the provided image with the provided color
    and line width.
    """

    def __init__(self, point1, point2, img):
        """Initializes an instance of the _ChairType class. This should never
        be done directly; Users should work with _ChairType through an instance
        of the RoomInfo class.


        Keyword arguments:

        point1 -- a tuple of length 2 containing integers to represent the
        coordinates of a corner of a rectangle bounding the chair orientation
        the user is defining the _ChairType object to represent.

        point2 -- a tuple of length 2 containing integers to represent the
        coordinates of the corner diagonally opposite point1 of a rectangle
        bounding the chair orientation the user is defining the _ChairType
        object to represent.

        img -- the image that the  chair orientation the user is defining the
        _ChairType object to represent resides in.
        """
        #Assert point1 and point2 arev alid tuples.
        assert(isinstance(point1, tuple)), "point1 is not a valid tuple"
        assert(isinstance(point2, tuple)), "point2 is not a valid tuple"
        assert(len(point1) == 2), "point1 is not a valid tuple"
        assert(len(point2) == 2), "point2 is not a valid tuple"

        #TODO assert img is a valid image.
        for item in point1:
            assert(isinstance(item, int)), "point1 is not a valid tuple"
        for item in point2:
            assert(isinstance(item, int)), "point2 is not a valid tuple"
        x1 = point1[0]
        x2 = point2[0]
        y1 = point1[1]
        y2 = point2[1]
        if x1 > x2:
            x1_temp = x1
            x1 = x2
            x2 = x1_temp
        if y1 > y2:
            y1_temp = y1
            y1 = y2
            y2 = y1_temp
        self.points = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
        cds = get_coords(np.array(self.points))
        self.template = img[cds[2] : cds[3], cds[0] : cds[1]]

    def draw(self, img, line_color, line_width):
        """Draws the _ChairType object in img with color line_color and line
        width line_width.


        Keyword arguments:

        img -- An image to draw on.

        line_color -- The color to draw the _ChairType object in. Must be a
        BGR color tuple.

        line_width -- The line width to use when drawing the _ChairType object.
        Must be an int.
        """
        #TODO: write assert statements.
        rect = cv2.rectangle(img, self.points[0], self.points[2], line_color,
                             line_width)


class _ChairPoly():
    """_ChairPoly is a private class used by the RoomInfo class to store
    information on a polygon representing the shape of a chair for a chair
    orientation represented by a _ChairType object. User's should
    not directly instantiate objects of the _ChairPoly class, but are able to
    create, set and use _ChairPoly objects through the RoomInfo class.


    Instance variables:

    chair_type -- A _ChairType object representing the chair orientation that
    the _ChairPoly object represents the polygon for.

    points -- A list of (int, int) pair tuples representing the coordinates
    of the points of the polygon of the chair for the chair orientation
    represented by the _ChairType object in the chair_type instance variable.

    offsets -- A stored value used by the code to shift the polygon of the
    chair. offsets is an (int, int) pair tuple.
    """

    def __init__(self, chair_type, points):
        """Initializes an instance of the _ChairPoly class. This should never
        be done directly; Users should work with _ChairPoly through an instance
        of the RoomInfo class.


        Keyword arguments:

        points -- A list of (int, int) pair tuples representing the coordinates
        of the points of the polygon of the chair for the chair orientation
        represented by the _ChairType object in the chair_type instance
        variable.

        chair_type -- A _ChairType object representing the chair orientation
        that the _ChairPoly object represents the polygon for.
        """
        #TODO: add assert statements
        self.chair_type = chair_type
        centroid = Polygon(np.array(points)).centroid
        self.offsets = (-(chair_type.points[2][0]
                          - chair_type.points[0][0]) / 2,
                        -(chair_type.points[2][1]
                          - chair_type.points[0][1]) / 2)
        self.points = points


class _Chair():
    """_Chair is a private class used by the RoomInfo class to store
    information on a possible chair.. User's should not directly instantiate
    objects of the _Chair class, but are able to create, set and use _Chair
     objects through the RoomInfo class.


    Instance variables:

    chair_type -- A _ChairType object representing the chair orientation of the
    _Chair object.

    chair_poly -- A _ChairPoly object representing the polygon of the possible
    chair that the _Chair object represents. chair_poly's chair_type instance
    variable should be the same as the instance variable chair_type.

    coords -- An (int, int) pair tuple used as coordinates for the center of
    the possible chair that the _Chair object represents.


    Public Method:

    draw -- Draws the instance in the provided image with the provided color
    and line width.
    """

    def __init__(self, chair_type, chair_poly, coords):
        """Initializes an instance of the _Chair class. This should never be
        done directly; Users should work with _Chair through an instance of the
        RoomInfo class.


        Keyword arguments:

        chair_type -- A _ChairType object representing the chair orientation of
        the possible chair that the _Chair object will represent.

        chair_poly -- A _ChairPoly object representing the polygon of the
        possible chair that the _Chair object will represent.  chair_poly's
        chair_type instance variable should be the same as the keyword argument
        chair_type.

        coords -- An (int, int) pair tuple used as coordinates for the center
        of the possible chair that the _Chair object will represent.
        """

        self.chair_type = chair_type
        self.chair_poly = chair_poly
        self.coords = coords

    def draw(self, img, line_color, line_width):
        """Draws the _Chair object in img with color line_color and line width
        line_width.


        Keyword arguments:

        img -- An image to draw on.

        line_color -- The color to draw the _Chair object in. Must be a BGR
        color tuple.

        line_width -- The line width to use when drawing the _Chair object.
        Must be an int.
        """
        #TODO: add assert statements.
        assert(isinstance(line_width, int))
        poly_points = self.chair_poly.points
        x_center = self.coords[0] + self.chair_poly.offsets[0]
        y_center = self.coords[1] + self.chair_poly.offsets[1]
        for point in range(len(poly_points)):
            line = cv2.line(img,
                            (int(poly_points[point][0] + x_center),
                             int(poly_points[point][1] + y_center)),
                            (int(poly_points[point - 1][0] + x_center),
                             int(poly_points[point - 1][1] + y_center)),
                            line_color, line_width)
        cv2.circle(img, self.coords, DOT_SIZE, line_color, -1)


class RoomInfo():
    """RoomInfo is a class used to store information about a room for use by
    the classroom solver. RoomInfo stores information on the scale, chair
    orientations, chair shapes, possible seat locations, and solution set.
    RoomInfo also allows the user to manipulte the values stored in order to
    allow users to make changes as needed while keeping data well organized.


    Instance variables:

    _scale -- The _RoomScale object used to store information about the room
    diagram's scale.

    _chair_types -- A list of _ChairType objects used to store information on
    the different chair orientations within the room diagram.

    _chair_polys -- A list of _ChairPoly objects used to store information on
    the chair shape polygons used for the _ChairType objects in _chair_types.

    _chairs -- A list of _Chair objects used to store information on possible
    seat locations for the room.

    _chairs_in_solution -- A list of _Chair objects used to store information
    on a set of _Chair objects from _chairs that form a valid solution to the
    socially distanced seat assignment problem.

    _completions -- A dict maintaining information on which input methods have
    already been completed.

    _completions_length -- An int used to keep track of the length of
    _completions.

    parameters_dict -- A dict containing info on the parameters used on the
    tool.

    window_info_dict -- A dict containing info on the window settings for the
    tool.


    Public Methods:

    create_new_chair_poly -- Instantiates a new _ChairPoly instance.

    create_new_chair -- Instantiates a new _Chair instance.

    set_new_scale -- Sets the instance variable _scale to a new _RoomScale
    instance created from the passed in arguments.

    set_scale -- Sets the instance variable _scale to the provided _RoomScale
    instance.

    get_scale -- Returns the instance variable _scale.

    set_new_chair_types -- Sets the instance variable _chair_types to a new
    list of _ChairType instances generated from the provided arguments.

    set_chair_types -- Sets the instance variable _chair_types to the provided
    list of _ChairType instances.

    get_chair_types -- Returns the instance variable _chair_types.

    set_chair_polys -- Sets the instance variable _chair_polys to the provided
    list of _ChairPoly instances.

    get_chair_polys -- Returns the instance variable _chair_polys.

    set_chairs -- Sets the instance variable _chairs to the provided list of
    _Chair instances.

    get_chairs -- Returns the instance variable _chairs.

    add_chair -- Appends the provided _Chair instance to the instance variable

    remove_chair -- Removes the provided _Chair instance from the instance
    variable _chairs.

    set_chairs_in_sol -- Sets the instance variable _chairs_in_solution to the
    provided list of _Chair instances.

    get_chairs_in_sol -- Returns the instance variable _chairs_in_solution.

    get_completions -- Returns the instance variable _completions.

    set_completions -- Sets the instance variable _completions to the provided
    completions dictionary if it is valid.
    """

    def __init__(self, parameters_dict, window_info_dict):
        """Initializes an instance of the RoomInfo class with the given room
        parameters.


        Keyword Arguments:

        parameters_dict -- A dict containing the parameters for the room. For
        the current version, this should be a dict formatted in the following
        way:
        {
        "screen_height" : <The height (int) of your physical screen in pixels.>

        "screen_width" : <The width (int) of Your physical screen in pixels.>

        "room_type" : <The type of room this is for (str) either "Fixed" or
                       "Empty".> (Currently not working)

        "floor" : <The path to the image file of the room diagram on your
                   computer (str).>

        "load_from_json" : <True or False (bool) whether or not to load the
                            data from json_load_name.> (Currently not working)

        "json_load_name" : <Json file to load data from if load_from_json is
                           True (str).> (Currently not working)

        "save_to_json" : <True or False (bool) whether or not to save the data
                          stored in room_info to a json file.> (Currently not
                          working)

        "json_save_name" : <The name of the json to save the data to if
                            save_to_json is True (str).> (Currently not
                            working)

        "scale_length_units" : <How many units long the room diagram's scale is
                                (int or float).>

        "units_to_distance" : <How many units to distance seats by
                               (int or float).>

        "scale_orientation" : <The orientation of the scale (str). Either
                               "Horizontal" or "Vertical".>

        "chair_scale" : <The amount by which to scale up chairs when defining
                         their shapes (int).>

        "solution_name" : <The name to give the solution image (str).>

        "solution_dpi" : <The dpi to use when making the solution image (int).>

        "finding_threshold" : <The finding threshold when recognizing chairs
                               (float). Less than 1.>

        "show_instructions" : <Whether or not to show instructions to the user
                               when having them make inputs. True or False
                               (bool).>
        }

        window_info_dict -- A dict containing other information for the tool
        window formatted in the following way:
        {
        "height" : <The image height (int).>,

        "width" : <The image width (int).>,

        "window_height" :  <The height to make the window (int).>,

        "window_width" : <The width to make the window (int).>,
        }
        """
        #TODO add assertions on parameters_dict
        self._scale = NOT_SET
        self._chair_types = NOT_SET
        self._chair_polys = NOT_SET
        self._chairs = NOT_SET
        self._chairs_in_solution = NOT_SET
        self._completions = {"Scale Selection Status" : False,
                             "Chair Type Selection Status" : False,
                             "Polygon Creation Status" : False,
                             "Chair Recognition Status" : False,
                             "Chair Addition Status" : False,
                             "Chair Deletion Status" : False,
                             "Input Confirmation Status" : False,
                             "Solve Room Status" : False}
        self._completions_length = len(self._completions)
        self.parameters_dict = parameters_dict
        self.window_info_dict = window_info_dict

    #TODO add create_new_room_scale()

    #TODO add create_new_chair_type()

    def create_new_chair_poly(self, chair_type, points):
        """Initializes and returns a new instance of the _ChairPoly class.


        Keyword arguments:

        points -- A list of (int, int) pair tuples representing the coordinates
        of the points of the polygon of the chair for the chair orientation
        represented by the _ChairType object in the chair_type instance
        variable.

        chair_type -- A _ChairType object representing the chair orientation
        that the _ChairPoly object represents the polygon for. Must be a
        _ChairType object that is a part of the RoomInfo instance variable
        _chair_types.
        """
        has_valid_type = False
        for type in self._chair_types:
            if chair_type == type:
                has_valid_type = True
        assert(has_valid_type), "chair_type is not a valid _ChairType object."
        assert(isinstance(points, list)), ("points must be a list of tuples "
                                           "representing points.")
        assert(len(points) >= 3), ("points must contain at least 3 points.")
        for point in points:
            assert(isinstance(point, tuple)), ("points must be a list of "
                                               "tuples representing points.")
            for i in point:
                assert(isinstance(i, int)), ("Each point must be a pair of "
                                             "ints.")
        return _ChairPoly(chair_type, points)

    def create_new_chair(self, chair_type, chair_poly, coords):
        """Initializes and returns a new instance of the _Chair class.


        Keyword arguments:

        chair_type -- A _ChairType object representing the chair orientation of
        the new _Chair object. Must be a _ChairType object that is a part of
        the RoomInfo instance variable _chair_types.

        chair_poly -- A _ChairPoly object representing the chair polygon of the
        new _Chair object. Must be a _ChairPoly object that is a part of the
        RoomInfo instance variable _chair_polys. chair_poly.chair_type must
        equal the keyword argument chair_type.

        coords -- An (int, int) pair tuple used as coordinates for the center
        of the possible chair that the _Chair object will represent.
        """
        assert(isinstance(chair_type, _ChairType)), ("chair_type is not a "
                                                     "valid _ChairType object "
                                                     "in _chair_types.")
        has_valid_type = False
        for type in self._chair_types:
            if chair_type == type:
                has_valid_type = True
        assert(has_valid_type), ("chair_type is not a valid _ChairType object "
                                 "in _chair_types.")
        assert(isinstance(chair_poly, _ChairPoly)), ("chair_poly is not a "
                                                     "valid _ChairPoly object "
                                                     "in _chair_polys.")
        has_valid_poly = False
        for poly in self._chair_polys:
            if chair_poly == poly:
                has_valid_poly = True
        assert(has_valid_poly), ("chair_poly is not a valid _ChairPoly object "
                                 "in _chair_polys.")
        assert(chair_poly.chair_type == chair_type), ("chair_poly and "
                                                      "chair_type do not "
                                                      "match.")
        assert(isinstance(coords, tuple)), ("coords is not a valid tuple "
                                            "representing a point.")
        assert(len(coords) == 2), ("coords is not a valid tuple representing a"
                                   " point.")

        for i in coords:
            assert(isinstance(i, int)
                   or isinstance(i, float)), ("coords is not a valid tuple"
                                             " representing a point.")
        return _Chair(chair_type, chair_poly, coords)

    def set_new_scale(self, point1, point2, units_to_distance,
                      scale_orientation, scale_length_units):
        """Initializes a new instance of the _RoomScale class and sets the
        instance variable _scale to it.


        Keyword arguments:

        point1 -- A tuple of length 2 containing integers to represent the
        coordinates of a corner of the room diagram's scale.

        point2 -- A tuple of length 2 containing integers to represent the
        coordinates of the corner of the room diagram's scale opposite to
        point1.

        units_to_distance -- An int or float representing how many units (feet,
        meters, inches, e.t.c.) to distance seats within the room by.

        scale_orientation -- A string that is either "Horizontal" or
        "Vertical" (case sensitive) indicating the orientation of the room
        diagram's scale.

        scale_length_units -- An int or float representing how many units
        (feet, meters, inches, e.t.c. must be the same unit as the
        units_to_distance keyword argument) long the scale is.
        """
        #Assert validity of point1 and point2
        assert(isinstance(point1, tuple)), "point1 is not a valid tuple"
        assert(isinstance(point2, tuple)), "point2 is not a valid tuple"
        assert(len(point1) == 2), "point1 is not a valid tuple"
        assert(len(point2) == 2), "point2 is not a valid tuple"
        for item in point1:
            assert(isinstance(item, int)), "point1 is not a valid tuple"
        for item in point2:
            assert(isinstance(item, int)), "point2 is not a valid tuple"
        #Assert validity of units_to_distance
        assert(isinstance(units_to_distance, (int, float))), ("units_to_"
                                                               "distance "
                                                               "must be an int"
                                                               " or a float")
        #Assert validity of scale_orientation
        assert(scale_orientation == "Vertical"
               or scale_orientation == "Horizontal"), ("scale_orientation must"
                                                       ' be either "Vertical"'
                                                       ' or "Horizontal"')
        #Assert validity of scale_units_length
        assert(isinstance(scale_length_units, (int, float))), ("scale_units_"
                                                                "length must "
                                                                "be an int or "
                                                                "a float")
        self._scale = _RoomScale(point1, point2, units_to_distance,
                                 scale_orientation, scale_length_units)

    def set_scale(self, scale):
        """Sets the instance variable _scale to the provided _RoomScale object.


        Keyword argument:

        scale -- The _RoomScale object to set _scale to.
        """
        assert(isinstance(scale, _RoomScale)), ("scale must be of type "
                                                "_RoomScale.")
        self._scale = scale

    def get_scale(self):
        """Returns the _RoomScale object stored in the instance variable
        _scale.
        """
        return self._scale

    def set_new_chair_types(self, list_of_points, img):
        """Creates a new list of _ChairType objects and sets the instance
        variable _chair_types to it.


        Keyword arguments:

        list_of_points -- A list of (int, int) pair tuples representing
        coordinates within img. list_of_points must have a length divisible by
        2. Every 2 tuples within list_of_points should be the coordinates to 2
        diagonally opposite corners of a rectangle bounding a unique chair
        orientation within img.

        img -- The image that the chair orientations of the _ChairType objects
        reside in.
        """
        assert(isinstance(list_of_points, list)), ("list_of_points must be a "
                                                   "list of tuples "
                                                   "representing points.")
        assert(len(list_of_points) % 2 == 0), ("list_of_points must have an "
                                               "even number of points.")
        for point in list_of_points:
            assert(isinstance(point, tuple)), ("list_of_points must be a list "
                                               "of tuples representing points."
                                               )
            assert(len(point) == 2), ("list_of_points must be a list of tuples"
                                      " representing points.")
            for item in point:
                assert(isinstance(item, int)), ("Tuple in list_of_points is "
                                                "invalid. every tuple must "
                                                "contain 2 ints.")
        chairs = []
        for r in range(len(list_of_points) // 2):
            ch = _ChairType(list_of_points[2 * r], list_of_points[2 * r + 1],
                            img)
            chairs.append(ch)
        self._chair_types = chairs

    def set_chair_types(self, list_of_chair_types):
        """Sets the instance variable _chair_types to the provided list of
        _ChairType objects.


        Keyword argument:

        list_of_chair_types -- The list of _ChairType objects to set
        _chair_types to.
        """
        assert(isinstance(list_of_chair_types, list)), ("list_of_chair_types "
                                                        "must be a list of "
                                                        "_ChairType objects.")
        for chair_type in list_of_chair_types:
            assert(isinstance(chair_type, _ChairType)), ("list_of_chair_types "
                                                         "must be a list of "
                                                         "_ChairType objects.")
        self._chair_types = list_of_chair_types

    def get_chair_types(self):
        """Returns the list of _ChairType objects stored in _chair_types."""
        return self._chair_types

    def set_chair_polys(self, list_of_chair_polys):
        """Sets the instance variable _chair_polys to the provided list of
        _ChairPoly objects.


        Keyword argument:

        list_of_chair_polys -- The list of _ChairPoly objects to set
        _chair_types to. Every _ChairPoly object in list_of_chair_polys must
        have a chair_type within the _chair_types instance variable of the
        RoomInfo object.
        """
        assert(isinstance(list_of_chair_polys, list)), ("list_of_chair_polys "
                                                         "must be a list of "
                                                         "_ChairPoly objects.")
        for chair_poly in list_of_chair_polys:
             assert(isinstance(chair_poly, _ChairPoly)), ("list_of_chair_polys"
                                                          " must be a list of "
                                                          "_ChairPoly objects."
                                                          )
        has_valid_chair_type = False
        for chair_type in self._chair_types:
            if chair_poly.chair_type == chair_type:
                has_valid_chair_type = True
        assert(has_valid_chair_type), ("_ChairPoly object in list_of_chair"
                                       "_polys has invalid chair_type.")
        self._chair_polys = list_of_chair_polys

    def get_chair_polys(self):
        """Returns the list of _ChairPoly objects stored in _chair_polys."""
        return self._chair_polys

    def set_chairs(self, list_of_chairs):
        """Sets the instance variable _chairs to the provided list of _Chair
        objects.


        Keyword argument:

        list_of_chairs -- The list of _Chair objects to set _chairs to. Every
        _Chair object in list_of_chairs must have a chair_poly in the RoomInfo
        instance variable _chair_polys.
        """
        assert(isinstance(list_of_chairs, list)), ("list_of_chairs must be a "
                                                    "list of _Chair objects.")
        for chair in list_of_chairs:
             assert(isinstance(chair, _Chair)), ("list_of_chairs must be a list"
                                                 " of _Chair objects.")
             has_valid_chair_poly = False
             for chair_poly in self._chair_polys:
                 if chair.chair_poly == chair_poly:
                     has_valid_chair_poly = True
             assert(has_valid_chair_poly), ("_Chair object in list_of_chairs "
                                            "has invalid chair_poly.")
        self._chairs = list_of_chairs

    def get_chairs(self):
        """Returns the list of _Chair objects stored in _chairs."""
        return self._chairs

    def add_chair(self, chair):
        """Adds the chair _Chair object to the instance variable _chairs.


        Keyword argument:

        chair -- The _Chair object to add to _chairs. chair.chair_poly must be
        in the RoomInfo instance variable _chair_polys.
        """
        assert(isinstance(chair, _Chair)), ("chair must be a _Chair object.")
        has_valid_chair_poly = False
        for chair_poly in self._chair_polys:
            if chair.chair_poly == chair_poly:
                has_valid_chair_poly = True
        assert(has_valid_chair_poly), ("_Chair object has invalid chair_poly.")
        self._chairs.append(chair)

    def remove_chair(self, chair):
        """Removes the chair _Chair object from the instance variable _chairs.


        Keyword argument:

        chair -- The _Chair object to remove from _chairs. chair must be in
        _chairs.
        """
        assert(isinstance(chair, _Chair)), ("chair must be a _Chair object.")
        in_chairs = False
        for included_chair in self._chairs:
            if chair == included_chair:
                in_chairs = True
        assert(in_chairs), "chair must be in _chairs."
        self._chairs.remove(chair)

    def set_chairs_in_sol(self, list_of_chairs):
        """Sets the instance variable _chairs_in_solution to the provided list
        of _Chair objects.


        Keyword argument:

        list_of_chairs -- The list of _Chair objects to set _chairs_in_solution
        to. Every _Chair object in list_of_chairs must be in the RoomInfo
        instance variable _chairs.
        """
        assert(isinstance(list_of_chairs, list)), ("list_of_chairs must be a "
                                                   "list of _Chair objects.")
        for chair in list_of_chairs:
            assert(isinstance(chair, _Chair)), ("list_of_chairs must be a list"
                                                " of _Chair objects.")
            is_in_chairs = False
            for graph_chair in self._chairs:
                if chair == graph_chair:
                    is_in_chairs = True
            assert(is_in_chairs), ("Chair in list_of_chairs is not a part of "
                                   "graph.")
        self._chairs_in_solution = list_of_chairs

    def get_chairs_in_sol(self):
        """Returns the list of _Chair objects stored in _chairs_in_solution."""
        return _chairs_in_solution

    def get_completions(self):
        """Returns the dict containing information on completed input methods
        stored in _completions.
        """
        return self._completions

    def set_completions(self, completions_dict):
        """Sets the instance variable _completions to the provided dict
        completions_dict.

        Keyword argument:
        completions_dict -- A dict of the same length and keys as _completions.
        All values in completions_dict must also be True or False bools.
        """
        assert(isinstance(completions_dict, dict)), ("completions_dict must be"
                                                     " a dict.")
        assert(len(completions_dict)
               == self._completions_length), ("completions_dict must be the "
                                              "same length as the original "
                                              "_completions dictionary.")
        assert(completions_dict.keys()
               == self._completions.keys()), ("completions_dict must have the "
                                              "same keys as _completions.")
        for value in completions_dict.values():
            assert(isinstance(value, bool)), ("values in completions_dict must"
                                              " be True or False booleans.")
        self._completions = completions_dict
