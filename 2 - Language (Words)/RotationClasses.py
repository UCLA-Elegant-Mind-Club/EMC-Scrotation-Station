from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, random
from TVStimuli import TVStimuli

class RotationProtocol(TVStimuli):
    rotations = [0, 30, 60, 90, 120, 150, 180, -150, -120, -90, -60, -30]
    
    def __init__(self, rotations, stimDescription, stimType, fileName = ''):
        for i in range(0,len(self.highScores)):
            self.highScores[i] -= random.randint(0, i * 400)
        self.highScores.sort(reverse = True)
        super().__init__(rotations, stimDescription, stimType, fileName)
    
    def instructions(self):
        self.genDisplay('Welcome player. In this module, there will be ' + str(self.numSets) + ' sets of 3 ' + self.stimDescription + self.stimType + 's', 0, 6)
        self.genDisplay('that you will have to memorize to 3 different keys. After a short training and', 0, 3)
        self.genDisplay('practice round, your mission will be to recognize these ' + self.stimType + 's as fast as', 0, 0)
        self.genDisplay('possible when they have been rotated, so make sure to use your dominant hand!', 0, -3)
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
        self.csvOutput(["Correct Response","Rotation (deg)", "Reaction Time (ms)", "Word"])
        
    def demoSequence(self, rotations, demoMessage):
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.refValue)
        self.genDisplay('(Press space to rotate)', 0, -8)
        self.showWait()
        for rotation in rotations:
            self.genDisplay(demoMessage, 0, 8)
            self.showImage(3, 0, rotation)
            self.showWait(0.1)
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.refValue)
        self.genDisplay('(Press space to continue)', 0, -8)
        self.showWait()
    
    def demo(self):
        self.demoSequence(self.rotations, 'The words will be rotated in a circle as shown below.')

class EnglishWordRoll (RotationProtocol):
    winners = ['Arisvt', 'Mila', 'KayLA', 'Minerva', 'WW', 'Owl', 'Snoopy', 'cm600286', 'Ana', 'Katsaka']
    highScores = [95472, 94725, 94503, 94468, 94274, 94130, 94052, 93668, 93427, 93091]

    if not TVStimuli.debug:
        trainingTime = 5
    
    def __init__(self, fileName = ''):
        super().__init__(self.rotations, 'English', 'word', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [['GLIDE','LEDGE','LIEGE'], ['GRACE','GREAT','GRATE'], ['DEER','DEAR','DOOR'], ['demo']]
        fileName = str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'English Words', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()

class HebrewWordRoll(RotationProtocol):
    winners = ['WW', 'KayLA', 'Arisvt', 'Minerva', 'Mila', 'Katsaka', 'Brian', 'Snoopy', 'cm600286', 'Samushka']
    highScores = [92560, 92319, 92276, 91589, 90669, 89813, 87408, 87336, 85451, 84110]

    def __init__(self, fileName):
        super().__init__(self.rotations, 'Hebrew', 'word', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [['GLIDE','LEDGE','LIEGE'], ['GRACE','GREAT','GRATE'], ['EQUIP','BOUND','PROWL'], ['demo']]
        fileName = str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'Hebrew Words', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()

class NonsenseWordRoll(RotationProtocol):
    winners = ['Minerva', 'WW', 'Arisvt', 'Mila', 'KayLA', 'Johnny2', 'Annika', 'Nat', 'BRGJ', 'Katsaka']
    highScores = [85696, 85646, 85191, 84935, 82726, 81222, 79835, 78097, 77787, 71178]

    def __init__(self, fileName = ''):
        super().__init__(self.rotations, 'Unfamiliar', 'words', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [['GLIDE','LEDGE','LIEGE'], ['GRACE','GLIDE','GRATE'], ['EQUIP','BOUND','PROWL'], ['demo']]
        fileName = str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'Nonsense Words', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()