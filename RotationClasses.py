from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, random
from TVStimuli import TVStimuli

class RotationProtocol(TVStimuli):
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
    
    def showImage(self, displayImage, set, showTarget, testValue):
        pass
    
    def initFile(self):
        self.csvOutput(["Correct Response","Rotation (deg)", "Reaction Time (ms)", "Target"])
        
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

class FaceRoll(RotationProtocol):
    rotations = [0, 30, 60, 90, 120, 150, 180, -150, -120, -90, -60, -30]
    winners = ['cm600286', 'Arisvt', 'Minerva', 'Cerisol', 'SausageBoy', 'Snoopy', 'CyndaquilIsFire', 'S0PH14', 'Owl', 'Will']
    highScores = [94162, 92286, 91199, 90935, 90735, 90392, 89626, 89352, 88800, 88545]
    
    def __init__(self, fileName = ''):
        super().__init__(self.rotations, '', 'face', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'Face ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'New Faces', 'Roll', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()
        self.displayImage.ori = 0
        
    def demo(self):
        self.demoSequence(self.rotations,
            'The faces will be rotated in a circle as shown below.')
        
class FaceYaw(RotationProtocol):
    rotations = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90]
    winners = ['S0PH14', 'Arisvt', 'cm600286', 'SausageBoy', 'Minerva', 'AmongUs', 'Cerisol', 'Snoopy', 'Ringo', 'CyndaquilIsFire']
    highScores = [92495, 91296, 90989, 90628, 90241, 90203, 90176, 89773, 89198, 88925]

    def __init__(self, fileName = ''):
        super().__init__(self.rotations, '', 'face', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        faceFolder = 'Face ' + str(targets[set][showTarget])
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'New Faces', 'Yaw', faceFolder, 'BW', (str(int(rotation))+'.png'))
        self.displayImage.draw()

    def demo(self):
        self.demoSequence(self.rotations, 'The faces will be rotated left and right as shown below.')
        
class FacePitch(RotationProtocol):
    rotations = [-60, -52.5, -45, -37.5, -30, -22.5, -15, -7.5, 0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5, 60]
    winners = ['Snoopy', 'Arisvt', 'Cerisol', 'cm600286', 'Ringo', 'CyndaquilIsFire', 'AmongUs', 'Ana', 'Stranger', 'XAVW']
    highScores = [92536, 92113, 90436, 89365, 88078, 86062, 85424, 83905, 83409, 82513]

    def __init__(self, fileName = ''):
        super().__init__(self.rotations, '', 'face', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        faceFolder = 'Face ' + str(targets[set][showTarget])
        if int(rotation) == rotation:
            self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'New Faces', 'Pitch', faceFolder, 'BW', (str(int(rotation))+'.png'))
        else:
            self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'New Faces', 'Pitch', faceFolder, 'BW', (str(round(rotation, 1))+'.png'))
        self.displayImage.draw()

    def demo(self):
        self.demoSequence(self.rotations, 'The faces will be rotated up and down as shown below.')

class EnglishRoll(RotationProtocol):
    rotations = [0, 30, 60, 90, 120, 150, 180, -150, -120, -90, -60, -30]
    winners = ['Arisvt', 'Mila', 'KayLA', 'Minerva', 'WW', 'Owl', 'Snoopy', 'cm600286', 'Ana', 'Katsaka']
    highScores = [95472, 94725, 94503, 94468, 94274, 94130, 94052, 93668, 93427, 93091]

    trainingTime = 5
    
    def __init__(self, fileName = ''):
        super().__init__(self.rotations, 'English', 'letter', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'char ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'English Characters', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()

    def demo(self):
        self.demoSequence(self.rotations, 'The letters will be rotated in a circle as shown below.')

class ThaiRoll(RotationProtocol):
    rotations = [0, 30, 60, 90, 120, 150, 180, -150, -120, -90, -60, -30]
    winners = ['WW', 'KayLA', 'Arisvt', 'Minerva', 'Mila', 'Katsaka', 'Brian', 'Snoopy', 'cm600286', 'Samushka']
    highScores = [92560, 92319, 92276, 91589, 90669, 89813, 87408, 87336, 85451, 84110]

    def __init__(self, fileName):
        super().__init__(self.rotations, 'Thai', 'characters', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'char ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'Thai Characters', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()

    def demo(self):
        self.demoSequence(self.rotations, 'The characters will be rotated in a circle as shown below.')

class ChineseRoll(RotationProtocol):
    rotations = [0, 30, 60, 90, 120, 150, 180, -150, -120, -90, -60, -30]
    winners = ['Minerva', 'WW', 'Arisvt', 'Mila', 'KayLA', 'Johnny2', 'Annika', 'Nat', 'BRGJ', 'Katsaka']
    highScores = [85696, 85646, 85191, 84935, 82726, 81222, 79835, 78097, 77787, 71178]

    def __init__(self, fileName = ''):
        super().__init__(self.rotations, 'Chinese', 'characters', fileName = fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'char ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'Chinese Characters', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()

    def demo(self):
        self.demoSequence(self.rotations, 'The characters will be rotated in a circle as shown below.')
        
class ChineseRollNew(ChineseRoll):
    trialsPerSet = 50
    practiceFreq = 25
    
    def __init__(self, fileName = ''):
        super().__init__(fileName)
    
    def showImage(self, set, showTarget, rotation):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'char ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'Chinese Characters New', fileName)
        self.displayImage.ori = rotation
        self.displayImage.draw()