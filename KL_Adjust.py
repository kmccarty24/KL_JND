from psychopy import visual, event, core, data, gui
import random, time

# gui at the start
info = {}
info['Participant No'] = ''
info['Date'] = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time

dlg = gui.DlgFromDict(info, fixed = ['Date'])
if not dlg.OK:
    print "Pressed Cancel"
    core.quit()
    
info['baseOri'] = 45 # A good start point

## -- ## Object Creation ## -- ##

# Generate some random orientation differences

probeTargetDiffs = [random.randint(1,20) for x in range(50)]


# Datafile (just in case not one written by PsychoPy)
fileName = info['Participant No'] + info['Date']
dataFile = open(fileName + '.txt', 'w')
dataFile.write('trialType\trt\tresp\ttargetOri\tprobeOri\toriIncrement\t correct\n')

# window
win = visual.Window(monitor= 'default', size = (1024, 768), fullscr = False, color = 'grey', screen = 1) # make fullscreen once it actually works!

# rt clock
rtClock = core.Clock()

# gratings
target = visual.GratingStim(win, tex='sin', 
                            mask='gauss', 
                            size = 3.0, 
                            sf=3.0, 
                            ori=info['baseOri'], 
                            contrast=1.0,
                            units = 'deg')

probe = visual.GratingStim(win, tex='sin', 
                           mask='gauss', 
                           size = 3.0, 
                           sf=3.0,
                           ori=info['baseOri'],
                           contrast=1.0,
                           units = 'deg')

# fixation
fix = visual.TextStim(win, color='black', text = '+')

# instructions
instrText = ('In this experiment you will see two gratings presented one after the other.' +
            'When the second grating appears, please use the left and right keys to match it ' +
            'to the orientation of the first. Press any key to continue.')

def displayInstructions(text, acceptedKeys = None):
    instruct = visual.TextStim(win, text=instrText, color='black')
    instruct.draw()
    win.flip()
    
    key = event.waitKeys(keyList = acceptedKeys)
    
    win.flip()

# Experiment Handler
filename = "data/" + info['Participant No']

jnd_exp = data.ExperimentHandler(
        name='Adjusting JND', version='1.0',
        extraInfo = info,
        dataFileName = filename
        )

# Trial handler
trials = data.TrialHandler(trialList = data.importConditions('trials.xlsx'), nReps = 25, method='random') 

# Trial sequence

displayInstructions(text = instrText)

for thisTrial in trials:
    
    event.clearEvents()
    rt = None
    resp = None
    
    iteration = 0
    
    # Choose Clockwise or anti Clockwise
    trialType = random.choice([1,-1]) # 1 = Clockwise, -1 = Anticlockwise
    if trialType == 1:
        trials.addData('TrialType', 'ClockWise')
    elif trialType == -1:
        trials.addData('TrialType', 'AntiClockWise')

    # EXPERIMENTAL RANDOM PICKER
    # Choose a random orientation for the target
    targetOri = random.randint(20,340) # 20 / 340 to alow a maximum of 20 degrees difference either way

    if targetOri in [90, 180, 270]: # to eliminate vertical or horizontal, no 0 as its not a valid int
        targetOri+= 10
    trials.addData('targetOri', targetOri)

    # Assign the Target and Probe Orientations
    target.ori = targetOri

    if trialType == 1: 
        probe.ori = targetOri + thisTrial['trialType'] # rotate clockwise
        probeOri = targetOri + thisTrial['trialType']
    elif trialType == -1:
        probe.ori = targetOri - thisTrial['trialType'] # rotate anticlockwise
        probeOri = targetOri - thisTrial['trialType']

    while True:

        event.clearEvents(eventType ='keyboard')

        for frameN in range(30): #changed as disptime misbehaving
            fix.draw()
            win.flip()

        for frameN in range(30):
            target.draw()
            win.flip()
            
        for frameN in range(30):
            fix.draw()
            win.flip()
            
            event.clearEvents()
            win.callOnFlip(rtClock.reset)
            
        for frameN in range(300):
            probe.draw()
            win.flip()

            keys = event.waitKeys(keyList = ['q', 'left', 'right'])

            if keys[0] == 'q':
                print 'Quitting'
                core.quit()
                quit()
            elif keys[0] == 'right':
                iteration +=1
                probe.ori+=1
            elif keys[0] == 'left':
                iteration +=1
                probe.ori-=1
                
            resp = target.ori - probe.ori

    trials.addData('Reaction Time', rt)
    trials.addData('Response', resp)
    RT_Exp.nextEntry()
    
trials.saveAsExcel(fileName = filename)
win.close()
core.quit()
quit() 