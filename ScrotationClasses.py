from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, random, math
from TVStimuli import TVStimuli

##### Parent Rotation and Scaling Classes #####
##### Parent Rotation and Scaling Classes #####
##### Parent Rotation and Scaling Classes #####

class RotationProtocol (TVStimuli):
    rotations = [0, 30, 60, 90, 120, 150, 180, -150, -120, -90, -60, -30]
    
    def initRotations(self, rotations):
        self.rotations = rotations
    
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
        self.displayImage.image = self.getImage(set, showTarget)
        self.displayImage.ori = rotation
        self.displayImage.draw()
    
    def getImage(self, set, showTarget):
        pass;
    
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
        self.demoSequence(self.rotations, 'The ' + self.stimType + 's will be rotated in a circle as shown below.')

class ScalingProtocol(TVStimuli):
    sizes = [1, 2, 4, 8, 16, 28]
    
    def initSizes(self, sizes):
        for i in range(0, len(self.sizes) - 1):
            diff = math.log10(self.sizes[i + 1] / self.sizes[i])/2
            intermed = self.sizes[i] * 10 ** diff
            sizes = sizes + [round(intermed,2)]
        sizes.sort()
        self.sizes = sizes
        self.refValue = self.referenceSize
    
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
        self.csvOutput(["Correct Response","Height (deg)", "Reaction Time (ms)", "Target"])
    
    def showImage(self, set, showTarget, size):
        self.displayImage.image = self.getImage(set, showTarget)
        faceWidth = self.angleCalc(size) * float(self.tvInfo['faceWidth'])
        faceHeight = self.angleCalc(size) * float(self.tvInfo['faceHeight'])
        self.displayImage.size = (faceWidth, faceHeight)
        self.displayImage.draw()
    
    def getImage(self, set, showTarget):
        pass;
    
    def demoSequence(self, sizes, demoMessage):
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(self.numSets, 0, self.referenceSize)
        self.genDisplay('(Press space to rescale)', 0, -8)
        self.showWait()
        for size in sizes:
            self.genDisplay(demoMessage, 0, 8)
            self.showImage(self.numSets, 0, size)
            self.showWait(0.1)
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(self.numSets, 0, self.referenceSize)
        self.genDisplay('(Press space to continue)', 0, -8)
        self.showWait()
        
    def demo(self):
        print(self.testValues)
        self.demoSequence(self.sizes, 'The ' + self.stimType + 's will be rescaled as shown below.')


##### Familiar Faces Protocols #####
##### Familiar Faces Protocols #####
##### Familiar Faces Protocols #####


class FamiliarFaces (TVStimuli):
    names = ["Biden", "Putin", "Trump", "Michael Jordan", "Obama", "Dwayne Johnson", "Oprah Winfrey"]
    numSets = 2
    trialsPerSet = 40
    
    trainingTime = 10
    trainingReps = 1
    
    def __init__(self, testValues, fileName = ''):
        super().__init__(testValues, 'Celebrity', 'Face', fileName = '')
    
    def getImage(self, set, showTarget):
        fileName = self.names[set * 3 + showTarget] + '.png'
        return os.path.join(os.getcwd(), '2 - Familiar Faces', 'Stimuli', 'Celeb Faces 2', fileName)
    
    def learningTrial(self, set, target, mapping, repeatText = False):
            yShift = repeatText * 3
            if(repeatText):
                self.genDisplay('Training has restarted from ' + self.names[0] + '.', 0, 6)
            self.genDisplay('You have ' + str(self.trainingTime) + ' seconds to', 0, 6 - yShift)
            self.genDisplay('memorize ' + self.names[set * 3 + target] + '\'s face on the next slide (mapped to ' + mapping + ')', 0, 3 - yShift)
            self.genDisplay('Press \'' + mapping + '\' to continue.', 0, -3)
            self.showWait(keys = [mapping])
            self.showImage(set, target, self.refValue)
            self.showWait(self.trainingTime)
            self.genDisplay('Press \'' + mapping + '\' to continue.', 0, 0)
            self.showWait(keys = [mapping])

#Rotation
class FamousFacesRoll(FamiliarFaces, RotationProtocol):
    def __init__(self, fileName = ''):
        self.initRotations(self.rotations)
        super().__init__(self.rotations, fileName = fileName)

#Scaling
class FamousFacesScaling(FamiliarFaces, ScalingProtocol):
    def __init__(self, fileName = ''):
        self.initSizes(self.sizes)
        super().__init__(self.sizes, fileName = fileName)


##### Complex Character Protocols #####
##### Complex Character Protocols #####
##### Complex Character Protocols #####


class ComplexCharacters (TVStimuli):
    numSets = 2
    trialsPerSet = 25

    def getImage(self, set, showTarget, folder):
        targets = [[1,2,3], [4,5,6], demo]
        fileName = 'char ' + targets[set][showTarget] + '.png'
        return os.path.join(os.getcwd(), '2 - Language (Complex Characters)', 'Stimuli', folder, fileName)

#Rotation
class EnglishCharsRoll(ComplexCharacters, RotationProtocol):
    def __init__(self, fileName = ''):
        self.initRotations(self.rotations)
        super().__init__(self.rotations, 'English', 'letter', fileName = fileName)
        if not TVStimuli.debug:
            self.trainingTime = 5
            self.trainingReps = 1
    
    def getImage(self, set, showTarget):
        super().getImage(set, showTarget, 'New English Characters')

class ChineseCharsRoll(ComplexCharacters, RotationProtocol):
    def __init__(self, fileName):
        self.initRotations(self.rotations)
        super().__init__(self.rotations, 'Chinese', 'character', fileName = fileName)
    
    def getImage(self, set, showTarget):
        super().getImage(set, showTarget, 'Chinese Characters')

class NonsenseCharsRoll(ComplexCharacters, RotationProtocol):
    def __init__(self, fileName = ''):
        self.initRotations(self.rotations)
        super().__init__(self.rotations, 'Combined', 'characters', fileName = fileName)
    
    def getImage(self, set, showTarget):
        super().getImage(set, showTarget, 'Nonsense Characters')

#Scaling
class EnglishCharsScaling(ComplexCharacters, ScalingProtocol):
    def __init__(self, fileName = ''):
        self.initSizes(self.sizes)
        super().__init__(self.sizes, 'English', 'letter', fileName = fileName)
        if not TVStimuli.debug:
            self.trainingTime = 5
            self.trainingReps = 1
    
    def getImage(self, set, showTarget):
        super().getImage(set, showTarget, 'New English Characters')

class ChineseCharsScaling(ComplexCharacters, ScalingProtocol):
    def __init__(self, fileName):
        self.initSizes(self.sizes)
        super().__init__(self.sizes, 'Chinese', 'character', fileName = fileName)
    
    def getImage(self, set, showTarget):
        super().getImage(set, showTarget, 'Chinese Characters')

class NonsenseCharsScaling(ComplexCharacters, ScalingProtocol):
    def __init__(self, fileName = ''):
        self.initSizes(self.sizes)
        super().__init__(self.sizes, 'Combined', 'characters', fileName = fileName)
    
    def getImage(self, set, showTarget):
        super().getImage(set, showTarget, 'Nonsense Characters')


##### Word Protocols #####
##### Word Protocols #####
##### Word Protocols #####


class WordsProtocol (TVStimuli):
    numSets = 2
    trialsPerSet = 25
    referenceSize = 2
    
    language = folder = ''
    def __init__(self, testValues, language, fileName = ''):
        super().__init__(testValues, language, 'word', fileName = fileName)
    
    def getImage(self, set, showTarget, folder):
        targets = [[1,2,3], [4,5,6], demo]
        fileName = 'word ' + targets[set][showTarget] + '.png'
        return os.path.join(os.getcwd(), '2 - Language (Words)', 'Stimuli', folder, fileName)

    def resizeImage(self, size):
        self.displayImage.size = None
        faceHeight = self.angleCalc(size) * float(self.tvInfo['faceHeight'])
        factor = faceHeight / self.displayImage.size[1]
        self.displayImage.size = (self.displayImage.size[0] * factor, self.displayImage.size[1] * factor)
    
    def getImage(self, set, showTarget):
        targets = [[1,2,3], [4,5,6], ['demo']]
        fileName = 'word ' + str(targets[set][showTarget]) + '.png'
        return os.path.join(os.getcwd(), '2 - Language (Words)', 'Stimuli', self.folder, fileName)
    
class WordsRotation(WordsProtocol, RotationProtocol):
    def __init__(self, fileName = ''):
        self.initRotations(self.rotations)
        super().__init__(self.rotations, self.language, fileName = fileName)

    def showImage(self, set, showTarget, rotation):
        self.displayImage.image = self.getImage(set, showTarget)
        self.resizeImage(self.referenceSize)
        self.displayImage.ori = rotation
        self.displayImage.draw()

class WordsScaling(WordsProtocol, ScalingProtocol):
    sizes = [size/4 for size in ScalingProtocol.sizes]
    
    def __init__(self, fileName = ''):
        self.initSizes(self.sizes)
        super().__init__(self.sizes, self.language, fileName = fileName)

    def showImage(self, set, showTarget, size):
        self.displayImage.image = self.getImage(set, showTarget)
        self.resizeImage(size)
        self.displayImage.draw()

#Rotation
class EnglishWordsRoll(WordsRotation):
    language = 'English'
    folder = 'English Words'

class LongEnglishWordsRoll(WordsRotation):
    language = 'English'
    folder = 'Long English Words'

class NonsenseWordsRoll(WordsRotation):
    language = 'Scrambled English'
    folder = 'Nonsense Words'

class LongNonsenseWordsRoll(WordsRotation):
    language = 'Scrambled English'
    folder = 'Long Nonsense Words'

#Scaling
class EnglishWordsScaling(WordsScaling):
    language = 'English'
    folder = 'English Words'

class LongEnglishWordsScaling(WordsScaling):
    language = 'English'
    folder = 'Long English Words'

class NonsenseWordsScaling(WordsScaling):
    language = 'Scrambled English'
    folder = 'Nonsense Words'

class LongNonsenseWordsScaling(WordsScaling):
    language = 'Scrambled English'
    folder = 'Long Nonsense Words'


##### Scrotation Combination Protocols #####
##### Scrotation Combination Protocols #####
##### Scrotation Combination Protocols #####


class ScrotationBination (TVStimuli):
    numSets = 3
    trialsPerSet = 75
    practiceFreq = 40
    initialPracticeTrials = 12
    interimPracticeTrials = 6
    
    sizes = [4, 8, 16]
    rotations = [0, 30, 60, 90, 120, 150, 180, -180, -150, -120, -90, -60, -30, 0]
    refValue = (TVStimuli.referenceSize, 0)
    
    def __init__(self, fileName = ''):
        values = []
        for size in self.sizes:
            for rot in self.rotations:
                values += [(size, rot)]
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
        self.csvOutput(["Correct Response","Size/Rotation (deg/deg)", "Reaction Time (ms)", "Target"])
    
    def demoSequence(self, testVars, demoMessage, buttonMessage, showTime):
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.refValue)
        self.genDisplay('(Press space to ' + buttonMessage + ')', 0, -8)
        self.showWait()
        for testVar in testVars:
            self.genDisplay(demoMessage, 0, 8)
            self.showImage(self.numSets, 0, testVar)
            self.showWait(showTime)
        self.genDisplay(demoMessage, 0, 8)
        self.showImage(3, 0, self.refValue)
        self.genDisplay('(Press space to continue)', 0, -8)
        self.showWait()
        
    def demo(self):
        print(self.testValues)
        self.demoSequence([(size, 0) for size in self.sizes], 'The faces will be resized as shown below.', 'resize', 0.2)
        self.demoSequence([(self.referenceSize, rot) for rot in self.rotations], 'The faces will also be rotated as shown below.', 'rotate', 0.1)
    
class RandomRotationAndScaling (ScrotationBination):
    def showImage(self, set, showTarget, testVar):
        targets = [[1,2,3], [4,5,6], [7,8,9], ['demo']];
        fileName = 'face ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), '2 - Scaling plus Rotation', 'Stimuli', fileName)
        faceWidth = self.angleCalc(testVar[0]) * float(self.tvInfo['faceWidth'])
        faceHeight = self.angleCalc(testVar[0]) * float(self.tvInfo['faceHeight'])
        self.displayImage.size = (faceWidth, faceHeight)
        self.displayImage.ori = testVar[1]
        self.displayImage.draw()

class SimulatedScaling (ScalingProtocol):
    numSets = 3
    trialsPerSet = 28
    initialPracticeTrials = 6
    
    recordFactor = 1
    distance = 1.4
    def __init__(self, fileName = ''):
        self.initSizes(self.sizes)
        super().__init__(self.sizes, 'Scrambled English', fileName = fileName)

    def getImage(self, set, showTarget):
        targets = [[1,2,3], [4,5,6], ['demo']];
        fileName = 'face ' + str(targets[set][showTarget]) + '.png'
        self.displayImage.image = os.path.join(os.getcwd(), '2 - Scaling simulated vs Actual', 'Stimuli', fileName)

    def demo(self):
        super().demo()
        self.genDisplay('Before we begin, please make sure that you are seated ' + self.distance + ' m from the screen.', 0, 3)
        self.genDisplay('Press spacebar to start.', 0, 0)
        self.showWait()
    
    def csvOutput(self, output):
        if output[0] != 'Correct Response':
            output[1] = output[1] * self.recordFactor
        super().csvOutput(output)
        
class FourDegrees70cm (SimulatedScaling):
    referenceSize = 2
    recordFactor = 2
    sizes = [size/2 for size in SimulatedScaling.sizes]
    
class FourDegrees140cm (SimulatedScaling):
    referenceSize = 4
    recordFactor = 1
    
class EightDegrees140cm (SimulatedScaling):
    referenceSize = 8
    recordFactor = 1
    
class EightDegrees280cm (SimulatedScaling):
    referenceSize = 16
    recordFactor = 0.5