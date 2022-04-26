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
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], ['demo']];
        folderName = 'face ' + str(targets[set][showTarget])
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', '6 Famous Faces', folderName, 'main.png')
        self.displayImage.ori = rotation
        self.displayImage.draw()
    
    def initFile(self):
        self.csvOutput(["Correct Response","Rotation (deg)", "Reaction Time (ms)", "Target"])
        
    def demoSequence(self, rotations, demoMessage):
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(self.numSets, 0, self.refValue)
        self.genDisplay('(Press space to rotate)', 0, -8)
        self.showWait()
        for rotation in rotations:
            self.genDisplay(demoMessage, 0, 8)
            self.showImage(self.numSets, 0, rotation)
            self.showWait(0.1)
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(self.numSets, 0, self.refValue)
        self.genDisplay('(Press space to continue)', 0, -8)
        self.showWait()
    
    def demo(self):
        self.demoSequence(self.rotations, 'The characters will be rotated in a circle as shown below.')

class FaceTraining(RotationProtocol):
    names = ["Biden", "Putin", "Trump", "Michael B Joran", "Obama", "Dwayne Johnson"]
    trainingTime = 1;
    
    def __init__(self):
        super().__init__(self.rotations, 'Famous', 'Faces', fileName = '')
        
    def main(self):
        for i in range(0,9):
            self.genDisplay('The following images are of ' + self.names[i] + '.', 0, 3)
            self.genDisplay('(Press space to continue)', 0, 0)
            self.showWait()
            dirList = os.listdir(os.path.join(os.getcwd(), 'Stimuli', 'face ' + str(i + 1)));
            for name in dirList:
                if name != 'main.png':
                    self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'face ' + str(i + 1), name)
                    self.displayImage.draw()
                    self.genDisplay('This is ' + self.names[i] + '.', 0, -8)
                    self.showWait(self.trainingTime)

class FaceRoll(RotationProtocol):
    winners = ['Arisvt', 'Mila', 'KayLA', 'Minerva', 'WW', 'Owl', 'Snoopy', 'cm600286', 'Ana', 'Katsaka']
    highScores = [95472, 94725, 94503, 94468, 94274, 94130, 94052, 93668, 93427, 93091]
    
    def __init__(self, fileName = ''):
        super().__init__(self.rotations, 'Famous', 'face', fileName = fileName)