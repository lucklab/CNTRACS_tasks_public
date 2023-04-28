from psychopy import visual, monitors, core, event, data, gui, parallel
from psychopy.tools.filetools import fromFile, toFile
import pandas as pd
import numpy as np
import os, json

## Verify particulars of this session
sessionInfo = {
    'Participant'   :   '---',
    'Group'         :   '',
    'Date'          :   data.getDateStr(),
    'Session'       :   ['', '1', '2'],
    'Seed'          :   core.getAbsTime(),
    'TaskFile'      :   os.path.basename(__file__),
    'local_path'    :   os.getcwd(),
    'set_id'        :   np.random.randint(1, 10),
    'task_id'       :   4,
    'responseWindow':   2.0,
    'feedbackDelay' :   0.5,
    'feedbackDuration': 1.0,
    'trainITI'      :   1.0,
    'testITI'       :   1.0 # changed from 1.5
    }

## Define a monitor
my_monitor = monitors.Monitor(name='ERP1_stim')
my_monitor.setSizePix((1920,1200))
my_monitor.setWidth(52)
my_monitor.setDistance(100)
my_monitor.saveMon()

dlg = gui.DlgFromDict(
    sessionInfo,
    title='RLWMPST',
    fixed=['Date','Seed','TaskFile','local_path','set_id','task_id','responseWindow','feedbackDelay','feedbackDuration','trainITI','testITI','Group'],
    order=['Participant','Session','Date','Seed','TaskFile','local_path','set_id','task_id','responseWindow','feedbackDelay','feedbackDuration','trainITI','testITI']
    )

## Check if session number is filled in with a number, quit if not
while True:
    try:
        sessionInfo['Session'] = int(sessionInfo['Session'])
        break
    except ValueError:
        print("Please enter a session number!")
        core.quit()

if dlg.OK:
    ## Create a visual window:
    mywin = visual.Window(
        size=my_monitor.getSizePix(),
        #color='black',
        monitor=my_monitor.name,
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
    mouse = event.Mouse(visible = True, win = mywin)
    #clock = core.Clock() moved to 250 code (roughly recording onset)
else:
    core.quit()  # the user hit cancel so exit

def save_data():
    savingScreen = visual.TextStim(
        win=mywin,
        autoLog=False,
        text="Thank you for participating!\n\nSaving to file..."
        )
    savingScreen.setAutoDraw(True)
    savingScreen.draw()
    mywin.flip()
    ## create the datafile
    practiceTrials.saveAsExcel(
        fileName=sessionInfo['TaskFile'][:-3]+"_practice_"+sessionInfo['Date']+"_"+sessionInfo['Participant']+'_TRT_'+str(sessionInfo['Session'])+'.csv',
        sheetName = sessionInfo['Participant']+"_"+sessionInfo['Date'],
        stimOut=[
            'Participant',
            'Group',
            'Date',
            'Session',
            'Seed',
            'set_id',
            'responseWindow',
            'feedbackDelay',
            'feedbackDuration',
            'trainITI',
            'testITI',
            'blockType',
            'blockNumber',
            'trialNumber',
            'trialSetSize',
            'trialStimFolder',
            'trialStimID',
            'trialStimInBlockID',
            'trialStimOverallID',
            'trialCorrectKey',
            'trialCorrectProb',
            'trialCorrectFBVal',
            'trialSetSize_Left',
            'trialSetSize_Right',
            'trialStimBlockNum_Left',
            'trialStimBlockNum_Right',
            'trialStimFolder_Left',
            'trialStimFolder_Right',
            'trialStimID_Left',
            'trialStimID_Right',
            'trialStimOverallID_Left',
            'trialStimOverallID_Right',
            'trialCorrectProb_Left',
            'trialCorrectProb_Right',
            'trialOnset',
            'resp',
            'respACC',
            'respKey',
            'respRT'
        ]
    )
    trainingTrials.saveAsExcel(
        fileName=sessionInfo['TaskFile'][:-3]+"_training_"+sessionInfo['Date']+"_"+sessionInfo['Participant']+'_TRT_'+str(sessionInfo['Session'])+'.csv',
        sheetName = sessionInfo['Participant']+"_"+sessionInfo['Date'],
        stimOut=[
            'Participant',
            'Group',
            'Date',
            'Session',
            'Seed',
            'set_id',
            'responseWindow',
            'feedbackDelay',
            'feedbackDuration',
            'trainITI',
            'testITI',
            'blockType',
            'blockNumber',
            'trialNumber',
            'trialSetSize',
            'trialStimFolder',
            'trialStimID',
            'trialStimInBlockID',
            'trialStimOverallID',
            'trialCorrectKey',
            'trialCorrectProb',
            'trialCorrectFBVal',
            'trialSetSize_Left',
            'trialSetSize_Right',
            'trialStimBlockNum_Left',
            'trialStimBlockNum_Right',
            'trialStimFolder_Left',
            'trialStimFolder_Right',
            'trialStimID_Left',
            'trialStimID_Right',
            'trialStimOverallID_Left',
            'trialStimOverallID_Right',
            'trialCorrectProb_Left',
            'trialCorrectProb_Right',
            'trialOnset',
            'resp',
            'respACC',
            'respKey',
            'respRT',
            'totalPoints'
        ]
    )
    testTrials.saveAsExcel(
        fileName=sessionInfo['TaskFile'][:-3]+"_test_"+sessionInfo['Date']+"_"+sessionInfo['Participant']+'_TRT_'+str(sessionInfo['Session'])+'.csv',
        sheetName = sessionInfo['Participant']+"_"+sessionInfo['Date'],
        stimOut=[
            'Participant',
            'Group',
            'Date',
            'Session',
            'Seed',
            'set_id',
            'responseWindow',
            'feedbackDelay',
            'feedbackDuration',
            'trainITI',
            'testITI',
            'blockType',
            'blockNumber',
            'trialNumber',
            'trialSetSize',
            'trialStimFolder',
            'trialStimID',
            'trialStimInBlockID',
            'trialStimOverallID',
            'trialCorrectKey',
            'trialCorrectProb',
            'trialCorrectFBVal',
            'trialSetSize_Left',
            'trialSetSize_Right',
            'trialStimBlockNum_Left',
            'trialStimBlockNum_Right',
            'trialStimFolder_Left',
            'trialStimFolder_Right',
            'trialStimID_Left',
            'trialStimID_Right',
            'trialStimOverallID_Left',
            'trialStimOverallID_Right',
            'trialCorrectProb_Left',
            'trialCorrectProb_Right',
            'trialOnset',
            'resp',
            'respACC',
            'respKey',
            'respRT'
        ]
    )
    #mywin.close()
    #core.quit()

# routes to a folder (s_1 thru S_11) in the V4 folder to load trial orders
base_path = os.path.join(sessionInfo['local_path'], 'rlwmpst', 'V{}'.format(sessionInfo['task_id']), 'S_{}'.format(sessionInfo['set_id']))

train_instruction_trials = pd.read_csv(os.path.join(base_path, 'train_instruction_10blocks.csv'), index_col=0)
train_trials = pd.read_csv(os.path.join(base_path, 'train.csv'), index_col=0)
test_trials = pd.read_csv(os.path.join(base_path, 'test.csv'), index_col=0)

jCode = 13
kCode = 14
lCode = 15

blockList=[]
for block in list(range(0,len(train_instruction_trials))):
    blockList.append({
        'blockNumber'   :   block,
        'setSize'       :   train_instruction_trials['set size'][block],
        'imageFolder'   :   train_instruction_trials['image folder'][block],
        'image1'        :   train_instruction_trials['image1'][block],
        'image2'        :   train_instruction_trials['image2'][block],
        'image3'        :   train_instruction_trials['image3'][block],
        'image4'        :   train_instruction_trials['image4'][block],
        'image5'        :   train_instruction_trials['image5'][block]
        })

pracList=[]
for x in list(range(0,10)):
    if (x%2)+13 == jCode:
        correctKey = 'j'
    if (x%2)+13 == kCode:
        correctKey = 'k'
    if (x%2)+13 == lCode:
        correctKey = 'l'
    pracList.append({
        'Participant'       :   sessionInfo['Participant'],
        'Group'             :   '',
        'Date'              :   sessionInfo['Date'],
        'Session'           :   sessionInfo['Session'],
        'Seed'              :   sessionInfo['Seed'],
        'set_id'            :   sessionInfo['set_id'],
        'responseWindow'    :   sessionInfo['responseWindow'],
        'feedbackDelay'     :   sessionInfo['feedbackDelay'],
        'feedbackDuration'  :   sessionInfo['feedbackDuration'],
        'trainITI'          :   sessionInfo['trainITI'],
        'testITI'           :   sessionInfo['testITI'],
        'blockType'         :   'practice',
        'blockNumber'       :   99,
        'trialNumber'       :   x,
        'trialSetSize'      :   2,
        'trialStimFolder'   :   99,
        'trialStimID'       :   (x%2)+1,
        'trialStimInBlockID':   'NA',
        'trialStimOverallID':   'NA',
        'trialCorrectKey'   :   correctKey,
        'trialCorrectProb'  :   'NA',
        'trialCorrectFBVal' :   np.random.randint(1, 3),
        'trialSetSize_Left'         :   'NA',
        'trialSetSize_Right'        :   'NA',
        'trialStimBlockNum_Left'    :   'NA',
        'trialStimBlockNum_Right'   :   'NA',
        'trialStimFolder_Left'      :   'NA',
        'trialStimFolder_Right'     :   'NA',
        'trialStimID_Left'          :   'NA',
        'trialStimID_Right'         :   'NA',
        'trialStimOverallID_Left'   :   'NA',
        'trialStimOverallID_Right'  :   'NA',
        'trialCorrectProb_Left'     :   'NA',
        'trialCorrectProb_Right'    :   'NA',
        'trialOnset'        :   0, #not yet set
        'resp'              :   0,
        'respACC'           :   0,
        'respKey'           :   '?',
        'respRT'            :   0.0
        })

trainList = []
for x in list(range(0,len(train_trials))):
    if train_trials['correct key#'][x] == jCode:
        correctKey = 'j'
    if train_trials['correct key#'][x] == kCode:
        correctKey = 'k'
    if train_trials['correct key#'][x] == lCode:
        correctKey = 'l'
   
    trainList.append({
        'Participant'       :   sessionInfo['Participant'],
        'Group'             :   '',
        'Date'              :   sessionInfo['Date'],
        'Session'           :   sessionInfo['Session'],
        'Seed'              :   sessionInfo['Seed'],
        'set_id'            :   sessionInfo['set_id'],
        'responseWindow'    :   sessionInfo['responseWindow'],
        'feedbackDelay'     :   sessionInfo['feedbackDelay'],
        'feedbackDuration'  :   sessionInfo['feedbackDuration'],
        'trainITI'          :   sessionInfo['trainITI'],
        'testITI'           :   sessionInfo['testITI'],
        'blockType'         :   'train',
        'blockNumber'       :   train_trials['block #'][x],
        'trialNumber'       :   x,
        'trialSetSize'      :   train_trials['set size'][x],
        'trialStimFolder'   :   train_trials['image folder'][x],
        'trialStimID'       :   train_trials['image number'][x],
        'trialStimInBlockID':   train_trials['in block stim #'][x],
        'trialStimOverallID':   train_trials['overall stimulus id'][x],
        'trialCorrectKey'   :   correctKey,
        'trialCorrectProb'  :   train_trials['2/1 correct FB proba'][x],
        'trialCorrectFBVal' :   train_trials['CorrectFB value'][x],
        'trialSetSize_Left'         :   'NA',
        'trialSetSize_Right'        :   'NA',
        'trialStimBlockNum_Left'    :   'NA',
        'trialStimBlockNum_Right'   :   'NA',
        'trialStimFolder_Left'      :   'NA',
        'trialStimFolder_Right'     :   'NA',
        'trialStimID_Left'          :   'NA',
        'trialStimID_Right'         :   'NA',
        'trialStimOverallID_Left'   :   'NA',
        'trialStimOverallID_Right'  :   'NA',
        'trialCorrectProb_Left'     :   'NA',
        'trialCorrectProb_Right'    :   'NA',
        'trialOnset'        :   0, #not yet set
        'resp'              :   0,
        'respACC'           :   0,
        'respKey'           :   '?',
        'respRT'            :   0.0,
        'totalPoints'       :   0
        })

testList = []
for x in list(range(0,len(test_trials))):
    testList.append({
        'Participant'       :   sessionInfo['Participant'],
        'Group'             :   '',
        'Date'              :   sessionInfo['Date'],
        'Session'           :   sessionInfo['Session'],
        'Seed'              :   sessionInfo['Seed'],
        'set_id'            :   sessionInfo['set_id'],
        'responseWindow'    :   sessionInfo['responseWindow'],
        'feedbackDelay'     :   sessionInfo['feedbackDelay'],
        'feedbackDuration'  :   sessionInfo['feedbackDuration'],
        'trainITI'          :   sessionInfo['trainITI'],
        'testITI'           :   sessionInfo['testITI'],
        'blockType'         :   'test',
        'blockNumber'       :   'NA',
        'trialNumber'       :   x,
        'trialSetSize'      :   'NA',
        'trialStimFolder'   :   'NA',
        'trialStimID'       :   'NA',
        'trialStimInBlockID':   'NA',
        'trialStimOverallID':   'NA',
        'trialFBEventCode'  :   'NA',
        'trialCorrectKey'   :   'NA',
        'trialCorrectProb'  :   'NA',
        'trialCorrectFBVal' :   'NA',
        'trialSetSize_Left'         :   test_trials['left set size'][x],
        'trialSetSize_Right'        :   test_trials['right set size'][x],
        'trialStimBlockNum_Left'    :   test_trials['left block number'][x],
        'trialStimBlockNum_Right'   :   test_trials['right block number'][x],
        'trialStimFolder_Left'      :   test_trials['left image folder'][x],
        'trialStimFolder_Right'     :   test_trials['right image folder'][x],
        'trialStimID_Left'          :   test_trials['left image number'][x],
        'trialStimID_Right'         :   test_trials['right image number'][x],
        'trialStimOverallID_Left'   :   test_trials['left stimulus id'][x],
        'trialStimOverallID_Right'  :   test_trials['right stimulus id'][x],
        'trialCorrectProb_Left'     :   test_trials['left stim value'][x],
        'trialCorrectProb_Right'    :   test_trials['right stim value'][x],
        'trialOnset'        :   0, #not yet set
        'resp'              :   0,
        'respACC'           :   'NA',
        'respKey'           :   '?',
        'respRT'            :   0.0
        })

practiceTrials = data.TrialHandler(
    trialList=pracList[0:len(pracList)],
    nReps=1,
    method='sequential',
    dataTypes=[]
    )
trainingTrials = data.TrialHandler(
    trialList=trainList[0:len(trainList)],
    nReps=1,
    method='sequential',
    dataTypes=[]
    )
testTrials = data.TrialHandler(
    trialList=testList[0:len(testList)],
    nReps=1,
    method='sequential',
    dataTypes=[]
    )

loadingScreen.setAutoDraw(False)

intro_text = visual.TextStim(
    win = mywin,
    alignHoriz='center',
    alignVert='center',
    units = 'deg',
    height = 0.5
    )
intro_textText = []
intro_textText.append(
    'Working Memory Reinforcement Learning Task\n\n'
    'In this experiment, you will see an image on the screen.\n\n'
    'You need to respond to each image by pressing one of the three buttons on the keyboard:\n\n'
    'j, k or l\n\n'
    'with your dominant hand.\n\n'
    )
intro_textText.append(
    'Your goal is to figure out which button makes you win for each image.\n\n'
    'You will have a few seconds to respond.\n\n'
    )
intro_textText.append(
    'Please respond to every image as quickly and accurately as possible.\n\n'
    'If you do not respond, the trial will be counted as a loss.\n\n'
    'If you select the correct button, you will gain points.\n\n'
    )
intro_textText.append(
    'You can gain either 1 or 2 points designated as \"$\" or \"$$\".\n\n'
    'The computer assigns points randomly, but only if you selected the correct button!\n\n'
    'You will be given extra money based on the total number of points you earn!'
    )
intro_textText.append(
    'After the practice section, there will be a dozen short blocks.\n\n'
    'You can rest between each block.\n\n'
    'At the beginning of each block, you will be shown the set of images for that block.\n\n'
    'Take some time to identify them correctly.\n\n'
    )
intro_textText.append(
    'Note the following important rules:\n\n'
    '1. There is ONLY ONE correct response for each image.\n\n'
    '2. One response button MAY be correct for multiple images, or not be correct for any image.\n\n'
    '3. Within each block, the correct response for each image will not change.\n\n'
    '4. The more correct responses you give, the faster you will finish the block.\n\n'
    )
demo_text = visual.TextStim(
    win = mywin,
    alignHoriz='center',
    alignVert='center',
    units = 'deg',
    height = 0.5
    )
demo_textText = []
demo_textText.append(
    'You will next get some practice trials which will not count to your final score.\n\n'
    '[Press space to continue.]'
    )
demo_textText.append(
    'Get Ready! [Press space to continue.]'
    )
demo_textText.append(
    'Take some time to familiarize yourself with the images. Press a key when ready to begin.'
    )
practiceText1 = visual.TextStim(
    win = mywin,
    pos = (0,-5),
    units = 'deg',
    height = 0.5,
    text = 'Press the j, k, or l key.'
    )
practiceText2 = visual.TextStim(
    win = mywin,
    pos = (0,-6),
    units = 'deg',
    height = 0.5,
    text = 'Learn from the feedback which keys are correct.'
    )
noResponseText = visual.TextStim(
    win = mywin,
    pos = (0,0),
    units = 'deg',
    height = 1,
    color = 'red',
    text = 'Timeout! Respond faster.'
    )
endOfBlock_text = visual.TextStim(
    win = mywin,
    alignHoriz='center',
    alignVert='center',
    units = 'deg',
    height = 0.5
    )
testInstructions = visual.TextStim(
    win = mywin,
    alignHoriz='center',
    alignVert='center',
    units = 'deg',
    height = 0.5,
    text = 'Great! You are almost done with this experiment.\n\n'
    'It is time to test what you have learned.\n\n'
    'During this set of trials you will NOT recieve feedback to your responses.\n\n'
    'You will see two images from the task on the screen at one time.\n\n'
    'One on the left and the other on the right.\n\n'
    'Pick the picture that won you the most points during the previous learning task!\n\n'
    'If you are not sure which one to pick, just go with your gut instinct!\n\n'
    'To choose the image on the left, hit the "1" key.\n'
    'To choose the image on the right, hit the "0" key.\n\n'
    '[Press space to continue.]'
    )
testPrompt = visual.TextStim(
    win = mywin,
    alignHoriz='center',
    alignVert='center',
    units = 'deg',
    height = 0.5,
    pos = (0,-5),
    text = 'Press 1 to select the left image, and 0 to select the right image.'
    )
demoStim1 = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image1.jpg'), mask=None,
    ori=0, pos=(-12, 0), size=5.0)
demoStim2 = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image2.jpg'), mask=None,
    ori=0, pos=(-6, 0), size=5.0)
demoStim3 = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image1.jpg'), mask=None,
    ori=0, pos=(0, 0), size=5.0)
demoStim4 = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image2.jpg'), mask=None,
    ori=0, pos=(6, 0), size=5.0)
demoStim5 = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image1.jpg'), mask=None,
    ori=0, pos=(12, 0), size=5.0)
trialStimA = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image1.jpg'), mask=None,
    ori=0, pos=(0, 0), size=5.0)
trialStimB = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','images99','image2.jpg'), mask=None,
    ori=0, pos=(3, 0), size=5.0)
currentReward = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','zero.png'), mask=None,
    ori=0, pos=(0, 0), size=5.0)
backButton = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','back.jpg'), mask=None,
    ori=0, pos=(-1.5, -8), size=2.5)
forwardButton = visual.ImageStim(
    win=mywin, name='Image',units='deg', 
    image=os.path.join(sessionInfo['local_path'],'rlwmpst','next.jpg'), mask=None,
    ori=0, pos=(1.5, -8), size=2.5)
backButton.size     *= [1,0.5]
forwardButton.size  *= [1,0.5]

mywin.flip()
clock = core.Clock() #start global clock

# new instructions
intro_text.setAutoDraw(True)
forwardButton.setAutoDraw(True)
i = 0
while i < len(intro_textText):
    if i > 0:
        backButton.setAutoDraw(True)
    
    intro_text.setText(intro_textText[i])
    mywin.flip()
    
    allKeys = event.getKeys(keyList=['escape', 'left', 'right'])
    for thisKey in allKeys:
        if thisKey in ['escape']:
            mywin.close()
            core.quit()
            
        if thisKey in ['left']:
            i -=1
            core.wait(.20)
        if thisKey in ['right']:
            i +=1
            core.wait(.20)
    
    if mouse.isPressedIn(backButton):
        i -=1
        core.wait(.20)
        
    if mouse.isPressedIn(forwardButton):
        i += 1
        core.wait(.20)
    
    event.clearEvents()

backButton.setAutoDraw(False)
forwardButton.setAutoDraw(False)
intro_text.setAutoDraw(False)
mouse.setVisible(False)

demo_text.setAutoDraw(True)
for x in range(0,len(demo_textText)):
    demo_text.setText(demo_textText[x])
    if x == len(demo_textText)-1:
        demoStim1.pos = (-3,0)
        demoStim2.pos = (3,0)
        demoStim1.setAutoDraw(True)
        demoStim2.setAutoDraw(True)
        demo_text.pos = (0,5)
    
    mywin.flip()
    allKeys = event.waitKeys(keyList=['escape','j','k','l','space'])
    for thisKey in allKeys:
        if thisKey in ['escape']:
            mywin.close()
            core.quit()
        elif thisKey in ['j','k','l','space']:
            event.clearEvents()

demoStim1.setAutoDraw(False)
demoStim2.setAutoDraw(False)
demoStim1.pos = (-12,0)
demoStim2.pos = (-6,0)
demo_text.pos = (0,0)
demo_text.setAutoDraw(False)

mywin.flip()

# PRACTICE #
for trial in practiceTrials:

    accuracy = False
    responded = False
    allKeys = event.waitKeys(maxWait=trial['trainITI'],keyList=['escape'])
    for thisKey in allKeys or []:
        if thisKey in ['escape']:
            save_data()
            mywin.close()
            core.quit()
    trialStimA.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(trial['trialStimFolder']),'image'+str(trial['trialStimID'])+'.jpg')
    trialStimA.setAutoDraw(True)
    practiceText1.setAutoDraw(True)
    practiceText2.setAutoDraw(True)
    
    mywin.flip()
    trial['trialOnset'] = clock.getTime()
    
    allKeys = event.waitKeys(maxWait=trial['responseWindow'],keyList=['j','k','l','escape'])
    print(allKeys)
    if allKeys and len(allKeys) == 1:
        print('no mashing detected')
        for thisKey in allKeys:
            if thisKey in ['escape',]:
                save_data()
                mywin.close()
                core.quit()
            elif thisKey in ['j','k','l']:
                if thisKey == trial['trialCorrectKey']:
                    trial['respACC'] = 1
                    accuracy = True
                else:
                    trial['respACC'] = 0
                    accuracy = False
        trial['resp'] = 1
        trial['respKey'] = thisKey
        trial['respRT'] = clock.getTime()-trial['trialOnset']
        responded = True
    elif allKeys and len(allKeys) >> 1:
        print('buttons mashed')
        trial['respACC'] = 0
        accuracy = False
        trial['resp'] = 1
        trial['respKey'] = allKeys
        trial['respRT'] = clock.getTime()-trial['trialOnset']
        responded = True
    else:
        responded = False

    event.clearEvents()
    trialStimA.setAutoDraw(False)
    practiceText1.setAutoDraw(False)
    practiceText2.setAutoDraw(False)
    mywin.flip()
    
    allKeys = event.waitKeys(maxWait=trial['feedbackDelay'],keyList=['escape'])
    for thisKey in allKeys or []:
        if thisKey in ['escape']:
            save_data()
            mywin.close()
            core.quit()
    if not responded:
        noResponseText.setAutoDraw(True)
    elif responded and not accuracy:
        currentReward.image = os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','zero.png')
        currentReward.setAutoDraw(True)
    else:
        if trial['trialCorrectFBVal'] == 1:
            currentReward.image = os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','small_reward.png')
        elif trial['trialCorrectFBVal'] == 2:
            currentReward.image = os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','large_reward.png')
        currentReward.setAutoDraw(True)
    
    mywin.flip()
        
    allKeys = event.waitKeys(maxWait=trial['feedbackDuration'],keyList=['escape','q'])
    for thisKey in allKeys or []:
        if thisKey in ['escape','q']:
            save_data()
            mywin.close()
            core.quit()
    currentReward.setAutoDraw(False)
    noResponseText.setAutoDraw(False)
    mywin.flip()

# # say practice is over
intro_text.setText(
    'End of practice, do you have any questions?\n\n'
    '       [Press space to continue.]'
    )

intro_text.draw()
mywin.flip()

allKeys = event.waitKeys(keyList=['escape','j','k','l','space'])
for thisKey in allKeys:
    if thisKey in ['escape']:
        mywin.close()
        core.quit()
    elif thisKey in ['j','k','l','space']:
        event.clearEvents()

core.wait(1)

# #

# TRAIN #
totalPoints = 0
newBlockTrialNum = 0
for currentBlock in range(0,len(blockList)):

    if blockList[currentBlock]['setSize'] == 5:
        demoStim1.setAutoDraw(True)
        demoStim2.setAutoDraw(True)
        demoStim3.setAutoDraw(True)
        demoStim4.setAutoDraw(True)
        demoStim5.setAutoDraw(True)
        demoStim1.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image1']))+'.jpg') # added int()
        demoStim2.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image2']))+'.jpg')
        demoStim3.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image3']))+'.jpg')
        demoStim4.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image4']))+'.jpg')
        demoStim5.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image5']))+'.jpg')
    elif blockList[currentBlock]['setSize'] == 4:
        demoStim1.pos = (-9,0)
        demoStim2.pos = (-3,0)
        demoStim3.pos = (3,0)
        demoStim4.pos = (9,0)
        demoStim1.setAutoDraw(True)
        demoStim2.setAutoDraw(True)
        demoStim3.setAutoDraw(True)
        demoStim4.setAutoDraw(True)
        demoStim1.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image1']))+'.jpg')
        demoStim2.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image2']))+'.jpg')
        demoStim3.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image3']))+'.jpg')
        demoStim4.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image4']))+'.jpg')
    elif blockList[currentBlock]['setSize'] == 3:
        demoStim1.pos = (-6,0)
        demoStim2.pos = (0,0)
        demoStim3.pos = (6,0)
        demoStim1.setAutoDraw(True)
        demoStim2.setAutoDraw(True)
        demoStim3.setAutoDraw(True)
        demoStim1.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image1']))+'.jpg')
        demoStim2.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image2']))+'.jpg')
        demoStim3.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image3']))+'.jpg')
    elif blockList[currentBlock]['setSize'] == 2:
        demoStim1.pos = (-3,0)
        demoStim2.pos = (3,0)
        demoStim1.setAutoDraw(True)
        demoStim2.setAutoDraw(True)
        demoStim1.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image1']))+'.jpg')
        demoStim2.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(blockList[currentBlock]['imageFolder'])),'image'+str(int(blockList[currentBlock]['image2']))+'.jpg')
    demo_text.setAutoDraw(True)
    demo_text.pos = (0,5)
    mywin.flip()
    allKeys = event.waitKeys(keyList=['escape','space','j','k','l'])
    for thisKey in allKeys:
        if thisKey in ['escape']:
            mywin.close()
            core.quit()
        elif thisKey in ['space','j','k','l']:
            event.clearEvents()
    demoStim1.setAutoDraw(False)
    demoStim2.setAutoDraw(False)
    demoStim3.setAutoDraw(False)
    demoStim4.setAutoDraw(False)
    demoStim5.setAutoDraw(False)
    demo_text.setAutoDraw(False)
    demoStim1.pos = (-12,0)
    demoStim2.pos = (-6,0)
    demoStim3.pos = (0,0)
    demoStim4.pos = (6,0)
    demoStim5.pos = (12,0)
    
    mywin.flip()
    
    # start block
    for num, trial in enumerate(trainingTrials, start=newBlockTrialNum):
        
        accuracy = False
        responded = False
        
        allKeys = event.waitKeys(maxWait=trial['trainITI'],keyList=['escape'])
        for thisKey in allKeys or []:
            if thisKey in ['escape']:
                save_data()
                mywin.close()
                core.quit()
        trialStimA.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(trial['trialStimFolder'])),'image'+str(int(trial['trialStimID']))+'.jpg') # added int()
        trialStimA.setAutoDraw(True)
        
        mywin.flip()
        trial['trialOnset'] = clock.getTime()
        
        allKeys = event.waitKeys(maxWait=trial['responseWindow'],keyList=['j','k','l','escape'],clearEvents=False)
        
        if allKeys and len(allKeys) == 1:
            print('no mashing detected')
            for thisKey in allKeys:
                if thisKey in ['escape',]:
                    save_data()
                    mywin.close()
                    core.quit()
                elif thisKey in ['j','k','l']:
                    if thisKey == trial['trialCorrectKey']:
                        trial['respACC'] = 1
                        accuracy = True
                    else:
                        trial['respACC'] = 0
                        accuracy = False
            trial['resp'] = 1
            trial['respKey'] = thisKey
            trial['respRT'] = clock.getTime()-trial['trialOnset']
            responded = True
        elif allKeys and len(allKeys) >> 1:
            print('buttons mashed')
            trial['respACC'] = 0
            accuracy = False
            trial['resp'] = 1
            trial['respKey'] = allKeys
            trial['respRT'] = clock.getTime()-trial['trialOnset']
            responded = True
        else:
            responded = False
        
        event.clearEvents()
        trialStimA.setAutoDraw(False)
        mywin.flip()

        allKeys = event.waitKeys(maxWait=trial['feedbackDelay'],keyList=['escape'])
        for thisKey in allKeys or []:
            if thisKey in ['escape']:
                save_data()
                mywin.close()
                core.quit()
        if not responded:
            noResponseText.setAutoDraw(True)
        elif responded and not accuracy:
            currentReward.image = os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','zero.png')
            currentReward.setAutoDraw(True)
        else:
            if trial['trialCorrectFBVal'] == 1:
                currentReward.image = os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','small_reward.png')
            elif trial['trialCorrectFBVal'] == 2:
                currentReward.image = os.path.join(sessionInfo['local_path'],'rlwmpst','reward_images','large_reward.png')
            currentReward.setAutoDraw(True)
        mywin.flip()

        allKeys = event.waitKeys(maxWait=trial['feedbackDuration'],keyList=['escape','q'])
        for thisKey in allKeys or []:
            if thisKey in ['escape','q']:
                save_data()
                mywin.close()
                core.quit()
        currentReward.setAutoDraw(False)
        noResponseText.setAutoDraw(False)
        
        trialPoints = trial['trialCorrectFBVal']*trial['respACC'] # get points from trial
        totalPoints = totalPoints + trialPoints
        trial['totalPoints'] = totalPoints
        #
        print(thisKey + ' ' + trial['trialCorrectKey'])
        print('total points accumulated: '+ str(totalPoints))
        #
        mywin.flip()
        
        if trial['trialNumber'] > 0:
            if (trial['trialNumber'] + 1 - newBlockTrialNum) % (blockList[currentBlock]['setSize'] * 10) == 0:
                newBlockTrialNum = trial['trialNumber'] + 1
                endOfBlock_text.text = 'End of block ' + str(currentBlock) + '. [Press space to continue]'
                endOfBlock_text.setAutoDraw(True)
                mywin.flip()
                allKeys = event.waitKeys(keyList=['escape','space','j','k','l'])
                for thisKey in allKeys:
                    if thisKey in ['escape']:
                        save_data()
                    elif thisKey in ['space','j','k','l']:
                        event.clearEvents()
                endOfBlock_text.setAutoDraw(False)
                break # go to next block

# Test #
testInstructions.setAutoDraw(True)
mywin.flip()
allKeys = event.waitKeys(keyList=['escape','space'])
for thisKey in allKeys:
    if thisKey in ['escape']:
        save_data()
        mywin.close()
        core.quit()
    elif thisKey in ['space']:
        event.clearEvents()
testInstructions.setAutoDraw(False)
trialStimA.pos = (-3,0)
trialStimB.pos = (3,0)

for trial in testTrials:
    mywin.flip()
    responded = False
    allKeys = event.waitKeys(maxWait=trial['testITI'],keyList=['escape'])
    for thisKey in allKeys or []:
        if thisKey in ['escape']:
            save_data()
            mywin.close()
            core.quit()
    trialStimA.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(trial['trialStimFolder_Left'])),'image'+str(int(trial['trialStimID_Left']))+'.jpg')
    trialStimA.setAutoDraw(True)
    trialStimB.image = os.path.join(sessionInfo['local_path'],'rlwmpst','images'+str(int(trial['trialStimFolder_Right'])),'image'+str(int(trial['trialStimID_Right']))+'.jpg')
    trialStimB.setAutoDraw(True)
    
    mywin.flip()
    
    trial['trialOnset'] = clock.getTime()
    allKeys = event.waitKeys(keyList=['0','1','escape'])

    for thisKey in allKeys or []:
        if thisKey in ['escape',]:
            save_data()
            mywin.close()
            core.quit()
        elif thisKey in ['0','1'] and len(allKeys) == 1:
            trial['resp'] = 1
            trial['respKey'] = thisKey
            trial['respRT'] = clock.getTime()-trial['trialOnset']
            responded = True
        elif len(allKeys) >> 1:
            trial['resp'] = 1
            trial['respKey'] = allKeys
            trial['respRT'] = clock.getTime()-trial['trialOnset']
            responded = True
        else:
            responded = False
    
    trialStimA.setAutoDraw(False)
    trialStimB.setAutoDraw(False)
    mywin.flip()
    event.clearEvents()

# payout
payout = str(int(totalPoints / 50) + (totalPoints % 50 > 0))  # Divide points by 50 to get money payout (rounded up)

testInstructions.setText('That\'s it! Thank you for participating.\n\n'
                        'You earned an extra $' + payout +'!') 

testInstructions.setAutoDraw(True)
mywin.flip()
allKeys = event.waitKeys()
testInstructions.setAutoDraw(False)

save_data()
core.quit()
