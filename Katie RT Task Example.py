from psychopy import visual, core, data, gui, event
from random import choice

# GUI at the start
info = {}
info['Participant'] = ''
info['Condition'] = '' # 1 = grey, 2 = black 
info['Date'] = data.getDateStr()

dlg = gui.DlgFromDict(info)
if not dlg.OK:
	print "Pressed Cancel"
	core.quit()


# Condition Checker
if info['Condition'] == '1':
	col = '#757575'
elif info['Condition'] == '2':
	col = '#000000'
else:
	core.quit()
	print ' invalid condition selection'


# Stimuli Creation #

#Window
win =  visual.Window(rgb = col, screen = 1, fullscr = False)

#RT Clock
rtClock = core.Clock()

# Square
sqr = visual.Rect(win, width = 0.2, height = 0.2, fillColor = 'red', lineColor = 'red')

# Triangle
tri = visual.ShapeStim(win, vertices = [[-50,-50], [50,-50], [0, 50]], fillColor = 'red', lineColor = 'red')

#instructions

instrText = ('Welcome to our experiment, you will see either a square or a traingle' +  
			 'press the spacebar only when you see a sqaure, press any key to continue')

def displayInstructions(text, acceptedKeys= None):
	instruct = visual.TextStim(win, text = text, color = 'red')
	instruct.draw()
	win.flip()

	key = event.waitKeys(keyList = acceptedKeys)

	win.flip()


# Fixation

fix = visual.Circle(win, size = 0.5, fillColor = 'red', lineColor = 'red')

# onset times 

times = [120, 60, 30, 12, 18]

# Experiment handler 
filename = "data/" + info['Participant'] #This is the file name in the data/ directory

RT_Exp = data.ExperimentHandler(
        name='Simple Reaction Time Task', version='1.0', #not needed, just handy
        extraInfo = info, #the info we created earlier
        dataFileName = filename, # using our string with data/name_date
        )


