
'''
3.1.2. WM Capacity: Here we illustrate the
model with one of our proposed tasks. As
shown in Fig. 2A, either one or a set of four
colored lines is briefly presented at random
locations around an invisible circle. After a
1000-ms delay, a colored disk is presented at
fixation and the invisible circle becomes
visible. The task is to recall the location
associated with this color and click it on the
peripheral circle
'''

## Import key parts of the PsychoPy library:
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import visual, monitors, core, event, sound, data, gui
import math, random, numpy, os

# set a seed - makes everything not actually random. Randomize seed or take out to randomize order of trials
seed = 10000 # use 20000 for a separate version?
random.seed(seed)

# make sure working directory is right
os.chdir(os.path.dirname(os.path.abspath(__file__)))

## start a datafile
expInfo = {
    'Participant'   :   '---',
    'Session'       :   ['', '1', '2'],
    'TrialsToAdminister':   'all',
    'TaskFile'      :   os.path.basename(__file__)[:-3],
    'Date'          :   data.getDateStr(),
    'Seed'          :   seed
    }
# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Working Memory', 
                      fixed=['TaskFile','Date','TrialsToAdminister','TaskFile','Date','Seed'], 
                      order=['Participant','Session'])

## Check if session number is filled in with a number, quit if not
while True:
    try:
        expInfo['Session'] = int(expInfo['Session'])
        break
    except ValueError:
        print("Please enter a session number!")
        core.quit()
        
if dlg.OK:
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
        text="Loading..."
        )
    loadingScreen.setAutoDraw(True)
    loadingScreen.draw()
    mywin.flip()
    mouse = event.Mouse(visible = False, win = mywin)
     # moved clock from here to beginning of run...
else:
    core.quit()  # the user hit cancel so exit

# for getting angle differences
def diff_wrap(a, b, half=True): # half means the direction doesnt matter
    if half:
        angle = (180 - numpy.abs(numpy.abs(a - b) - 180))
    else:
        #flip the negative an positive so that right is positive
        angle = (180 - numpy.abs(numpy.abs(a - b) - 180)) * -1* numpy.sign(numpy.sin(numpy.radians(a-b)))
    return angle

# Monitor test happens in the practice

def give_instructions(): # real instruction in practice
    mywin.flip()
    instructionsText = visual.TextStim(
        win=mywin,
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
        name=None,
        autoLog=None
        )

    # real instructions in practice
    
    instructionsText.setText(
        'When you are ready, click the mouse to begin the task.'
        )
    
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
    
    
    fixation0.draw()
    mywin.flip()    
    core.wait(1)
    

def break_between_blocks(breakNum):
    mywin.flip()
    core.wait(1.0)
    
    breakScreen.setText(
        'Block ' + str(breakNum) + ' of ' + str(int(round(float(numTrialsRequested/numTrialsPerBlock)))) + '.\n\nClick the mouse button when you are ready to continue.'
        )
    
    while len(event.getKeys())==0:
        buttons = mouse.getPressed()
        if buttons[0]>0:
            mywin.flip()
            core.wait(1.0)
            break
        breakScreen.draw()
        mywin.flip()
        
    fixationB.radius = dvaArrayItemWidth*2
    fixationB.draw()
    mywin.flip()
    
    core.wait(1) # buffer

def setup_trial():

    mouse.setPos([0,0])
    trial['trialOnset'] = clock.getTime()

    acs=trial['allColors']
    aos=trial['allOrientations']
    axy=trial['allXY']

    trial['respRT']     = -0.0
    trial['respXY']     = [-0.0,-0.0]
    trial['respAngle']  = -0.0

    fixation1.setLineColor(trial['probedColor'])
    fixation1.setFillColor(trial['probedColor'])

    if trial['setSize'] >= 1:
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
        trial['unprobedAngles']=[]

    if trial['setSize'] >= 2:
        shape1.setLineColor(acs[1])
        shape1.setFillColor(acs[1])
        shape1.setOri(aos[1])
        shape1.setPos(axy[1])
        mX1,mY1=axy[1]
        if math.atan2(mY1,mX1)*180/math.pi>0:
            angle1=math.atan2(mY1,mX1)*180/math.pi
        else:
            angle1= (2*math.pi + math.atan2(mY1,mX1))*180/math.pi
        trial['unprobedAngles']=[int(angle1)]
        
        # could add triggers for other set sizes...

    if trial['setSize'] >= 3:
        shape2.setLineColor(acs[2])
        shape2.setFillColor(acs[2])
        shape2.setOri(aos[2])
        shape2.setPos(axy[2])
        mX2,mY2=axy[2]
        if math.atan2(mY2,mX2)*180/math.pi>0:
            angle2=math.atan2(mY2,mX2)*180/math.pi
        else:
            angle2=(2*math.pi + math.atan2(mY2,mX2))*180/math.pi
        trial['unprobedAngles']=[int(angle1),int(angle2)]

    if trial['setSize'] >= 4:
        shape3.setLineColor(acs[3])
        shape3.setFillColor(acs[3])
        shape3.setOri(aos[3])
        shape3.setPos(axy[3])
        mX3,mY3=axy[3]
        if math.atan2(mY3,mX3)*180/math.pi>0:
            angle3=math.atan2(mY3,mX3)*180/math.pi
        else:
            angle3=(2*math.pi + math.atan2(mY3,mX3))*180/math.pi
        trial['unprobedAngles']=[int(angle1),int(angle2),int(angle3)]

    if trial['setSize'] >= 5:
        shape4.setLineColor(acs[4])
        shape4.setFillColor(acs[4])
        shape4.setOri(aos[4])
        shape4.setPos(axy[4])
        mX4,mY4=axy[4]
        if math.atan2(mY4,mX4)*180/math.pi>0:
            angle4=math.atan2(mY4,mX4)*180/math.pi
        else:
            angle4=(2*math.pi + math.atan2(mY4,mX4))*180/math.pi
        trial['unprobedAngles']=[int(angle1),int(angle2),int(angle3),int(angle4)]
               
    if trial['setSize'] >= 6:
        shape5.setLineColor(acs[5])
        shape5.setFillColor(acs[5])
        shape5.setOri(aos[5])
        shape5.setPos(axy[5])
        mX5,mY5=axy[5]
        if math.atan2(mY5,mX5)*180/math.pi>0:
            angle5=math.atan2(mY5,mX5)*180/math.pi
        else:
            angle5=(2*math.pi + math.atan2(mY5,mX5))*180/math.pi
        trial['unprobedAngles']=[int(angle1),int(angle2),int(angle3),int(angle4),int(angle5)]

def present_ITI():
    
    for frame in range(framesBlankITI):  # blank screen
        mywin.flip()
        
    fixationB.radius = dvaArrayItemWidth*2
    fixationB.draw() # more salient fixation
    mywin.flip()
    
    for frame in range(framesFixITI-1):  # minus 1 because of flip before
        fixationB.radius -= 0.005
        fixationB.draw()
        mywin.flip()
        
    for frame in range(trial['framesITI']-framesFixITI-framesBlankITI-1): # - one for flip between 2 response codes
        fixation0.draw()
        mywin.flip()

def present_encoding_array():
    fixation0.draw()
    if trial['setSize'] >= 1:
        shape0.draw()
    if trial['setSize'] >= 2:
        shape1.draw()
    if trial['setSize'] >= 3:
        shape2.draw()
    if trial['setSize'] >= 4:
        shape3.draw()
    if trial['setSize'] >= 5:
        shape4.draw()
    if trial['setSize'] >= 6:
        shape5.draw()
       
    # Target flip
    mywin.flip()
    
    trial['trialITIDuration'] = clock.getTime()-trial['trialOnset'] #ITI Duration
    trial['trialOnsetEncoding'] = clock.getTime() # start of encoding time   
    
    for frame in range(trial['framesEncoding']-1): #target flips -1
        fixation0.draw()
        if trial['setSize'] >= 1:
            shape0.draw()
        if trial['setSize'] >= 2:
            shape1.draw()
        if trial['setSize'] >= 3:
            shape2.draw()
        if trial['setSize'] >= 4:
            shape3.draw()
        if trial['setSize'] >= 5:
            shape4.draw()
        if trial['setSize'] >= 6:
            shape5.draw()
        mywin.flip()
    
    # retention flip
    fixation0.draw()
    mywin.flip()
    trial['trialEncodingDuration'] = clock.getTime()-trial['trialOnsetEncoding'] #Encoding Duration

def present_retention_interval():
    fixation0.draw()
    mywin.flip()
    for frame in range(trial['framesRetention']-2): #minus 2
        fixation0.draw()
        mywin.flip()
    
    mouse.setPos([0,0])
    trial['trialRetentionDuration'] = clock.getTime()-trial['trialEncodingDuration']-trial['trialOnsetEncoding'] #Retention Duration

def present_response_window():
    mouse = event.Mouse(visible = False, win = mywin)
    mouse.setPos([0,0])
    fixation1.pos=mouse.getPos()
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)
    
    trial['trialOnsetRespWindow'] = clock.getTime()
    
    if event.getKeys(keyList=['escape', 'q']):
        save_data()
        mywin.close()
        core.quit()
    while trial['respRT'] == 0:
        fixation1.pos=mouse.getPos()
        innerResponseLimit.draw()
        outerResponseLimit.draw()
        stimRadius.lineColor=[-0.5,-0.5,-0.5]
        stimRadius.draw()
        fixation1.draw()
        mywin.flip()
        if event.getKeys(keyList=['escape', 'q']):
            save_data()
            mywin.close()
            core.quit()
        if mouse.isPressedIn(outerResponseLimit, buttons=[0]):
            if not mouse.isPressedIn(innerResponseLimit, buttons=[0]):
                trial['respRT']     = clock.getTime()-trial['trialOnsetRespWindow'] #reaction time                
                trial['respXY']     = mouse.getPos()
                mX,mY   =   trial['respXY']
                
                if math.atan2(mY,mX)*180/math.pi>0:
                    rA  = math.atan2(mY, mX)*180/math.pi
                else:
                    rA  = (2*math.pi + math.atan2(mY, mX))*180/math.pi
                trial['respAngle']=round(rA,1)
                break
        if clock.getTime()-trial['trialOnsetRespWindow'] >= trial['durBeforeWarning'] and trial['respLateWarning'] == False:
            warning.play(loops = 0)
            trial['respLateWarning'] = True
        event.clearEvents()
    
    # response error
        
    trial['respError'] = diff_wrap(trial['probedAngle'],trial['respAngle']) # function doing this defined above
    mywin.flip() # response code buffer, subtracted one flip from ITI

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
        fileName=expInfo['TaskFile']+"_"+expInfo['Date']+"_"+expInfo['Participant']+'_TRT_'+str(expInfo['Session'])+'.csv',
        sheetName = expInfo['Participant']+"_"+expInfo['Date'],
        stimOut=[
            'Participant',
            'TaskFile',
            'Date',
            'Session',
            'Seed',
            'durITI',
            'durEncoding',
            'durRetention',
            'durBeforeWarning',
            'durRespWindow',
            'trialIndex',
            'trialNumber',
            'trialWithinBlock',
            'blockNumber',
            'setSize',
            'probedColor',
            'probedLocation',
            'unprobedColors',
            'unprobedLocations',
            'trialOnset',
            'trialITIDuration',
            'trialOnsetEncoding',
            'trialEncodingDuration',
            'trialRetentionDuration',
            'trialOnsetRespWindow',
            'respLateWarning',
            'respRT',
            'respXY',
            'probedXY',
            'unprobedXY',
            'respAngle',
            'respError',
            'probedAngle',
            'unprobedAngles'
            ]
        )


## timing constants
durITI              =   1 # changed from 1.5 - now 1 with 50ms jitter
durBlankITI         =   .25 # blank ITI without fixation
durFixITI           =   .5  # will be subtracted from durITI as bigger fixation
durEncoding         =   0.5  # array duration
durRetention        =   1.0     
durBeforeWarning    =   3.0 #beep if no response after given duration
durRespWindow       =   -1.0 #open-ended response window

frameRate           =   mywin.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)
framesITI           =   int(round(durITI/frameRate[0]*1000))
framesBlankITI      =   int(round(durBlankITI/frameRate[0]*1000))
framesFixITI        =   int(round(durFixITI/frameRate[0]*1000))
framesEncoding      =   int(round(durEncoding/frameRate[0]*1000))
framesRetention     =   int(round(durRetention/frameRate[0]*1000))
framesBeforeWarning =   int(round(durBeforeWarning/frameRate[0]*1000))

## Stimulus dimensions
dvaArrayRadius = 3.5
dvaArrayItemLength = 1
dvaArrayItemWidth = 0.1

## Array values
setSizes            =[1,5]
numTrialsPerSetSize =200
numTrialsPerBlock   =40
sortedTrials        =list(range(0,numTrialsPerSetSize*len(setSizes)))
randomizedTrials    =list(range(0,numTrialsPerSetSize*len(setSizes)))
random.shuffle(randomizedTrials)
numStimulusLocations=100 # changed to 100 from 90
locations           =list(range(0,numStimulusLocations))
colors              =['#000000', '#1e00b4', '#00aaff', '#ffffff', '#00ff00'] #black/darkblue/cyan/white/lightgreen
itemSeparation      = 360/numStimulusLocations #degrees arc (changed from hardcoded 4 deg)
angles              = []
angle_XYs           = []
for x in range(0,numStimulusLocations):
    angles.append(x*itemSeparation+1)
    angle_X=math.cos((x*itemSeparation+1)*math.pi/180)*dvaArrayRadius
    angle_Y=-math.sin((x*itemSeparation+1)*math.pi/180)*dvaArrayRadius
    angle_XYs.append([angle_X, angle_Y])

# looks like 0 degrees (and location 0) is on the right most end of the circle (3 oclock)
# 90 degrees (location 25 if there are 100) is on the bottom (6 oclock) and so on around the circle...

## define parameters for each trial of each trial type
tList=[]
for x in list(range(0,numTrialsPerSetSize*len(setSizes))):
    ss  =   setSizes[math.trunc(randomizedTrials[x]/numTrialsPerSetSize)]  #set size
    pl  =   [randomizedTrials[x]%numStimulusLocations]                       #probed location
    pc  =   colors[randomizedTrials[x]%len(colors)]                        #probed color
    if ss == 1:
        ul  = []
        uc  = []
    else:
        temp = list(range(0,len(locations))) # added list
        temp.remove(pl[0])
        ul  =   random.sample(temp,ss-1)                    #unprobed locations
        tempc = list(colors)
        tempc.remove(pc)
        uc = random.sample(tempc,ss-1) #unprobed colors
    alll=   pl + ul
    
    random.shuffle(uc) # added shuffle here
    allc=   [pc] + uc
    
    # jitter ITI
    tITI = durITI + (random.randrange(-50,50,1))*0.001 # 1000 ms with a 50ms jitter
    tList.append({
        'Participant'       :   expInfo['Participant'],
        'Session'           :   expInfo['Session'],
        'TaskFile'          :   expInfo['TaskFile'],
        'Date'              :   expInfo['Date'],
        'Seed'              :   expInfo['Seed'],
        'trialNumber'       :   sortedTrials[x],
        'trialIndex'        :   randomizedTrials[x],
        'trialWithinBlock'  :   sortedTrials[x]%numTrialsPerBlock,
        'trialOnset'        :   0, #not yet set
        'trialITIDuration'     :   0,
        'trialOnsetEncoding':   0,
        'trialEncodingDuration':    0,
        'trialRetentionDuration':  0,
        'trialOnsetRespWindow': 0,
        'blockNumber'       :   math.trunc(sortedTrials[x]/numTrialsPerBlock),
        'setSize'           :   ss,
        'probedLocation'    :   pl,
        'probedColor'       :   pc,
        'unprobedLocations' :   ul,
        'unprobedColors'    :   uc,
        'allLocations'      :   alll,
        'allColors'         :   allc,
        'allOrientations'   :   [i * itemSeparation+1 for i in alll],
        'probedXY'          :   angle_XYs[randomizedTrials[x]%numStimulusLocations],
        'unprobedXY'        :   [angle_XYs[i] for i in ul],
        'allXY'             :   [angle_XYs[i] for i in alll],
        'durITI'            :   tITI,
        'durEncoding'       :   durEncoding,
        'durRetention'      :   durRetention,
        'durBeforeWarning'  :   durBeforeWarning,
        'durRespWindow'     :   durRespWindow,
        'framesITI'         :   int(round(tITI/frameRate[0]*1000)),
        'framesEncoding'    :   framesEncoding,
        'framesRetention'   :   framesRetention,
        'framesBeforeWarning':  framesBeforeWarning,
        'respLateWarning'   :   False,
        'respRT'           :   0.0,
        'respXY'           :   [[0,0],[0,0]],
        'respAngle'         :   0,
        'respError'         :   -1, # unresponse
        'probedAngle'       :   0,
        'unprobedAngles'    :   []
        })

## define trial stimuli
breakScreen = visual.TextStim(
    win=mywin,
    text='Take a break.\n\n'
    'Press to continue.'
    )
stimRadius = visual.Circle(
    win=mywin,
    units='deg',
    edges=90,
    lineColor=[0,0,0],
    radius=dvaArrayRadius,
    pos=(0, 0)
    )
innerResponseLimit = visual.Circle(
    win=mywin,
    units='deg',
    lineColor=[0,0,0],
    radius=dvaArrayRadius-dvaArrayItemWidth*2,
    pos=(0, 0)
    )
outerResponseLimit = visual.Circle(
    win=mywin,
    units='deg',
    lineColor=[0,0,0],
    radius=dvaArrayRadius+dvaArrayItemWidth*2,
    pos=(0, 0)
    )
fixation0 = visual.Circle(
    win=mywin,
    autoLog=True,
    units='deg',
    radius=dvaArrayItemWidth/2,
    lineColor=[-.5,-.5,-.5],
    fillColor=[0,0,0],
    pos=(0, 0)
    )
fixation1 = visual.Circle(
    win=mywin,
    autoLog=True,
    units='deg',
    radius=dvaArrayItemWidth,
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
vtx=(
    (-dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (dvaArrayItemLength/2, dvaArrayItemWidth/2),
    (-dvaArrayItemLength/2, dvaArrayItemWidth/2)
    )
shape0 = visual.ShapeStim(
    win=mywin,
    autoLog=True,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape1 = visual.ShapeStim(
    win=mywin,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape2 = visual.ShapeStim(
    win=mywin,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape3 = visual.ShapeStim(
    win=mywin,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape4 = visual.ShapeStim(
    win=mywin,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )
shape5 = visual.ShapeStim(
    win=mywin,
    units='deg',
    lineWidth=1,
    vertices=vtx,
    closeShape=True
    )

if expInfo['TrialsToAdminister']=='all':
    numTrialsRequested = len(tList)
else:
    numTrialsRequested = expInfo['TrialsToAdminister']
trials = data.TrialHandler(
    trialList=tList[0:int(numTrialsRequested)],
    nReps=1,
    method='sequential',
    dataTypes=[],
    seed=expInfo['Seed']
    )

loadingScreen.setAutoDraw(False)

clock = core.Clock() #initialize clock that will be reset in give_instructions
breakNum = 0
# Monitor test now defaults to not happen since it happens in the practice

give_instructions()

mouse = event.Mouse(visible = False, win = mywin)

# actual experiment
for trial in trials:
    if trial['trialNumber']%numTrialsPerBlock == 0 and trial['trialNumber'] != 0:
        breakNum += 1
        break_between_blocks(breakNum)
    setup_trial()
    present_ITI()
    present_encoding_array()
    present_retention_interval()
    present_response_window()

save_data()
give_thanks()

# Finishing touches
mywin.close()
core.quit()
