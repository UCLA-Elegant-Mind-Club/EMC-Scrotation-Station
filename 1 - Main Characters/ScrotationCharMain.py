from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time
from RotationClasses import RotationProtocol as RP
from RotationClasses import *
from ScalingClasses import *

protocolNames = ['English Scale RT', 'Thai Scale RT', 'Chinese Scale RT',
        'English Roll RT', 'Thai Roll RT', 'Chinese Roll RT']
debug = False
customCalibration = False

if debug:
    debugDlg = gui.Dlg(title='Debug Mode?', pos=None, size=None, style=None,\
         labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
    debugResponse = debugDlg.show()
    debug = debugDlg.OK

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

def getProtocolList(group, includeThai, participantCode, dirPath):
    participant = participantCode + '_' + time.strftime("%m_%d")
    fileNames = ['']*6
    for protocol in range(0, len(protocolNames)):
        fileNames[protocol] = os.path.join(dirPath, participantCode, protocolNames[protocol],
            participant + protocolNames[protocol] + '.csv')
    if group == 'Scaling':
        e = EnglishScaling(fileNames[0])
        t = ThaiScaling(fileNames[1])
        c = ChineseScaling(fileNames[2])
    else:
        e = EnglishRoll(fileNames[3])
        t = ThaiRoll(fileNames[4])
        c = ChineseRoll(fileNames[5])
    if includeThai == 'Yes':
        return [e, t, c]
    else:
        return [e, c]

def loadSounds():
    RP.genDisplay('Loading...', 0, 0, height = 3)
    playThread = RP.playNotes(notes = [440, 554.37, 659.25, 554.37, 440],
        beats = [1, 1, 1, 1, 1], beatLength = 0.5)
    RP.showWait(0)
    playThread.join()
    RP.showWait(0)

def protocolBreak():
    for i in range(0, 61):
        RP.genDisplay('Longer Break', 0, 9)
        RP.genDisplay('You now have a 4 minute break to rest your eyes, get up,', 0, 6)
        RP.genDisplay('and stretch your arms. If you need to use the restroom,', 0, 4)
        RP.genDisplay('please notify the operator. You can also start the next', 0, 2)
        RP.genDisplay('protocol early after 1 minute if you are ready.', 0, 0)
        if i < 60:
            RP.genDisplay('Seconds left until early start: ' + str(60 - i), 0, -4)
            RP.showWait(1)
        else:
            RP.genDisplay('[Press space to start next protocol]', 0, -4)
            RP.showWait()

if __name__ == '__main__':
    if debug:
        RP.trialsPerSet = 5
        RP.initialPracticeTrials = 3
        RP.trainingTime = 1
        RP.interimPracticeTrials = 0
        RP.prePracticeBreak = 1
        RP.postPracticeBreak = 1
        RP.postSetBreak = 1
        RP.dummyTrials = 1
    
    codeInfo = {'Participant Name': ''}
    codeDialog = gui.DlgFromDict(dictionary = codeInfo, sortKeys = False, title = 'Participant Info')
    if codeDialog.OK == False:
        core.quit()
    
    autoProtocol = 2;
    protocolDialog = gui.Dlg(title='Select protocols to run', screen=-1)
    protocolDialog.addField('Group: ', choices = ['Scaling', 'Rotation'])
    includeThai = ['Yes', 'No']
    
    if autoProtocol == 0:
        protocolInfo = ['', '']
    else:
        if autoProtocol == 2:
            protocolDialog.addField('Include Thai: ', choices = includeThai)
        protocolInfo = protocolDialog.show()
        if protocolInfo is None:
            core.quit()
        protocolInfo += ['Yes'];
    
    if customCalibration:
        RP.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration1.csv'))
    else:
        RP.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration.csv'))
    makeDataDirs(codeInfo['Participant Name'])
    protocolList = getProtocolList(protocolInfo[0], protocolInfo[1], codeInfo['Participant Name'],
        os.path.join(os.getcwd(), 'Data'))
        
    for protocolNum in range(0, len(protocolList)):    
        loadSounds()
        protocolList[protocolNum].main()
        if protocolNum < len(protocolList) - 1: protocolBreak()

    RP.playNotes(notes = [220, 277.18, 329.63, 277.18, 329.63, 440, 329.63, 440, 554.37, 440, 554.37, 659.25, 554.37, 659.25, 880],
        beats = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4], beatLength = 0.1)
    RP.genDisplay('All done for today!', 0, 8, height = 3)
    RP.genDisplay('Thank you for your time!', 0, 4, height = 2)
    RP.genDisplay('Final Scores', 0, 0, height = 3)
    for i in range(0, len(protocolList)):
        RP.genDisplay(str(protocolList[i].score), 0, -4 - 2 * i, color = [0,1,0])
        print(protocolList[i].score)
    RP.showWait()
