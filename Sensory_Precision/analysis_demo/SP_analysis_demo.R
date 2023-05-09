## This is a demo for how to get the estimates out of data from the CNTRACTS SP task
## there should be one sample data file included next to this script (its my own data)
## - Kurt Winsler (kurtwinsler@gmail.com)

# Usually this would be done per subject, per experimental condition
# Here I just apply it to one subject

# This is a very simple task, with a very simple analysis

# The two parameters it measures are:
# Sensory precision threshold: the angular separation between two bars which gives an accuracy of 82% 
# Lapse rate: and estimate of what percent of trials the participant lapses on
#  (two times the percent correct on very easy 'catch' trials)

# All this information can be found in the last trial of the experiment

#### Setup + functions ####

## load packages
library(readxl)
library(dplyr)
library(tidyr)

# set directory (will need to be changed to match your directory...)
setwd("C:/Users/kwinsler/Documents/GitHub/CNTRACS_tasks_public/Sensory_precision/analysis_demo")


# load data (here its just one file)
dat <- read_excel("Sensory_Precision_BEH_2023_May_09_1155_000.csv.xlsx")

# get last trial info
LastTrial_estimates <- dat %>%
  filter(trialNumber == 399) %>% # trial 399 is 400th trial 
  select(Participant, currentThresholdEst, questLapseRate) %>% # get columns
  mutate(LapseRateEst = 2*questLapseRate) # multiply % incorrect on catchtrials by 2

print(LastTrial_estimates)

# currentThresholdEst = The best estimate of the threshold (threshold after last trial)
# questLapseRate = percent incorrect on the catch trials
# LapseRateEst = 2 times this value ^ (because chance is 50%)

# Another way to calculate lapse rate:
lapse_dat <- dat %>%
  filter(catchTrial == 1) %>% # just get catch trials
  summarize(nTrials = n(), # number of catch trials
            nCorrect = sum(respACC), # number of correct catch trials
            percentCorrect = nCorrect/nTrials, # percent correct
            percentIncorrect = 1-percentCorrect, # percent incorrect
            LapseRate = 2*percentIncorrect) # lapse rate estimate

print(lapse_dat)


### I should have purposefully missed some catch trials to make the example better...
# Here I'll set some catch trials to incorrect for this example...

# set 3 catch trials to incorrect (RespAcc is col 23)
dat[1,23] <- 0
dat[10,23] <- 0
dat[12,23] <- 0

# now with a non-zero lapse rate...
lapse_dat <- dat %>%
  filter(catchTrial == 1) %>% # just get catch trials
  summarize(nTrials = n(), # number of catch trials
            nCorrect = sum(respACC), # number of correct catch trials
            percentCorrect = nCorrect/nTrials, # percent correct
            percentIncorrect = 1-percentCorrect, # percent incorrect
            LapseRate = 2*percentIncorrect) # lapse rate estimate

print(lapse_dat)
