import sys
sys.path.append('../')
from TVStimuli import *

with open(os.path.join(os.getcwd(), 'GroupProtocols.csv')) as file:
    protocolFile = list(csv.reader(file, delimiter=','))

# Select group project
groupDialog = gui.Dlg(title='Select Group Project', screen=-1)
groups = [row[0] for row in protocolFile]
groupDialog.addField('Group: ', choices = groups[1:])
groupInfo = groupDialog.show()
if groupInfo is None:
    core.quit()

# Get protocols list
groupNum = groups.index(groupInfo[0])
protocols = protocolFile[groupNum][1].split('. ')

label = TVStimuli.calibrate(os.path.join(os.getcwd(), 'monitors.csv'), crossFile = 'cross.png')
if label == None:
    calibDlg = gui.Dlg(title = "Could not find calibration")
    calibDlg.addText('Could not find system calibration. Please calibrate before continuing.')
    calibDlg.show()
    core.quit();


class ScoreBoard (TVStimuli):
    def __init__(self): return
    def initFile(self): return
    def showImage(self): return
    def demo(self): return

protocol = ScoreBoard()

for protocolName in protocols:
    scoreFolder = os.path.join(os.getcwd(), 'HighScores', groupInfo[0], protocolName)
    dirList = os.listdir(scoreFolder);
    winners = [[0,'cm600286']] * 5
    for name in dirList:
        with open(os.path.join(scoreFolder,name)) as file:
            score = int(file.read())
        winners += [[score, name[10:-4]]]
    recentWinners = winners[-5:]
    recentWinners.reverse()
    winners.sort(reverse = True)
    topWinners = winners[:5]

    protocol.highScores = [score[0] for score in topWinners + recentWinners]
    protocol.winners = [score[1] for score in topWinners + recentWinners]
    protocol.levelScreen("Showing scores for", protocolName)
    protocol.showHighScores()
