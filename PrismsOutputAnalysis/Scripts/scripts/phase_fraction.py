#!/usr/bin/env python3

import sys
from visit import *

#DeleteAllPlots()

loc=sys.argv[1]
var=sys.argv[2]
sloc=sys.argv[3]

# Step 1: Open a database (the whole .vtu time series)
dbname=loc+"solution-*.vtu database"
OpenDatabase(dbname)

# Step 2: Add plots (using variable "n")
# This variable must be in the range [0,1]
# with 0 representing one phase, 1 representing another phase
# and n=0.5 representing the midpoint accross the interface
AddPlot("Pseudocolor", var)

# Step 3: Draw the plots
DrawPlots()

# Step 4: Get the number of grid points in the domain
Query("Grid Information")
gpq = GetQueryOutputValue()
# Extracting number of grid points in each direction
num_x_coords = int(gpq[2])
num_y_coords = int(gpq[3])
num_z_coords = int(gpq[4])

# Step 5 Get the area (or volume) of the whole domain
av=0.0
if num_z_coords >= 1:
    Query("Volume")
    # Assign result to variable a
    av=GetQueryOutputValue()
else:
    Query("2D area")
    # Assign result to variable a   
    av=GetQueryOutputValue()

# Step 6: Initialize phase fraction and open output file
phasefrac=[0.0]*TimeSliderGetNStates()
# Set the output file name
ofnm=sloc+"phi_vs_t.txt"
# Open  output file
outF = open(ofnm, "w")
print("Step\tTime\tfraction_1\tfraction_0")
outF.write("Step\tTime\tfraction_1\tfraction_0\n")
# Step 7: Animate through time and save results
for states in range(TimeSliderGetNStates()):
    #Set slider to state
    SetTimeSliderState(states)
    # Get the time corresponding to the state
    Query("Time")
    # Assign this time to the variable "t"
    t = GetQueryOutputValue()
    # Get the total area (or volume) of domains where n=1 by integration
    Query("Weighted Variable Sum")
    # Set this area (or volume) to the variable wvs
    wvs=GetQueryOutputValue()
    # Calculate phase fraction
    phasefrac[states]=wvs/av
    # Print the state number, time and phase fraction to
    # screen and to files
    print("% d, %.1f, %.5f, %.5f" %(states, t, phasefrac[states], 1 - phasefrac[states]))
    outF.write("% d\t%.1f\t%.5f\t%.5f\n" %(states, t, phasefrac[states], 1 - phasefrac[states]))
outF.close()

DeleteAllPlots()
CloseDatabase(dbname)

sys.exit()
