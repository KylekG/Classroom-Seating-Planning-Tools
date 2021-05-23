import cv2
import input as cpi
import numpy as np

AVAILABLE_COLOR = (0, 0, 0)
UNAVAILABLE_COLOR = (150, 150, 150)
COMPLETED_COLOR = (0, 255, 0)
NOT_COMPLETED_COLOR = (0, 0, 255)
COMPLETED_TEXT = "Completed"
NOT_COMPLETED_TEXT = "Not Completed"
NOT_COMPLETED_X_ADJUST = 12
COMPLETED_X_ADJUST = 36
BUTTON_THICKNESS = 5

GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (0, 0, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

SCALE_SELECT_BUTTON_START_PT = (470, 65)
SCALE_SELECT_BUTTON_END_PT = (670, 115)
SCALE_SELECT_BUTTON_BL = (75, 100)

CHAIR_SELECT_BUTTON_START_PT = (470, 165)
CHAIR_SELECT_BUTTON_END_PT = (670, 215)
CHAIR_SELECT_BUTTON_BL = (75, 200)

POLY_CREATE_BUTTON_START_PT = (470, 265)
POLY_CREATE_BUTTON_END_PT = (670, 315)
POLY_CREATE_BUTTON_BL = (75, 300)

CHAIR_RECOGNITION_BUTTON_START_PT = (470, 365)
CHAIR_RECOGNITION_BUTTON_END_PT = (670, 415)
CHAIR_RECOGNITION_BUTTON_BL = (75, 400)

CHAIR_ADDITION_BUTTON_START_PT = (470, 465)
CHAIR_ADDITION_BUTTON_END_PT = (670, 515)
CHAIR_ADDITION_BUTTON_BL = (75, 500)

CHAIR_DELETION_BUTTON_START_PT = (470, 565)
CHAIR_DELETION_BUTTON_END_PT = (670, 615)
CHAIR_DELETION_BUTTON_BL = (75, 600)

INPUT_PREVIEW_BUTTON_START_PT = (470, 665)
INPUT_PREVIEW_BUTTON_END_PT = (670, 715)
INPUT_PREVIEW_BUTTON_BL = (75, 700)

SOLVE_BUTTON_START_PT = (470, 765)
SOLVE_BUTTON_END_PT = (670, 815)
SOLVE_BUTTON_BL = (75, 800)


class MenuButton():
    """MenuButton is a class used to create the buttons in the menu given to
    the user. Each button stores information on its position, its completion
    status, the buttons it is dependent on in order to be made available to the
    user, its name, and the corresponding input callback to its name. Using the
    methods for MenuButton, it is possible to verify whether or not a button is
    elligible to be run, check if a button has been clicked, run the input
    callback stored in the buttton, and update the completion status of the
    button.


    Instance variables:

    text_BL -- An (int,int) tuple representing the bottom left corner for
    where to write the button text.

    points -- An array of 4 (int, int) tuples representing the coordinates
    of the corners of the button.

    dependencies -- An array of MenuButton instances that need to be
    completed before the button should be run.

    input_callback -- The input callback tied to the button. This should
    be a function that corresponds to title_text and takes only
    (non_writable_img, menu_refresh, window_name, room_info) as its keyword
    arguments. non_writable_img should be a cv2 image of the room diagram. Not
    meant to be written on by the code. menu_refresh should be a list that will
    be appended to upon completion of the function. window_name should be the
    name (string) of the cv2 window for the function to use. And room_info
    should be the RoomInfo instance being used to keep track of input
    information.

    completed -- A bool representing whether or not the button has been
    completed by the user.

    title_text -- A string storing the text that should be written on the
    button.

    completions_key -- The key corresponding to the input callback for the
    button used in the completions_dict in the RoomInfo instance being used to
    keep track of tasks completed by the user.


    Public Methods:

    draw -- A method to draw the button in a provided image.

    try_run_callback -- A method to run the callback if dependencies have been
    completed.

    check_click -- A method to check if the coords provided constitute a valid
    button click.

    update_completion_status -- A method to update the completion status of a
    button.

    mark_as_completed -- A method to update the completions_dict used to keep
    track of completions with the completion of the button.
    """

    def __init__(self, text_BL, point1, point2, dependencies, input_callback,
                 title_text, completions_key):
        """ The constructor for the MenuButton class.


        Keyword Arguments:

        text_BL -- An (int,int) tuple representing the bottom left corner for
        where to write the button text.

        point1 -- An (int,int) tuple representing a corner of the button.

        point2 -- An (int,int) tuple representing the corner of the button
        opposite to point1.

        dependencies -- An array of MenuButton instances that need to be
        completed before the input_callback of the button should be run.

        input_callback -- The input callback tied to the button. This should
        be a function that corresponds to title_text and takes only
        (non_writable_img, menu_refresh, window_name, room_info) as its keyword
        arguments. non_writable_img should be a cv2 image of the room diagram.
        Not meant to be written on by the code. menu_refresh should be a list
        that will be appended to upon completion of the function. window_name
        should be the name (string) of the cv2 window for the function to use.
        And room_info should be the RoomInfo instance being used to keep track
        of input information.

        title_text -- A string storing the text that should be written on the
        button.

        completions_key -- The key corresponding to the input callback for the
        button used in the completions_dict in the RoomInfo instance being used
        to keep track of tasks completed by the user.
        """
        assert(isinstance(text_BL, tuple)), "text_BL is not a valid tuple"
        assert(isinstance(point1, tuple)), "point1 is not a valid tuple"
        assert(isinstance(point2, tuple)), "point2 is not a valid tuple"
        assert(len(text_BL) == 2), "text_BL is not a valid tuple"
        assert(len(point1) == 2), "point1 is not a valid tuple"
        assert(len(point2) == 2), "point2 is not a valid tuple"
        for item in text_BL:
            assert(isinstance(item, int)), "text_BL is not a valid tuple"
        for item in point1:
            assert(isinstance(item, int)), "point1 is not a valid tuple"
        for item in point2:
            assert(isinstance(item, int)), "point2 is not a valid tuple"
        assert(isinstance(dependencies, list)), ("dependencies must be a list"
                                                 " of other MenuButton "
                                                 "instances.")
        for item in dependencies:
            assert(isinstance(item, MenuButton)), ("dependencies must be a "
                                                   "list of other MenuButton "
                                                   "instances.")
            assert(item != self), ("A button cannot be dependent on itself.")
        assert(isinstance(title_text,str)), ("title_text must be a string.")
        #TODO assert completions_key is in room_info.completions
        #TODO: assert input_callback is a callable function.
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
        self.text_BL = text_BL
        self.points = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
        self.dependencies = dependencies
        self.input_callback = input_callback
        self.completed = False
        self.title_text = title_text
        self.completions_key = completions_key

    def draw(self, generated_img):
        """ The draw method for the MenuButton class. Calling this correctly
        draws the button in the provided image.


        Keyword Argument:

        generated_img -- the cv2 image to draw the button in.
        """
        text_color = AVAILABLE_COLOR
        if self.completed:
            button_color = COMPLETED_COLOR
            status_text = COMPLETED_TEXT
            write_pt = (self.points[0][0] + COMPLETED_X_ADJUST,
                        self.text_BL[1])
        else:
            button_color = NOT_COMPLETED_COLOR
            status_text = NOT_COMPLETED_TEXT
            write_pt = (self.points[0][0] + NOT_COMPLETED_X_ADJUST,
                        self.text_BL[1])
        for button in self.dependencies:
            if not button.completed:
                text_color = UNAVAILABLE_COLOR
                button_color = UNAVAILABLE_COLOR

        generated_img = cv2.rectangle(generated_img, self.points[0],
                                      self.points[2], button_color,
                                      BUTTON_THICKNESS)
        generated_img = cv2.putText(generated_img, self.title_text,
                                    self.text_BL, cv2.FONT_HERSHEY_SIMPLEX,
                                    0.75, text_color, 1, cv2.LINE_AA)
        generated_img = cv2.putText(generated_img, status_text, write_pt,
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color,
                                    1, cv2.LINE_AA)

    def try_run_callback(self, non_writable_img, menu_refresher, window_name,
                         room_info):
        """ A method used to try and run the input_callback of the button. This
        method will run the input_callback function for the button if all of
        the buttons designated in the button's dependencies have been
        completed.


        Keyword arguments:

        non_writable_img -- A cv2 image of the room diagram. Not meant to be
        written on by the code.

        menu_refresher -- A list that will be appended to upon completion of
        the function.

        window_name -- The name (string) of the cv2 window for the function to
        use.

        room_info -- The RoomInfo instance being used to keep track of input
        information.

        """
        for button in self.dependencies:
            if not button.completed:
                return
        self.input_callback(non_writable_img, menu_refresher, window_name,
                            room_info)

    def check_click(self, coords):
        """ Checks to see if the provided coords can click the button. Returns
        True if coords is within the button rectangle from points, and all
        buttons in dependencies have been marked as completed.


        Keyword argument:

        coords -- An (int, int) tuple to check the validity for.
        """
        if (coords[0] > self.points[0][0]
            and coords[0] < self.points[2][0]
            and coords[1] > self.points[0][1]
            and coords[1] < self.points[2][1]):
            for button in self.dependencies:
                if not button.completed:
                    return
            return True

    def update_completion_status(self, room_info):
        """ Updates the completion status for the button.


        Keyword argument:

        room_info -- The RoomInfo instance being used to keep track of progress
        on the room.
        """
        if (room_info.get_completions()[self.completions_key]):
            self.completed = True
        else:
            self.completed = False

    def mark_as_completed(self, room_info, menu_buttons):
        """ Updates the completion status stored in the completions_dict in the
        RoomInfo instance provided to reflect the completion of the button.
        This method will mark all buttons dependent on the button the method is
        being called from as not being completed, then mark the button as
        completed.


        Keyword arguments:

        room_info -- The RoomInfo instance being used to keep track of progress
        on the room.

        menu_buttons -- A list of all of the MenuButton instances.
        """
        completions_copy = room_info.get_completions().copy()
        for button in menu_buttons:
            for dependent_button in button.dependencies:
                if dependent_button == self:
                    completions_copy[button.completions_key] = False
        completions_copy[self.completions_key] = True
        room_info.set_completions(completions_copy)


class _MenuInformation:
    """A class to store information for the menu to function properly.


    Instance variable:

    menu_tasks -- A list to keep track of queued tasks by the user. Any time a
    user wants to do an input step, the clicked button is added to the list.
    """
    
    def __init__(self):
        """Initializes an instance of the menu information class.
        """
        self.menu_tasks = []


scale_select_button = MenuButton(SCALE_SELECT_BUTTON_BL,
                                 SCALE_SELECT_BUTTON_END_PT,
                                 SCALE_SELECT_BUTTON_START_PT, [],
                                 cpi.scale_selection,
                                 "Scale pixels to distance:",
                                 "Scale Selection Status")
chair_select_button = MenuButton(CHAIR_SELECT_BUTTON_BL,
                                 CHAIR_SELECT_BUTTON_START_PT,
                                 CHAIR_SELECT_BUTTON_END_PT, [],
                                 cpi.chair_type_selection,
                                 "Chair Type Selection:",
                                 "Chair Type Selection Status")
poly_create_button = MenuButton(POLY_CREATE_BUTTON_BL,
                                POLY_CREATE_BUTTON_START_PT,
                                POLY_CREATE_BUTTON_END_PT,
                                [chair_select_button],
                                cpi.polygon_creation, "Polygon Creation:",
                                "Polygon Creation Status")
chair_recognition_button = MenuButton(CHAIR_RECOGNITION_BUTTON_BL,
                                      CHAIR_RECOGNITION_BUTTON_START_PT,
                                      CHAIR_RECOGNITION_BUTTON_END_PT,
                                      [chair_select_button,
                                       poly_create_button],
                                      cpi.chair_recognition,
                                      "Chair Recognition:",
                                      "Chair Recognition Status")
chair_addition_button = MenuButton(CHAIR_ADDITION_BUTTON_BL,
                                   CHAIR_ADDITION_BUTTON_START_PT,
                                   CHAIR_ADDITION_BUTTON_END_PT,
                                   [chair_select_button, poly_create_button,
                                    chair_recognition_button],
                                   cpi.chair_addition, "Chair Addition:",
                                   "Chair Addition Status")
chair_deletion_button = MenuButton(CHAIR_DELETION_BUTTON_BL,
                                   CHAIR_DELETION_BUTTON_START_PT,
                                   CHAIR_DELETION_BUTTON_END_PT,
                                   [chair_select_button, poly_create_button,
                                    chair_recognition_button],
                                   cpi.chair_deletion, "Chair Deletion:",
                                   "Chair Deletion Status")
input_preview_button = MenuButton(INPUT_PREVIEW_BUTTON_BL,
                                  INPUT_PREVIEW_BUTTON_START_PT,
                                  INPUT_PREVIEW_BUTTON_END_PT,
                                  [scale_select_button, chair_select_button,
                                   poly_create_button,
                                   chair_recognition_button],
                                  cpi.input_preview, "Input Preview:",
                                  "Input Confirmation Status")
solve_room_button = MenuButton(SOLVE_BUTTON_BL, SOLVE_BUTTON_START_PT,
                               SOLVE_BUTTON_END_PT,
                               [scale_select_button, chair_select_button,
                                poly_create_button, chair_recognition_button,
                                input_preview_button],
                               cpi.solve_room, "Solve Room:",
                               "Solve Room Status")
menu_buttons = [scale_select_button, chair_select_button, poly_create_button,
                chair_recognition_button, chair_addition_button,
                chair_deletion_button, input_preview_button, solve_room_button]


def __get_menu_click_coords(event, x, y, flags, menu_info):
    """The private callback for mouse events in the cv2 window for the main
    menu of the tool. On right click within the button for an input method,
    will add the button to menu_info.menu_tasks if its dependencies have been
    completed.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        for button in menu_buttons:
            if(button.check_click((x,y))):
                menu_info.menu_tasks.append(button)

def __draw_menu(screen_height, screen_width):
    """Helper function used to draw the menu.

    Keyword arguments:

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """

    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)

    for button in menu_buttons:
        button.draw(generated_img)

    return generated_img

def main_menu(screen_height, screen_width, room_type, room_info, window_name,
              non_writable_img):
    """This function handles the menu of the classroom solving tool. First, the
    function generates an image of the menu and has the cv2 window display it.
    Whenever a click is detected within the window, the function checks to see
    if the click occured within a button with completed task prerequisites. If
    it did, then the function adds the task to a list in order to have the
    task's function called later on in the code. Otherwise, the click does
    nothing. This function checks that list repeatedly until a task has been
    added or the key 'E' has been pressed to terminate the function. When a
    task has been added to the list, the function calls the function for that
    task and updates both room_info and menu_info's completions dicts to
    reflect both the completion of the task and the undoing of the completion
    of all tasks that rely on the information provided. This is done so that
    all information that has prerequisites must be redone with the information
    from the prerequisites to prevent errors. On the completion of the solve
    and save task, or if the user presses the 'E' key within the menu, the
    function terminates.


    Keyword Arguments:

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    room_type -- The type of room being solved. (Currently not functional.)

    room_info -- The RoomInfo instance being used by the tool to keep track of
    the data for the room.

    window_name -- The name (string) of the cv2 window for the function to use.

    non_writable_img -- The image of the room diagram.
    """
    menu_refresher = ['r']
    menu_info = _MenuInformation()

    generated_img = __draw_menu(screen_height, screen_width)
    cv2.setMouseCallback(window_name, __get_menu_click_coords, menu_info)
    while True:
        if len(menu_refresher) > 0:
            for button in menu_buttons:
                button.update_completion_status(room_info)
            generated_img = __draw_menu(screen_height, screen_width)
            menu_refresher = []
        cv2.imshow(window_name, generated_img)

        if len(menu_info.menu_tasks) > 0:
            menu_info.menu_tasks[0].try_run_callback(non_writable_img,
                                                     menu_refresher,
                                                     window_name,
                                                     room_info)
            menu_info.menu_tasks[0].mark_as_completed(room_info, menu_buttons)
            menu_info.menu_tasks = []
        else:
            cv2.setMouseCallback(window_name, __get_menu_click_coords,
                                 menu_info)
        key = cv2.waitKey(1) & 0xFF

        # if the 'e' key is pressed, break from the loop
        if key == ord("e"):
            cv2.destroyAllWindows()
            break
