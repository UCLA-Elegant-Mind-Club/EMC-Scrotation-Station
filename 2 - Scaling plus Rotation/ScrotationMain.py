from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time
from TVStimuli import TVStimuli as TV
from ScrotationClasses import *
from RotationClasses import *

protocolNames = ['Normal Face Roll RT', 'Large Face Roll RT', 'Small Face Roll RT', 'Scaling with rotations']
TV.debug = True
longBreakTime = 60

if TV.debug:
    debugDlg = gui.Dlg(title='Debug Mode?', pos=None, size=None, style=None,\
         labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
    debugDlg.show()
    TV.debug = debugDlg.OK

calibDlg = gui.Dlg(title='Testing location?', pos=None, size=None, style=None,\
     labelButtonOK=' Local at Knudson ', labelButtonCancel=' Remotely ', screen=-1)
calibDlg.show()
standardCalibration = calibDlg.OK

def makeDataDirs(participant):
    dataFolder = os.path.join(os.getcwd(), 'Data')
    if not os.path.isdir(dataFolder):
        os.mkdir(dataFolder)
    dataFolder = os.path.join(dataFolder, participant)
    if not os.path.isdir(dataFolder):
        os.mkdir(dataFolder)
    for protocol in protocolNames:
        protocolPath = os.path.join(dataFolder, protocol)
        if not os.path.isdir(protocolPath):
            os.mkdir(protocolPath)

def getProtocolList(group, participantCode, dirPath):
    participant = participantCode + '_' + time.strftime("%m_%d")
    fileNames = ['']*4
    for protocol in range(0, len(protocolNames)):
        fileNames[protocol] = os.path.join(dirPath, participantCode, protocolNames[protocol],
            participant + protocolNames[protocol] + '.csv')
    if group == 'Rotation Protocols at Different Scalings':
        a = NormalFaceRoll(fileNames[0])
        b = LargeFaceRoll(fileNames[1])
        c = SmallFaceRoll(fileNames[2])
        if random.randint(0,1) == 0:
            return [a, b, c]
        else:
            return [a, c, b]
    else:
        return [ScalingRotationProtocol(fileNames[4])]

def loadSounds():
    TV.genDisplay('Loading...', 0, 0, height = 3)
    playThread = TV.playNotes(notes = [440, 554.37, 659.25, 554.37, 440],
        beats = [1, 1, 1, 1, 1], beatLength = 0.5)
    TV.showWait(0)
    playThread.join()
    TV.showWait(0)

def protocolBreak():
    for i in range(0, longBreakTime + 1):
        TV.genDisplay('Longer Break', 0, 9)
        TV.genDisplay('You now have a 4 minute break to rest your eyes, get up,', 0, 6)
        TV.genDisplay('and stretch your arms. If you need to use the restroom,', 0, 4)
        TV.genDisplay('please notify the operator. You can also start the next', 0, 2)
        TV.genDisplay('protocol early after 1 minute if you are ready.', 0, 0)
        if i < longBreakTime:
            TV.genDisplay('Seconds left until early start: ' + str(longBreakTime - i), 0, -4)
            TV.showWait(1)
        else:
            TV.genDisplay('[Press space to start next protocol]', 0, -4)
            TV.showWait()

if __name__ == '__main__':
    if TV.debug:
        TV.trialsPerSet = 5
        TV.initialPracticeTrials = 3
        TV.trainingTime = 1
        TV.interimPracticeTrials = 0
        TV.prePracticeBreak = 1
        TV.postPracticeBreak = 1
        TV.postSetBreak = 1
        TV.dummyTrials = 1
        longBreakTime = 1
    
    codeInfo = {'Participant Name': ''}
    codeDialog = gui.DlgFromDict(dictionary = codeInfo, sortKeys = False, title = 'Participant Info')
    if codeDialog.OK == False:
        core.quit()
    
    autoProtocol = 1;
    protocolDialog = gui.Dlg(title='Select protocols to run', screen=-1)
    protocolDialog.addField('Type of Combination: ', choices = ['Rotation Protocols at Different Scalings', 'Scaling protocol with random rotation'])
    
    if autoProtocol == 0:
        protocolInfo = ['', '']
    else:
        protocolInfo = protocolDialog.show()
        if protocolInfo is None:
            core.quit()
    
    if standardCalibration:
        TV.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration_Knudson.csv'))
    else:
        TV.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration.csv'))
    makeDataDirs(codeInfo['Participant Name'])
    protocolList = getProtocolList(protocolInfo[0], codeInfo['Participant Name'],
        os.path.join(os.getcwd(), 'Data'))
        
    for protocolNum in range(0, len(protocolList)):    
        loadSounds()
        protocolList[protocolNum].main()
        if protocolNum < len(protocolList) - 1: protocolBreak()

    TV.playNotes(notes = [220, 277.18, 329.63, 277.18, 329.63, 440, 329.63, 440, 554.37, 440, 554.37, 659.25, 554.37, 659.25, 880],
        beats = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4], beatLength = 0.1)
    TV.genDisplay('All done for today!', 0, 8, height = 3)
    TV.genDisplay('Thank you for your time!', 0, 4, height = 2)
    TV.genDisplay('Final Scores', 0, 0, height = 3)
    for i in range(0, len(protocolList)):
        TV.genDisplay(str(protocolList[i].score), 0, -4 - 2 * i, color = [0,1,0])
        print(protocolList[i].score)
    TV.showWait()
