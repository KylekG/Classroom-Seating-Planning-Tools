import cv2
import input as cpi
import numpy as np

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

NOT_COMPLETED_X_ADJUST = 12
COMPLETED_X_ADJUST = 36

class _MenuInformation:
    """A class to store information for the menu to function properly.


    Instance variables:

    completions -- A dict with keys representing input methods. Values must be
    True or False booleans to indicate whether or not they have been completed.
    Must mirror room_info.get_completions.

    menu_tasks -- A list to keep track of queued tasks by the user. Any time a
    user wants to do an input step, a string representing the step is added to
    the list.
    """
    def __init__(self, room_info):
        """Initializes an instance of the menu information class.


        Keyword argument:

        room_info -- The RoomInfo instance being used by the tool to keep track
        of information about the room.
        """
        self.completions = room_info.get_completions()
        self.menu_tasks = []

def __get_menu_click_coords(event, x, y, flags, menu_info):
    """The private callback for mouse events in the cv2 window for the main
    menu of the tool. On right click within the button for an input method,
    will add the string representing the input method to menu_info.menu_tasks
    if the necessary prerequisites for the input method have been marked as
    True in menu_info.completions.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        if (x < SCALE_SELECT_BUTTON_END_PT[0]
            and x > SCALE_SELECT_BUTTON_START_PT[0]
            and y < SCALE_SELECT_BUTTON_END_PT[1]
            and y > SCALE_SELECT_BUTTON_START_PT[1]):
            menu_info.menu_tasks.append('Scale Selection')
        elif (x < CHAIR_SELECT_BUTTON_END_PT[0]
              and x > CHAIR_SELECT_BUTTON_START_PT[0]
              and y < CHAIR_SELECT_BUTTON_END_PT[1]
              and y > CHAIR_SELECT_BUTTON_START_PT[1]):
            menu_info.menu_tasks.append('Chair Type Selection')
        elif (x < POLY_CREATE_BUTTON_END_PT[0]
              and x > POLY_CREATE_BUTTON_START_PT[0]
              and y < POLY_CREATE_BUTTON_END_PT[1]
              and y > POLY_CREATE_BUTTON_START_PT[1]
              and menu_info.completions["Chair Type Selection Status"]):
            menu_info.menu_tasks.append('Polygon Creation Selection')
        elif (x < CHAIR_RECOGNITION_BUTTON_END_PT[0]
              and x > CHAIR_RECOGNITION_BUTTON_START_PT[0]
              and y < CHAIR_RECOGNITION_BUTTON_END_PT[1]
              and y > CHAIR_RECOGNITION_BUTTON_START_PT[1]
              and menu_info.completions["Chair Type Selection Status"]):
            menu_info.menu_tasks.append('Chair Recognition Selection')
        elif (x < CHAIR_ADDITION_BUTTON_END_PT[0]
              and x > CHAIR_ADDITION_BUTTON_START_PT[0]
              and y < CHAIR_ADDITION_BUTTON_END_PT[1]
              and y > CHAIR_ADDITION_BUTTON_START_PT[1]
              and menu_info.completions["Chair Recognition Status"]
              and menu_info.completions["Polygon Creation Status"]):
            menu_info.menu_tasks.append("Chair Addition Selection")
        elif (x < CHAIR_DELETION_BUTTON_END_PT[0]
              and x > CHAIR_DELETION_BUTTON_START_PT[0]
              and y < CHAIR_DELETION_BUTTON_END_PT[1]
              and y > CHAIR_DELETION_BUTTON_START_PT[1]
              and menu_info.completions["Chair Recognition Status"]
              and menu_info.completions["Polygon Creation Status"]):
            menu_info.menu_tasks.append("Chair Deletion Selection")
        elif (x < INPUT_PREVIEW_BUTTON_END_PT[0]
              and x > INPUT_PREVIEW_BUTTON_START_PT[0]
              and y < INPUT_PREVIEW_BUTTON_END_PT[1]
              and y > INPUT_PREVIEW_BUTTON_START_PT[1]
              and menu_info.completions["Polygon Creation Status"]
              and menu_info.completions["Chair Recognition Status"]):
            menu_info.menu_tasks.append("Input Preview")
        elif (x < SOLVE_BUTTON_END_PT[0]
              and x > SOLVE_BUTTON_START_PT[0]
              and y < SOLVE_BUTTON_END_PT[1]
              and y > SOLVE_BUTTON_START_PT[1]
              and menu_info.completions["Input Confirmation Status"]):
            menu_info.menu_tasks.append("Solve And Save")

def __draw_scale_selection_button(menu_info, generated_img, not_complete_color,
                                  complete_color, available_color,
                                  button_thickness):
    """Helper function used to draw the button for the scale selection input
    method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button's text in.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if not menu_info.completions["Scale Selection Status"]:
        scale_selection_button_color = not_complete_color
        scale_selection_status = "Not Completed"
        scale_selection_status_write_point = ((SCALE_SELECT_BUTTON_START_PT[0]
                                               + NOT_COMPLETED_X_ADJUST),
                                              SCALE_SELECT_BUTTON_BL[1])
    else:
        scale_selection_button_color = complete_color
        scale_selection_status = "Completed"
        scale_selection_status_write_point = ((SCALE_SELECT_BUTTON_START_PT[0]
                                               + COMPLETED_X_ADJUST),
                                              SCALE_SELECT_BUTTON_BL[1])
    generated_img = cv2.rectangle(generated_img, SCALE_SELECT_BUTTON_START_PT,
                                  SCALE_SELECT_BUTTON_END_PT,
                                  scale_selection_button_color,
                                  button_thickness)
    generated_img = cv2.putText(generated_img, "Scale pixels to distance:",
                                SCALE_SELECT_BUTTON_BL,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                available_color, 1, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, scale_selection_status,
                                scale_selection_status_write_point,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                available_color, 1, cv2.LINE_AA)

def __draw_chairtype_selection_button(menu_info, generated_img,
                                      not_complete_color,
                                      complete_color, available_color,
                                      button_thickness):
    """Helper function used to draw the button for the chair type selection
    input method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button's text in.

    button_thickness -- The thickness to use when drawing the button's edges.
    """

    if not menu_info.completions["Chair Type Selection Status"]:
        chair_selection_button_color = not_complete_color
        chair_selection_status = "Not Completed"
        chair_selection_status_write_point = ((CHAIR_SELECT_BUTTON_START_PT[0]
                                               + NOT_COMPLETED_X_ADJUST),
                                              CHAIR_SELECT_BUTTON_BL[1])
    else:
        chair_selection_button_color = complete_color
        chair_selection_status = "Completed"
        chair_selection_status_write_point = ((CHAIR_SELECT_BUTTON_START_PT[0]
                                               + COMPLETED_X_ADJUST),
                                              CHAIR_SELECT_BUTTON_BL[1])
    generated_img = cv2.rectangle(generated_img, CHAIR_SELECT_BUTTON_START_PT,
                                  CHAIR_SELECT_BUTTON_END_PT,
                                  chair_selection_button_color,
                                  button_thickness)
    generated_img = cv2.putText(generated_img, "Chair Type Selection:",
                                CHAIR_SELECT_BUTTON_BL,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                available_color, 1, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, chair_selection_status,
                                chair_selection_status_write_point,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                available_color, 1, cv2.LINE_AA)

def __draw_polygon_creation_selection_button(menu_info, generated_img,
                                             not_complete_color,
                                             complete_color, available_color,
                                             unavailable_color,
                                             button_thickness):
    """Helper function used to draw the button for the polygon creation input
    method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have been met.

    unavailable_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have not been met.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if menu_info.completions["Polygon Creation Status"]:
        poly_creation_button_color = complete_color
        poly_creation_status = "Completed"
        poly_creation_status_write_point = ((POLY_CREATE_BUTTON_START_PT[0]
                                             + COMPLETED_X_ADJUST),
                                            POLY_CREATE_BUTTON_BL[1])
    else:
        poly_creation_button_color = not_complete_color
        poly_creation_status = "Not Completed"
        poly_creation_status_write_point = ((POLY_CREATE_BUTTON_START_PT[0]
                                             + NOT_COMPLETED_X_ADJUST),
                                            POLY_CREATE_BUTTON_BL[1])
    if menu_info.completions["Chair Type Selection Status"]:
        text_color = available_color
    else:
        text_color = unavailable_color
        poly_creation_button_color = unavailable_color
    generated_img = cv2.rectangle(generated_img,
                                  POLY_CREATE_BUTTON_START_PT,
                                  POLY_CREATE_BUTTON_END_PT,
                                  poly_creation_button_color, button_thickness)
    generated_img = cv2.putText(generated_img, "Polygon Creation:",
                                POLY_CREATE_BUTTON_BL,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, poly_creation_status,
                                poly_creation_status_write_point,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                cv2.LINE_AA)

def __draw_chair_recognition_selection_button(menu_info, generated_img,
                                              not_complete_color,
                                              complete_color, available_color,
                                              unavailable_color,
                                              button_thickness):
    """Helper function used to draw the button for the chair recognition input
    method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have been met.

    unavailable_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have not been met.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if menu_info.completions["Chair Recognition Status"]:
        recognition_button_color = complete_color
        recognition_status = "Completed"
        recognition_status_write_point = ((CHAIR_RECOGNITION_BUTTON_START_PT[0]
                                           + COMPLETED_X_ADJUST),
                                          CHAIR_RECOGNITION_BUTTON_BL[1])
    else:
        recognition_button_color = not_complete_color
        recognition_status = "Not Completed"
        recognition_status_write_point = ((CHAIR_RECOGNITION_BUTTON_START_PT[0]
                                           + NOT_COMPLETED_X_ADJUST),
                                          CHAIR_RECOGNITION_BUTTON_BL[1])
    if menu_info.completions['Polygon Creation Status']:
        text_color = available_color
    else:
        text_color = unavailable_color
        recognition_button_color = unavailable_color
    generated_img = cv2.rectangle(generated_img,
                                 CHAIR_RECOGNITION_BUTTON_START_PT,
                                 CHAIR_RECOGNITION_BUTTON_END_PT,
                                 recognition_button_color, button_thickness)
    generated_img = cv2.putText(generated_img, "Chair Recognition:",
                               CHAIR_RECOGNITION_BUTTON_BL,
                               cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                               cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, recognition_status,
                                 recognition_status_write_point,
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                 cv2.LINE_AA)

def __draw_chair_addition_selection_button(menu_info, generated_img,
                                           not_complete_color, complete_color,
                                           available_color, unavailable_color,
                                           button_thickness):
    """Helper function used to draw the button for the chair addition input
    method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have been met.

    unavailable_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have not been met.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if menu_info.completions["Chair Addition Status"]:
        addition_button_color = complete_color
        addition_status = "Completed"
        addition_status_write_point = ((CHAIR_ADDITION_BUTTON_START_PT[0]
                                        + COMPLETED_X_ADJUST),
                                       CHAIR_ADDITION_BUTTON_BL[1])
    else:
        addition_button_color = not_complete_color
        addition_status = "Not Completed"
        addition_status_write_point = ((CHAIR_ADDITION_BUTTON_START_PT[0]
                                        + NOT_COMPLETED_X_ADJUST),
                                       CHAIR_ADDITION_BUTTON_BL[1])
    if menu_info.completions["Chair Recognition Status"]:
        text_color = available_color
    else:
        text_color = unavailable_color
        addition_button_color = unavailable_color
    generated_img = cv2.rectangle(generated_img,
                                  CHAIR_ADDITION_BUTTON_START_PT,
                                  CHAIR_ADDITION_BUTTON_END_PT,
                                  addition_button_color, button_thickness)
    generated_img = cv2.putText(generated_img, "Chair Addition:",
                                CHAIR_ADDITION_BUTTON_BL,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, addition_status,
                                addition_status_write_point,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                cv2.LINE_AA)

def __draw_chair_deletion_selection_button(menu_info, generated_img,
                                           not_complete_color, complete_color,
                                           available_color, unavailable_color,
                                           button_thickness):
    """Helper function used to draw the button for the chair deletion input
    method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have been met.

    unavailable_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have not been met.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if menu_info.completions["Chair Deletion Status"]:
        deletion_button_color = complete_color
        deletion_status = "Completed"
        deletion_status_write_point = ((CHAIR_DELETION_BUTTON_START_PT[0]
                                        + COMPLETED_X_ADJUST),
                                       CHAIR_DELETION_BUTTON_BL[1])
    else:
        deletion_button_color = not_complete_color
        deletion_status = "Not Completed"
        deletion_status_write_point = ((CHAIR_DELETION_BUTTON_START_PT[0]
                                        + NOT_COMPLETED_X_ADJUST),
                                       CHAIR_DELETION_BUTTON_BL[1])
    if menu_info.completions["Chair Recognition Status"]:
        text_color = available_color
    else:
        text_color = unavailable_color
        deletion_button_color = unavailable_color
    generated_img = cv2.rectangle(generated_img,
                                  CHAIR_DELETION_BUTTON_START_PT,
                                  CHAIR_DELETION_BUTTON_END_PT,
                                  deletion_button_color, button_thickness)
    generated_img = cv2.putText(generated_img, "Chair Deletion:",
                                CHAIR_DELETION_BUTTON_BL,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, deletion_status,
                                deletion_status_write_point,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                cv2.LINE_AA)

def __draw_input_confirmation_selection_button(menu_info, generated_img,
                                               not_complete_color,
                                               complete_color, available_color,
                                               unavailable_color,
                                               button_thickness):
    """Helper function used to draw the button for the input confirmation
    method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    available_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have been met.

    unavailable_color -- The BGR tuple color to draw the button and its text in
    if the task's prerequisites have not been met.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if menu_info.completions["Input Confirmation Status"]:
        input_preview_button_color = complete_color
        confirmation_status = "Completed"
        confirmation_status_write_point = ((INPUT_PREVIEW_BUTTON_START_PT[0]
                                            + COMPLETED_X_ADJUST),
                                           INPUT_PREVIEW_BUTTON_BL[1])
    else:
        input_preview_button_color = not_complete_color
        confirmation_status = "Not Completed"
        confirmation_status_write_point = ((INPUT_PREVIEW_BUTTON_START_PT[0]
                                            + NOT_COMPLETED_X_ADJUST),
                                           INPUT_PREVIEW_BUTTON_BL[1])
    if menu_info.completions["Chair Recognition Status"]:
        text_color = available_color
    else:
        text_color = unavailable_color
        input_preview_button_color = unavailable_color
    generated_img = cv2.rectangle(generated_img, INPUT_PREVIEW_BUTTON_START_PT,
                                  INPUT_PREVIEW_BUTTON_END_PT,
                                  input_preview_button_color, button_thickness)
    generated_img = cv2.putText(generated_img, "Input Confirmation:",
                                 INPUT_PREVIEW_BUTTON_BL,
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                 cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, confirmation_status,
                                 confirmation_status_write_point,
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.75, text_color, 1,
                                 cv2.LINE_AA)

def __draw_solve_and_save_button(menu_info, generated_img, not_complete_color,
                                 available_color, unavailable_color,
                                 button_thickness):
    """Helper function used to draw the button for the solve and save method.


    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    generated_img -- The image to draw the button in.

    not_complete_color -- The BGR Tuple color to draw the button in if the task
    has not been completed.

    complete_color -- The BGR tuple color to draw the button in if the task has
    been completed.

    unavailable_color -- The BGR tuple color to draw the button and its text
    in.

    button_thickness -- The thickness to use when drawing the button's edges.
    """
    if menu_info.completions["Input Confirmation Status"]:
        solve_button_color = not_complete_color
        text_color = available_color
    else:
        solve_button_color = unavailable_color
        text_color = unavailable_color
    solve_write_point = ((SOLVE_BUTTON_START_PT[0] + NOT_COMPLETED_X_ADJUST),
                         SOLVE_BUTTON_BL[1])
    generated_img = cv2.rectangle(generated_img, SOLVE_BUTTON_START_PT,
                                  SOLVE_BUTTON_END_PT, solve_button_color,
                                  button_thickness)
    generated_img = cv2.putText(generated_img, "Solve and Save Room:",
                                SOLVE_BUTTON_BL, cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, text_color, 1, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, "Not Completed",
                                solve_write_point, cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, text_color, 1, cv2.LINE_AA)

def __draw_menu(menu_info, not_complete_color, complete_color, available_color,
                unavailable_color, button_thickness, screen_height,
                screen_width):
    """Helper function used to draw the menu.

    Keyword arguments:

    menu_info -- The _MenuInformation instance being used by the menu.

    not_complete_color -- The BGR Tuple color to draw buttons in if their tasks
    has not been completed.

    complete_color -- The BGR Tuple color to draw buttons in if their tasks
    have been completed.

    available_color -- The BGR tuple color to draw buttons in if their
    prerequisites have been met.

    unavailable_color -- The BGR tuple color to draw buttons in if their
    prerequisites have not been met.

    button_thickness -- The thickness to use when drawing the button's edges.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)

    __draw_scale_selection_button(menu_info, generated_img, not_complete_color,
                                  complete_color, available_color,
                                  button_thickness)
    __draw_chairtype_selection_button(menu_info, generated_img,
                                      not_complete_color, complete_color,
                                      available_color, button_thickness)
    __draw_polygon_creation_selection_button(menu_info, generated_img,
                                             not_complete_color,
                                             complete_color, available_color,
                                             unavailable_color,
                                             button_thickness)
    __draw_chair_recognition_selection_button(menu_info, generated_img,
                                              not_complete_color,
                                              complete_color, available_color,
                                              unavailable_color,
                                              button_thickness)
    __draw_chair_addition_selection_button(menu_info, generated_img,
                                           not_complete_color, complete_color,
                                           available_color, unavailable_color,
                                           button_thickness)
    __draw_chair_deletion_selection_button(menu_info, generated_img,
                                           not_complete_color, complete_color,
                                           available_color, unavailable_color,
                                           button_thickness)
    __draw_input_confirmation_selection_button(menu_info, generated_img,
                                               not_complete_color,
                                               complete_color, available_color,
                                               unavailable_color,
                                               button_thickness)
    __draw_solve_and_save_button(menu_info, generated_img, not_complete_color,
                                 available_color, unavailable_color,
                                 button_thickness)
    return generated_img

def main_menu(screen_height, screen_width, room_type, room_info,
             save_to_json, json_save_name, scale_units_length,
             units_to_distance, scale_orientation, chair_scale, solution_name,
             sol_dpi, finding_threshold, show_instr, window_name, dot_size,
             height, width, non_writable_img):
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

    window_name -- The name (string) of the cv2 window for the function to use.

    dot_size -- The size (int) to use when drawing dots.

    height -- The height (int) to make the window.

    width -- The width (int) to make the window.

    non_writable_img --
    """
    menu_refresher = ['r']
    menu_info = _MenuInformation(room_info)

    button_thickness = 5
    available_color = BLACK
    unavailable_color = GRAY
    not_complete_color = RED
    complete_color = GREEN

    generated_img = __draw_menu(menu_info, not_complete_color, complete_color,
                                available_color, unavailable_color,
                                button_thickness, screen_height, screen_width)
    cv2.setMouseCallback(window_name, __get_menu_click_coords, menu_info)
    while True:
        if len(menu_refresher) > 0:
            generated_img = __draw_menu(menu_info, not_complete_color,
                                        complete_color, available_color,
                                        unavailable_color, button_thickness,
                                        screen_height, screen_width)
            menu_refresher = []
        cv2.imshow(window_name, generated_img)

        if len(menu_info.menu_tasks) > 0:
            if menu_info.menu_tasks[0] == 'Scale Selection':
                cpi.scale_selection(non_writable_img, menu_refresher,
                                    show_instr, window_name, screen_height,
                                    screen_width, room_info, height, width,
                                    PURPLE, GREEN, scale_orientation,
                                    scale_units_length, units_to_distance)
                menu_info.completions["Scale Selection Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Chair Type Selection':
                menu_info.completions["Polygon Creation Status"] = False
                menu_info.completions["Chair Recognition Status"] = False
                menu_info.completions["Chair Addition Status"] = False
                menu_info.completions["Chair Deletion Status"] = False
                menu_info.completions["Input Confirmation Status"] = False
                cpi.chair_type_selection(non_writable_img, menu_refresher,
                                         show_instr, window_name,
                                         screen_height, screen_width,
                                         room_info, height, width, PURPLE,
                                         GREEN)
                menu_info.completions["Chair Type Selection Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Polygon Creation Selection':
                menu_info.completions["Chair Recognition Status"] = False
                menu_info.completions["Chair Addition Status"] = False
                menu_info.completions["Chair Deletion Status"] = False
                menu_info.completions["Input Confirmation Status"] = False
                cpi.polygon_creation(non_writable_img, menu_refresher,
                                     room_info, show_instr, window_name,
                                     screen_height, screen_width, height,
                                     width, RED, chair_scale, dot_size)
                menu_info.completions["Polygon Creation Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Chair Recognition Selection':
                menu_info.completions["Chair Addition Status"] = False
                menu_info.completions["Chair Deletion Status"] = False
                menu_info.completions["Input Confirmation Status"] = False
                cpi.chair_recognition(non_writable_img, menu_refresher,
                                      room_info, show_instr, window_name,
                                      screen_height, screen_width, height,
                                      width, finding_threshold, RED)
                menu_info.completions["Chair Recognition Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Chair Addition Selection':
                menu_info.completions["Input Confirmation Status"] = False
                cpi.chair_addition(non_writable_img, menu_refresher, room_info,
                                   show_instr, window_name, screen_height,
                                   screen_width, height, width, RED, PURPLE,
                                   GREEN)
                menu_info.completions["Chair Addition Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Chair Deletion Selection':
                menu_info.completions["Input Confirmation Status"] = False
                cpi.chair_deletion(non_writable_img, menu_refresher, window_name,
                                   screen_height, screen_width, room_info,
                                   show_instr, height, width, PURPLE, GREEN,
                                   RED)
                menu_info.completions["Chair Deletion Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Input Preview':
                cpi.input_preview(non_writable_img, menu_refresher, window_name,
                                  screen_height, screen_width, room_info,
                                  show_instr, height, width, RED, PURPLE,
                                  save_to_json, json_save_name)
                menu_info.completions["Input Confirmation Status"] = True
                room_info.set_completions(menu_info.completions)
                menu_info.menu_tasks = []
            elif menu_info.menu_tasks[0] == 'Solve And Save':
                cpi.solve_room(non_writable_img, menu_refresher, show_instr,
                               window_name, screen_height, screen_width,
                               room_info, sol_dpi, solution_name)
                cv2.destroyAllWindows()
                break


        else:
            cv2.setMouseCallback(window_name, __get_menu_click_coords,
                                 menu_info)
        key = cv2.waitKey(1) & 0xFF

        # if the 'e' key is pressed, break from the loop
        if key == ord("e"):
            cv2.destroyAllWindows()
            break
