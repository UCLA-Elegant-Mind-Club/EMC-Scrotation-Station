from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, math
from TVStimuli import TVStimuli

class ScalingProtocol(TVStimuli):
    baseSizes = [1, 2, 4, 8, 16, 28]
    
    def __init__(self, stimDescription, stimType, fileName = ''):
        sizes = self.baseSizes
        for i in range(0, len(self.baseSizes) - 1):
            diff = math.log10(self.baseSizes[i + 1] / self.baseSizes[i])/2
            intermed = self.baseSizes[i] * 10 ** diff
            sizes = sizes + [round(intermed,2)]
        sizes.sort()
        super().__init__(sizes, stimDescription, stimType, fileName)
    
    def instructions(self):
        self.genDisplay('Welcome player. In this module, there will be ' + str(self.numSets) + ' sets of 3 ' + self.stimDescription + self.stimType + 's', 0, 6)
        self.genDisplay('that you will have to memorize to 3 different keys. After a short training and', 0, 3)
        self.genDisplay('practice round, your mission will be to recognize these ' + self.stimType + 's as fast as', 0, 0)
        self.genDisplay('possible when they have been rescaled, so make sure to use your dominant hand!', 0, -3)
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
        self.csvOutput(['Correct Response', 'Height', 'RT', 'Face'])
    
    def showImage(self, set, showTarget, size, folder):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'char ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', folder, fileName)
        faceWidth = self.angleCalc(size) * float(self.tvInfo['faceWidth'])
        faceHeight = self.angleCalc(size) * float(self.tvInfo['faceHeight'])
        self.displayImage.size = (faceWidth, faceHeight)
        self.displayImage.draw()
    
    def demoSequence(self, sizes, demoMessage):
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.referenceSize)
        self.genDisplay('(Press space to rescale)', 0, -8)
        self.showWait()
        for size in sizes:
            self.genDisplay(demoMessage, 0, 8)
            self.showImage(3, 0, size)
            self.showWait(0.1)
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.referenceSize)
        self.genDisplay('(Press space to continue)', 0, -8)
        self.showWait()
        
    def demo(self):
        print(self.testValues)
        self.demoSequence(self.testValues, 'The characters will be rescaled as shown below.')
    
class EnglishScaling(ScalingProtocol):
    winners = ['Ana', 'Minerva', 'Will', 'Cerisol', 'RNFO', 'CyndaquilIsFire', ' ', 'SausageBoy', 'cm600286', 'AmongUs']
    highScores = [145301, 142012, 141954, 138562, 134953, 128433, 127950, 126169, 124406, 121526]

    if not debug:
        trainingTime = 5
    
    def __init__(self, fileName = ''):
        super().__init__('English', 'letter', fileName = fileName)
    
    def showImage(self, set, showTarget, size):
        super().showImage(set, showTarget, size, 'English Characters')

class ThaiScaling(ScalingProtocol):
    winners = ['WW', 'KayLA', 'Arisvt', 'Minerva', 'Mila', 'Katsaka', 'Brian', 'Snoopy', 'cm600286', 'Samushka']
    highScores = [92560, 92319, 92276, 91589, 90669, 89813, 87408, 87336, 85451, 84110]

    def __init__(self, fileName):
        super().__init__('Thai', 'characters', fileName = fileName)
    
    def showImage(self, set, showTarget, size):
        super().showImage(set, showTarget, size, 'Thai Characters')

class ChineseScaling(ScalingProtocol):
    winners = ['cm600286', 'Mila', 'KayLA', 'Minerva', 'Arisvt', 'RNFO', 'Bot6', 'Snoopy', 'Ana', 'BruinCub']
    highScores = [143509, 135973, 134306, 133651, 133637, 132135, 131291, 116550, 114824, 114323]

    def __init__(self, fileName = ''):
        super().__init__('Chinese', 'characters', fileName = fileName)
    
    def showImage(self, set, showTarget, size):
        super().showImage(set, showTarget, size, 'Chinese Characters')