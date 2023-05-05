# P R A C T I C E #

# set currently at 10 trials, run through QUEST 

'''
3.1.4. Sensory Precision: We have also developed a task for assessing the sensory precision of the same
spatial information used in the WM and EM tasks. As shown in Fig. 2D, two lines are presented on each trial,
abutting each other near the same invisible circle that defines the stimulus locations for the WM and EM tasks.
Participants are required to report whether the outer line is to the left or right of the inner line. The amount of
physical left-right displacement is varied across trials using a highly efficient QUEST staircase procedure,
which produces a Bayesian estimate of the amount of offset needed to achieve 75% correct (the sensory
threshold). As in our previous work, catch trials are included so that we can measure the rate of attention
lapses and estimate the sensory threshold without contamination from lapses. In the study shown in Fig. 3
above, we used a nearly identical (but less efficient) task in which we tested equal numbers of trials for each
spatial offset of the two lines. As the offset increased, subjects were more accurate at discriminating their
relative locations (Fig. 3B), but performance reached asymptote well below 100% correct, reflecting attention
lapses (which were significantly greater in patients than controls). The slope of the function can be used to
estimate the precision of the spatial discrimination on non-lapse trials, which is isomorphic with the measure of
precision used in the WM task. This made it possible to show that the greater WM imprecision in patients than
in controls could not be explained by greater sensory imprecision in the patients.
'''

## Import key parts of the PsychoPy library:
from psychopy import visual, monitors, core, event, data, gui
import math, random, numpy, os, glob

# make sure working directory is right
os.chdir(os.path.dirname(os.path.abspath(__file__)))

## start a datafile
sessionInfo = {
    'Participant'           :   'PRACTICE',
    'TrialsToAdminister'    :   '10',
    'CatchTrialPercentage'  :   20,
    'cmFromSubjToScreen'    :   100,
    'windowFullScreen'      : True
    }
# present a dialogue to change params
dlg = gui.DlgFromDict(
    sessionInfo,
    title='Sensory Precision',
    fixed=['TaskFile','Date','Seed','TrialsToAdminister','CatchTrialPercentage','windowFullScreen', 'cmFromSubjToScreen'],
    order=['Participant']
    )

if dlg.OK:  # or if ok_data is not None
    ## Define a monitor
    my_monitor = monitors.Monitor(name='ERP1_stim')
    my_monitor.setSizePix((1920,1200))
    my_monitor.setWidth(52)
    my_monitor.setDistance(sessionInfo['cmFromSubjToScreen'])
    my_monitor.saveMon()
    ## Create a visual window:
    mywin = visual.Window(
        monitor='ERP1_stim',
        autoLog=False,
        units='deg',
        screen=0, #screen=0 for primary monitor, screen=1 to display on secondary monitor
        fullscr=sessionInfo['windowFullScreen'] #fullscrn=False if window is small, True to take the full screen
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
    clock = core.Clock()
else:
    core.quit()  # the user hit cancel so exit

if sessionInfo['TrialsToAdminister']=='all':
    numTrialsRequested = 400
else:
    numTrialsRequested = int(sessionInfo['TrialsToAdminister'])

expInfo = {
    'TaskFile'      :   os.path.basename(__file__)[:-3],
    'Date'          :   data.getDateStr(),
    'stimDuration'  :   0.1,
    'stimLength'    :   0.5,
    'stimWidth'     :   0.1,
    'stimOffsetFromScreenCenter'                        :   3.5,
    'stimUseFixedOffsetsNotQuestRecommendedOffsets'     :   False,
    'questInitialThresholdEstimateDegreesRadialAngle'   :   2.6, #"tGuess" or "startVal"
    'questInitialThresholdSD'                           :   5.0,
    'questCatchTrialRadialAngle'                        :   6.0,
    'questAccuracyAtThreshold'                          :   0.82, #"pThreshold"  (changed from 82% to 80.35% to match online threshold - kpw)
    'questNumberOfTrials'                               :   numTrialsRequested-(sessionInfo['CatchTrialPercentage']/100*numTrialsRequested),
    'questPercentConfidenceRequired'                    :   None, #The minimum 5-95% confidence interval required in the threshold estimate before stopping. If both this and nTrials is specified, whichever happens first will determine when Quest will stop.
    'questMethod'                                       :   'quantile', #The method used to determine the next threshold to test. If you want to get a specific threshold level at the end of your staircasing, please use the quantile, mean, and mode methods directly.
    'questSteepness'                                    :   3.5,  #"beta" Controls the steepness of the psychometric function.
    'questLapseRate'                                    :   0.01, #"delta" The fraction of trials on which the observer presses blindly.
    'questResponseBias'                                 :   0.5,  #"gamma" The fraction of trials that will generate response 1 when intensity=-Inf.
    'questGrain'                                        :   0.01, #The quantization of the internal table.
    'questRange'                                        :   None, #The intensity difference between the largest and smallest intensity that the internal table can store. This interval will be centered on the initial guess tGuess. QUEST assumes that intensities outside of this range have zero prior probability (i.e., they are impossible).
    'questExtraInfo'                                    :   None, #A dictionary (typically) that will be stored along with collected data using saveAsPickle() or saveAsText() methods.
    'questMinVal'                                       :   0, #The smallest legal value for the staircase, which can be used to prevent it reaching impossible contrast values, for instance.
    'questMaxVal'                                       :   None, #The largest legal value for the staircase, which can be used to prevent it reaching impossible contrast values, for instance.
    'questStaircase'                                    :   None, #Can supply a staircase object with intensities and results. Might be useful to give the quest algorithm more information if you have it. You can also call the importData function directly.
    'questOriginPath'                                   :   None,
    'questName'                                         :   ''
    }

loadingScreen.setAutoDraw(False)

# give instructions

instructionDir= 'InstructionSlides' #folder/directory the images are in,
instructionFiles = []
instructionFiles = sorted(glob.glob(os.path.join(instructionDir, '*.png')))  # where the image files get loaded

for instr in list(range(0,len(instructionFiles))):
    instrImage = visual.ImageStim(win=mywin, image=instructionFiles[instr])
    
    instrImage.draw()
    mywin.flip()

    allKeys = event.waitKeys(keyList=['escape','left','right'])
    for thisKey in allKeys:
        if thisKey in ['escape']:
            mywin.close()
            core.quit()
        elif thisKey in ['left','right']:
            event.clearEvents()

## Stimulus dimensions
stimDuration        =   expInfo['stimDuration'] #seconds
stimPresentaionFlips=   int(round(stimDuration/frameRate[0]*1000))
stimITI = 1 #seconds ITI - gets jittered 50ms
framesStimITI        =   int(round(stimITI/frameRate[0]*1000))
durFixITI           =   .5  # will be subtracted from durITI as bigger fixation
framesFixITI        =   int(round(durFixITI/frameRate[0]*1000))

dvaArrayRadius      =   expInfo['stimOffsetFromScreenCenter']
dvaArrayOuterRadius =   dvaArrayRadius+0.26
dvaArrayInnerRadius =   dvaArrayRadius-0.26
dvaArrayItemLength  =   expInfo['stimLength']
dvaArrayItemWidth   =   expInfo['stimWidth']

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

## define parameters for each trial of each trial type
tList=[]
for x in list(range(0,numTrialsRequested)):
    tList.append({
        'Participant'       :   sessionInfo['Participant'],
        'Session'           :   sessionInfo['Session'],
        'TaskFile'          :   expInfo['TaskFile'],
        'Date'              :   expInfo['Date'],
        'cmFromSubjToScreen':   sessionInfo['cmFromSubjToScreen'],
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
        'trialOnset'        :   0, #not yet set
        'trialOnsetITI'     :   0,
        'catchTrial'        :   0,
        'questRecommendedSeparation' : 0.0,
        'probedSeparation'  :   0.0,
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

#1 in 5 trials is a catch trial
catchTrials=[1,0,0,0,0,0,0,0,0,1]
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

fixationB.radius = dvaArrayItemWidth*2

for frame in range(framesStimITI-framesFixITI):
    fixation0.draw()
    mywin.flip()

for nTrial in trials:
    fixation0.setAutoDraw(True)
    # moved onset timer from here
    
    
    #check for catch trial
    if catchTrials[nTrial['trialNumber']%len(catchTrials)] == 1:
        separationToTest = expInfo['questCatchTrialRadialAngle']
        catchTrialTracker += 1
        strCatch = 'catch trial'
        nTrial['catchTrial'] = 1
    else:
        quest.next()
        if expInfo['stimUseFixedOffsetsNotQuestRecommendedOffsets']:
            previousNonCatchSeparationTested = round (quest.quantile() / expInfo['questMajorAdjustmentRadialAngle']) * expInfo['questMajorAdjustmentRadialAngle']
        else:
            previousNonCatchSeparationTested = quest.quantile()
        strCatch = ''
        if nTrial['trialNumber'] < 10:
            if correctRespTracker == 3 or incorrectRespTracker == 1:
                correctRespTracker = 0
                incorrectRespTracker = 0
                if expInfo['stimUseFixedOffsetsNotQuestRecommendedOffsets']:
                    if separationToTest >= 2 * expInfo['questMajorAdjustmentRadialAngle']:
                        separationToTest = round (quest.quantile() / expInfo['questMajorAdjustmentRadialAngle']) * expInfo['questMajorAdjustmentRadialAngle']
                    else:
                        separationToTest = round (quest.quantile() / expInfo['questMinorAdjustmentRadialAngle']) * expInfo['questMinorAdjustmentRadialAngle']
                else:
                    separationToTest = quest.quantile()
            else:
                separationToTest = previousNonCatchSeparationTested
        else:
            separationToTest = quest.quantile()
        previousNonCatchSeparationTested = separationToTest
    
    nTrial['questRecommendedSeparation']    =   quest.quantile()
    nTrial['probedSeparation']  =   separationToTest
    
    #assign random stim location
    angleRange = 40
    innerStimAngle = random.randint(0,angleRange) #outer radius stimulus angle will be offset from here
    stimVertical = random.choice([1, -1]) #whether the stimulus is above or below screen center
    
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
    
    nTrial['trialOnset']    = clock.getTime()
    
    for flip in range(0,stimPresentaionFlips):
        shapeInner.draw()
        shapeOuter.draw() 
        mywin.flip()
    mywin.flip()
    
    thisResp = None
    while thisResp == None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            nTrial['respRT']    =   clock.getTime()-nTrial['trialOnset']
            if thisKey == correctResp:
                thisResp=1
                strResp = 'responded correctly'
                if catchTrials[nTrial['trialNumber']%len(catchTrials)] != 1:
                    correctRespTracker += 1

            elif thisKey == incorrectResp:
                thisResp=0
                strResp = 'responded incorrectly'
                correctRespTracker = 0
                incorrectRespTracker = 1
                
            elif thisKey in ['escape','q']:
                quest.addResponse(0,0)
                mywin.close()
                core.quit()
        event.clearEvents()
    
    nTrial['respACC']   =   thisResp
    
    if catchTrialTracker >= 10:
        quest.setDelta          =   1-catchTrialAccuracy/catchTrialTracker
        nTrial['questLapseRate']=   1-catchTrialAccuracy/catchTrialTracker
    
    print(str(nTrial['trialNumber']) + ':   ' + strResp + '        correctRespTracker = ' + str(correctRespTracker) + '   incorrectRespTracker = ' + str(incorrectRespTracker) + '   separation tested =    ' + str(separationToTest) + '   QUEST recommended: ' + str(quest.quantile()) + '    ' + strCatch)
    if catchTrials[nTrial['trialNumber']%len(catchTrials)] != 1:
        quest.addResponse(thisResp,separationToTest)
        quest.calculateNextIntensity()
    
    if (nTrial['trialNumber']+1)%len(catchTrials) == 0:
        random.shuffle(catchTrials)
        print(catchTrials)
    
    nTrial['trialOnsetITI'] =   clock.getTime()
    
    fixation0.setAutoDraw(False)
    # jittered ITI
    thisITI = stimITI - 0.005 + (random.randrange(-50, 50, 1))*0.001 # 50ms jitter
    thisFramesITI = int(round(thisITI/frameRate[0]*1000)) - framesFixITI
    
    fixationB.radius = dvaArrayItemWidth*2
    fixationB.draw() # more salient fixation
    mywin.flip()
    
    for frame in range(framesFixITI-1):  # minus 1 because of flip before
        fixationB.radius -= 0.005
        fixationB.draw()
        mywin.flip()
        
    for frame in range(thisFramesITI):
        fixation0.draw()
        mywin.flip()
    
    fixation0.setAutoDraw(False)
    
endPractice = visual.TextStim(
        win=mywin,
        autoLog=False,
        text="End of practice - do you have any questions?",
        height = .5
        )

mywin.flip()
core.wait(1)

mywin.close()
core.quit()
