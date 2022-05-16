from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time, math
from TVStimuli import TVStimuli as TV

TV.calibrate(os.path.join(os.getcwd(), 'eccentricity_monitor_calibration_Knudson.csv'))

class Test(TV):
    def __init__(self):
        super().__init__([0.5], 'test', 'test', fileName = '')
        
    def showImage(self):
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'face 1.png')
        self.displayImage.size = None
        faceHeight = self.angleCalc(8) * float(self.tvInfo['faceHeight'])
        factor = faceHeight / self.displayImage.size[1]
        self.displayImage.size = (self.displayImage.size[0] * factor, self.displayImage.size[1] * factor)
        posX = math.tan(math.radians(20)) * float(self.tvInfo['leftEdge'])
        self.displayImage.pos = (posX, 0)
        self.displayImage.draw()
        
    def showImage2(self):
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'face 1 yaw 15.png')
        self.displayImage.size = None
        faceHeight = self.angleCalc(8) * float(self.tvInfo['faceHeight'])
        factor = faceHeight / self.displayImage.size[1]
        self.displayImage.size = (self.displayImage.size[0] * factor, self.displayImage.size[1] * factor)
        posX = math.tan(math.radians(20)) * float(self.tvInfo['rightEdge'])
        self.displayImage.pos = (-posX, 0)
        self.displayImage.draw()
    
    
    def initFile(self):
        return
        
    def demo(self):
        return
        
    def main(self):
        self.showImage()
        self.showImage2()
        self.cross.draw()
        self.showWait()

test = Test()
test.main()