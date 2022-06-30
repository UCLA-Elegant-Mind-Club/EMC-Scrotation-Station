### This is a documentation file for TVStimuli.py
### Please run and import methods from TVStimuli
from abc import ABC, abstractmethod
import os, threading

class TVStimuli_Doc:
    """Superclass for all TV stimulus experiments with game features
    """

    def __init__(self, testValues: list, stimDescription: str, stimType: str, fileName: str = ''):
        """Initializes a TV stimulus experiment

        Parameters
        ----------
        testValues : list[any]
            List of testing values to affect image i.e. rotation and scaling values
        stimDescription : str
            Defining attribute of stimulus
            Leave as empty string to omit
        stimType : str
            Type of stimulus i.e. faces, words, sentences, etc.
        fileName : str, optional
            Name of existing csv file to save data (default is empty string)
            Leave as empty string to not save data
        """
        return

    def initTestValues(self, testValues: list):
        """Private method to initialize testing array

        Parameters
        ----------
        testValues : list[any]
            Values of testing values to affect image i.e. rotation and scaling values
        """
        return

    @abstractmethod
    def showImage(self, set: int, showTarget: int, testValue: any):
        """Abstract method used by learningTrial and stimTest to show image onto the screen
        
        Parameters
        ----------
        set : int
            Current set number used to choose image
        showTarget : int
            Current target number within set between 1- 3
        testValue : any
            Test value used to manipulate image size or rotation
        """
        pass
    
    @abstractmethod
    def initFile(self):
        """ Abstract method used to initialize csv to save data
        """
        pass

    
    def csvOutput(self, output: list):
        """Outputs a single line of data to csv file. Used by experimentalRound
        
        Parameters
        ----------
        output : list[any]
            List containing single row of output data used by csv file
        """
        return
    
    @staticmethod
    def calibrate(calibrationFile: str = 'monitors.csv', mon: str = 'TV',
                    crossFile: str = os.path.join(os.getcwd(), 'Calibration', 'cross.png')) -> None or str:
        """Static Method, calibrates monitor and initializes window to begin experiment
        
        Parameters
        ----------
        calibrationFile : str
            Name of file to retrieve calibration data
        mon : str
            Name of saved monitor from Monitor Settings
        crossFile: str
            Path to cross image file
        
        Returns
        -------
        None or str
            Returns label of monitor from calibration file
        """
        return
    
    @staticmethod
    def angleCalc(angle: float):
        """Static Method, calculates the stimulus height based on viewing angle
        
        Parameters
        ----------
        angle : float
            Viewing angle in degrees
        
        Returns
        -------
        float
            Height of image to show in cm
        """
        return
    
    @staticmethod
    def genDisplay(text: str, xPos: float, yPos: float, height: float = 1.5, color: str = 'white'):
        """Static Method, displays a line of text
        
        Parameters
        ----------
        text : str
            String to display
        xPos : float
            Horizontal distance between center of text and center of screen
        yPos : float
            Vertical distance between center of text and center of screen
        height : float, optional
            Height of letters in cm (Default is 1.5)
        color : str, optional
            Color of text (Default is white)
        """
        return
    
    @abstractmethod
    def instructions(self):
        """Displays instructions for each subclass
        """
        pass
    
    @abstractmethod
    def demoSequence(self, testValues: list, demoMessage: str):
        """Private method to display sequence of images for demo
        
        Parameters
        ----------
        testValues : list
            List of testing values to show during demo
        demoMessage : str
            Line of text to show above demo image
        """
        pass
    
    @abstractmethod
    def demo(self):
        """Shows demonstration of experiment (uses private function demoSequence)
        """
        pass
    
    def showHighScores(self):
        """Uses self.winners list to shows high scores (first 5) and recent scores (last 5)
        """
        return
    
    @staticmethod
    def showWait(seconds: float = -1, keys: list = ['space'], flip: bool = True, timeOnly: bool = True):
        """Refreshes screen if flip is True and waits for key input or time. Quits if escape is pressed
        If no parameters are given, flips and waits for space to be pressed
        
        Parameters
        ----------
        seconds : float, optional
            Time to wait in seconds. If negative, will wait infinitely until keys are pressed
            (Default is infinite)
        keys : list, optional
            Key inputs to wait for (Default is space)
        flip : bool, optional
            Determines whether screen should refresh before waiting (Default is True)
        timeOnly : bool, optional
            If a time is specified, determines if keys should be ignored. If False, will wait
            until either key has been pressed or time has passed. (Default is True)
        """
        return

    def breakScreen(self, trialsLeft: int = 0):
        """Shows break screen for self.postSetBreak seconds.
        Displays current score and trials left in experiment.
        """
        return
    
    def levelScreen(self, text1: str, text2: str):
        """Displays level transition animation
        
        Parameters
        ----------
        text1 : str
            First line of text, usually 'Level'
        text2 : str
            Second line of text, usually '1', '2', or '3'.
            If one of these is given, the corresponding level sound will play.
        """
        return
    
    def learningTrial(self, set: int, target: int, mapping: str, repeatText: bool = False):
        """Private method that shows one target on screen during the learning/training period.
        Used by learningPeriod, which shows all three targets in a set.
        
        Parameters
        ----------
        set : int
            The set number of the target to show
        target : int
            The number of the target to show (between 1 and 3)
        mapping : str
            They key letter that corresponds to the target image
        repeatText : bool, optional
            Determines whether to show repeat text: 'Training has restarted from the first stimulus'
            Should be True when trainingReps > 1 and restarting from target 1 (Default is False)
        """
        return
    
    def learningPeriod(self, set: int):
        """Shows all three targets in a set on screen in order during the learning/training period.
        
        Parameters
        ----------
        set : int
            The current set of three target images to show.
        """
        return

    @staticmethod
    def showCross(prePause: float = 0.5, postPause: float = 0.2):
        """Static method that clears screen and shows interstimulus cross to refresh participant mind.
        
        Parameters
        ----------
        prePause : float
            Time to wait after clearing the screen before showing cross
        postPause : float
            Time to wait after showing cross before clearing screen
        """
        return
    
    def stimTest(self, set: int, target: int, testValue: any, correctKey: str, practice: bool = False) -> list:
        """Executes a single experimental trial by showing cross, image, and waiting for key press.
        After flashing the cross on screen, waits between 0.5 and 1.5 seconds before showing target.
        Detects user input (times out after self.timeOut seconds) and executes feedback method.
        If correct, rewards 400 + (self.timeOut - response time)/2 points, capping at 1000 for times below 400 ms (minimum reward is 400).
        If incorrect, deducts (response time)/2 points, with a cap at -400 points (minimum deduction is 0).
        If timed out, automatically deducts 400 points.
        
        Parameters
        ----------
        set : int
            Set number of target to show
        target : int
            Target number to show: 1, 2, or 3
        testValue : any
            Testing value to modify target through showImage method
        correctKey : str
            Correct key input corresponding to target
        practice : bool, optional
            Determines if score should be changed in feedback method
            (Default is False)
        
        Returns
        -------
        list
            A list with a single row of data to record in csv file
        """
        return
    
    def feedback(self, correct: bool or int, scoreChange: float = 0):
        """Private method used by stimTest to show feedback. Results can be correct, incorrect, or overtimed.
        If practice trial, scoreChange should be set to 0. Uses playNotes for sound effects.
        
        Parameters
        ----------
        correct : bool or int
            If 1 or True, shows feedback for correct trial.
            If 0 or False, shows feedback for incorrect trial.
            If -1, shows feedback for overtimed trial.
        scoreChange : float
            Points to add (deducts if negative) to self.score
            If 0, the feedback message will change to '(Still warming up)'
        """
        return
    
    @staticmethod
    def playNotes(notes: list, beats: list, beatLength: float = 0.15, loop: int = 0, freeze: bool = False) -> threading.Thread:
        """Static method that uses noteThread to play a series of notes in a background thread
        
        Parameters
        ----------
        notes : list[float]
            List of note frequencies in hertz. If '' is included, will rest for the length of the note.
        beats : list[float]
            List of note lengths or beats
        beatLength : float
            Length of a single beat in seconds
        loop : int, optional
            Number of extra times to loop note sequence. If negative, will run infinitely (Default is 0)
        freeze : bool, optional
            Determines whether screen should freeze for duration of sound or continue separately.
            If infinite loop, will automatically be set to False (Default is False)
        
        Returns
        -------
        Thread
            The note thread to play
        """
        return
    
    @staticmethod
    def noteThread(notes: list, beats: list, beatLength: float, loop: int):
        """Private method used by playNotes to play a sequence of notes for their corresponding beats
        
        Parameters
        ----------
        notes : list[float]
            List of note frequencies in hertz. If '' is included, will rest for the length of the note.
        beats : list[float]
            List of note lengths or beats
        beatLength : float
            Length of a single beat in seconds
        loop : int
            Number of extra times to loop note sequence. If negative, will run infinitely.
        """
        return
    
    def practiceRound(self, set: int, practiceTrials: int = {'initialPracticeTrials'}, trialsLeft: int = 0):
        """Executes a practice round for a set of targets, dividing trials evenly.
        Begins experimental round with unrecorded trials given by self.dummyTrials.
        
        Parameters
        ----------
        set : int
            The set of targets to test
        practiceTrials : int, optional
            The number of trials to run (Default is initialPracticeTrials)
        trialsLeft : int, optional
            The number of trials left to display. If 0, will not display trials left (Default is 0)
        """
        return

    def experimentalRound(self, set: int):
        """Executes experiment for a set of targets. Should be used after practiceRound.
        
        Parameters
        ----------
        set : int
            The set of targets to test
        """
        return
    
    def main(self):
        """Main program to run entire experiment.
        """
        return