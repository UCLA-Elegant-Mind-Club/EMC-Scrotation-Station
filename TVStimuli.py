from psychopy import gui, visual, core, event, monitors, prefs
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import threading
from psychopy.sound import Sound
from psychopy.event import waitKeys
import numpy as np
import os, time, random, math, csv, re, uuid
from abc import ABC, abstractmethod

textZoom = 1.25

class TVStimuli(ABC):
    debug = False
    
    numSets = 3
    trialsPerSet = 32
    totalTrials = numSets * trialsPerSet
    
    trainingTime = 10
    trainingReps = 2
    
    crossSize = 4
    referenceSize = 8
    refValue = 0
    
    practiceFreq = -1
    prePracticeBreak = 5
    postPracticeBreak = 5
    postSetBreak = 60
    initialPracticeTrials = 12
    interimPracticeTrials = 6
    dummyTrials = 3
    timeOut = 1.2
    
    tvInfo = mon = win = displayImage = 0
    recordData = True
    winners = []
    highScores = []
    rank = [-1, -1]
    
    def __init__(self, testValues: list, stimDescription: str, stimType: str, fileName: str = ''):
        self.testValues = testValues
        
        if len(stimDescription) > 0:
            stimDescription += ' '
        self.stimDescription = stimDescription
        self.stimType = stimType
        
        self.totalTrials = self.numSets * self.trialsPerSet
        self.fileName = fileName
        self.recordData = self.recordData and fileName != ''
        if self.recordData and not os.path.isfile(fileName):
            self.initFile()
        self.score = 0
        self.streak = 0
        
        self.initTestValues(testValues)

    def initTestValues(self, testValues: list):
        trialsPerValue = math.floor(self.totalTrials/len(testValues))
        extraTrials = self.totalTrials - trialsPerValue * len(testValues)
        self.testArray = testValues * trialsPerValue + random.sample(testValues, extraTrials)
        random.shuffle(self.testArray)

    @abstractmethod
    def showImage(self, set: int, showTarget: int, testValue: float):
        pass
        
    @abstractmethod
    def initFile(self):
        pass

    def csvOutput(self, output: list):
        if(self.fileName != ''):
            with open(self.fileName, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(output)
            csvFile.close()
    
    @staticmethod
    def calibrate(calibrationFile: str = 'monitors.csv', mon: str = 'TV',
                    crossFile: str = os.path.join(os.getcwd(), 'Calibration', 'cross.png')) -> None or str:
            
        macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        with open(calibrationFile) as csvFile:
            reader = csv.DictReader(csvFile, delimiter = ',')
            tvInfo = {'MacAddress' : 0}
            while tvInfo['MacAddress'] != macAddress:
                try: tvInfo = next(reader)
                except:
                    csvFile.close()
                    return None
        csvFile.close()
        screenBrightness = -0.3
        mon = monitors.Monitor(mon)
        mon.setWidth(float(tvInfo['Width (cm)']))
        win = visual.Window(size = (int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])),
            fullscr = True, screen = int(tvInfo['Screen number']), winType = 'pyglet',
            allowGUI = True, allowStencil = False, monitor = mon, color = np.multiply([1,1,1], screenBrightness),
            colorSpace = 'rgb', blendMode = 'avg', useFBO = True, units = 'cm')
        win.mouseVisible = False;
        
        TVStimuli.mon = mon
        TVStimuli.win = win
        TVStimuli.tvInfo = tvInfo
        
        crossImg = os.path.join(crossFile)
        crossWidth = TVStimuli.angleCalc(TVStimuli.crossSize) * float(tvInfo['faceHeight'])
        crossHeight = TVStimuli.angleCalc(TVStimuli.crossSize) * float(tvInfo['faceWidth'])
        TVStimuli.cross = visual.ImageStim(win = win, units = 'cm', image = crossImg, size = (crossWidth, crossHeight))

        trainingHeight = TVStimuli.angleCalc(TVStimuli.referenceSize) * float(tvInfo['faceHeight'])
        trainingWidth = TVStimuli.angleCalc(TVStimuli.referenceSize) * float(tvInfo['faceWidth'])
        TVStimuli.displayImage = visual.ImageStim(win = win, units='cm',
            size = (trainingWidth,trainingHeight), interpolate=True)
        return tvInfo['Label']
            
    @staticmethod
    def angleCalc(angle: float):
        radians = math.radians(angle)
        spacer = 2 * math.tan(radians/2) * float(TVStimuli.tvInfo['Distance to screen'])
        return spacer
    
    @staticmethod
    def genDisplay(text: str, xPos: float, yPos: float, height: float = 1.5, color: str = 'white'):
        displayText = visual.TextStim(win = TVStimuli.win, text = text, font = 'Arial',
        pos = (xPos * textZoom, yPos * textZoom + yPos * float(TVStimuli.tvInfo['spacer'])),
        height = height * float(TVStimuli.tvInfo['height']) * textZoom, wrapWidth = 500, color = color)
        displayText.draw();
    
    @abstractmethod
    def instructions(self):
        pass
    
    @abstractmethod
    def demoSequence(self, testValues: list, demoMessage: str):
        pass
    
    @abstractmethod
    def demo(self):
        pass
    
    def showHighScores(self):
        i = 0
        leftEdge, rightEdge = -float(self.tvInfo['leftEdge']), float(self.tvInfo['rightEdge'])
        scoreText = 'Try to beat these High Scores!'
        while i < len(self.winners):
            self.genDisplay(scoreText, 0, 8, height = 3)
            for j in range (0, 5):
                if i + j < len(self.winners):
                    self.genDisplay(str(self.winners[i + j]), (rightEdge - leftEdge) * -1/8, 4 - 2 * j)
                    self.genDisplay(str(self.highScores[i + j]), (rightEdge - leftEdge) * 1/8, 4 - 2 * j)
                    self.genDisplay('Press space to continue', 0, -8)
            i += 5
            scoreText = 'Here are some recent scores!'
            self.showWait()
 
    def checkHighScores(self):
        rank = [-1, -1]
        for i in range(0, 5):
            if self.score > self.highScores[i]:
                rank[0] = i + 1
                break;
        for i in range(5, len(self.highScores)):
            if self.score > self.highScores[i]:
                rank[1] = i - 4
                break;
        return rank;
    
    @staticmethod
    def showWait(seconds: float = -1, keys: list = ['space'], flip: bool = True, timeOnly: bool = True):
        if flip: TVStimuli.win.flip()
        if seconds < 0:
            key = waitKeys(keyList = keys + ['escape'])
        elif timeOnly:
            key = waitKeys(keyList = ['escape'], maxWait = seconds)
        else:
            key = waitKeys(keyList = keys + ['escape'], maxWait = seconds)
        if key != None and key[0] == 'escape':
            core.quit()

    def breakScreen(self, trialsLeft: int = 0):
        print('Short Set Break')
        self.streak = 0
        for i in range(0, self.postSetBreak):
            self.genDisplay('Quick Break', 0, 6)
            self.genDisplay('You have ' + str(self.postSetBreak - i) + ' seconds to rest your eyes', 0, 3)
            self.genDisplay('and stretch your arms.', 0, 1)
            if trialsLeft > 0:
                self.genDisplay('Trials left in experiment: ' + str(trialsLeft), 0, -6)
            self.genDisplay('Current score: ' + str(self.score), 0, -9, height = 3)
            self.showWait(1)
    
    def levelScreen(self, text1: str, text2: str):
        if text2 == '1':
            self.playNotes(notes = [220, 277.18, 329.63, 277.18, 329.63, 554.37, 277.18, 329.63, 440],
                beats = [1, 1, 1, 1, 1, 1, 1, 1, 4], beatLength = 0.1)
        elif text2 == '2':
            self.playNotes(notes = [440, 466.16, 440, 415.30, 440, '', 220, '', 220, '', 220],
                beats = [1, 1, 1, 1, 4, 2, 0.5, 0.5, 0.5, 0.5, 2], beatLength = 0.1)
        elif text2 == '3':
            self.playNotes(notes = [220, 277.18, 329.63, 440, 554.37, 440, 329.63, 277.18, 220],
                beats = [1, 1, 1, 1, 1, 1, 1, 1, 4], beatLength = 0.1)
        leftEdge, rightEdge = -float(self.tvInfo['leftEdge']), float(self.tvInfo['rightEdge'])
        xPos = leftEdge
        while xPos < rightEdge:
            self.genDisplay(text1, xPos, 6, height = 6)
            self.genDisplay(text2, -xPos, -2, height = 4)
            xPos += max(abs(xPos)/2, (rightEdge - leftEdge)/1000)
            self.win.flip()
    
    def learningTrial(self, set: int, target: int, mapping: str, repeatText: bool = False):
            yShift = repeatText * 3
            if(repeatText):
                self.genDisplay('Training has restarted from the first ' + self.stimType + '.', 0, 6)
            self.genDisplay('You have ' + str(self.trainingTime) + ' seconds to', 0, 6 - yShift)
            self.genDisplay('memorize the ' + self.stimType + ' on the next slide (mapped to ' + mapping + ')', 0, 3 - yShift)
            self.genDisplay('Press \'' + mapping + '\' to continue.', 0, -3)
            self.showWait(keys = [mapping])
            self.showImage(set, target, self.refValue)
            self.showWait(self.trainingTime)
            self.genDisplay('Press \'' + mapping + '\' to continue.', 0, 0)
            self.showWait(keys = [mapping])
    
    def learningPeriod(self, set: int):
        self.genDisplay('You have ' + str(self.trainingTime) + ' seconds to', 0, 6)
        self.genDisplay('memorize each of the 3 ' + self.stimType + 's on the next slides.', 0, 3)
        self.genDisplay('Don\'t focus on memorizing minor details.', 0, 0)
        if self.trainingReps > 1:
            self.genDisplay('The ' + self.stimType + 's will each be repeated ' + str(self.trainingReps) + ' times', 0, -3)
        self.genDisplay('Press spacebar to continue.', 0, -5 - (self.trainingReps > 1))
        self.showWait()
        for rep in range(0, self.trainingReps):
            self.learningTrial(set, target = 0, mapping = 'v', repeatText = rep > 0)
            self.learningTrial(set, target = 1, mapping = 'b')
            self.learningTrial(set, target = 2, mapping = 'n')

    @staticmethod
    def showCross(prePause: float = 0.5, postPause: float = 0.2):
        TVStimuli.showWait(prePause)
        TVStimuli.cross.draw()
        TVStimuli.showWait(postPause)
        TVStimuli.win.flip()
    
    def stimTest(self, set: int, target: int, testValue: any, correctKey: str, practice: bool = False):
        self.showCross()
        self.showWait(random.randint(5,15)/10, flip = False)
        self.showImage(set, target, testValue)
        result = {'start': 0, 'end': 0}
        self.win.timeOnFlip(result, 'start')
        self.win.flip()
        
        keys = event.waitKeys(timeStamped = True, maxWait = self.timeOut + float(self.tvInfo['timeDelay'])/1000)
        if keys == None:
            response = 'timedOut'
            result['end'] = result['start']
        else:
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
    
    def feedback(self, correct: bool or int, scoreChange: float = 0):
        rightMessage = random.sample(['Correct!'], 1)[0]
        wrongMessage = random.sample(['Incorrect'], 1)[0]
        overTimeMessage = random.sample(['Out of time'], 1)[0]
        
        if self.score + scoreChange < 0:
            scoreChange = -self.score
        scoreChange = 0 if round(scoreChange) == 0 else min(round(scoreChange) + self.streak * 5 * correct, 1000)
        scoreDisplay = self.score if scoreChange != 0 else self.score + 1 - 2 * correct
        self.score += scoreChange 
        scoreInc = math.pow(abs(self.score - scoreDisplay), 2/3) if scoreChange != 0 else 1
        
        if correct == 1:
            base = 400 + self.streak * 20
            self.streak = self.streak + (self.streak < 10 and scoreChange > 0)
            playThread = self.playNotes([base, base * 5/4, base * 3/2, ''], [1, 1, 2, 1])
            while scoreDisplay < self.score:
                self.genDisplay(rightMessage, 0, 2, height = 3, color = [0,1,0])
                scoreDisplay = min(scoreDisplay + scoreInc, self.score)
                if scoreChange != 0:
                    self.genDisplay('+' + str(scoreChange), 0, -2, color = [0,1,0])
                    self.genDisplay('Score: ' + str(round(scoreDisplay)), 0, -5, height = 2)
                else:
                    self.genDisplay('(Still Warming Up)', 0, -2)
                self.win.flip()
            self.showWait(0.5, flip = False)
            playThread.join()
        else:
            self.streak = 0
            message = wrongMessage if correct == 0 else overTimeMessage
            playThread = self.playNotes([440, 349.23, ''], [2, 2, 1])
            while scoreDisplay > self.score:
                self.genDisplay(message, 0, 2, height = 3, color = [1,-0.5,-0.5])
                scoreDisplay = max(scoreDisplay - scoreInc, self.score)
                if scoreChange != 0:
                    self.genDisplay(str(scoreChange), 0, -2, color = [1,-0.5,-0.5])
                    self.genDisplay('Score: ' + str(round(scoreDisplay)), 0, -5, height = 2)
                else:
                    self.genDisplay('(Still Warming Up)', 0, -2)
                self.win.flip()
            self.showWait(0.5, flip = False)
            playThread.join()

    @staticmethod
    def playNotes(notes: list, beats: list, beatLength: float = 0.15, loop: int = 0, freeze: bool = False) -> threading.Thread:
        noteThread = threading.Thread(target = TVStimuli.noteThread, args = (notes, beats, beatLength, loop))
        noteThread.start()
        if loop >= 0 and freeze: TVStimuli.showWait(sum(beats) * beatLength * (loop + 1), flip = False)
        return noteThread
    
    @staticmethod
    def noteThread(notes: list, beats: list, beatLength: float, loop: int):
        i = 0
        while i < len(notes):
            if notes[i] != '':
                notes[i] = Sound(value = notes[i], secs = beats[i] * beatLength, stereo = -1, volume = 0.5)
                notes[i].play()
            time.sleep(beats[i] * beatLength)
            i += 1
            if i == len(notes) and loop != 0:
                i = 0
                loop -= 1
    
    def practiceRound(self, set: int, practiceTrials: int = initialPracticeTrials, trialsLeft: int = 0):
        print('Practice Round')
        
        perStim = int(math.ceil(practiceTrials/6))
        practiceStim = [0,1,2]*perStim
        extra = practiceTrials - perStim*3
        extra = extra * (extra > 0)
        practiceStim += random.sample(practiceStim, extra)
        random.shuffle(practiceStim);
        
        for i in range(self.prePracticeBreak):
            self.genDisplay('Practice round starts in:', 0, 6, height = 3)
            self.genDisplay(str(self.prePracticeBreak - i) + ' seconds', 0, 2, height = 3)
            self.genDisplay('Number of practice trials: ' + str(len(practiceStim)), 0, -3)
            if trialsLeft > 0:
                self.genDisplay('Trials left in experiment: ' + str(trialsLeft), 0, -6)
            self.showWait(1)
        
        for target in practiceStim:
            self.stimTest(set, target, self.refValue, ['v','b','n'][target], practice = True)

        for i in range(self.postPracticeBreak):
            self.genDisplay('Experiment starts in:', 0, 3, height = 3)
            self.genDisplay(str(self.postPracticeBreak - i) + ' seconds', 0, -1, height = 3)
            self.genDisplay('Trials left in experiment: ' + str(trialsLeft), 0, -6)
            self.showWait(1)
            
        for i in range(self.dummyTrials):
            target = random.randint(0,2)
            self.stimTest(set, target, random.sample(self.testValues, 1)[0], ['v','b','n'][target], practice = True)

    def experimentalRound(self, set: int):
        trialNum = 0
        print('Experimental Round')
        while trialNum < self.trialsPerSet:
            fullTrialNum = set * self.trialsPerSet + trialNum
            if trialNum > 0 and self.practiceFreq > 0 and trialNum % self.practiceFreq == 0:
                self.practiceRound(set, self.interimPracticeTrials,
                    trialsLeft = self.totalTrials - fullTrialNum)
                
            self.showWait(1)
            testValue = self.testArray[fullTrialNum]
            target = random.randint(0,2)
            result = self.stimTest(set, target, testValue, ['v','b','n'][target])
            print('Trial ' + str(fullTrialNum + 1) + ' time: ' + str(result[2]) + '; Correct = ' + str(result[0]))
            if(result[0] == 1):
                trialNum += 1
            else:
                insert = random.randint(fullTrialNum + 1, len(self.testArray))
                self.testArray = self.testArray[0:fullTrialNum] + self.testArray[fullTrialNum + 1:insert] \
                    + [testValue] + self.testArray[insert:]
            if self.recordData:
                self.csvOutput(result)
            
    def main(self):
        self.instructions()
        for setNum in range(0, self.numSets):
            self.levelScreen('Level', str(setNum + 1))
            self.learningPeriod(setNum)
            self.practiceRound(setNum, self.initialPracticeTrials, trialsLeft = self.totalTrials - setNum * self.trialsPerSet)
            self.experimentalRound(setNum)
            if setNum < self.numSets - 1:
                self.breakScreen(trialsLeft = self.totalTrials - (setNum + 1) * self.trialsPerSet)
                
        self.playNotes(notes = [220, 277.18, 329.63, 277.18, 329.63, 440, 329.63, 440, 554.37, 440, 554.37, 659.25, 554.37, 659.25, 880],
            beats = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4], beatLength = 0.1)
        self.genDisplay('Done!', 0, 6, height = 3)
        self.genDisplay('Final Score: ' + str(self.score), 0, 2, height = 3, color = [0,1,0])
        rank = self.checkHighScores()
        if rank[0] > 0:
            self.genDisplay('Congratulations! You ranked in place ' + str(rank[0]) + ' among the top scores!', 0, -2, color = [1,1,-1])
        if rank[1] > 0:
            self.genDisplay('Congratulations! You ranked in place ' + str(rank[1]) + ' among the recent scores!', 0, -2 - 3 * (rank[0] > 0), color = [1,1,-1])
        self.genDisplay('Press space to continue.', 0, -6 - 3 * (rank[0] > 0))
        print('Current Protocol Finished. Score = ' + str(self.score) + '; Rank = ' + str(rank))
        self.rank = rank
        self.showWait()

# Import documentation for tooltips
from TVStimuli_Doc import TVStimuli_Doc as doc
TVStimuli.__doc__ = doc.__doc__
functions = doc.__dict__
for funct in list(functions.keys())[2:-2]:
    getattr(TVStimuli, funct).__doc__ = functions[funct].__doc__
