from psychopy import gui, core, prefs
from psychopy.sound import Sound
from psychopy.event import waitKeys
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, csv, re, uuid, random
from TVStimuli import TVStimuli as TV
from ScrotationClasses import *

longBreakTime = 60

def showWaitAuto(seconds = -1, keys = ['space'], flip = True):
    if seconds < 0:
        if flip: TVStimuli.win.flip()
        key = waitKeys(keyList = keys + ['escape'], maxWait = 3)
        if key != None and key[0] == 'escape':
            core.quit()
    else:
        TV.showWait(seconds, keys, flip)

TV.afkStreak = 0
def stimTestAuto(self, set, target, testValue, correctKey, practice = False):
    self.showCross()
    self.showWait(random.randint(5,15)/10, flip = False)
    self.showImage(set, target, testValue)
    result = {'start': 0, 'end': 0}
    self.win.timeOnFlip(result, 'start')
    self.win.flip()
    
    wait = self.timeOut
    if self.afkStreak >= 3:
        wait = random.randint(600, int(self.timeOut * 1000)) / 1000
        if random.randint(1,100) < 10:
            wait += self.timeOut
    
    keys = waitKeys(timeStamped = True, maxWait = min(wait, self.timeOut) + float(self.tvInfo['timeDelay'])/1000)
    if keys == None:
        self.afkStreak += 1
        if wait >= self.timeOut:
            response = 'timedOut'
            result['end'] = result['start']
        else:
            response = correctKey
            if random.randint(1, 100) < 30:
                response = random.sample(['v', 'b', 'n'], 1)[0]
            result['end'] = wait + result['start']
    else:
        self.afkStreak = 0
        response = keys[0][0]
        result['end'] = keys[0][1]
    self.win.flip()
    
    if response == 'escape':
        core.quit()
    reactionTime = (result['end'] - result['start']) * 1000 - float(self.tvInfo['timeDelay'])
    
    if response == correctKey:
        self.feedback(True, scoreChange = (not practice) * (min(self.timeOut * 1000 - reactionTime, 800)/2 + 600))
    elif response == 'timedOut':
        self.feedback(-1, scoreChange = (not practice) * -400)
    else:
        self.feedback(False, scoreChange = (not practice) * -min(reactionTime, 800)/2)
    return [(response == correctKey) * 1, testValue, reactionTime, set * 3 + target]

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
            rows = sum(1 for row in file if row[0:3] == 'Rem')
        with open(os.path.join(os.getcwd(), 'Calibration', monitorFile), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Remote " + str(rows + 1), description[0], macAddress] + tvInfo[1])
        return " " + TV.calibrate(os.path.join(os.getcwd(), 'Calibration', monitorFile))

def loadSounds():
    TV.genDisplay('Loading...', 0, 0, height = 3)
    print(TV.debug)
    playThread = TV.playNotes(notes = [440, 554.37] + (not TV.debug) * [659.25, 554.37, 440],
        beats = [1, 1, 1, 1, 1], beatLength = 0.5)
    TV.showWait(0)
    playThread.join()
    TV.showWait(0)


def main():
    with open(os.path.join(os.getcwd(), 'Calibration', groupFile)) as file:
        protocolFile = list(csv.reader(file, delimiter=','))
    
    # Random project
    groupNum = random.randint(1, len(protocolFile)-1)
    protocols = protocolFile[groupNum][1].split('. ')
    protocolName = random.sample(protocols, 1)[0]
    protocol = globals()[protocolName.replace(' ','')]
    
    # Prepare Highscores
    scoreFolder = os.path.join(os.getcwd(), 'Calibration', 'HighScores', protocolFile[groupNum][0])
    if not os.path.exists(scoreFolder):
        os.mkdir(scoreFolder)
    scoreFolder = os.path.join(scoreFolder, protocolName)
    if not os.path.exists(scoreFolder):
        os.mkdir(scoreFolder)
    
    winners = [[0,'cm600286']] * 5
    dirList = os.listdir(scoreFolder)
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
    
    origTrials = protocol.trialsPerSet * protocol.numSets
    protocol.trialsPerSet = 16
    protocol.numSets = 2
    protocol.highScores = [round(score * 32 / origTrials) for score in protocol.highScores]
    
    protocol.initialPracticeTrials = 3
    protocol.trainingTime = 5
    protocol.trainingReps = 1
    protocol.interimPracticeTrials = 0
    protocol.prePracticeBreak = 5
    protocol.postPracticeBreak = 5
    protocol.postSetBreak = 0
    protocol.dummyTrials = 2
    
    calibrate()
    loadSounds()
    
    protocol = protocol('')
    protocol.showWait = showWaitAuto
    stimTestOld = funcType = type(protocol.stimTest)
    protocol.stimTest = funcType(stimTestAuto, protocol)
    protocol.main()
    protocol.win.mouseVisible = False;
    protocol.win.winHandle.minimize()
    protocol.win.winHandle.close()

debugDlg = gui.Dlg(title='Debug Mode?', pos=None, size=None, style=None,\
     labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
debugDlg.show()
TV.debug = debugDlg.OK
longBreakTime = 1

while True:
    main()
