from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, csv, re, uuid
from TVStimuli import TVStimuli as TV
from ScrotationClasses import *

longBreakTime = 60
TV.debug = True
groupFile = 'GroupProtocols.csv'
monitorFile = 'monitors.csv'

def calibrate():
    #standard calibration uses Knudson TV data
    #if taking data remotely, replace the calibration file with your own before running code
    label = TV.calibrate(os.path.join(os.getcwd(), 'Calibration', monitorFile))
    if label != None:
        return " " + label
    else:
        calibDlg = gui.Dlg(title='Calibration File Required',
            labelButtonOK=' I have a file ready. Open File Chooser. ', labelButtonCancel=' I have not calibrated my system. Cancel Experiment. ', screen=-1)
        calibDlg.addText('Could not find system calibration. You will now be prompted to choose your calibration file.')
        calibDlg.addText('If you have not yet recieved a calibration csv, you can run the script in the \'Calibration\' folder.\n')
        calibDlg.show()
        if not calibDlg.OK: core.quit()
        
        calibFile = gui.fileOpenDlg(os.getcwd(), prompt = "Select Calibration File", allowed = '*.csv')
        if calibFile == None: core.quit()
        with open(os.path.join(os.getcwd(), 'Calibration', calibFile[0])) as file:
            tvInfo = list(csv.reader(file, delimiter=','))
        
        calibDlg = gui.Dlg(title='System Description', screen=-1)
        calibDlg.addText('Please provide a short description of the system like your name and type of computer.')
        calibDlg.addField('Description: ')
        description = calibDlg.show()
        if description == None: core.quit()
        macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        with open(os.path.join(os.getcwd(), 'Calibration', monitorFile)) as file:
            rows = sum(1 for row in file)
        with open(os.path.join(os.getcwd(), 'Calibration', monitorFile), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Remote " + str(rows), description[0], macAddress] + tvInfo[1])
        return " " + TV.calibrate(os.path.join(os.getcwd(), 'Calibration', monitorFile))

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

    with open(os.path.join(os.getcwd(), 'Calibration', groupFile)) as file:
        protocolFile = list(csv.reader(file, delimiter=','))
    
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
    
    scoreFolder = os.path.join(os.getcwd(), 'Calibration', 'HighScores', groupInfo[0], protocolName[0])
    dirList = os.listdir(scoreFolder);
    winners = [[0,'cm600286']] * 5
    for name in dirList:
        with open(os.path.join(scoreFolder,name)) as file:
            score = int(file.read())
        winners += [[score, name[10:-4]]]
    recentWinners = winners[-5:]
    recentWinners.reverse()
    winners.sort(reverse = True)
    topWinners = winners[:5]
    
    protocol.highScores = [score[0] for score in topWinners + recentWinners]
    protocol.winners = [score[1] for score in topWinners + recentWinners]
    
    if not TV.debug:
        # Participant Name
        codeInfo = {'Participant Name': ''}
        codeDialog = gui.DlgFromDict(dictionary = codeInfo, sortKeys = False, title = 'Participant Info')
        if codeDialog.OK == False:
            core.quit()
    else:
        codeInfo = {'Participant Name': 'Test'}
        protocol.trialsPerSet = 3
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
    
    fileName += calibrate()
    loadSounds()
    
    protocol = protocol(os.path.join(dataFolder, fileName + '.csv'))
    protocol.main()
    protocol.win.mouseVisible = False;
    protocol.win.winHandle.minimize()
    protocol.win.winHandle.close()
    
    scoreDialog = gui.Dlg(title = "Record Score", labelButtonCancel='Choose Premade Random Name.')
    scoreDialog.addText('Do you want to record your score on the leaderboard?')
    scoreDialog.addField('Display Name:', 'Daddy ' + codeInfo['Participant Name'])
    displayName = scoreDialog.show()
    if displayName == None:
        displayName = random.sample(['cm600286', 'Powell Cat Sushi', 'Bot' + '%04d' % random.randint(0,1000), 'Baby Monster', 'Scroptimus Prime', 'Michael Scrott',
            'Scrotation Crustacean', 'AmogUs', 'PikachYOU', 'Chuck Norris', 'Fast and Curious', 'Daddy Gene', 'Russian Spy', 'Ariana Grande\'s Ponytail'], 1)
    scoreFile = os.path.join(scoreFolder, time.strftime("%y%m%d%H%m") + displayName[0])
    with open(scoreFile + '.txt', 'w', newline='') as file:
        file.write(str(protocol.score))
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
