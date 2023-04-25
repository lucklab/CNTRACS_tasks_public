# P R A C T I C E #
# currently set to present 4 trials #
'''
3.1.3. Episodic Memory: Our team has also applied this
model to episodic memory (EM) using the task shown in Fig.
2C76. The participant sees a sequence of 8 word-bar location
pairs, clicking on the location of each bar per word shown, and must store these pairs in memory.
After a filled retention interval, the participant sees each word and must click on the location of the bar that was 
originally paired with that word. The amount of information substantially exceeds WM capacity,
and the information is therefore stored in EM (even though the memory is probed within
1-2 minutes of the initial presentation). This procedure is then repeated several times with different words and
locations. When the mixture model is applied to data from this task, it is possible to estimate the probability that
a given pair was stored in EM, the precision of the EM representation, and the probability of a binding error
(reporting the location associated with a different word). We have found that measures of EM precision are
particularly sensitive for detecting memory impairments and hippocampal dysfunction in patient populations
(see 49 for review). For example, Kolarik17, 77 examined the ability of patients with MTL damage to remember
object locations and found a deficit only when they were required to report precise spatial locations. Similarly,
Koen18 found that MTL lesion patients were significantly more impaired when the test required high-precision
discriminations than low-precision discriminations, even when overall difficulty was controlled. Use of precision
metrics to increase sensitivity to EM impairments and hippocampal dysfunction will provide an integrated
understanding of the unique contribution that EM dysfunction makes to a range of affective and psychotic
disorders78-81. This may help to identify either a shared psychopathology across diagnostic categories or show
differential associations with specific symptom domains, which can help to guide treatment interventions.
'''

# Import key parts of the PsychoPy library:
from psychopy import visual, monitors, core, event, sound, data, gui, prefs
prefs.general['audioLib'] = ['pyo']
from psychopy.tools.filetools import fromFile, toFile
import math, random, numpy, os
import glob 
# EEG
from psychopy import parallel
import serial

# make sure working directory is right
os.chdir(os.path.dirname(os.path.abspath(__file__)))
imageDirectory = 'Practice_30' #folder/directory the images are in, must contain exactly the images to be used

# set a seed - makes everything not actually random. Randomize seed or take out to randomize order of trials
seed = 10000 # use 20000 for a separate version?
random.seed(seed)

## start a datafile
expInfo = {
    'Participant'   :   'PRACTICE',
    'EEG Triggers?'      :   ['Yes','No'], #default to send triggers
    'Session'       :   '1',
    'Version'       :   'A', #only one version
    'TrialsToAdminister':   '4',
    'BlockLength'   :   '4',
    'EncodingArrayDuration' :   6.0,
    'TaskFile'      :   os.path.basename(__file__)[:-3],
    'Date'          :   data.getDateStr(),
    'Seed'          :   seed
    }
# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Picture-Bar Pairs', fixed=['TrialsToAdminister','Version','EncodingArrayDuration','TaskFile','Date','Seed'], order=['Participant','Session','BlockLength'])

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
        fullscr=True #fullscrn=False if window is small, True to take the full screen
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

# FOR EEG TRIGGERS  #
# trigs should be set to 'Yes' if you are running with EEG
# trigs can be set to 'No' for testing without triggers

# send triggers?
trigs = expInfo['EEG Triggers?'] # Yes -- if triggers should be sent
portType = 'Serial' # or 'Parallel'

# portType should be set to Parallel or Serial

if trigs =='Yes':
    if portType == 'Parallel':
        port = parallel.ParallelPort(address=0x3FF8) # has to be the correct address...
        
        def sendTrigger(trigger):
            port.setData(int(trigger))
            core.wait(0.005)
            port.setData(0)

    if portType == 'Serial':
        port = serial.Serial('COM3') # correct address...

        def sendTrigger(trigger):
            port.write(bytes([int(trigger)]))
            core.wait(0.005)
            port.write(bytes([0]))

    if portType not in ['Parallel','Serial'] :
        print('Set "portType" variable to "Serial" or "Parallel" at the top of script')
        core.quit()

elif trigs == 'No':
    def sendTrigger(trigger):
        core.wait(0.005)

else:
    print('Set "trigs" variable to "Yes" or "No" at the top of script')
    core.quit()

#                   #
def give_instructions():
    mywin.flip()
    
    instructionDir= 'InstructionSlides' #folder/directory the images are in,
    instructionFiles = []
    instructionFiles = sorted(glob.glob(os.path.join(instructionDir, '*.png')))  # where the image files get loaded
    
    sendTrigger(252) # instructions onset 
    
    for instr in list(range(0,len(instructionFiles))):
        instrImage = visual.ImageStim(win=mywin, image=instructionFiles[instr])
        
        instrImage.draw()
        mywin.flip()
        
        if event.getKeys(keyList=['escape', 'q']):
            mywin.close()
            core.quit()
        
        click = mouse.getPressed()
        while click[0] == 0:
            instrImage.draw()
            fixation0.pos=mouse.getPos()
            fixation0.draw()
            mywin.flip()
            
            click = mouse.getPressed()
        
        core.wait(.20)
        event.clearEvents()

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
        bold=False,
        italic=False,
        alignHoriz='center',
        alignVert='center',
        fontFiles=(),
        wrapWidth=None,
        flipHoriz=False,
        flipVert=False,
        name=None
        )
    thanksText.setText(
        'Thank you for participating!\n\n'
        'You have now finished the practice, do you have any questions?\n\n'
        'Click the mouse to exit the practice.'
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

def break_between_blocks():
    fixation0.draw()
    mywin.flip()
    buttons = mouse.getPressed()
    while buttons[0] == 0:
        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()
        buttons = mouse.getPressed()
        if buttons [0] > 0:
            fixation0.setAutoDraw(False)
    core.wait(1.0)

def long_break_between_blocks(breakNum):
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
        bold=False,
        italic=False,
        alignHoriz='center',
        alignVert='center',
        fontFiles=(),
        wrapWidth=None,
        flipHoriz=False,
        flipVert=False,
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
    if math.atan2(mY,mX)*180/math.pi>0:
        angle0= math.atan2(mY,mX)*180/math.pi
    else:
        angle0= (2*math.pi + math.atan2(mY,mX))*180/math.pi
    trial['probedAngle']=int(angle0)
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
    stimRadius.lineColor=[-0.5,-0.5,-0.5]
    stimRadius.draw()
    fixation0.pos=mouse.getPos()
    fixation0.draw()
    fixation1.pos=mouse.getPos()
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)
    mywin.flip()
    sendTrigger(249)
    trial['trialOnsetEncoding'] = clock.getTime()-trial['trialOnset'] #time stamp start of encoding
    while clock.getTime() - (trial['trialOnset'] + trial['trialOnsetEncoding']) <= trial['durEncoding']:
        while correctClicks == 0 and clock.getTime() - (trial['trialOnset'] + trial['trialOnsetEncoding']) <= trial['durEncoding']:
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
                    trial['respRT_encoding'] = clock.getTime() - (trial['trialOnset'] + trial['trialOnsetEncoding'])
                    correctClicks+=1
                    break
            if clock.getTime() - (trial['trialOnset'] + trial['trialOnsetEncoding']) >= trial['durBeforeWarning'] and trial['respLateWarning_encoding'] == False and correctClicks == 0:
                warning.play(loops = 1)
                trial['respLateWarning_encoding'] = True
        shape0.draw()
        backgroundCircle.draw()
        trialImage.draw(win = mywin)
        stimRadius.draw()
        mywin.flip()
        event.clearEvents()

def present_retention_interval():
    mywin.flip()
    trial['trialOnsetRetention'] = clock.getTime()-trial['trialOnset'] #time stamp start of retention
    for frame in range(trial['framesITI']*2):
        mywin.flip()
    for frame in range(trial['framesRetention']-trial['framesITI']*2):
        breakScreen.draw()
        mywin.flip()

def present_response_window(i,j):
    mouse = event.Mouse(visible = False, win = mywin)
    mouse.setPos([0,0])
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)
    tested_trial=trials.getEarlierTrial((numTrialsPerBlock-1)-i)
    trialImageFile = tested_trial['imageFile'] # image file with path
    trialImage.setImage(trialImageFile)
    tested_trial['trialOnsetRespWindow'] = clock.getTime()-trial['trialOnset']
    tested_trial['trialTestOrder'] = j
    rawOnset=clock.getTime()
    if event.getKeys(keyList=['escape', 'q']):
        save_data()
        mywin.close()
        core.quit()
    while tested_trial['respRT'] == 0:
        innerResponseLimit.draw()
        outerResponseLimit.draw()
        stimRadius.lineColor=[-0.5,-0.5,-0.5]
        stimRadius.draw()
        backgroundCircle.draw()
        trialImage.draw(win = mywin)
        fixation0.pos=mouse.getPos() # changed to fixation0
        fixation0.draw()
        mywin.flip()
        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()
        if mouse.isPressedIn(outerResponseLimit, buttons=[0]):
            if not mouse.isPressedIn(innerResponseLimit, buttons=[0]):
                tested_trial['respRT']     = clock.getTime()-rawOnset #reaction time
                tested_trial['respXY']     = mouse.getPos()
                sendTrigger(248)
                mX,mY   =   tested_trial['respXY']
                if math.atan2(mY,mX)*180/math.pi>0:
                    rA  = math.atan2(mY, mX)*180/math.pi
                else:
                    rA  = (2*math.pi + math.atan2(mY, mX))*180/math.pi
                tested_trial['respAngle']=round(rA,1)
                break
        if clock.getTime()-rawOnset >= tested_trial['durBeforeWarning'] and tested_trial['respLateWarning'] == False:
            warning.play(loops = 1)
            tested_trial['respLateWarning'] = True
        event.clearEvents()

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
            'Session',
            'Version',
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
            'trialOnsetEncoding',
            'trialOnsetRetention',
            'trialOnsetRespWindow',
            'trialTestOrder',
            'respLateWarning_encoding',
            'respRT_encoding',
            'respLateWarning',
            'respRT',
            'respXY',
            'probedXY',
            'respAngle',
            'probedAngle'
            ]
        )
# Added for images 
imageFiles = []
imageFiles = glob.glob(os.path.join(imageDirectory, '*.jpg'))  # where the image files get loaded

trialImage = visual.ImageStim(win=mywin, image=imageFiles[0]) # temp image
trialImage.size = [3.5,3.5] # set image size
backgroundRadius = math.sqrt((trialImage.size[0]/2)**2 + (trialImage.size[0]/2)**2) # set background size - smallest circle around square image

#                 #
## timing constants
durITI              =   1.5
durFixITI           =   .5  # will be subtracted from durITI as salient fixation
durEncoding         =   expInfo['EncodingArrayDuration']
durRetention        =   4.0 #"Get ready to be tested!" appears onscreen for this period
durBeforeWarning    =   5.0 #beep if no response after given duration
durRespWindow       =   -1.0 #open-ended response window
frameRate           =   mywin.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)
framesITI           =   int(round(durITI/frameRate[0]*1000))
framesFixITI        =   int(round(durFixITI/frameRate[0]*1000))
framesEncoding      =   int(round(durEncoding/frameRate[0]*1000))
framesRetention     =   int(round(durRetention/frameRate[0]*1000))
framesBeforeWarning =   int(round(durBeforeWarning/frameRate[0]*1000))

## Stimulus dimensions
dvaArrayRadius = 3.5
dvaArrayItemLength = 1
dvaArrayItemWidth = 0.1

## Array values
setSizes            =[1]
numTrialsPerBlock   =int(expInfo['BlockLength']) #pairs per block
numTrialsPerSetSize =int(len(imageFiles)) #picture-bar pairs 
numBlocksBetweenBreaks = 10
sortedTrials        =list(range(0,numTrialsPerSetSize*len(setSizes)))
randomizedTrials    =list(range(0,numTrialsPerSetSize*len(setSizes)))
random.shuffle(randomizedTrials)
numStimulusLocations=30
locations           =list(range(0,numStimulusLocations))
colors              =['white']
itemSeparation      =4 * (90/numStimulusLocations) #degrees arc
angles              = []
angle_XYs           = []
for x in range(0,numStimulusLocations):
    angles.append(x*itemSeparation+1)
    angle_X=math.cos((x*itemSeparation+1)*math.pi/180)*dvaArrayRadius
    angle_Y=-math.sin((x*itemSeparation+1)*math.pi/180)*dvaArrayRadius
    angle_XYs.append([angle_X, angle_Y])

## define parameters for each trial of each trial type

tList=[]

for x in list(range(0,numTrialsPerSetSize*len(setSizes))):
    ss  =   setSizes[math.trunc(randomizedTrials[x]/numTrialsPerSetSize)]  #set size
    pl  =   [randomizedTrials[x]%numStimulusLocations]                      #probed location
    pc  =   colors[randomizedTrials[x]%len(colors)]                        #probed color
    if ss == 1:
        ul  = []
        uc  = []
    else:
        temp = range(0,len(locations))
        temp.remove(pl[0])
        ul  =   random.sample(temp,ss-1)                    #unprobed locations
        uc  =   [i for i in colors if i != pc]              #unprobed colors
    alll=   pl + ul
    allc=   [pc] + uc
    tList.append({
        'Participant'       :   expInfo['Participant'],
        'Session'           :   expInfo['Session'],
        'Version'           :   expInfo['Version'],
        'TaskFile'          :   expInfo['TaskFile'],
        'Date'              :   expInfo['Date'],
        'Seed'              :   expInfo['Seed'],
        'BlockLength'       :   expInfo['BlockLength'],
        'trialNumber'       :   sortedTrials[x],
        'trialIndex'        :   randomizedTrials[x],
        'trialWithinBlock'  :   sortedTrials[x]%numTrialsPerBlock,
        'trialOnset'        :   0, #not yet set
        'trialOnsetEncoding':   0,
        'trialOnsetRetention':  0,
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
#        'image'             :   imageFiles[randomizedTrials[x]][len(imageDirectory)+2:], # might need to change the 2 here...
        'imageFile'         :   imageFiles[randomizedTrials[x]],
        'durITI'            :   durITI,
        'durEncoding'       :   durEncoding,
        'durRetention'      :   durRetention,
        'durBeforeWarning'  :   durBeforeWarning,
        'durRespWindow'     :   durRespWindow,
        'framesITI'         :   framesITI,
        'framesEncoding'    :   framesEncoding,
        'framesRetention'   :   framesRetention,
        'framesBeforeWarning':  framesBeforeWarning,
        'respLateWarning'   :   False,
        'respLateWarning_encoding'   :   False,
        'respRT_encoding'   :   0.0,
        'respRT'            :   0.0,
        'respXY'            :   [[0,0],[0,0]],
        'respAngle'         :   0,
        'probedAngle'       :   0
        })
    

## define trial stimuli
breakScreen = visual.TextStim(
    win=mywin,
    autoLog=False,
    text="Get ready to get tested!"
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
#
fixationB = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    radius=dvaArrayItemWidth*2,
    lineColor=[-.5,-.5,-.5],
    fillColor=[-.5,-.5,-.5],
    pos=(0, 0)
    )
#
fixation1 = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    radius=dvaArrayItemWidth,
    pos=(0, 0)
    )
vtx=(
    (-dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (dvaArrayItemLength/2, dvaArrayItemWidth/2),
    (-dvaArrayItemLength/2, dvaArrayItemWidth/2)
    )
shape0 = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape1 = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape2 = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape3 = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
text0 = visual.TextStim(
    win=mywin,
    autoLog=False,
    height=0.75,
    text='test'
    )
# Added for image version #
backgroundCircle = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg', # note unit
    edges=48,
    radius = backgroundRadius, # minimum possible, scales with image size
    fillColorSpace = 'rgb255',
    fillColor = 255
    )

#                          #

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

# Experiment Start #
give_instructions()

blockNum = 0
breakNum = 0
mouse = event.Mouse(visible = False, win = mywin)
for trial in trials:
    setup_trial()
    present_ITI()
    present_encoding_array()
    if trial['trialNumber']%numTrialsPerBlock == numTrialsPerBlock-1 or trial['trialNumber'] == numTrialsRequested-1:
        present_retention_interval() #prepare to get tested
        
        core.wait(1)
        if trial['trialNumber']%numTrialsPerBlock == numTrialsPerBlock-1:
            testrange=list(range(0,numTrialsPerBlock)) # added a list() 
        elif trial['trialNumber'] == numTrialsRequested-1:
            testrange=list(range(numTrialsPerBlock-numTrialsRequested%numTrialsPerBlock,numTrialsPerBlock)) # Kurt added a list() here to make it work, revert if needed
        random.shuffle(testrange)
        j=0
        for i in testrange:
            present_response_window(i,j)
            j+=1
        blockNum += 1
        if trial['trialNumber'] != numTrialsRequested-1:
            long_break_between_blocks(blockNum)
give_thanks()
# Finishing touches
#save_data()
mywin.close()
core.quit()