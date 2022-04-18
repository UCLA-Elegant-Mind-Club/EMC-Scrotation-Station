from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, random, math
from TVStimuli import TVStimuli

class ScalingRotationProtocol(TVStimuli):
    winners = ['Ana', 'Minerva', 'Will', 'Cerisol', 'RNFO', 'CyndaquilIsFire', ' ', 'SausageBoy', 'cm600286', 'AmongUs']
    highScores = [95472, 94725, 94503, 94468, 94274, 94130, 94052, 93668, 93427, 93091]
    
    baseSizes = [4, 8, 16]
    rotations = [0, 45, 90, 135, -135, -90, -45, 0]
    refValue = (TVStimuli.referenceSize, 0)
    
    def __init__(self, fileName = ''):
        values = []
        for size in self.baseSizes:
            for rot in self.rotations:
                values += [(size, rot)]
        
        for i in range(0,len(self.highScores)):
            self.highScores[i] -= random.randint(0, i * 400)
        self.highScores.sort(reverse = True)
        
        super().__init__(values, '', 'face', fileName)
    
    def instructions(self):
        self.genDisplay('Welcome player. In this module, there will be ' + str(self.numSets) + ' sets of 3 ' + self.stimDescription + self.stimType + 's', 0, 6)
        self.genDisplay('that you will have to memorize to 3 different keys. After a short training and', 0, 3)
        self.genDisplay('practice round, your mission will be to recognize these ' + self.stimType + 's as fast as possible', 0, 0)
        self.genDisplay('when they have been rescaled and/or rotated, so make sure to use your dominant hand!', 0, -3)
        self.genDisplay('Press spacebar to continue.', 0, -6)
        self.showWait()
        self.genDisplay('The faster you respond, the more points you can score - you can win up to 1000', 0, 8)
        self.genDisplay('points in each trial. However, after ' + str(self.timeOut) + ' seconds, you\'ll automatically lose', 0, 5)
        self.genDisplay('400 points for taking too long. If you make an error, you\'ll also lose points, but', 0, 2)
        self.genDisplay('slightly less than 400. However, try not to randomly guess. Your trial number will', 0, -1)
        self.genDisplay('only advance for correct trials, so you\'ll have the same chances to win points.', 0, -4)
        self.genDisplay('Press spacebar to continue.', 0, -7)
        self.showWait()
        self.demo()
        self.showHighScores()
        self.genDisplay('Are you ready?', 0, 3, height = 3)
        self.genDisplay('Press space to start.', 0, -2)
        self.showWait()
    
    def initFile(self):
        self.csvOutput(['Correct Response', 'Height/Rotation', 'RT', 'Face'])
    
    def showImage(self, set, showTarget, testVar):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'face ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', fileName)
        faceWidth = self.angleCalc(testVar[0]) * float(self.tvInfo['faceWidth'])
        faceHeight = self.angleCalc(testVar[0]) * float(self.tvInfo['faceHeight'])
        self.displayImage.size = (faceWidth, faceHeight)
        self.displayImage.ori = testVar[1]
        self.displayImage.draw()
    
    def demoSequence(self, testVars, demoMessage, buttonMessage, showTime):
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.refValue)
        self.genDisplay('(Press space to ' + buttonMessage + ')', 0, -8)
        self.showWait()
        for testVar in testVars:
            self.genDisplay(demoMessage, 0, 8)
            self.showImage(3, 0, testVar)
            self.showWait(showTime)
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.refValue)
        self.genDisplay('(Press space to continue)', 0, -8)
        self.showWait()
        
    def demo(self):
        print(self.testValues)
        self.demoSequence([(size, 0) for size in self.baseSizes], 'The faces will be resized as shown below.', 'resize', 0.2)
        self.demoSequence([(self.referenceSize, rot) for rot in self.rotations], 'The faces will also be rotated as shown below.', 'rotate', 0.1)
