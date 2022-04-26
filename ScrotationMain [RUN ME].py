from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, csv
from TVStimuli import TVStimuli as TV
from ScrotationClasses import *

longBreakTime = 60
TV.debug = True
groupFile = 'GroupProtocols.csv'
    
def calibrate():
    calibDlg = gui.Dlg(title='Testing location?', pos=None, size=None, style=None,\
         labelButtonOK=' Local at Knudson ', labelButtonCancel=' Remotely ', screen=-1)
    calibDlg.show()
    standardCalibration = calibDlg.OK

    #standard calibration uses Knudson TV data
    #if taking data remotely, replace the calibration file with your own before running code
    if standardCalibration:
        TV.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration_Knudson.csv'))
    else:
        TV.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration.csv'))

def loadSounds():
    TV.genDisplay('Loading...', 0, 0, height = 3)
    playThread = TV.playNotes(notes = [440, 554.37, 659.25, 554.37, 440],
        beats = [1, 1, 1, 1, 1], beatLength = 0.5)
    TV.showWait(0)
    playThread.join()
    TV.showWait(0)

def protocolBreak(time = 60):
    for i in range(0, time + 1):
        TV.genDisplay('Longer Break', 0, 9)
        TV.genDisplay('You now have a 4 minute break to rest your eyes, get up,', 0, 6)
        TV.genDisplay('and stretch your arms. If you need to use the restroom,', 0, 4)
        TV.genDisplay('please notify the operator. You can also start the next', 0, 2)
        TV.genDisplay('protocol early after 1 minute if you are ready.', 0, 0)
        if i < time:
            TV.genDisplay('Seconds left until early start: ' + str(time - i), 0, -4)
            TV.showWait(1)
        else:
            TV.genDisplay('[Press space to start next protocol]', 0, -4)
            TV.showWait()


def main():
    if TV.debug:
        debugDlg = gui.Dlg(title='Debug Mode?', pos=None, size=None, style=None,\
             labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
        debugDlg.show()
        TV.debug = debugDlg.OK
        
    if TV.debug:
        longBreakTime = 1

    protocolFile = list(csv.reader(open(groupFile), delimiter=','))
    
    # Select group project
    groupDialog = gui.Dlg(title='Select Group Project', screen=-1)
    groups = [row[0] for row in protocolFile]
    groupDialog.addField('Group: ', choices = groups[1:])
    groupInfo = groupDialog.show()
    if groupInfo is None:
        core.quit()
    
    # Select protocol to run
    groupNum = groups.index(groupInfo[0])
    protocolDialog = gui.Dlg(title='Select protocol to run', screen=-1)
    protocols = protocolFile[groupNum][1].split('. ')
    protocolDialog.addField('Protocol: ', choices = protocols)
    protocolName = protocolDialog.show()
    if protocolName is None:
        core.quit()
    protocol = globals()[protocolName[0].replace(' ','')]
    
    # Prepare Highscores
    protocolNum = protocols.index(protocolName[0])
    protocol.winners = protocolFile[groupNum][2 + 2 * protocolNum].split('. ')
    scores = protocolFile[groupNum][3 + 2 * protocolNum].split('. ')
    protocol.highScores = [int(num) for num in scores]
    
    if not TV.debug:
        # Participant Name
        codeInfo = {'Participant Name': ''}
        codeDialog = gui.DlgFromDict(dictionary = codeInfo, sortKeys = False, title = 'Participant Info')
        if codeDialog.OK == False:
            core.quit()
    else:
        codeInfo = {'Participant Name': 'Test'}
        protocol.trialsPerSet = 1
        protocol.numSets = 1
        protocol.initialPracticeTrials = 3
        protocol.trainingTime = 1
        protocol.interimPracticeTrials = 0
        protocol.prePracticeBreak = 1
        protocol.postPracticeBreak = 1
        protocol.postSetBreak = 1
        protocol.dummyTrials = 1
    
    # Prepare directories
    dataFolder = os.path.join(os.getcwd(), 'Data')
    if not os.path.isdir(dataFolder):
        os.mkdir(dataFolder)
    dataFolder = os.path.join(dataFolder, str(groupInfo[0]))
    if not os.path.isdir(dataFolder):
        os.mkdir(dataFolder)
    dataFolder = os.path.join(dataFolder, protocolName[0])
    if not os.path.isdir(dataFolder):
        os.mkdir(dataFolder)
    
    fileName = codeInfo['Participant Name'] + ' (' + time.strftime("%m %d") + ') ' + groupInfo[0] + ', ' + protocolName[0]
    
    calibrate()
    loadSounds()
    
    protocol = protocol(os.path.join(dataFolder, fileName + '.csv'))
    protocol.main()
    protocol.win.mouseVisible = False;
    protocol.win.winHandle.minimize()
    protocol.win.winHandle.close()
    
    rank = protocol.rank
    scoreInfo = {'Display Name': ''}
    scoreDialog = gui.Dlg(title = "Record Score", labelButtonCancel='I don\'t want to record my score.')
    scoreDialog.addText('Do you want to record your score on the leaderboard?')
    scoreDialog.addField('Display Name:')
    displayName = scoreDialog.show()
    if scoreDialog.OK == True:
        if rank[0] > 0:
            topWinners = protocol.winners[0:rank[0] - 1] + displayName + protocol.winners[rank[0]:4]
            topScores = protocol.highScores[0:rank[0] - 1] + [protocol.score] + protocol.highScores[rank[0]:4]
        else:
            topWinners = protocol.winners[0:5]
            topScores = protocol.highScores[0:5]
        recentWinners = displayName + protocol.winners[6:10]
        recentScores = [protocol.score] + protocol.highScores[6:10]
        protocolFile[groupNum][2 + 2 * protocolNum] = '. '.join(topWinners + recentWinners)
        protocolFile[groupNum][3 + 2 * protocolNum] = '. '.join([str(num) for num in topScores + recentScores])
        
        with open(groupFile, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(protocolFile)
        csvFile.close()
        
    #if protocolNum < len(protocols) - 1: protocolBreak(longWaitTime)

def endScene(protocolList):
    TV.playNotes(notes = [220, 277.18, 329.63, 277.18, 329.63, 440, 329.63, 440, 554.37, 440, 554.37, 659.25, 554.37, 659.25, 880],
        beats = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4], beatLength = 0.1)
    TV.genDisplay('All done for today!', 0, 8, height = 3)
    TV.genDisplay('Thank you for your time!', 0, 4, height = 2)
    TV.genDisplay('Final Scores', 0, 0, height = 3)
    for i in range(0, len(protocolList)):
        TV.genDisplay(str(protocolList[i].score), 0, -4 - 2 * i, color = [0,1,0])
        print(protocolList[i].score)
    TV.showWait()

main()