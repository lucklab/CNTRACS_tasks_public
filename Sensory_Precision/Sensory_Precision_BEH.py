'''
Sensory Precision

This task for assesses the sensory precision of the same spatial information used in the WM and EM tasks.

Two lines are presented on each trial, abutting each other near the same invisible circle that defines the stimulus locations for the WM and EM tasks.

Participants report whether the outer line is to the left or right of the inner line.

The amount of physical left-right displacement is varied across trials using a highly efficient QUEST staircase procedure,
which produces a Bayesian estimate of the amount of offset needed to achieve 82% correct (the sensory threshold, in angular degrees).

Catch trials are included so that we can measure the rate of attention lapses
and estimate the sensory threshold without contamination from lapses.

Note on trial number:
It is currently set to run 400 trials, 20% of which are "catch trials"
If one does not need to get a precise measure of the lapse rate, 
fewer trials are likely sufficient to measure the sensory threshold (e.g. 200 total trials)
This can be set in the "TrialsToAdminister" field of "sessionInfo"

Note on QUEST staircase parameters:
These are currently set to be able to measure a wide range of possible thresholds (.1 degrees through 5.1 degrees of angular separation),
but to further optimize the efficiency of the staircase, one could center the prior on a more precise value, based on pilot data.
(e.g. healthy young adults will likely have thresholds below 2.6, which is the current mean of the prior.)
Note that if you change the QUEST parameters, you should manually set the min/max value of the staircase to make sure it can sample all the intended values
    (currently this script will not measure a threshold above 5.1 degrees, to keep it separate from the catch trials which are set at 6 degrees)
'''

## Import modules
from psychopy import visual, monitors, core, event, data, gui
import math, random, numpy, os

# Set seed for randomization.
# In this task, no consistent seed was used by CNTRACS (unlike in the WM and EM tasks)
seed = int(random.uniform(1, 1000000))

# make sure working directory is right (currently set to where the script is located)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

## start a datafile
sessionInfo = {
    'Participant'           :   '---',
    'TrialsToAdminister'    :   'all', # currently set as 400
    'CatchTrialPercentage'  :   20, # if this is changed, the "catchTrials" varible needs to be changed accordingly
    'windowFullScreen'      : True,
    'Date'          :   data.getDateStr(),
    'Seed'          :   seed
    }
    
# present a dialogue to change params
dlg = gui.DlgFromDict(
    sessionInfo,
    title='Sensory Precision',
    fixed=['TaskFile','Date','Seed','TrialsToAdminister','CatchTrialPercentage','windowFullScreen'],
    order=['Participant']
    )

if dlg.OK:
 
    ## Define a monitor
    my_monitor = monitors.Monitor(name='ERP1_stim') 
    my_monitor.setSizePix((1920,1200))
    my_monitor.setWidth(52)
    my_monitor.setDistance(100)
    my_monitor.saveMon()
    ## Create a visual window:
    mywin = visual.Window(
        monitor='ERP1_stim', #name must match above
        autoLog=False,
        units='deg',
        screen=0, #screen=0 for primary monitor, screen=1 to display on secondary monitor
        fullscr=sessionInfo['windowFullScreen'] #True to take the full screen
        )
    loadingScreen = visual.TextStim(
        win=mywin,
        autoLog=False,
        text="Loading..."
        )
    loadingScreen.setAutoDraw(True)
    loadingScreen.draw()
    frameRate = mywin.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)
    mywin.flip()
    mouse = event.Mouse(visible = False, win = mywin)
else:
    core.quit()  # the user hit cancel so exit

if sessionInfo['TrialsToAdminister']=='all':
    numTrialsRequested = 400 # could potentially be lowered
else:
    numTrialsRequested = int(sessionInfo['TrialsToAdminister'])

expInfo = {
    'TaskFile'      :   os.path.basename(__file__)[:-3],
    'Date'          :   sessionInfo['Date'],
    'Seed'          :   sessionInfo['Seed'],
    'stimDuration'  :   0.1, # in seconds
    'stimLength'    :   0.5, # in degrees
    'stimWidth'     :   0.1,
    'stimOffsetFromScreenCenter'                        :   3.5, # radius of circle bars on
    'questInitialThresholdEstimateDegreesRadialAngle'   :   2.6, # starting place of staircase, mean of prior (could be set to match)
    'questInitialThresholdSD'                           :   5.0, # SD of prior^ (a wide prior is preferable here, but could be set more narrow - if so, set the range parameter)
    'questCatchTrialRadialAngle'                        :   6.0, # The spacing for catch trials
    'questAccuracyAtThreshold'                          :   0.82, #"pThreshold" (percent accuracy threshold being estimated)
    'questNumberOfTrials'                               :   numTrialsRequested-(sessionInfo['CatchTrialPercentage']/100*numTrialsRequested),
    'questMethod'                                       :   'quantile', #The method used to determine the next threshold to test. If you want to get a specific threshold level at the end of your staircasing, please use the quantile, mean, and mode methods directly.
    'questSteepness'                                    :   3.5,  #"beta" Controls the steepness of the psychometric function.
    'questLapseRate'                                    :   0.01, #"delta" The fraction of trials on which the observer presses blindly.
    'questResponseBias'                                 :   0.5,  #"gamma" The fraction of trials that will generate response 1 when intensity=-Inf.
    'questGrain'                                        :   0.01, #The quantization of the internal table.
    # these are unused, but kept here to let people know they could set these parameters in the staircase
    'questPercentConfidenceRequired'                    :   None, #The minimum 5-95% confidence interval required in the threshold estimate before stopping. If both this and nTrials is specified, whichever happens first will determine when Quest will stop.
    'questRange'                                        :   None, #The intensity difference between the largest and smallest intensity that the internal table can store. This interval will be centered on the initial guess tGuess. QUEST assumes that intensities outside of this range have zero prior probability (i.e., they are impossible).
    'questExtraInfo'                                    :   None, #A dictionary (typically) that will be stored along with collected data using saveAsPickle() or saveAsText() methods.
    'questMinVal'                                       :   0, #The smallest legal value for the staircase, which can be used to prevent it reaching impossible contrast values, for instance.
    'questMaxVal'                                       :   None, #The largest legal value for the staircase, which can be used to prevent it reaching impossible contrast values, for instance.
    'questStaircase'                                    :   None, #Can supply a staircase object with intensities and results. Might be useful to give the quest algorithm more information if you have it. You can also call the importData function directly.
    'questName'                                         :   ''
    }


## Stimulus parameters
stimDuration        =   expInfo['stimDuration'] #seconds
stimPresentaionFlips=   int(round(stimDuration/frameRate[0]*1000))

stimITI = 1 #seconds ITI - gets jittered 50ms
framesStimITI        =   int(round(stimITI/frameRate[0]*1000)) # base iti

durFixITI           =   .5  # will be subtracted from stimITI as bigger fixation
framesFixITI        =   int(round(durFixITI/frameRate[0]*1000))

dvaArrayRadius      =   expInfo['stimOffsetFromScreenCenter']
dvaArrayOuterRadius =   dvaArrayRadius+0.26
dvaArrayInnerRadius =   dvaArrayRadius-0.26
dvaArrayItemLength  =   expInfo['stimLength']
dvaArrayItemWidth   =   expInfo['stimWidth']

angleRange = 40 #range in degrees from center that presentation can be

# Make array of catchTrials (will be shuffled after first iteration)
# currently 1 in 5 trials is a catch trial
# 1st trial is easy catch trial
catchTrials=[1,0,0,0,0,0,0,0,0,1] # for 20%

## Make array of when breaks are (100 means there would be 3 breaks)
breakInverval = 100 # number of trials before break, must divide into total number of trials

breakArray = numpy.linspace(breakInverval, numTrialsRequested-breakInverval, int((numTrialsRequested-breakInverval)/breakInverval))
breakArray = [ int(x) for x in breakArray ]

## Define functions

def give_break():

    fixation0.setAutoDraw(False)
    mywin.flip()
    breakText.setAutoDraw(True)

    breakText.draw()

    mywin.flip()
    
    while len(event.waitKeys())==0:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            if thisKey == 'left' or thisKey == 'right':
                event.clearEvents()
                break
                
            elif thisKey in ['escape','q']:
                mywin.close()
                core.quit()
    
    breakText.setAutoDraw(False)
    
    mywin.flip()
    core.wait(1)
    
    fixationB.radius = dvaArrayItemWidth*2
    
    for frame in range(framesFixITI):  # minus 1 because of flip before
        fixationB.radius -= 0.005
        fixationB.draw()
        mywin.flip()
    
    for frame in range(framesStimITI-framesFixITI):
        fixation0.draw()
        mywin.flip()
    
    fixation0.setAutoDraw(True)

def save_data():
    savingScreen = visual.TextStim(
        win=mywin,
        autoLog=False,
        text="Saving to file..."
        )
    savingScreen.setAutoDraw(True)
    savingScreen.draw()
    mywin.flip()
    ## create the datafile
    trials.saveAsExcel(
        fileName=expInfo['TaskFile']+"_"+expInfo['Date']+"_"+sessionInfo['Participant']+'.csv',
        sheetName = sessionInfo['Participant']+"_"+expInfo['Date'],
        stimOut=[
            'Participant',
            'TaskFile',
            'Date',
            'Seed',
            'questInitialThresholdEstimateDegreesRadialAngle',
            'questInitialThresholdSD', 
            'questAccuracyAtThreshold',
            'questNumberOfTrials',
            'questSteepness',
            'questResponseBias',
            'questGrain',
            'questRange',
            'questLapseRate',
            'trialNumber',
            'trialOnset',
            'trialDuration',
            'trialOnsetITI',
            'catchTrial',
            'questRecommendedSeparation',
            'probedSeparation',
            'currentThresholdEst',
            'respRT',
            'respACC'
        ]
    )

## Make trial list
tList=[]
for x in list(range(0,numTrialsRequested)):
    tList.append({
        'Participant'       :   sessionInfo['Participant'],
        'TaskFile'          :   expInfo['TaskFile'],
        'Date'              :   expInfo['Date'],
        'Seed'              :   expInfo['Seed'],
        'cmFromSubjToScreen':   100,
        'questInitialThresholdEstimateDegreesRadialAngle'   :   expInfo['questInitialThresholdEstimateDegreesRadialAngle'],
        'questInitialThresholdSD'                           :   expInfo['questInitialThresholdSD'], 
        'questAccuracyAtThreshold'                          :   expInfo['questAccuracyAtThreshold'],
        'questNumberOfTrials'                               :   expInfo['questNumberOfTrials'],
        'questSteepness'                                    :   expInfo['questSteepness'],
        'questResponseBias'                                 :   expInfo['questResponseBias'],
        'questGrain'                                        :   expInfo['questGrain'],
        'questRange'                                        :   expInfo['questRange'],
        'questLapseRate'                                    :   expInfo['questLapseRate'],
        'trialNumber'       :   x,
        'trialOnset'        :   0, # these not yet set
        'trialDuration'     :   0,
        'trialOnsetITI'     :   0,
        'catchTrial'        :   0, # 1 = yes
        'questRecommendedSeparation' : 0.0, # threshold estimate, before trial
        'probedSeparation'  :   0.0, # should match ^ unless catch trial
        'currentThresholdEst':  0.0, # new threshold estimate, after trial
        'respRT'            :   0.0,
        'respACC'           :   0
        })

trials = data.TrialHandler(
    trialList=tList[0:int(numTrialsRequested)],
    nReps=1,
    method='sequential',
    dataTypes=[]
    )

quest = data.QuestHandler(
    startVal    =   expInfo['questInitialThresholdEstimateDegreesRadialAngle'],
    startValSd  =   expInfo['questInitialThresholdSD'], 
    pThreshold  =   expInfo['questAccuracyAtThreshold'],
    nTrials     =   expInfo['questNumberOfTrials'],
    beta        =   expInfo['questSteepness'],
    delta       =   expInfo['questLapseRate'],
    gamma       =   expInfo['questResponseBias'],
    grain       =   expInfo['questGrain'],
    range       =   expInfo['questRange'],
    autoLog     =   True
    )

## Create stimuli
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
fixationB = visual.Circle(
    win=mywin,
    autoLog=False,
    units='deg',
    radius=dvaArrayItemWidth*2,
    lineColor=[-.5,-.5,-.5],
    fillColor=[-.5,-.5,-.5],
    pos=(0, 0)
    )

gapMultiplier = 0.8
# corners of bars
vtx=(
    (gapMultiplier*-dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (gapMultiplier*dvaArrayItemLength/2, -dvaArrayItemWidth/2),
    (gapMultiplier*dvaArrayItemLength/2, dvaArrayItemWidth/2),
    (gapMultiplier*-dvaArrayItemLength/2, dvaArrayItemWidth/2)
    )
shapeOuter = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    lineColor='white',
    fillColor='white',
    vertices=vtx,
    autoDraw=False,
    closeShape=True
    )
shapeInner = visual.ShapeStim(
    win=mywin,
    autoLog=False,
    units='deg',
    lineWidth=1,
    lineColor='black',
    fillColor='black',
    vertices=vtx,
    autoDraw=False,
    closeShape=True
    )

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
        antialias=True
        )

breakText.setText(
    'Take a break.\n\n'
    'When you are ready, press either the left or right arrow buttons to continue.'
    )

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
    antialias=True
    )

instructionsText.setText(
    'When you are ready, press either the left or right arrow buttons to begin the task.'
    )

## Start instructions (real instructions in practice)
loadingScreen.setAutoDraw(False)

instructionsText.draw()

mywin.flip()
clock = core.Clock() #start global clock

allKeys = event.waitKeys(keyList=['escape','left','right'])
for thisKey in allKeys:
    if thisKey in ['escape']:
        mywin.close()
        core.quit()
    elif thisKey in ['left','right']:
        event.clearEvents()

mywin.flip()
instructionsText.setAutoDraw(False)

## Start experiment

catchTrialTracker = 0
catchTrialAccuracy = 0.0
strCatch = ''
correctRespTracker = 0
incorrectRespTracker = 0

fixationB.draw()
mywin.flip()

for frame in range(framesFixITI):  # minus 1 because of flip before
    fixationB.radius -= 0.005
    fixationB.draw()
    mywin.flip()
    
for frame in range(framesStimITI-framesFixITI):
    fixation0.draw()
    mywin.flip()

fixation0.setAutoDraw(True)

# Trial loop
for nTrial in trials:
    
    # check if time for break
    if nTrial['trialNumber'] in breakArray:
        give_break()
    else:
        pass
    
    #check for catch trial
    if catchTrials[nTrial['trialNumber']%len(catchTrials)] == 1:
        separationToTest = expInfo['questCatchTrialRadialAngle']
        catchTrialTracker += 1
        strCatch = 'catch trial'
        nTrial['catchTrial'] = 1
    
    # real trial
    else:
        strCatch = ''
        separationToTest = quest.quantile()
    
    nTrial['questRecommendedSeparation']    =   quest.quantile()
    nTrial['probedSeparation']  =   separationToTest
    
    #assign random stim location
    innerStimAngle = random.randint(0,angleRange) #outer radius stimulus angle will be offset from here
    stimVertical = random.choice([1, -1]) #whether the stimulus is above or below screen center
    
    # Get angles of the two bars
    if innerStimAngle - separationToTest < 0:
        outerStimAngle = innerStimAngle + separationToTest
    elif innerStimAngle + separationToTest > angleRange:
        outerStimAngle = innerStimAngle - separationToTest
    else:
        stimOffset = random.choice([1, -1])
        outerStimAngle = innerStimAngle + (stimOffset * separationToTest)
    
    if stimVertical == -1:
        #stim on bottom
        '''bottom angles from 225:315 on a unit circle, in steps of 0.25'''
        '''but for bottom range we will add only 45 degrees to each tic in the for loop'''
        angleAdjust=90-angleRange/2
        
        if innerStimAngle<outerStimAngle:
            correctResp='left'
            incorrectResp='right'
        else:
            correctResp='right'
            incorrectResp='left'
    else:
        #stim on top
        '''top angles from 45:135 on a unit circle, in steps of 0.25'''
        '''but becuase python circle starts at zero, then wraps clockwise...'''
        '''for the top range we will add 225 degrees to each tic in this for loop'''
        angleAdjust=270-angleRange/2
        
        if innerStimAngle<outerStimAngle:
            correctResp='right'
            incorrectResp='left'
        else:
            correctResp='left'
            incorrectResp='right'
    
    # set positions, orientations for the two bars
    innerStimAngle  =   innerStimAngle+angleAdjust
    xInner          =    math.cos(innerStimAngle*math.pi/180)
    yInner          =   -math.sin(innerStimAngle*math.pi/180)
    innerXY         =   [xInner*dvaArrayInnerRadius,yInner*dvaArrayInnerRadius]
    shapeInner.ori  =   innerStimAngle
    shapeInner.pos  =   innerXY
    
    outerStimAngle  =   outerStimAngle+angleAdjust
    xOuter          =    math.cos(outerStimAngle*math.pi/180)
    yOuter          =   -math.sin(outerStimAngle*math.pi/180)
    outerXY         =   [xOuter*dvaArrayOuterRadius,yOuter*dvaArrayOuterRadius]
    shapeOuter.ori  =   outerStimAngle
    shapeOuter.pos  =   outerXY
    
    # TARGET FLIP
    shapeInner.draw()
    shapeOuter.draw()
    mywin.flip()
    
    nTrial['trialOnset']    = clock.getTime() # trial onset
    
    for flip in range(0,stimPresentaionFlips-1): #minus one for flip above
        shapeInner.draw()
        shapeOuter.draw()
        mywin.flip()
    
    # ITI FLIP
    mywin.flip()
    nTrial['trialDuration'] = clock.getTime() - nTrial['trialOnset']# get stimulus duration (time minus onset time)
        
    ## response
    thisResp = None
    while thisResp == None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            
            if thisKey == correctResp:
                nTrial['respRT']    =   clock.getTime()-nTrial['trialOnset']
                thisResp=1
                strResp = 'responded correctly'
                if catchTrials[nTrial['trialNumber']%len(catchTrials)] != 1:
                    correctRespTracker += 1
                else:
                    catchTrialAccuracy += 1
                            
            elif thisKey == incorrectResp:
                nTrial['respRT']    =   clock.getTime()-nTrial['trialOnset']
                thisResp=0
                strResp = 'responded incorrectly'
                correctRespTracker = 0
                incorrectRespTracker = 1
                            
            elif thisKey in ['escape','q']:
                save_data()
                mywin.close()
                core.quit()
        event.clearEvents()
    
    nTrial['respACC']   =   thisResp
    nTrial['trialOnsetITI'] =   clock.getTime()
    
    if catchTrialTracker >= 10:
        quest.setDelta          =   1-catchTrialAccuracy/catchTrialTracker
        nTrial['questLapseRate']=   1-catchTrialAccuracy/catchTrialTracker
    
    # if end of catchTrial array, reshuffle
    if (nTrial['trialNumber']+1)%len(catchTrials) == 0:
        random.shuffle(catchTrials)
        
    # if not catch trial, add info to QUEST
    if catchTrials[nTrial['trialNumber']%len(catchTrials)] != 1:
        quest.addResponse(thisResp,separationToTest)
        #quest.calculateNextIntensity()
        #quest.next()
        
    nTrial['currentThresholdEst'] = quest.quantile()
    
    fixation0.setAutoDraw(False)
    
    # jittered ITI
    thisITI = stimITI - 0.005 + (random.randrange(-50, 50, 1))*0.001 # 50ms jitter
    thisFramesITI = int(round(thisITI/frameRate[0]*1000)) - framesFixITI
    
    fixationB.radius = dvaArrayItemWidth*2
    fixationB.draw() # more salient fixation
    mywin.flip()
    
    # shrinking fixation
    for frame in range(framesFixITI-1):  # minus 1 because of flip before
        fixationB.radius -= 0.005
        fixationB.draw()
        mywin.flip()
    
    # fixation
    for frame in range(thisFramesITI):
        fixation0.draw()
        mywin.flip()
    
    fixation0.setAutoDraw(True)
    # end of trial loop iteration, go to new trial

## End
save_data()
mywin.close()
core.quit()
