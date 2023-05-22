# In-person, behavioral tasks for phase 3 of the CNTRACS consortium

This repository contains PsychoPy scripts for most of the tasks used in phase three of the CNTRACS grant.
These versions do not have an option to run with EEG event codes, but those versions are available upon request.

### Technical information
###### Environment

The tasks were written and tested to work in Windows 10 and versions of PsychoPy from the year 2019/2020, when our data collection for these tasks began.
We are not actively maintaining these tasks to work on other operating systems or newer versions of PsychoPy, however most or all of the code should still work in other enviroments with a little troubleshooting.

If you wish to use the latest version of PsychoPy that these tasks were developed/tested in, it can be downloaded [here.](https://github.com/psychopy/psychopy/releases/tag/2020.2.10)

###### Set up

Each task has its own folder, and each has supplementary files such as images.
Each task is designed to run right out of a downloaded copy of its folder. 

The most straightfoward way to run these tasks is just to download or clone the entire repository, and then copy over the folder for the task you wish to run.
The folder can be placed in any local directory, but the organization in that folder needs to stay the same.

Included with each task is a folder called "analysis_demo" which has a sample data file and an R script to load and analyze that data file.
This folder is not used by the PsychoPy scipt, so it can be moved or deleted.

###### Monitors 

Default is 1920x1200px resolution - 52cm monitor width - 100cm viewing distance.

*If this is not how your setup is, you need to set these parameters in each script (near the top of the script where it defines the monitor)* 

### Task summaries

There is more information about each of the tasks in their respective scripts.

##### [Sensory Precision](Sensory_Precision) 
Participants fixate in the center of the screen as two bars (one black, one white) briefly appear 3.5 degrees from fixation. The task is to indicate using a keyboard (arrow keys) which side (left or right) the white bar was relative to the black bar. The spacing between the bars is controlled using a staircase (QUEST) and there are catch trials to estimate lapse rate.

**Parameters measured:** Sensory precision threshold, lapse rate

**Duration:** ~12-15 minutes

**Behavioral input:** Keyboard (L/R arrow keys)

##### [Working Memory](Working_Memory)
Participants fixate in the center of the screen as 1 or 5 colored bars briefly appear 3.5 degrees from fixation. After a delay, a cursor replaces the fixation circle in the center of the screen, and the task is to click the location of the bar which color matched the color of the cursor.

**Parameters measured:** Visual working memory precision (Kappa), proportion of trials in working memory (Pmem). For both set size 1 and 5

**Duration:** ~25-30 minutes

**Behavioral input:** Mouse

##### [Episodic Memory](Episodic_Memory)
Particpants are presented with 8-trial blocks of pairings between picures and bars on a 3.5 degree radius around the picture. For each encoding trial particpants must click the location of the bar. When the block finishes, particpants are again presented with the picures in shuffled order, and must click where the bar was for that picture.

**Parameters measured:** Episodic memory precision (Kappa), proportion of trials in episodic memory (Pmem).

**Duration:** ~27-32 minutes

**Behavioral input:** Mouse

##### [Reinforcement Learning](Reinforcement_Learning)
Participants are presented with 12 trial blocks of a set of pictures (3-6 images per block). After viewing the set of images, participants are instructed to choose between 3 keys (j, k, l) for a single image presented. Each image has a corresponding key that will earn points (1 or 2 points). Participants must try to learn which key corresponds with each image to obtain the maximum number of points. At the end of the 12 blocks, participants are presented with two images, each from a different block, and tasked with choosing the image that earned more points.

**Duration:** ~30-40 minutes

**Behavioral input:** Keyboard (J/K/L, 1/0)

**Payment:** Participants get money equal to the number of points they receive in the trial blocks phase divided by 50 (The amount is output at the end, max = $11)

##### [Effort Based Decision Making](https://github.com/lnccbrown/task-effort)
Participants are instructed to choose using keyboard keys (q or p) between two balloons (green or blue) to inflate up to a spike in order to receive a predetermined number of points. At the start of each trial the participant is informed of the probability (50% or 100%) of receiving points. The blue balloon will always require 20 button presses and the participant can only receive 1 point. The green balloon requires more button presses (100, 120, 150) but may yield more points. The object of the task is to earn as many points as possible.

*This task does not use PsychoPy and is hosted on a separate repository*

**It can be accessed here:** https://github.com/lnccbrown/task-effort
