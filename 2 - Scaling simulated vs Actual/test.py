from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time
from TVStimuli import TVStimuli as TV

TV.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration_Knudson.csv'))

class Test(TV):
    def __init__(self):
        super().__init__([0.5], 'test', 'test', fileName = '')
        
    def showImage(self):
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'Celeb Faces 2', 'demo', 'main.png')
        faceWidth = self.angleCalc(0.5) * float(self.tvInfo['faceWidth'])
        faceHeight = self.angleCalc(0.5) * float(self.tvInfo['faceHeight'])
        self.displayImage.size = (faceWidth, faceHeight)
        self.displayImage.draw()
    
    def initFile(self):
        return
        
    def demo(self):
        return

test = Test()
test.showImage()