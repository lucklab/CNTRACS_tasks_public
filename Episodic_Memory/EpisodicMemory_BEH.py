'''
Episodic Memory

The participant sees a sequence of 8 picture-bar location pairs, 
clicks on the location of each bar per picture shown,
and must store these pairs in memory.

After a filled retention interval, the participant sees each picture again
and must click on the location of the bar that was originally paired with that picture.

The amount of information substantially exceeds WM capacity,
and the information is therefore stored in EM 
(even though the memory is probed within 1-2 minutes of the initial presentation).

This procedure is then repeated several times with different pictures and locations.

When a mixture model is applied to data from this task, it is possible to estimate the probability that
a given pair was stored in EM, the precision of the EM representation.


This version of the task uses pictures, an earlier version used words instead.
The pictures were gotten from --  "cvcl.mit.edu/MM/"

Note:
This task is set up to run with just one set size (1)
However there is some currently unused code in this script for running with trials at other set sizes (more bars than 1)
I've chosen to leave this code here in case it's helpful for someone who wishes to modify the code for more set size conditions.
'''

## Import modules
from psychopy import visual, monitors, core, event, sound, data, gui, prefs
prefs.general['audioLib'] = ['pyo']
import math, random, numpy, os, glob, csv
import pandas as pd


## Important: set seed for randomization.
# The seed used by the CNTRACS group was 10000 always, meaning the 'randomization' was the same for all runs
# To use this (and thus get the same exact version), un-comment the line below, and comment out the other seed line
#seed = 10000 # could use a different arbitrary number for a separate version that would be consistent across runs

# To have the trial ordering random each run, have the line below un-commented
seed = int(random.uniform(1, 1000000))

# Actually set the seed
random.seed(seed)

## start a datafile
expInfo = {
    'Participant'   :   '---',
    'TrialsToAdminister':   'all',
    'BlockLength'   :   '8',
    'EncodingArrayDuration' :   6.0,
    'TaskFile'      :   os.path.basename(__file__)[:-3],
    'Date'          :   data.getDateStr(),
    'Seed'          :   seed
    }

# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Picture-Bar Pairs', 
                      fixed=['TrialsToAdminister','EncodingArrayDuration','TaskFile','Date','Seed','BlockLength'], 
                      order=['Participant'])
        
if dlg.OK:  # or if ok_data is not None
    ## Define a monitor
    my_monitor = monitors.Monitor(name='ERP1_stim')
    my_monitor.setSizePix((1920,1200))
    my_monitor.setWidth(52)
    my_monitor.setDistance(100)
    my_monitor.saveMon()
    ## Create a visual window:
    mywin = visual.Window(
        monitor='ERP1_stim',
        autoLog=False,
        units='deg',
        screen=0, #screen=0 for primary monitor, screen=1 to display on secondary monitor
        fullscr=True 
        )
    loadingScreen = visual.TextStim(
        win=mywin,
        autoLog=False,
        text="Loading..."
        )

    loadingScreen.setAutoDraw(True)
    loadingScreen.draw()
    mywin.flip()
    mouse = event.Mouse(visible = False, win = mywin)
    clock = core.Clock()

else:
    core.quit()  # the user hit cancel so exit

## For images

# make sure working directory is right
os.chdir(os.path.dirname(os.path.abspath(__file__))) # this sets the wd to be where the script is located 
imageDirectory = 'Objects_160' #folder/directory the images are in, must contain exactly the images to be used

imageFiles = []
imageFiles = glob.glob(os.path.join(imageDirectory, '*.jpg'))  # where the image files get loaded

trialImage = visual.ImageStim(win=mywin, image=imageFiles[0]) # temp image
trialImage.size = [3.5,3.5] # set image size, in degrees

backgroundRadius = math.sqrt((trialImage.size[0]/2)**2 + (trialImage.size[0]/2)**2) # set background size - smallest circle around square image

# makes a dict with event codes for each image file based on csv file ( alphabetical order by filename )
eventMap = pd.read_csv("image_codes.csv", sep=',', index_col = 0, squeeze = True).to_dict()

## Set parameters

# Timing (seconds)
durITI              =   1 # 1 sec with 50ms jitter
durFixITI           =   .5  # will be subtracted from durITI as salient fixation
durEncoding         =   expInfo['EncodingArrayDuration']
durRetention        =   4.0 #"Get ready to be tested!" appears onscreen for this period
durBeforeWarning    =   5.0 #beep if no response after given duration
durRespWindow       =   -1.0 #open-ended response window
# in frames
frameRate           =   mywin.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)
framesITI           =   int(round(durITI/frameRate[0]*1000))
framesFixITI        =   int(round(durFixITI/frameRate[0]*1000))
framesEncoding      =   int(round(durEncoding/frameRate[0]*1000))
framesRetention     =   int(round(durRetention/frameRate[0]*1000))
framesBeforeWarning =   int(round(durBeforeWarning/frameRate[0]*1000))

## Stimulus dimensions
dvaArrayRadius = 3.5 # radius of circle 
dvaArrayItemLength = 1 # length of bars
dvaArrayItemWidth = 0.1 # width of bars

## Conditions, locations info
setSizes            =[1] # Just 1 set size now
numTrialsPerBlock   =int(expInfo['BlockLength']) #pairs per block
numTrialsPerSetSize =int(len(imageFiles)) #picture-bar pairs
numBlocksBetweenBreaks = 10
sortedTrials        =list(range(0,numTrialsPerSetSize*len(setSizes)))
randomizedTrials    =list(range(0,numTrialsPerSetSize*len(setSizes)))
random.shuffle(randomizedTrials) # uses a seed defined at the top

# Note on stimulus locations: The original version used 90, but this led to a bias in what locations were most likely
numStimulusLocations=numTrialsPerSetSize # currently set so that each of the 160 items can have their own location, original = 90
locations           =list(range(0,numStimulusLocations))
colors              =['white']
itemSeparation      = 360/numStimulusLocations # even spaced locations, original version used '4' here
angles              = []
angle_XYs           = []


#  0 degrees (and location 0) is on the right most end of the circle (3 oclock)
# 90 degrees is on the bottom (6 oclock) and so on around the circle...

for x in range(0,numStimulusLocations):
    angles.append(x*itemSeparation+1) # this +1 offset works for our purposes, breaks if numStimulusLocations >= 360
    # the +1 offset ^ is not strictly needed, just takes angles off the cardinal axes
    angle_X=math.cos((x*itemSeparation+1)*math.pi/180)*dvaArrayRadius
    angle_Y=-math.sin((x*itemSeparation+1)*math.pi/180)*dvaArrayRadius
    angle_XYs.append([angle_X, angle_Y])

### Make trial list

tList=[]

for x in list(range(0,numTrialsPerSetSize*len(setSizes))):
    ss  =   setSizes[math.trunc(randomizedTrials[x]/numTrialsPerSetSize)]  #set size (in this task, just SS = 1)
    pl  =   [randomizedTrials[x]%numStimulusLocations]                     #probed location 
    pc  =   colors[randomizedTrials[x]%len(colors)]                        #probed color (in this task, just white)

    if ss == 1: # always true in this version
        ul  = []
        uc  = []

    else:
        temp = range(0,len(locations))
        temp.remove(pl[0])
        ul  =   random.sample(temp,ss-1)                    #unprobed locations
        uc  =   [i for i in colors if i != pc]              #unprobed colors

    alll=   pl + ul
    allc=   [pc] + uc
    # jitter adding
    tITI = durITI + (random.randrange(-50,50,1))*0.001
    tframesITI           =   int(round(tITI/frameRate[0]*1000))

    thisImage = imageFiles[randomizedTrials[x]][len(imageDirectory)+1:]# might need to change the 1 here depending on OS?
    
    tList.append({
        'Participant'       :   expInfo['Participant'],
        'TaskFile'          :   expInfo['TaskFile'],
        'Date'              :   expInfo['Date'],
        'Seed'              :   expInfo['Seed'],
        'BlockLength'       :   expInfo['BlockLength'],
        'trialNumber'       :   sortedTrials[x],
        'trialIndex'        :   randomizedTrials[x],
        'trialWithinBlock'  :   sortedTrials[x]%numTrialsPerBlock,
        'trialOnset'        :   0, #not yet set
        'trialITIDuration'  :   0,
        'OnsetRetention'    :   0,
        'trialOnsetRespWindow': 0,
        'trialTestOrder'    :   0,
        'blockNumber'       :   math.trunc(sortedTrials[x]/numTrialsPerBlock),
        'probedLocation'    :   pl,
        'probedColor'       :   pc,
        'allLocations'      :   alll,
        'allColors'         :   allc,
        'allOrientations'   :   [i * itemSeparation+1 for i in alll],
        'probedXY'          :   angle_XYs[randomizedTrials[x]%numStimulusLocations],
        'allXY'             :   [angle_XYs[i] for i in alll],
        'image'             :   thisImage, # defined above
        'imageFile'         :   imageFiles[randomizedTrials[x]], 
        'durITI'            :   tITI, #jittered
        'durEncoding'       :   durEncoding,
        'durRetention'      :   durRetention,
        'durBeforeWarning'  :   durBeforeWarning,
        'durRespWindow'     :   durRespWindow,
        'framesITI'         :   tframesITI,
        'framesEncoding'    :   framesEncoding,
        'framesRetention'   :   framesRetention,
        'framesBeforeWarning':  framesBeforeWarning,
        'respLateWarning'   :   False,
        'respLateWarning_encoding'   :   False,
        'respRT_encoding'   :   0.0,
        'respRT'            :   0.0,
        'respXY'            :   [[0,0],[0,0]],
        'respAngle'         :   0,
        'probedAngle'       :   0,
        'respError'         :   -1
        })

### Define functions

# for getting angle differences
def diff_wrap(a, b, half=True): # half means the direction doesnt matter
    if half:
        angle = (180 - numpy.abs(numpy.abs(a - b) - 180))
    else:
        #flip the negative an positive so that right is positive
        angle = (180 - numpy.abs(numpy.abs(a - b) - 180)) * -1* numpy.sign(numpy.sin(numpy.radians(a-b)))
    return angle

def give_instructions():
    mywin.flip()

    instructionsText = visual.TextStim(
        win=mywin,
        autoLog=False,
        font='Arial',
        pos=(0.0, 0.0),
        rgb=None,
        color=(1.0,1.0,1.0),
        colorSpace='rgb',
        opacity= 1.0,
        contrast=1.0,
        units='',
        ori=0,
        height=0.5,
        antialias=True,
        name=None
        )
    
    instructionsText.setText(
        'When you are ready, click the mouse to begin the task.'
        )
    
    instructionsText.setAutoDraw(True)
    instructionsText.draw()
    
    mywin.flip()
    clock.reset(newT=0.0) #resets clock
    
    buttons = mouse.getPressed()
    
    while buttons[0] == 0:
        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()
        buttons = mouse.getPressed()
    
        if buttons [0] > 0:
            instructionsText.setAutoDraw(False)
            break
    
    fixationB.draw()
    mywin.flip()
    core.wait(1)

def break_between_blocks(breakNum):
    mywin.flip()
    core.wait(1.0)
    breakText = visual.TextStim(
        win=mywin,
        autoLog=False,
        font='Arial',
        pos=(0.0, 0.0),
        rgb=None,
        color=(1.0, 1.0, 1.0),
        colorSpace='rgb',
        opacity=1.0,
        contrast=1.0,
        units='',
        ori=0.0,
        height=0.5,
        antialias=True,
        name=None
        )
    breakText.setText(
        'Block ' + str(breakNum) + ' of ' + str(int(round(float(numTrialsRequested/numTrialsPerBlock)))) + '.\n\nClick the mouse button when you are ready to continue.'
        )
    breakText.setAutoDraw(True)
    breakText.draw()
    mywin.flip()

    buttons = mouse.getPressed()

    while buttons[0] == 0:
        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()
        buttons = mouse.getPressed()
        if buttons [0] > 0:
            breakText.setAutoDraw(False)
            break
    
    fixationB.radius = dvaArrayItemWidth*2
    fixationB.draw()
    mywin.flip()
    
    core.wait(1) # buffer

def setup_trial():
    trial['trialOnset'] = clock.getTime()
    acs=trial['allColors']
    aos=trial['allOrientations']
    axy=trial['allXY']

    trial['respRT']     = -0.0
    trial['respXY']     = [-0.0,-0.0]
    trial['respAngle']  = -0.0

    fixation1.setLineColor(trial['probedColor'])
    fixation1.setFillColor(trial['probedColor'])

    shape0.setLineColor(acs[0])
    shape0.setFillColor(acs[0])
    shape0.setOri(aos[0])
    shape0.setPos(axy[0])
    mX,mY=axy[0]

    # if running at higher set sizes, need to add more shape objects here.
    
    if math.atan2(mY,mX)*180/math.pi>0:
        angle0= math.atan2(mY,mX)*180/math.pi
    else:
        angle0= (2*math.pi + math.atan2(mY,mX))*180/math.pi

    trial['probedAngle']=angle0
    trialImageFile = trial['imageFile'] # image file with path
    trialImage.setImage(trialImageFile) # set the image

def present_ITI():
    
    mouse.setPos([0,0])
    fixation0.pos=mouse.getPos()
    
    fixationB.radius = dvaArrayItemWidth*2
    fixationB.draw() # more salient fixation
    mywin.flip()
    
    for frame in range(framesFixITI-1):  # minus 1 because of flip before
        fixationB.radius -= 0.005 #shrinks fixation
        fixationB.draw()
        mywin.flip()
        
    for frame in range(trial['framesITI']-framesFixITI-1):  # minus 1 because of flip after ITI
        fixation0.draw()
        mywin.flip()

def present_encoding_array():
    correctClicks = 0
    mouse.setPos([0,0])
    backgroundCircle.draw() # draw background
    trialImage.draw(win = mywin) # draw image
    shape0.draw()
    # add more shapes to draw here, if running at higher set sizes
    stimRadius.lineColor=[-0.5,-0.5,-0.5]
    stimRadius.draw()
    fixation0.pos=mouse.getPos()
    fixation0.draw()
    fixation1.pos=mouse.getPos()
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)

    mywin.flip()

    trial['trialITIDuration'] = clock.getTime()-trial['trialOnset'] #time stamp start of encoding
    
    while clock.getTime() - (trial['trialOnset'] + trial['trialITIDuration']) <= trial['durEncoding']:

        while correctClicks == 0 and clock.getTime() - (trial['trialOnset'] + trial['trialITIDuration']) <= trial['durEncoding']:

            if event.getKeys(keyList=['escape', 'q']):
                save_data()
                mywin.close()
                core.quit()

            backgroundCircle.draw()
            trialImage.draw(win = mywin)
            shape0.draw()
            stimRadius.draw()
            fixation0.pos=mouse.getPos()
            fixation0.draw()
            fixation1.pos=mouse.getPos()
            mywin.flip()
            buttons = mouse.getPressed()

            if buttons[0]>0:

                if fixation0.overlaps(shape0):

                    trial['respRT_encoding'] = clock.getTime() - (trial['trialOnset'] + trial['trialITIDuration'])
                    correctClicks+=1
                    break

            if clock.getTime() - (trial['trialOnset'] + trial['trialITIDuration']) >= trial['durBeforeWarning'] and trial['respLateWarning_encoding'] == False and correctClicks == 0:
                warning.play(loops = 0)
                trial['respLateWarning_encoding'] = True

        shape0.draw()
        backgroundCircle.draw()
        trialImage.draw(win = mywin)
        stimRadius.draw()
        mywin.flip()
        event.clearEvents()

def present_retention_interval():
    mywin.flip()
    trial['OnsetRetention'] = clock.getTime() # raw time stamp start of retention

    for frame in range(trial['framesITI']): # took a *2 muliplier off of the frames...
        mywin.flip()

    for frame in range(trial['framesRetention']-trial['framesITI']): # took a *2 muliplier off of the frames...
        breakScreen.draw()
        mywin.flip()

def present_response_window(i,j):
    mouse = event.Mouse(visible = False, win = mywin)
    mouse.setPos([0,0])
    tested_trial=trials.getEarlierTrial((numTrialsPerBlock-1)-i)
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)

    trialImageFile = tested_trial['imageFile'] # image file with path
    trialImage.setImage(trialImageFile)    
    tested_trial['trialOnsetRespWindow'] = clock.getTime()-trial['OnsetRetention'] # testing time RELATIVE TO 'OnsetRetention'
    tested_trial['trialTestOrder'] = j
    
    if event.getKeys(keyList=['escape', 'q']):
        save_data()
        mywin.close()
        core.quit()
    
    rawOnset=clock.getTime()
    
    while tested_trial['respRT'] == 0:
        innerResponseLimit.draw()
        outerResponseLimit.draw()
        stimRadius.lineColor=[-0.5,-0.5,-0.5]
        stimRadius.draw()
        backgroundCircle.draw()
        trialImage.draw(win = mywin)
        fixation0.pos=mouse.getPos() # changed to fixation0
        fixation0.draw() # changed to fixation0
        mywin.flip()

        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()

        if mouse.isPressedIn(outerResponseLimit, buttons=[0]):

            if not mouse.isPressedIn(innerResponseLimit, buttons=[0]):
                tested_trial['respRT']     = clock.getTime()-rawOnset #reaction time
                tested_trial['respXY']     = mouse.getPos()
                mX,mY   =   tested_trial['respXY']

                if math.atan2(mY,mX)*180/math.pi>0:
                    rA  = math.atan2(mY, mX)*180/math.pi

                else:
                    rA  = (2*math.pi + math.atan2(mY, mX))*180/math.pi

                tested_trial['respAngle']=round(rA,1)

                break

        if clock.getTime()-rawOnset >= tested_trial['durBeforeWarning'] and tested_trial['respLateWarning'] == False:
            warning.play(loops = 0)
            tested_trial['respLateWarning'] = True

        event.clearEvents()
        
    # response error
    tested_trial['respError'] = diff_wrap(tested_trial['probedAngle'],tested_trial['respAngle']) # function doing this defined above

def save_data():
    savingScreen = visual.TextStim(
        win=mywin,
        text="Saving to file..."
        )

    savingScreen.setAutoDraw(True)
    savingScreen.draw()
    mywin.flip()

    ## create the datafile
    trials.saveAsExcel(
        fileName=expInfo['TaskFile']+"_"+expInfo['Date']+"_"+expInfo['Participant']+'.csv',
        sheetName = expInfo['Participant']+"_"+expInfo['Date'],
        stimOut=[
            'Participant',
            'TaskFile',
            'Date',
            'Seed',
            'BlockLength',
            'durITI',
            'durEncoding',
            'durRetention',
            'durBeforeWarning',
            'durRespWindow',
            'trialIndex',
            'trialNumber',
            'trialWithinBlock',
            'blockNumber',
            'probedLocation',
            'image',
            'imageFile',
            'trialOnset',
            'trialITIDuration',
            'OnsetRetention',
            'trialOnsetRespWindow',
            'trialTestOrder',
            'respLateWarning_encoding',
            'respRT_encoding',
            'respLateWarning',
            'respRT',
            'respXY',
            'probedXY',
            'respAngle',
            'probedAngle',
            'respError'
            ]
        )

def give_thanks():
    mywin.flip()

    thanksText = visual.TextStim(
        win=mywin,
        autoLog=False,
        font='Arial',
        pos=(0.0, 0.0),
        rgb=None,
        color=(1.0,1.0,1.0),
        colorSpace='rgb',
        opacity= 1.0,
        contrast=1.0,
        units='',
        ori=0,
        height=0.5,
        antialias=True,
        name=None
        )

    thanksText.setText(
        'Thank you for participating!\n\n'
        'You have now finished the experiment, please alert the experimenter.\n\n'
        'Click the mouse to exit the experiment.'
        )

    thanksText.setAutoDraw(True)
    thanksText.draw()
    mywin.flip()
    
    core.wait(1.5)
    buttons = mouse.getPressed()

    while buttons[0] == 0:
        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()
        buttons = mouse.getPressed()

        if buttons [0] > 0:
            thanksText.setAutoDraw(False)
            break

### Create stimuli

breakScreen = visual.TextStim(
    win=mywin,
    autoLog=False,
    text="Get ready to be tested!"
    )

stimRadius = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    edges=90,
    lineColor=[0,0,0],
    radius=dvaArrayRadius,
    pos=(0, 0)
    )

innerResponseLimit = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    lineColor=[0,0,0],
    radius=dvaArrayRadius-dvaArrayItemWidth*2,
    pos=(0, 0)
    )

outerResponseLimit = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    lineColor=[0,0,0],
    radius=dvaArrayRadius+dvaArrayItemWidth*2,
    pos=(0, 0)
    )

fixation0 = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    radius=dvaArrayItemWidth/2,
    lineColor=[-.5,-.5,-.5],
    fillColor=[0,0,0],
    pos=(0, 0)
    )

fixation1 = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    radius=dvaArrayItemWidth,
    pos=(0, 0)
    )
# more salient fixation loom
fixationB = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    radius=dvaArrayItemWidth*2,
    lineColor=[-.5,-.5,-.5],
    fillColor=[-.5,-.5,-.5],
    pos=(0, 0)
    )
# bar dimensions
vtx=(
    (-dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (dvaArrayItemLength/2, dvaArrayItemWidth/2),
    (-dvaArrayItemLength/2, dvaArrayItemWidth/2)
    )
# the bar stim
shape0 = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )

# background added for images
backgroundCircle = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg', # note unit
    edges=48,
    radius = backgroundRadius, # minimum possible, scales with image size
    fillColorSpace = 'rgb255',
    fillColor = 255
    )

# Set up trials

if expInfo['TrialsToAdminister']=='all':
    numTrialsRequested = len(tList)
else:
    numTrialsRequested = int(expInfo['TrialsToAdminister'])

trials = data.TrialHandler(
    trialList=tList[0:int(numTrialsRequested)],
    nReps=1,
    method='sequential',
    dataTypes=[],
    seed=expInfo['Seed']
    )

loadingScreen.setAutoDraw(False)

### Experiment Start ###

give_instructions()

blockNum = 0
breakNum = 0
mouse = event.Mouse(visible = False, win = mywin)

for trial in trials:

    setup_trial()

    present_ITI()

    present_encoding_array()
    
    # check if time for test
    if trial['trialNumber']%numTrialsPerBlock == numTrialsPerBlock-1 or trial['trialNumber'] == numTrialsRequested-1:

        present_retention_interval() #prepare to get tested

        if trial['trialNumber']%numTrialsPerBlock == numTrialsPerBlock-1:
            testrange=list(range(0,numTrialsPerBlock)) 

        elif trial['trialNumber'] == numTrialsRequested-1:
            testrange=list(range(numTrialsPerBlock-numTrialsRequested%numTrialsPerBlock,numTrialsPerBlock)) 

        random.shuffle(testrange)
        j=0

        for i in testrange:
            present_response_window(i,j)
            j+=1

        blockNum += 1

        if trial['trialNumber'] != numTrialsRequested-1:
            break_between_blocks(blockNum)
        
give_thanks()

# End
save_data()
mywin.close()
core.quit()
