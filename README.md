# Classroom-Seating-Planning-Tools

## Description
These tools use an integer program to help users optimize room seating 
assignments for social distancing. Users must provide a png image of the 
architectural diagram of a room alongside several configurable parameters to 
the tool of their choice to have it load up the room for the room solving 
process. Through the tool, users can then designate several key features of 
the image to have the tool create its own graph rendition of the room. The 
tool will then solve for the maximum independent set of that graph, which
results in a socially distanced possible solution on how to seat people within
the room. Upon completion, the tool will create its own copy of the room 
diagram indicating the spaces chosen by the tool. 


## Dependencies
Matplotlib 3.1.3
Numoy 1.18.1
Pandas 1.0.1
Networkx 2.4
Shapely 1.7.0
Scipy 1.4.1
Skimage 0.16.2
Cv2 4.3.0
Ortools 7.7.7810
JupyterNotebook

## Disclaimer
- All room diagrams provided to the tool must have a scale and example 
chair drawn onto the image. 
- As the tool uses pixels within the room diagram to determine distances within 
the room, images with more pixels relative to physical room size will result in 
higher accuracy. 
- Do not blindly trust solutions given by the tool. The tool was made to give 
suggestions on where to seat individuals, not create final draft seating plans. 
All solutions from the tool should be evaluated properly for feasibility and 
adjusted accordingly. Similarly, all distances determined by the tool should be
measured in person.
- As distances are calculated based off the image and user inputs, it is 
possible for an input mistake to cause seats to be too close together. 
- Finally, the non fixed seating tools will not obtain a guaranteed max 
capacity seating assignment for the room. Instead, the non fixed seating tools 
are meant to help users determine good seating patterns to use when placing 
chairs in an empty room.


## Helpful Tips (e.g. bigger images are more accurate)
- Use larger images for more precise measurements.
- The less messy your diagram is, the easier it is for the tool to recognize 
chairs. If the tool is having difficulty locating chairs correctly, try using
a clearer image (e.g. without lines drawn on top of chairs) or adjust the 
finding threshold.
- Certain steps in the process may take a while to run. If the tool seems
stuck, check the jupyter notebook to see if it is still running. Rooms with
more nodes (chairs) and edges (conflicts between chairs) take longer to run. If
a room is taking too long to solve, try rerunning it with less nodes and edges.
(Note that this may result in a lower seating count for the solution).
- Extra information is included within the ipynb jupyter notebook file for each 
tool.

## Licensing
Use this project under the terms of the MIT license.


## Included Tools

###Fixed-Seating-Classroom-Planner
This tool is used for rooms in which the seats are all drawn into the diagram,
and cannot be moved. To run the tool, add the room diagram image to the tool 
folder then launch the ClassroomPlanner.ipynb file through your Jupyter 
notebook. Use the Jupyter notebook to configure your parameters as needed
then restart and run all cells to launch the tool. The tool will bring up a 
window containing a menu that can be used to navigate between different 
required inputs. Right click within a menu button to navigate to the input
function if its prerequisite input functions have been completed.

### Non-Fixed-Seating-Classroom-Planners
#### EmptyClassroomPlanner
This tool is used for rooms with movable seats. To use the tool, add the room
diagram image to the tool folder then launch the EmptyClassroomPlanner.ipynb
file through your Jupyter notebook. To use the tool, run the cells within the
notebook individually and complete the inputs required by each cell. If you 
need to redo an input, re-run the cells for that input and all cells 
dependent on it.
#### EmptyClassroomChunkingPlanner
This tool is used to help visualize how a large empty room can be chunked into 
smaller subsections. To use the tool, add the room diagram image to the tool 
folder then launch the EmptyClassroomChunkingPlanner.ipynb file through your 
Jupyter notebook. To use the tool, run the cells within the notebook 
individually and complete the inputs required by each cell. If you need to 
redo an input, re-run the cells for that input and all cells dependent on it. 


Authors: Kyle K. Greenberg, Trey Hensel, Qihan Zhu, Sander Aarts, Samuel C. Gutekunst, and David B. Shmoys
