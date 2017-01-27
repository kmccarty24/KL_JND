from psychopy import visual, core, data, gui, event
import random 

# gui at the start
info = {}
info['Participant No'] = ''
info['Date'] = data.getDateStr()

dlg = gui.DlgFromDict(info)
if not dlg.OK:
    print "Pressed Cancel"
    core.quit()

# stimuli creation
# window
win = visual.Window(monitor= 'default', size = (1084, 768), fullscr = False, color = 'grey') # make fullscreen once it actually works!

# rt clock
rtClock = core.Clock()

# gratings
target = visual.GratingStim(win, tex='sin', mask='gauss', units= 'deg', size = 3.0, sf=3.0, ori=45.0, contrast=1.0)
probe = visual.GratingStim(win, tex='sin', mask='gauss', units = 'deg', size = 3.0, sf=3.0, ori=45.0, contrast=1.0)

# fixation
# fix = visual.ShapeStim(win, lineColor='black', vertices=((-10, 10), (-10, 10)), closeShape=False)

fix = visual.TextStim(win, color='black', text = '+')



# instructions
instrText = ('In this experiment you will see two gratings presented one after the other. ' +
            'When the second grating appears, please press the right arrow key if it is rotated ' +
            'clockwise in relation to the first grating, or the left arrow key if it is rotated ' +
            'anticlockwise in relation to the first grating. ' +
            'Press any key to continue.')

def displayInstructions(text, acceptedKeys = None):
    instruct = visual.TextStim(win, text=instrText, color='black')
    instruct.draw()
    win.flip()
    
    key = event.waitKeys(keyList = acceptedKeys)
    
    win.flip()
    
# experiment handler
filename = "data/" + info['Participant No']

jnd_exp = data.ExperimentHandler(
        name='Forced choice JND', version='1.0',
        extraInfo = info,
        dataFileName = filename,
        )

# stairhandler
staircase = data.StairHandler(
        startVal=20.0, 
        nReversals=10, 
        stepSizes=[1], 
        nUp=1, nDown=3, 
        stepType='log',
        nTrials=20,
        minVal=0.01, maxVal=25.0)

displayInstructions(text = instrText)

# step through staircase
for thisIncrement in staircase:
    
    print thisIncrement
    
    event.clearEvents()
    resp = None
    rt = None

    for frameN in range (30):
        fix.draw()
        win.flip()

    for frameN in range(30):
        target.draw()
        win.flip()

    for frameN in range(30):
        fix.draw()
        win.flip()
    
    win.callOnFlip(rtClock.reset)
    event.clearEvents()
    
    probe.ori += thisIncrement 

    for frameN in range(120):
        probe.draw()
        win.flip()
        keys = event.getKeys(keyList = ['left', 'right'])
        if len(keys)>0:
            resp = keys[0]
            rt = rtClock.getTime()
            break

        # get response
        if resp is None:
            keys = event.waitKeys(keyList = ['left', 'right'])
            resp = keys[0]
            rt = rtClock.getTime()
            correct = 0
        elif resp is 'left' and thisIncrement < 45:
            correct = 1
            rt = rtClock.getTime()
        elif resp is 'right' and thisIncrement > 45:
            correct = 1
            rt = rtClock.getTime()
            resp = None
        elif resp is 'left' and thisIncrement > 45:
            correct = 0
            rt = 'N/A'
        elif resp is 'right' and thisIncrement < 45:
            correct = 0
            rt = 'N/A'
    staircase.addData('Reaction Time', rt)
    staircase.addData('Response', resp)
    staircase.addData('Correct', correct)
    jnd_exp.nextEntry()

staircase.saveAsExcel(fileName = filename)
win.close()
core.quit()

