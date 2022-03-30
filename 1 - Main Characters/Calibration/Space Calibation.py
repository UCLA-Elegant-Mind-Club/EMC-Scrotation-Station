from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.hardware import keyboard
import os, time, csv

# Opens the csvFile and writes the output argument specified by to the file
def csvOutput(output, fileName):
    with open(fileName,'a', newline ='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()

info = {'Width (px)': '', 'Height (px)': '', 'Width (cm)': '', 'Distance to screen (cm)': '50', 'Screen number (Try 0, 1, 2, or -1)': 0}
# Input dialogue: session type, subject code
dlg = gui.DlgFromDict(dictionary=info, sortKeys=False, title='TV Info')
if dlg.OK == False:
    core.quit()
    
tvInfo = {'Width (px)': info['Width (px)'],\
    'Height (px)': info['Height (px)'],\
    'Width (cm)': info['Width (cm)'],\
    'Distance to screen':  info['Distance to screen (cm)'],\
    'Screen number': info['Screen number (Try 0, 1, 2, or -1)'],\
    'Device': '',\
    'height': 0,\
    'faceHeight': 0,\
    'faceWidth': 0,\
    'circleRadius': 0,\
    'centerx': 0,\
    'centery': 0,\
    'rightx': 0,\
    'rightEdge': 0,\
    'leftx': 0,\
    'leftEdge': 0,\
    'spacer': 0}
    
# Input dialogue: directions to test
datadlg = gui.Dlg(title='Are you running this from a laptop or desktop computer?', screen=-1)
datadlg.addField('Device: ', choices = ["Laptop", "Desktop"])
ok_data = datadlg.show()
if ok_data is None:
    endExp()
elif ok_data[0] == 'Laptop':
    chSize = 0.3
    tSize = 0.3
else:
    chSize = 1.2
    tSize = 1.2
tvInfo['Device'] = ok_data[0]


mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=tvInfo['Screen number'], 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
        

dotSize = 1.7

# Returns a displayText object with the given text, coordinates, height, color
def genDisplay(displayInfo):
    displayText = visual.TextStim(win=win,
    text= displayInfo['text'],
    font='Arial',
    pos=(displayInfo['xPos'], displayInfo['yPos']),
    height=displayInfo['heightCm'],
    wrapWidth=500,
    ori=0, 
    color=displayInfo['color'],
    colorSpace='rgb',
    opacity=1, 
    languageStyle='LTR',
    depth=0.0)
    return displayText
    
def getKeyboardInput():
    keys = event.waitKeys()
    if keys[0] == 'escape':
        core.quit()
    return keys[0]

def checkHeightResponse(info):
    if info['thisResponse'] == 'down' and info['lastResponse'] == 'up':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'up':
        info['adjuster'] += info['increment']
    else:
        info['adjuster'] -= info['increment']
    return info 
    
def setHeight(tvInfo):
    heights = [1, 3, 7, 10]
    final = 0
    for height in heights:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the I is', 'heightCm': tSize, 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': str(height) + ' centimeters tall', 'heightCm': tSize, 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (height*info['adjuster']), 'xPos': 0, 'yPos': -2, 'color': 'white'}).draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = getKeyboardInput()
            info = checkHeightResponse(info)
        final += info['adjuster']
    tvInfo['height'] = final/(len(heights))
    return tvInfo
    
    
faceFile = (os.path.join(os.getcwd(), 'calibration_face.jpg')) 

face = visual.ImageStim( 
    win=win,
    name='', units='cm', 
    image= faceFile, mask=None,
    ori=0, pos=(0, 0), size = (0,0),
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0) 
    
def setFaceHeight(tvInfo):
    sizes = [1, 2, 4, 6]
    final = 0
    for size in sizes:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the image is', 'heightCm': tSize, 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': str(size) + ' centimeters tall', 'heightCm': tSize, 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            face.size = (size, (size*info['adjuster']))
            face.draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = getKeyboardInput()
            info = checkHeightResponse(info)
        final += info['adjuster']
    tvInfo['faceHeight'] = final/(len(sizes))
    return tvInfo
    
def setFaceWidth(tvInfo):
    sizes = [1, 2, 4, 6]
    final = 0
    for size in sizes:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the image is', 'heightCm': tSize, 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': str(size) + ' centimeters wide', 'heightCm': tSize, 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            face.size = ((size*info['adjuster']), size)
            face.draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = getKeyboardInput()
            info = checkHeightResponse(info)
        final += info['adjuster']
    tvInfo['faceWidth'] = final/(len(sizes))
    return tvInfo
    
circle = visual.Circle(win=win, radius=0, edges=32, lineColor = 'white', fillColor = 'white', pos = (0,-2))
def setCircle(tvInfo):
    radii = [0.5, 1, 2, 3]
    final = 0
    for radius in radii:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the circle is', 'heightCm': tSize, 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': str(radius*2) + ' centimeters in diameter', 'heightCm': tSize, 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            circle.radius = radius*info['adjuster']
            circle.draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = getKeyboardInput()
            info = checkHeightResponse(info)
        final += info['adjuster']
    tvInfo['circleRadius'] = final/(len(radii))
    return tvInfo

def checkCenterResponse(info):
    if info['response'] == 'space':
        info['complete'] = True 
    elif info['response'] == 'up':
        info['y'] += 0.05
    elif info['response'] == 'down':
        info['y'] -= 0.05
    elif info['response'] == 'left':
        info['x'] -= 0.05
    elif info['response'] == 'right':
        info['x'] += 0.05
    return info 
    
def setCenter(tvInfo):
    info = {'x': 0, 'y': 0, 'complete': False}
    while not info['complete']:
            
        genDisplay({'text': 'Use the arrow keys to move the dot. Press spacebar once the dot is centered on the A', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
        genDisplay({'text': 'A', 'heightCm': (1*tvInfo['height']), 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
        genDisplay({'text': '.', 'heightCm': (dotSize*tvInfo['height']), 'xPos': info['x'], 'yPos': info['y'], 'color': 'lawngreen'}).draw()
        win.flip()
            
        info['response'] = getKeyboardInput()
        info = checkCenterResponse(info)
    tvInfo['centerx'], tvInfo['centery'] = info['x'], info['y']
    return tvInfo
    
def checkRightResponse(info):
    if info['thisResponse'] == 'left' and info['lastResponse'] == 'right':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'right':
        info['adjuster'] += info['increment']
    else:
        info['adjuster'] -= info['increment']
    return info 
    
def setRight(tvInfo):
    angles = [2, 3, 5, 7, 10]
    for angle in angles:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Arrow keys to move the I. Press spacebar once the center of the I is', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 5, 'color': 'white'}).draw()
            genDisplay({'text': str(angle) + ' centimeters to the right of the center dot', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (tSize*tvInfo['height']), 'xPos': (angle*info['adjuster']), 'yPos': 0, 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (dotSize*tvInfo['height']), 'color': 'lawngreen'}).draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            
            info['thisResponse'] = getKeyboardInput()
            info = checkRightResponse(info)
        tvInfo['rightx'] += info['adjuster']
    tvInfo['rightx'] = tvInfo['rightx']/len(angles)
    return tvInfo
    
def setRightEdge(tvInfo):
    info = {'adjuster': 0, 'increment': 5, 'lastResponse': None, 'thisResponse': None,'complete': False}
    while not info['complete']:
        genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 5, 'color': 'white'}).draw()
        genDisplay({'text': 'at the right edge of the screen', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
        genDisplay({'text': 'I', 'heightCm': (tSize*tvInfo['height']), 'xPos': info['adjuster'], 'yPos': 0, 'color': 'white'}).draw()
        win.flip()
            
        info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
        info = checkRightResponse(info)
    tvInfo['rightEdge'] = (info['adjuster']/tvInfo['rightx'])
    return tvInfo
    
def checkLeftResponse(info):
    if info['thisResponse'] == 'right' and info['lastResponse'] == 'left':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'left':
        info['adjuster'] += info['increment']
    else:
        info['adjuster'] -= info['increment']
    return info 
    
def setLeft(tvInfo):
    angles = [2, 3, 5, 7, 10]
    for angle in angles:
        info = {'adjuster': -(tvInfo['rightx']), 'increment': -0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 5, 'color': 'white'}).draw()
            genDisplay({'text': str(angle) + ' centimeters to the left of the center dot', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (tSize*tvInfo['height']), 'xPos': (angle*info['adjuster']), 'yPos': 0, 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (dotSize*tvInfo['height']), 'color': 'lawngreen'}).draw()
            win.flip()
            
            info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
            info = checkLeftResponse(info)
        tvInfo['leftx'] += info['adjuster']
    tvInfo['leftx'] = tvInfo['leftx']/len(angles)
    return tvInfo
    
def setLeftEdge(tvInfo):
    info = {'adjuster': 0, 'increment': -5, 'lastResponse': None, 'thisResponse': None,'complete': False}
    while not info['complete']:
        genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 5, 'color': 'white'}).draw()
        genDisplay({'text': 'at the left edge of the screen', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
        genDisplay({'text': 'I', 'heightCm': (tSize*tvInfo['height']), 'xPos': info['adjuster'], 'yPos': 0, 'color': 'white'}).draw()
        win.flip()
            
        info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
        info = checkLeftResponse(info)
    tvInfo['leftEdge'] = (info['adjuster']/tvInfo['leftx'])
    return tvInfo
    
def setSpacer(tvInfo):
    heights = [3, 5]
    for height in heights:
        info = {'adjuster': -1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 5, 'color': 'white'}).draw()
            genDisplay({'text': '0.1 cm below the E', 'heightCm': (chSize*tvInfo['height']), 'xPos': 0, 'yPos': 3, 'color': 'white'}).draw()
            genDisplay({'text': 'E', 'heightCm': (height*tvInfo['height']), 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (height*tvInfo['height']), 'xPos': 0, 'yPos': (height*info['adjuster']), 'color': 'white'}).draw()
            win.flip()
            
            info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
            info = checkHeightResponse(info)
        tvInfo['spacer'] += (-info['adjuster'])
    tvInfo['spacer'] = tvInfo['spacer']/len(heights)
    return tvInfo

tvInfo = setHeight(tvInfo)
tvInfo = setFaceHeight(tvInfo)
tvInfo = setFaceWidth(tvInfo)
tvInfo = setCircle(tvInfo)
tvInfo = setCenter(tvInfo)
tvInfo = setRight(tvInfo)
tvInfo = setRightEdge(tvInfo)
tvInfo = setLeft(tvInfo)
tvInfo = setLeftEdge(tvInfo)
tvInfo = setSpacer(tvInfo)

# Change directory to script directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
fileName = os.path.join(os.getcwd(), 'eccentricity_monitor_calibration.csv')
    
csvOutput(list(tvInfo.keys()), fileName)
csvOutput(list(tvInfo.values()), fileName)
    
win.flip() 
logging.flush()
win.close()
core.quit()