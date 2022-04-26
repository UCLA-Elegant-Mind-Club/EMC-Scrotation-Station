import psychopy
from psychopy import gui, visual, core, event, monitors, prefs
import numpy as np  
import os, sys, time, random, math, csv
import string

date = time.strftime("%m_%d")
expName = 'Letter Three Decision Overt'
expInfo = {'Subject Name': ''}

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()
    
# Create folder for each experiment, will contain CSV data file and all eye tracking data files.
# This folder will have the same name as the CSV file.
OUTPATH = os.path.join(os.getcwd(), 'Data', \
    (expInfo['Subject Name'] + '_' + date + '_' + expName))
if not os.path.isdir(OUTPATH):
    os.mkdir(OUTPATH)


filePath = os.path.join('"' + OUTPATH,\
    (expInfo['Subject Name'] + '_' + date + '_' + expName + ' Eye_Tracking.txt"'))

commandLine = 'cmd /k eye-tracker-naive\TobiiStream\TobiiStream.exe > ' + filePath
os.system(commandLine)