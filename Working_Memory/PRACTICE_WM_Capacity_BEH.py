
# P R A C T I C E #

# currently set to 15 random trials #


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
import math, random, numpy, os, glob

# set a seed - makes everything not actually random. Randomize seed or take out to randomize order of trials
seed = 100 # use different seed for practice than real run - otherwise will be the same first 15 trials
random.seed(seed)

# make sure working directory is right
os.chdir(os.path.dirname(os.path.abspath(__file__)))

## start a datafile
expInfo = {
    'Participant'   :   'PRACTICE',
    'Session'       :   'Practice',
    'TrialsToAdminister':   '15',
    'MonitorTest?'      :   ['Yes','No'], #default to test colors
    'TaskFile'      :   os.path.basename(__file__)[:-3],
    'Date'          :   data.getDateStr(),
    'Seed'          :   core.getAbsTime()
    }
# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='LocateColor', 
fixed=['TaskFile','Session','Date','TrialsToAdminister','TaskFile','Date','Seed'], 
order=['Participant','MonitorTest?'])
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
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)
else:
    core.quit()  # the user hit cancel so exit

def test_monitor_colors():
    mouse = event.Mouse(visible = False, win = mywin)
    ## test participant's ability to click on item of each color
    testColors=colors[:]
    random.shuffle(testColors)
    testText = visual.TextStim(
        win=mywin,
        font='Arial',
        pos=(0.0, -5.5),
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
    fixation1.setAutoDraw(True)
    shape0.setLineColor(testColors[0])
    shape1.setLineColor(testColors[1])
    shape2.setLineColor(testColors[2])
    shape3.setLineColor(testColors[3])
    shape4.setLineColor(testColors[4])
    #shape5.setLineColor(testColors[5])
    shape0.setFillColor(testColors[0])
    shape1.setFillColor(testColors[1])
    shape2.setFillColor(testColors[2])
    shape3.setFillColor(testColors[3])
    shape4.setFillColor(testColors[4])
    #shape5.setFillColor(testColors[5])
    shape0.setOri(36 * 4+1) # 4 is old itemSeparation for 90 locations
    shape1.setOri(54 * 4+1)
    shape2.setOri(72 * 4+1)
    shape3.setOri(0 * 4+1)
    shape4.setOri(18 * 4+1)
    #shape5.setOri(30 * 4+1)
    shape0.setPos(angle_XYs[40]) # hard coded for now
    shape1.setPos(angle_XYs[60])
    shape2.setPos(angle_XYs[80])
    shape3.setPos(angle_XYs[0])
    shape4.setPos(angle_XYs[20])
    #shape5.setPos(angle_XYs[34])
    shape0.setAutoDraw(True)
    shape1.setAutoDraw(True)
    shape2.setAutoDraw(True)
    shape3.setAutoDraw(True)
    shape4.setAutoDraw(True)
    #shape5.setAutoDraw(True)
    testText.setText('Click the bar whose color matches your cursor.')
    testText.setAutoDraw(True)
    shape0.draw()
    shape1.draw()
    shape2.draw()
    shape3.draw()
    shape4.draw()
    #shape5.draw()
    testText.draw()
    countErrors=0
    correctClicks=0
    
    for i in testColors:
        fixation1.setFillColor(i)
        fixation1.setLineColor(i)
        mouse.setPos([0,0])
        warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)
        mywin.flip()
        buttons = mouse.getPressed()
        buttons[0]=0
        while correctClicks<len(testColors):
            fixation1.pos=mouse.getPos()
            mywin.flip()
            buttons = mouse.getPressed()
            if buttons[0]>0:
                if i==testColors[0]:
                    if fixation1.overlaps(shape0):
                        core.wait(0.1)
                        correctClicks+=1
                        mouse.setPos([0,0])
                        break
                    else:
                        core.wait(0.1)
                        countErrors+=1
                        warning.play(loops=0)
                elif i==testColors[1]:
                    if fixation1.overlaps(shape1):
                        core.wait(0.1)
                        correctClicks+=1
                        mouse.setPos([0,0])
                        break
                    else:
                        core.wait(0.1)
                        countErrors+=1
                        warning.play(loops=0)
                elif i==testColors[2]:
                    if fixation1.overlaps(shape2):
                        core.wait(0.1)
                        correctClicks+=1
                        mouse.setPos([0,0])
                        break
                    else:
                        core.wait(0.1)
                        countErrors+=1
                        warning.play(loops=0)
                elif i==testColors[3]:
                    if fixation1.overlaps(shape3):
                        core.wait(0.1)
                        correctClicks+=1
                        mouse.setPos([0,0])
                        break
                    else:
                        core.wait(0.1)
                        countErrors+=1
                        warning.play(loops=0)
                elif i==testColors[4]:
                    if fixation1.overlaps(shape4):
                        core.wait(0.1)
                        correctClicks+=1
                        mouse.setPos([0,0])
                        break
                    else:
                        core.wait(0.1)
                        countErrors+=1
                        warning.play(loops=0)
                #elif i==testColors[5]:
                #    if fixation1.overlaps(shape5):
                #        core.wait(0.1)
                #        correctClicks+=1
                #        mouse.setPos([0,0])
                #        break
                #    else:
                #        core.wait(0.1)
                #        countErrors+=1
                #        warning.play(loops=0)
            elif len(event.getKeys())>0:
                break
    fixation1.setAutoDraw(False)
    shape0.setAutoDraw(False)
    shape1.setAutoDraw(False)
    shape2.setAutoDraw(False)
    shape3.setAutoDraw(False)
    shape4.setAutoDraw(False)
    #shape5.setAutoDraw(False)
    testText.setAutoDraw(False)
    mywin.flip()
    ##kill task if too many errors
    if countErrors>4:
        core.wait(1.0)
        testText.setText('You made a number of misclicks. Perhaps your monitor needs to be recalibrated?\n\nThe task will quit now, but you are welcome to try again.')
        testText.setAutoDraw(True)
        mywin.flip()
        core.wait(2) # changed from a click to continue
        core.quit()
    else:
        mywin.flip()
        core.wait(1)

def give_instructions():
    mywin.flip()
    
    instructionDir= 'InstructionSlides' #folder/directory the images are in,
    instructionFiles = []
    instructionFiles = sorted(glob.glob(os.path.join(instructionDir, '*.png')))  # where the image files get loaded
        
    for instr in list(range(0,len(instructionFiles))):
        instrImage = visual.ImageStim(win=mywin, image=instructionFiles[instr])
        
        instrImage.draw()
        mywin.flip()
        
        mouse.setPos([0,-.60]) # adjusted to match instruction slide
        
        click = mouse.getPressed()
        while click[0] == 0:
            instrImage.draw()
            fixation0.pos=mouse.getPos()
            fixation0.draw()
            
            if instr in [2,3]:
                fixation1.setFillColor('#ffffff') #white
                fixation1.setLineColor('#ffffff')
                fixation1.pos = mouse.getPos()
                fixation1.draw()
            
            if instr in [5,6]:
                fixation1.setFillColor('#00ff00') #green
                fixation1.setLineColor('#00ff00')
                fixation1.pos = mouse.getPos()
                fixation1.draw()
            
            if event.getKeys(keyList=['escape', 'q']):
                mywin.close()
                core.quit()
            
            mywin.flip()
            
            click = mouse.getPressed()
        
        core.wait(.20)
        event.clearEvents()
    
    mouse.setPos([0,0])
    fixation0.pos=mouse.getPos()
    mywin.flip()

def break_between_blocks():
    mywin.flip()
    core.wait(1.0)
    while len(event.getKeys())==0:
        buttons = mouse.getPressed()
        if buttons[0]>0:
            mywin.flip()
            core.wait(1.0)
            break
        breakScreen.draw()
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
        
    mywin.flip()
    trial['trialOnsetEncoding'] = clock.getTime()-trial['trialOnset'] #time stamp start of encoding
    for frame in range(trial['framesEncoding']-1):
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

def present_retention_interval():
    fixation0.draw()
    mywin.flip()
    trial['trialOnsetRetention'] = clock.getTime()-trial['trialOnset'] #time stamp start of retention
    for frame in range(trial['framesRetention']-1):
        fixation0.draw()
        mywin.flip()

def present_response_window():
    mouse = event.Mouse(visible = False, win = mywin)
    mouse.setPos([0,0])
    warning = sound.Sound('A', octave=3, sampleRate=44100, secs=0.2, stereo=True, volume=0.8)
    
    trial['trialOnsetRespWindow'] = clock.getTime()-trial['trialOnset']
    
    if event.getKeys(keyList=['escape', 'q']):
        mywin.close()
        core.quit()
    while trial['respRT'] == 0:
        innerResponseLimit.draw()
        outerResponseLimit.draw()
        stimRadius.lineColor=[-0.5,-0.5,-0.5]
        stimRadius.draw()
        fixation1.pos=mouse.getPos()
        fixation1.draw()
        mywin.flip()
        if event.getKeys(keyList=['escape', 'q']):
            mywin.close()
            core.quit()
        if mouse.isPressedIn(outerResponseLimit, buttons=[0]):
            if not mouse.isPressedIn(innerResponseLimit, buttons=[0]):
                trial['respRT']     = clock.getTime()-trial['trialOnset']-trial['trialOnsetRespWindow'] #reaction time                
                trial['respXY']     = mouse.getPos()
                mX,mY   =   trial['respXY']
                
                if math.atan2(mY,mX)*180/math.pi>0:
                    rA  = math.atan2(mY, mX)*180/math.pi
                else:
                    rA  = (2*math.pi + math.atan2(mY, mX))*180/math.pi
                trial['respAngle']=round(rA,1)
                break
        if clock.getTime()-trial['trialOnset']-trial['trialOnsetRespWindow'] >= trial['durBeforeWarning'] and trial['respLateWarning'] == False:
            warning.play(loops = 0)
            trial['respLateWarning'] = True
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
            mywin.close()
            core.quit()
        buttons = mouse.getPressed()
        if buttons [0] > 0:
            thanksText.setAutoDraw(False)
            break

## timing constants
durITI              =   1 # changed from 1.5 - now 1 with 50ms jitter
durBlankITI         =   .25 # blank ITI without fixation
durFixITI           =   .5  # will be subtracted from durITI as bigger fixation
durEncoding         =   0.5
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
        'trialOnsetITI'     :   0,
        'trialOnsetEncoding':   0,
        'trialOnsetRetention':  0,
        'trialOnsetRespWindow': 0,
        'trialOnsetTrigger': 0,
        'trialRespTrigger': 0,
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
        'probedAngle'       :   0,
        'unprobedAngles'    :   []
        })

## define trial stimuli
breakScreen = visual.TextStim(
    win=mywin,
    text="New block!"
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

# Monitor test defaults to happen 
if expInfo['MonitorTest?']=='Yes':
    test_monitor_colors()
else:
    pass
    
give_instructions()
mouse = event.Mouse(visible = False, win = mywin)
clock = core.Clock() #start clock

for trial in trials:
    if trial['trialNumber']%numTrialsPerBlock == 0 and trial['trialNumber'] != 0:
        break_between_blocks()
    setup_trial()
    present_ITI()
    present_encoding_array()
    present_retention_interval()
    present_response_window()

# Finishing touches
give_thanks()
mywin.close()
core.quit()
