'''
The procedure I'm working towards at the moment would be a fixation cross for 500ms, 
the first stimulus for 500ms, a fixation again for 500ms, and then the second stimulus 
at a different orientation to the first for another 500ms. Both first and second stimulus
need to be at oblique orientations rather than vertical or horizontal, and they have to
differ from eachother by a maximum of 20 degrees. The multistairhandler came in because
last time we were working on it you thought we might need one staircase for clockwise
rotation and another for anticlockwise.
'''


from psychopy import visual, core, data, gui, event
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

# Datafile (just in case not one written by PsychoPy)
fileName = info['Participant No'] + info['Date']
dataFile = open(fileName + '.txt', 'w')
dataFile.write('trialType\trt\tresp\ttargetOri\tprobeOri\toriIncrement\t correct\n')


# window
win = visual.Window(monitor= 'default', size = (1024, 768), fullscr = False, screen = 2, color = 'grey') # make fullscreen once it actually works!

# rt clock
rtClock = core.Clock()

# gratings
target = visual.GratingStim(win, tex='sin', 
                            mask='gauss', 
                            size = 10.0, 
                            sf=3.0, 
                            ori=info['baseOri'], 
                            contrast=1.0,
                            units = 'deg')

probe = visual.GratingStim(win, tex='sin', 
                           mask='gauss', 
                           size = 10.0, 
                           sf=3.0,
                           ori=info['baseOri'],
                           contrast=1.0,
                           units = 'deg')

# fixation
fix = visual.TextStim(win, color='black', text = '+')

# instructions
instrText = ('''In this experiment you will see two gratings presented one after the other.
            When the second grating appears, please press the right arrow key if it is rotated
            clockwise in relation to the first grating, or the left arrow key if it is rotated
            anticlockwise in relation to the first grating.
            Press any key to continue.''')

def displayInstructions(text, acceptedKeys = None):
    instruct = visual.TextStim(win, text=instrText, color='black')
    instruct.draw()
    win.flip()
    
    key = event.waitKeys(keyList = acceptedKeys)
    
    win.flip()

# Experiment Handler
filename = "data/" + info['Participant No']

jnd_exp = data.ExperimentHandler(
        name='Forced choice JND', version='1.0',
        extraInfo = info,
        dataFileName = filename,
        )

# Staircase Handler
stairs = data.StairHandler(startVal = 10,
                           nTrials = 25,
                           nReversals = 10,
                           nUp = 1, nDown = 3,
                           minVal = 1, maxVal = 20,
                           stepType = 'log',
                           stepSizes = 4)


## -- ## Trial Sequence ## -- ##

displayInstructions(text = instrText)

for thisIncrement in stairs:
    
    #Set Trial Up 

    event.clearEvents()
    rt = None
    resp = None

    print thisIncrement

    # Choose Clockwise or anti Clockwise
    trialType = random.choice([1,-1]) # 1 = Clockwise, -1 = Anticlockwise
    if trialType == 1:
        stairs.addOtherData('TrialType', 'ClockWise')
    elif trialType == -1:
        stairs.addOtherData('TrialType', 'AntiClockWise')

    # EXPERIMENTAL RANDOM PICKER
    # Choose a random orientation for the target
    targetOri = random.randint(20,340) # 20 / 340 to alow a maximum of 20 degrees difference either way

    if targetOri in [90, 180, 270]: # to eliminate vertical or horizontal, no 0 as its not a valid int
        targetOri+= 10
    stairs.addOtherData('targetOri', targetOri)

    # Assign the Target and Probe Orientations
    target.ori = targetOri

    if trialType == 1: 
        probe.ori = targetOri + thisIncrement # rotate clockwise
        probeOri = targetOri + thisIncrement
        corrAns = 'right'
        print 'Target ori = ', targetOri
        print 'Probe ori = ', (targetOri + thisIncrement)
    elif trialType == -1:
        probe.ori = targetOri - thisIncrement # rotate anticlockwise
        probeOri = targetOri - thisIncrement

        corrAns = 'left'
        print 'Target ori = ', targetOri
        print 'Probe ori = ', (targetOri + thisIncrement)


    # Start Drawing

    for frameN in range(30): # 500ms @ 60Hz
        fix.draw()
        win.flip()

    for frameN in range(30): #500ms
        target.draw()
        win.flip()

    for frameN in range(30): # 500ms
        fix.draw()
        win.flip()

        event.clearEvents()
        win.callOnFlip(rtClock.reset)

    for frameN in range(30): # 500ms
        probe.draw()
        win.flip()
        keys = event.getKeys(keyList = ['left', 'right','q'])
        if len(keys)>0:
            resp = keys[0]
            rt = rtClock.getTime()
            break
    
    print resp, 'this is the resp'
    # get response if one hasnt been given
    if resp is None:
        print 'entering this loop'
        keys = event.waitKeys(keyList = ['left', 'right', 'q'])
        resp = keys[0]
        rt = rtClock.getTime()

    # is it right?
    if resp == 'right' and trialType == 1:
        correctIncorrect = 1
        rt = rtClock.getTime()
        print 'Opt 1'
    elif resp == 'right' and trialType == -1:
        correctIncorrect = 0
        rt = rtClock.getTime()
        print 'Opt 2'
    elif resp == 'left' and trialType == 1:
        correctIncorrect = 0
        rt = rtClock.getTime()
        print 'Opt 3'
    elif resp == 'left' and trialType == -1:
        correctIncorrect = 1
        rt = rtClock.getTime()
        print 'Opt 4'
    elif resp == 'q':
        stairs.finished = True
        core.quit()
        win.close()
        quit()
        print 'Pressed Q, Quitting....'
        correct = 0
    else:
        print 'This was not forseen, hmmmm'

    dataFile.write('%i \t %.3f \t %s \t %i \t %i \t %i \t %i\n' %(trialType, 
                                                          rt, resp,
                                                          targetOri,
                                                          probeOri,
                                                          thisIncrement,
                                                          correctIncorrect))

    stairs.addOtherData('rt', rt)
    stairs.addOtherData('response', resp)
    stairs.addOtherData('correct', correctIncorrect)

    stairs.addResponse(correctIncorrect) # progress the staircase 1 = correct, 0 = incorrect
    jnd_exp.nextEntry()

dataFile.close()
stairs.saveAsExcel(fileName = filename)
win.close()
core.quit()