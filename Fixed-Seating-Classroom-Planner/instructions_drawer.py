import cv2
import numpy as np

INSTRUCT_TEXT_COLOR = (0, 0, 0)
INSTRUCT_TITLE_TEXT_SIZE = 2
INSTRUCT_EXPLANATION_TEXT_SIZE = 0.75
INSTRUCT_TEXT_LINE_SIZE = 1

SCALE_SELECT_TITLE_BL = (750, 100)
SCALE_SELECT_INSTRUCT1_BL = (270, 150)
SCALE_SELECT_INSTRUCT2_BL = (270, 175)
SCALE_SELECT_INSTRUCT3_BL = (270, 200)
SCALE_SELECT_INSTRUCT4_BL = (270, 225)

CHAIR_TYPE_SELECT_TITLE_BL = (670, 100)
CHAIR_TYPE_SELECT_INSTRUCT1_BL = (270, 150)
CHAIR_TYPE_SELECT_INSTRUCT2_BL = (270, 175)
CHAIR_TYPE_SELECT_INSTRUCT3_BL = (270, 200)
CHAIR_TYPE_SELECT_INSTRUCT4_BL = (270, 225)
CHAIR_TYPE_SELECT_INSTRUCT5_BL = (270, 250)

POLY_CREATE_TITLE_BL = (700, 100)
POLY_CREATE_INSTRUCT1_BL = (135, 150)
POLY_CREATE_INSTRUCT2_BL = (135, 175)
POLY_CREATE_INSTRUCT3_BL = (135, 200)
POLY_CREATE_INSTRUCT4_BL = (135, 225)
POLY_CREATE_INSTRUCT5_BL = (135, 250)
POLY_CREATE_INSTRUCT6_BL = (135, 275)
POLY_CREATE_INSTRUCT7_BL = (135, 300)
POLY_CREATE_INSTRUCT8_BL = (135, 325)

CHAIR_RECOGNITION_TITLE_BL = (700, 100)
CHAIR_RECOGNITION_INSTRUCT1_BL = (135, 150)
CHAIR_RECOGNITION_INSTRUCT2_BL = (135, 175)
CHAIR_RECOGNITION_INSTRUCT3_BL = (135, 200)
CHAIR_RECOGNITION_INSTRUCT4_BL = (135, 225)
CHAIR_RECOGNITION_INSTRUCT5_BL = (135, 250)
CHAIR_RECOGNITION_INSTRUCT6_BL = (135, 275)
CHAIR_RECOGNITION_INSTRUCT7_BL = (135, 300)
CHAIR_RECOGNITION_INSTRUCT8_BL = (135, 325)
CHAIR_RECOGNITION_INSTRUCT9_BL = (135, 350)

CHAIR_ADDITION_TITLE_BL = (770, 100)
CHAIR_ADDITION_INSTRUCT1_BL = (535, 150)
CHAIR_ADDITION_INSTRUCT2_BL = (535, 175)
CHAIR_ADDITION_INSTRUCT3_BL = (535, 200)
CHAIR_ADDITION_INSTRUCT4_BL = (535, 225)
CHAIR_ADDITION_INSTRUCT5_BL = (535, 250)
CHAIR_ADDITION_INSTRUCT6_BL = (535, 275)
CHAIR_ADDITION_INSTRUCT7_BL = (535, 300)
CHAIR_ADDITION_INSTRUCT8_BL = (535, 325)
CHAIR_ADDITION_INSTRUCT9_BL = (535, 350)

CHAIR_DELETION_TITLE_BL = (770, 100)
CHAIR_DELETION_INSTRUCT1_BL = (535, 150)
CHAIR_DELETION_INSTRUCT2_BL = (535, 175)
CHAIR_DELETION_INSTRUCT3_BL = (535, 200)
CHAIR_DELETION_INSTRUCT4_BL = (535, 225)
CHAIR_DELETION_INSTRUCT5_BL = (535, 250)
CHAIR_DELETION_INSTRUCT6_BL = (535, 275)
CHAIR_DELETION_INSTRUCT7_BL = (535, 300)
CHAIR_DELETION_INSTRUCT8_BL = (535, 325)

INPUT_PREVIEW_TITLE_BL = (800, 100)
INPUT_PREVIEW_INSTRUCT1_BL = (435, 150)
INPUT_PREVIEW_INSTRUCT2_BL = (435, 175)
INPUT_PREVIEW_INSTRUCT3_BL = (435, 200)
INPUT_PREVIEW_INSTRUCT4_BL = (435, 225)
INPUT_PREVIEW_INSTRUCT5_BL = (435, 250)

SOLVE_ROOM_TITLE_BL = (800, 100)
SOLVE_ROOM_INSTRUCT1_BL = (385, 150)
SOLVE_ROOM_INSTRUCT2_BL = (385, 175)
SOLVE_ROOM_INSTRUCT3_BL = (385, 200)
SOLVE_ROOM_INSTRUCT4_BL = (385, 225)
SOLVE_ROOM_INSTRUCT5_BL = (385, 250)

SCALE_SELECT_TITLE_TEXT = "Scale Selection"
SCALE_SELECT_INSTRUCT1_TEXT = ("Left click two diagonal corners of the room "
                               "diagram's scale.")
SCALE_SELECT_INSTRUCT2_TEXT = "Right click to cancel your previous click."
SCALE_SELECT_INSTRUCT3_TEXT = ("When you are done, make sure the selection "
                               "rectangle is purple. Press 'e' to finalize "
                               "your scale selection.")
SCALE_SELECT_INSTRUCT4_TEXT = ("Press 'e' to continue to the scale selection "
                               "screen.")

CHAIR_TYPE_SELECT_TITLE_TEXT = "Chair Type Selection"
CHAIR_TYPE_SELECT_INSTRUCT1_TEXT = ("Left click two diagonal corners to "
                                    "define a rectangle bounding each unique "
                                    "chair orientation in the room.")
CHAIR_TYPE_SELECT_INSTRUCT2_TEXT = "Right click to cancel your previous click."
CHAIR_TYPE_SELECT_INSTRUCT3_TEXT = ("Do this for each unique chair shape and "
                                    "rotation in the image.")
CHAIR_TYPE_SELECT_INSTRUCT4_TEXT = ("Make sure that each chair orientation is "
                                    "bounded by a purple rectangle before "
                                    "pressing 'e' to finalize your "
                                    "selections.")
CHAIR_TYPE_SELECT_INSTRUCT5_TEXT = ("Press 'e' to continue to the chair "
                                    "type selection screen.")

POLY_CREATE_TITLE_TEXT = "Polygon Creation"
POLY_CREATE_INSTRUCT1_TEXT = ("Left click points on the perimeter of each "
                              "chair to add them to that chair's polygon.")
POLY_CREATE_INSTRUCT2_TEXT = "Right click to cancel your previous click."
POLY_CREATE_INSTRUCT3_TEXT = ("You must create a polygon for each chair "
                              "orientation selected in the chair type "
                              "selection.")
POLY_CREATE_INSTRUCT4_TEXT = ("These polygons define the shape of each chair, "
                              "so it is important to define them accurately.")
POLY_CREATE_INSTRUCT5_TEXT = ("Order matters between points clicked, so click "
                              "the points around the edge in order as if you "
                              "were tracing around the chair's shape.")
POLY_CREATE_INSTRUCT6_TEXT = ("Press 'e' to finalize the polygon for the "
                              "current chair and advance to the next one.")
POLY_CREATE_INSTRUCT7_TEXT = ("Pressing 'e' on the final polygon creation "
                              "screen will finalize that polygon and send you "
                              "back to the menu.")
POLY_CREATE_INSTRUCT8_TEXT = ("Press 'e' to proceed to the first polygon "
                              "creation screen.")

CHAIR_RECOGNITION_TITLE_TEXT = "Chair Recognition"
CHAIR_RECOGNITION_INSTRUCT1_TEXT = ("Chair recognition does not require user "
                                    "input.")
CHAIR_RECOGNITION_INSTRUCT2_TEXT = ("This step can take a long time depending "
                                    "on the size of the room and/or how many "
                                    "chairs it is detecting.")
CHAIR_RECOGNITION_INSTRUCT3_TEXT = ('This step will often show up as '
                                    '"Not Responding" even though it is '
                                    'working.')
CHAIR_RECOGNITION_INSTRUCT4_TEXT = ("When completed, it will show chairs "
                                    "highlighted within the room.")
CHAIR_RECOGNITION_INSTRUCT5_TEXT = ("Press 'e' at that point to confirm the "
                                    "completion of Chair Recognition.")
CHAIR_RECOGNITION_INSTRUCT6_TEXT = ("Remember, the results of Chair "
                                    "Recognition can be adjusted in the "
                                    "following steps, so it is not necessary "
                                    "to have perfect results.")
CHAIR_RECOGNITION_INSTRUCT7_TEXT = ("If a substantial amount of chairs are "
                                    "being placed erroneously, restart the "
                                    "tool with a higher finding_threshold.")
CHAIR_RECOGNITION_INSTRUCT8_TEXT = ("Similarly, if there are way too many "
                                    "chairs that failed to be recognized, "
                                    "restrt the tool with a lower "
                                    "finding_threshold.")
CHAIR_RECOGNITION_INSTRUCT9_TEXT = "Press 'e' to proceed to chair recognition."

CHAIR_ADDITION_TITLE_TEXT = "Chair Addition"
CHAIR_ADDITION_INSTRUCT1_TEXT = "Press 'd' to cycle to the next chair type"
CHAIR_ADDITION_INSTRUCT2_TEXT = "Press 'a' to cycle to the previous chair type"
CHAIR_ADDITION_INSTRUCT3_TEXT = ("A preview chair will be shown in green "
                                 "around your cursor.")
CHAIR_ADDITION_INSTRUCT4_TEXT = ("Left click to confirm placement of the "
                                 "preview chair.")
CHAIR_ADDITION_INSTRUCT5_TEXT = ("At this point, the chair should turn purple "
                                 "indicating its placement.")
CHAIR_ADDITION_INSTRUCT6_TEXT = ("You can place multiple chairs during this "
                                 "step.")
CHAIR_ADDITION_INSTRUCT7_TEXT = ("Right click to undo your most recent chair "
                                 "placement.")
CHAIR_ADDITION_INSTRUCT8_TEXT = ("Press 'e' to confirm all your placed chairs "
                                 "and return to the menu")
CHAIR_ADDITION_INSTRUCT9_TEXT = "Press 'e' to proceed to chair addition."

CHAIR_DELETION_TITLE_TEXT = "Chair Deletion"
CHAIR_DELETION_INSTRUCT1_TEXT = "Left click to select a point."
CHAIR_DELETION_INSTRUCT2_TEXT = ("Left click again to define a rectangle "
                                 "between the two clicked points.")
CHAIR_DELETION_INSTRUCT3_TEXT = ("This rectangle should be purple when "
                                 "completed correctly.")
CHAIR_DELETION_INSTRUCT4_TEXT = ("All chairs within the rectangle will be "
                                 "deleted upon completion.")
CHAIR_DELETION_INSTRUCT5_TEXT = "Multiple rectangles can be defined."
CHAIR_DELETION_INSTRUCT6_TEXT = ("Right click to undo the previously selected "
                                 "rectangle point.")
CHAIR_DELETION_INSTRUCT7_TEXT = ("Press 'e' to confirm all your deleted "
                                 "chairs and return to the menu")
CHAIR_DELETION_INSTRUCT8_TEXT = "Press 'e' to proceed to chair deletion."

INPUT_PREVIEW_TITLE_TEXT = "Input Preview"
INPUT_PREVIEW_INSTRUCT1_TEXT = ("You do not need to do anything during input "
                                "preview.")
INPUT_PREVIEW_INSTRUCT2_TEXT = ("This step is to allow you to confirm that "
                                "all the input you have made is correct.")
INPUT_PREVIEW_INSTRUCT3_TEXT = ("Any incorrect input can be re-run through "
                                "the menu.")
INPUT_PREVIEW_INSTRUCT4_TEXT = ("Press 'e' when you are done confirming your "
                                "input to return to the menu.")
INPUT_PREVIEW_INSTRUCT5_TEXT = ("Press 'e' to continue to the Input Preview "
                                "Screen.")

SOLVE_ROOM_TITLE_TEXT = "Solve Room"
SOLVE_ROOM_INSTRUCT1_TEXT = ("You do not need to do anything during the Solve "
                             "Room step.")
SOLVE_ROOM_INSTRUCT2_TEXT = ("During this step the tool will take all your "
                             "input and create a solution for the room.")
SOLVE_ROOM_INSTRUCT3_TEXT = ("When finished, the tool will save the solution "
                             "as an image in the same folder it is located "
                             "in.")
SOLVE_ROOM_INSTRUCT4_TEXT = "The tool will automatically quit when completed."
SOLVE_ROOM_INSTRUCT5_TEXT = "Press 'e' to continue and solve the room."

def scale_selection_explanation(window_name, screen_height, screen_width):
    """scale_selection_explanation draws the instructions for the scale
    selection input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """


    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, SCALE_SELECT_TITLE_TEXT,
                                SCALE_SELECT_TITLE_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SCALE_SELECT_INSTRUCT1_TEXT,
                                SCALE_SELECT_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SCALE_SELECT_INSTRUCT2_TEXT,
                                SCALE_SELECT_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SCALE_SELECT_INSTRUCT3_TEXT,
                                SCALE_SELECT_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SCALE_SELECT_INSTRUCT4_TEXT,
                                SCALE_SELECT_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)

    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def chair_type_selection_explanation(window_name, screen_height, screen_width):
    """chair_type_selection_explanation draws the instructions for the chair
    type selection input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, CHAIR_TYPE_SELECT_TITLE_TEXT,
                                CHAIR_TYPE_SELECT_TITLE_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_TYPE_SELECT_INSTRUCT1_TEXT,
                                CHAIR_TYPE_SELECT_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_TYPE_SELECT_INSTRUCT2_TEXT,
                                CHAIR_TYPE_SELECT_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_TYPE_SELECT_INSTRUCT3_TEXT,
                                CHAIR_TYPE_SELECT_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_TYPE_SELECT_INSTRUCT4_TEXT,
                                CHAIR_TYPE_SELECT_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_TYPE_SELECT_INSTRUCT5_TEXT,
                                CHAIR_TYPE_SELECT_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)

    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def polygon_creation_explanation(window_name, screen_height, screen_width):
    """polygon_creation_explanation draws the instructions for the polygon
    creation input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1),np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, POLY_CREATE_TITLE_TEXT,
                                POLY_CREATE_TITLE_BL, cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT1_TEXT,
                                POLY_CREATE_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT2_TEXT,
                                POLY_CREATE_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT3_TEXT,
                                POLY_CREATE_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT4_TEXT,
                                POLY_CREATE_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT5_TEXT,
                                POLY_CREATE_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT6_TEXT,
                                POLY_CREATE_INSTRUCT6_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT7_TEXT,
                                POLY_CREATE_INSTRUCT7_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, POLY_CREATE_INSTRUCT8_TEXT,
                                POLY_CREATE_INSTRUCT8_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)

    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def chair_recognition_explanation(window_name, screen_height, screen_width):
    """chair_recognition_explanation draws the instructions for the chair
    recognition input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, CHAIR_RECOGNITION_TITLE_TEXT,
                                CHAIR_RECOGNITION_TITLE_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT1_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT2_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT3_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT4_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT5_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT6_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT6_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT7_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT7_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT8_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT8_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img,
                                CHAIR_RECOGNITION_INSTRUCT9_TEXT,
                                CHAIR_RECOGNITION_INSTRUCT9_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def chair_addition_explanation(window_name, screen_height, screen_width):
    """chair_addition_explanation draws the instructions for the chair addition
    input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_TITLE_TEXT,
                                CHAIR_ADDITION_TITLE_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT1_TEXT,
                                CHAIR_ADDITION_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT2_TEXT,
                                CHAIR_ADDITION_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT3_TEXT,
                                CHAIR_ADDITION_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT4_TEXT,
                                CHAIR_ADDITION_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT5_TEXT,
                                CHAIR_ADDITION_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT6_TEXT,
                                CHAIR_ADDITION_INSTRUCT6_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT7_TEXT,
                                CHAIR_ADDITION_INSTRUCT7_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT8_TEXT,
                                CHAIR_ADDITION_INSTRUCT8_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_ADDITION_INSTRUCT9_TEXT,
                                CHAIR_ADDITION_INSTRUCT9_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def chair_deletion_explanation(window_name, screen_height, screen_width):
    """chair_deletion_explanation draws the instructions for the chair deletion
    input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_TITLE_TEXT,
                                CHAIR_DELETION_TITLE_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT1_TEXT,
                                CHAIR_DELETION_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT2_TEXT,
                                CHAIR_DELETION_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT3_TEXT,
                                CHAIR_DELETION_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT4_TEXT,
                                CHAIR_DELETION_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT5_TEXT,
                                CHAIR_DELETION_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT6_TEXT,
                                CHAIR_DELETION_INSTRUCT6_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT7_TEXT,
                                CHAIR_DELETION_INSTRUCT7_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, CHAIR_DELETION_INSTRUCT8_TEXT,
                                CHAIR_DELETION_INSTRUCT8_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def input_preview_explanation(window_name, screen_height, screen_width):
    """input_preview_explanation draws the instructions for the input preview
    input method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, INPUT_PREVIEW_TITLE_TEXT,
                                INPUT_PREVIEW_TITLE_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, INPUT_PREVIEW_INSTRUCT1_TEXT,
                                INPUT_PREVIEW_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, INPUT_PREVIEW_INSTRUCT2_TEXT,
                                INPUT_PREVIEW_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, INPUT_PREVIEW_INSTRUCT3_TEXT,
                                INPUT_PREVIEW_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, INPUT_PREVIEW_INSTRUCT4_TEXT,
                                INPUT_PREVIEW_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, INPUT_PREVIEW_INSTRUCT5_TEXT,
                                INPUT_PREVIEW_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

def solve_room_explanation(window_name, screen_height, screen_width):
    """solve_room_explanation draws the instructions for the solve room input
    method in the provided window.


    Keyword arguments:

    window_name -- The name of the window to draw instructions in.

    screen_height -- The height (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.

    screen_width -- The width (in pixels) of the user's screen. Must be an
    int. Can be less than the true amount but cannot be more.
    """
    generated_img = np.ones((screen_height, screen_width, 1), np.uint8) * 255
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_GRAY2RGB)
    generated_img = cv2.putText(generated_img, SOLVE_ROOM_TITLE_TEXT,
                                SOLVE_ROOM_TITLE_BL, cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_TITLE_TEXT_SIZE, INSTRUCT_TEXT_COLOR,
                                INSTRUCT_TEXT_LINE_SIZE, cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SOLVE_ROOM_INSTRUCT1_TEXT,
                                SOLVE_ROOM_INSTRUCT1_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SOLVE_ROOM_INSTRUCT2_TEXT,
                                SOLVE_ROOM_INSTRUCT2_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SOLVE_ROOM_INSTRUCT3_TEXT,
                                SOLVE_ROOM_INSTRUCT3_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SOLVE_ROOM_INSTRUCT4_TEXT,
                                SOLVE_ROOM_INSTRUCT4_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    generated_img = cv2.putText(generated_img, SOLVE_ROOM_INSTRUCT5_TEXT,
                                SOLVE_ROOM_INSTRUCT5_BL,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                INSTRUCT_EXPLANATION_TEXT_SIZE,
                                INSTRUCT_TEXT_COLOR, INSTRUCT_TEXT_LINE_SIZE,
                                cv2.LINE_AA)
    while True:
        cv2.imshow(window_name, generated_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break
