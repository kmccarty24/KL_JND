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

def RandomOffsets(iterations = 50):
    '''This Function acts as generator for a list of dictionaires to be fed into a trial handler'''

    probeTargetDiffs = [random.randint(1,20) for x in range(iterations)]

    trialList = []
    for angleOffset in probeTargetDiffs:
        trialList.append({'Offset': angleOffset, 'Direction': (random.choice(['Clock', 'AntiClock']))})

    return trialList


# Datafile (just in case not one written by PsychoPy)
fileName = info['Participant No'] + info['Date']
dataFile = open(fileName + '.txt', 'w')
dataFile.write('TrialNo\ttrialType\tTargetOri\tProbeStart\tInitialOffset\tEndOffset\tDecisionTime\tMoves\n')

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
trials = data.TrialHandler(trialList = RandomOffsets(), nReps = 25, method='random') 

jnd_exp.addLoop(trials)

# Trial sequence

displayInstructions(text = instrText)

trialNo = 0

for thisTrial in trials:

    trials.addData('Direction', thisTrial['Direction'])
    
    event.clearEvents()
    rt = None
    resp = None
    iteration = 0
    trialNo += 1

    # Choose a random orientation for the target
    targetOri = random.randint(20,340) # 20 / 340 to alow a maximum of 20 degrees difference either way

    if targetOri in [0, 90, 180, 270]: # to eliminate vertical or horizontal, no 0 as its not a valid int
        targetOri+= 10
    trials.addData('targetOri', targetOri)

    # Assign the Target and Probe Orientations
    target.ori = targetOri


    #Probe Fixing
    if thisTrial['Direction'] == 'Clock': 
        probe.ori = (targetOri + thisTrial['Offset']) # rotate clockwise
        probeOri = (targetOri + thisTrial['Offset'])
        trials.addData('trialType', thisTrial['Direction'])
    elif thisTrial['Direction'] == 'AntiClock':
        probe.ori = (targetOri - thisTrial['Offset']) # rotate anticlockwise
        probeOri = (targetOri - thisTrial['Offset'])
        trials.addData('trialType', thisTrial['Direction'])

     
     #Display Fixation / Target / Fixation for 500ms (30 frames @ 60Hz)

    for frameN in range(30): #changed as disptime misbehaving
        fix.draw()
        win.flip()

    for frameN in range(30):
        target.draw()
        win.flip()

    for frameN in range(30):
        fix.draw()
        win.flip()
    

    win.callOnFlip(rtClock.reset)

    # Now draw the Probe and allow participants to tinker

    while True:

        event.clearEvents(eventType ='keyboard')

        probe.draw()
        win.flip()

        keys = event.waitKeys(keyList = ['q', 'left', 'right', 'space'])

        if keys[0] == 'q':
            print 'Quitting'
            trials.finished = True
            core.quit()
            quit()
        elif keys[0] == 'right':
            iteration +=1
            probe.ori+=1
        elif keys[0] == 'left':
            iteration +=1
            probe.ori-=1
        elif keys[0] == 'space':
            rt = rtClock.getTime()
            trials.addData('Moves', iteration)
            trials.addData('Target Ori', targetOri)
            trials.addData('Probe Start', probeOri)
            trials.addData('Initial Offset', (targetOri - probeOri))
            trials.addData('End Offset', (targetOri - probe.ori))
            trials.addData('Decision Time',rt)
            dataFile.write("%i \t %s \t %i \t %i \t %i \t %i \t %2f \t %i \n" %(trialNo, 
                                                                                thisTrial['Direction'], 
                                                                                targetOri, ProbeOri, 
                                                                                (targetOri - ProbeOri),
                                                                                (targetOri - probe.ori),
                                                                                rt, iteration))
            break

    jnd_exp.nextEntry()

dataFile.close()
win.close()
core.quit()
quit() 
