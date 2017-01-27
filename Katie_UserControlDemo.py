from psychopy import visual, event, core, data, gui


win = visual.Window(
        size = (1024,768),
        fullscr = False,
        screen = 0,
        color = (-.75,-.75,-.75))

grate = visual.GratingStim(win, 
                            ori=45, # Unit to vary but placeholder here 
                            tex ='sin',
                            mask = 'circle', 
                            size= 300, 
                            sf=0.2, 
                            #pos = (x_cent -x_off, y_cent), 
                            color= 'white',
                            colorSpace = 'rgb',
                            units = 'pix',
                            autoLog=False)



def displayInstructions(text, acceptedKeys= None):

    instruct = visual.TextStim(win, text = text, color = 'red')
    instruct.draw()
    win.flip()
    key = event.waitKeys(keyList = acceptedKeys)
    win.flip()


displayInstructions(text = 'Press the SpaceBar to Continue, press the left and right arrow keys to adjust the orientation 1 degree', acceptedKeys = 'space')


iteration = 0

while True:

    event.clearEvents(eventType ='keyboard')

    grate.draw()
    win.flip()

    keys = event.waitKeys(keyList = ['q', 'left', 'right'])

    if keys[0] == 'q':
        print 'Quitting'
        break
    elif keys[0] == 'right':
        iteration +=1
        grate.ori+=1
    elif keys[0] == 'left':
        iteration +=1
        grate.ori-=1

win.close()
core.quit()
quit() # Needed for SublimeREPL only