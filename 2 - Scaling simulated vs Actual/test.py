from psychopy import gui, core, prefs
from psychopy.sound import Sound
prefs.hardware['audioLib'] = ['ptb', 'pyo']
import os, time
from TVStimuli import TVStimuli as TV

TV.calibrate(os.path.join(os.getcwd(), 'Calibration', 'eccentricity_monitor_calibration_Knudson.csv'))

class Test(TV):
    def __init__(self):
        super().__init__([0.5], 'test', 'test', fileName = '')
        
    def showImage(self, size):
        self.displayImage.image = os.path.join(os.getcwd(), 'Stimuli', 'face demo.png')
        faceWidth = self.angleCalc(size) * float(self.tvInfo['faceWidth'])
        faceHeight = self.angleCalc(size) * float(self.tvInfo['faceHeight'])
        self.displayImage.size = (faceWidth, faceHeight)
        self.displayImage.draw()
    
    def initFile(self):
        return
        
    def demo(self):
        return
        
    def main(self):
        scales = [0.5, 0.75, 1, 1.2, 1.4, 1.7, 2, 2.5 , 3, 3.5, 4];
        while True:
            for i in range(0, len(scales)):
                self.showImage(scales[i])
                self.showWait()
                print(str(i))
            for i in range(0, len(scales) - 2):
                self.showImage(scales[len(scales) - 2 - i])
                self.showWait(0.05)
                print(str(i))
test = Test()
test.main()