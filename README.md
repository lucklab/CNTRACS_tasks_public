# Tasks used for the second study of the CNTRACS grant focus on test-retest reliability
*currently in the process of adding/changing information here... 

This repository contains scripts for most of the tasks used in the CNTRACS grant.
These versions do not have an option to run with EEG event codes, and have shorter ITIs than in study one (1.5s -> 1s)

Each task has its own folder, some have supplementary files such as images or sound clips.
In any case, each task is designed to run right out of a downloaded copy of its folder. 

The most straightfoward way to run these tasks is just to download or clone the entire repository.
*Changes may still be made to the tasks - you will have to redownload/pull the repository if this is the case*

### Technical details... (add more - maybe should be a different file)
The tasks are intended to work in Windows 10 and a newer version of PsychoPy (>3.2).

###### Monitors 
Default is 1920x1200px resolution - 52cm monitor width - 100cm viewing distance.

*If this is not how your setup is, you need to set these parameters in each script (near the top of the script where it defines the monitor)* 

### Task summaries

##### [Sensory Precision](Sensory_Precision) 
Participants fixate in the center of the screen as two bars (one black, one white) briefly appear 3.5 degrees from fixation. The task is to indicate using a keyboard (arrow keys) which side (left or right) the white bar was relative to the black bar. The spacing between the bars is controlled using a staircase (QUEST) and there are catch trials to estimate lapse rate.

**Duration:** ~ UPDATE FOR SHORTER VERSION

**Behavioral input:** Keyboard (L/R arrow keys)

##### [Working Memory](Working_Memory)
Participants fixate as 1 or 5 colored bars briefly appear 3.5 degrees from fixation. After a delay, a cursor replaces the fixation circle in the center of the screen, and the task is to click the location of the bar which color matched the color of the cursor.

**Duration:** ~ UPDATE FOR SHORTER VERSION

**Behavioral input:** Mouse

##### [Episodic Memory](Episodic_Memory)
Particpants are presented with 8 trial blocks of pairings between picures and bars on a 3.5 degree radius around the picture. For each encoding trial particpants must click the location of the bar. When the block finishes, particpants are presented with the picures, and must click where the bar was for that picture.

**Duration:** ~ UPDATE FOR SHORTER VERSION

**Behavioral input:** Mouse

##### [Reinforcement Learning](Reinforcement_Learning)
Participants are presented with 12 trial blocks of a set of pictures (3-6 images per block). After viewing the set of images, participants are instructed to choose between 3 keys (j, k, l) for a single image presented. Each image has a corresponding key that will earn points (1 or 2 points). Participants must try to learn which key corresponds with each image to obtain the maximum number of points. At the end of the 12 blocks, participants are presented with two images, each from a different block, and tasked with choosing the image that earned more points.

**Duration:** ~ UPDATE FOR SHORTER VERSION

**Behavioral input:** Keyboard (J/K/L, 1/0)

**Payment:** Participants get money equal to the number of points they receive in the trial blocks phase divided by 50 (The amount is output at the end, max = $11)

##### Effort Based Decision Making
*This task is needs to be downloaded and installed separately -- the new version is not uploaded yet...*

Participants are instructed to choose using keyboard keys (q or p) between two balloons (green or blue) to inflate up to a spike in order to receive a predetermined number of points. At the start of each trial the participant is informed of the probability (50% or 100%) of receiving points. The blue balloon will always require 20 button presses and the participant can only receive 1 point. The green balloon requires more button presses (100, 120, 150) but may yield more points. The object of the task is to earn as many points as possible.

**Duration:** ~??min

**Behavioral input:** Keyboard (q/p)

**Payment:** ??
