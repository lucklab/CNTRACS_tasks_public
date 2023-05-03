## This is a demo for how to fit a mixture model to data from the CNTRACTS WM task
## there should be one sample data file included next to this script (its my own data)
## - Kurt Winsler (kurtwinsler@gmail.com)

# Usually this would be done per subject, per experimental condition
# Here I just apply it to one subject, separately at two set sizes

# Some background on this model...

# This mixture model models the response error as a mixture of two distributions in a circular space
# A uniform distribution - which represents guessing
#   (i.e. completely random responses would generate a uniform distribution)

# And a Von Mises dsitribution (normal distribution in circular space) - which represents non-guessing
#   (i.e. responses to information which made it into memory should have response errors closer to 0)

# Thus the model can estimate these parameters:
# The mean of the Von Mises distribution (here, fixed at 0)
# The precision of the Von Mises distribution (Kappa), which can be thought of as inversely relatede to the variance of a normal distribution
# The mixture parameter, which is the ratio of the response distribution which comes from the two distibutions
#   (e.g. 25% from uniform, 75% from Von Mises)
#   This means the model estimates the subject was guessing for 25% of the responses, not guessing for 75% of the responses
#   We refer to this parameter as "Pmem" (proportion in memory), which is the percent of the distribution from not guessing
#   So 1 minus Pmem, would be the percentage of trials the model estimates is from random guessing

# Summary of parameters estimated by this script:
# Kappa -> how narrow the Von Mises distribution is -> how precise the VWM representation is -> Higher values = more precision 
# Pmem -> how much of the total distribution is from Von Mises distribution -> what proportion of trials made it into VWM -> Higher values = more trials in memory
# Rsqr -> R squared -> how well the mixture model predicts the actual data -> Higher values = better fit
# AvError -> This is not from the mixture model, just the average of all the absolute values of the response errors

#### Setup + functions ####

## load packages
library(CircStats)
library(readxl)
library(rlang)
library(Hmisc)
library(dplyr)
library(tidyr)

# set directory (will need to be changed to match your directory...)
setwd("C:/Users/kwinsler/Documents/GitHub/CNTRACS_tasks_public/Working_Memory/analysis_demo")

## Functions ##

# Wrap angular differences function
wrap <- function(x, xmin, xmax){
  wrap.error <- x - floor((x-xmin)/(xmax-xmin))*(xmax-xmin)	
}

# Likelihood function (with kappa and pmem)
# used to fit the mixture model
MixMod <-function(theta,y) { 
  #Data
  TargetError <-y;
  #Target Based density
  kr <- theta[1];
  #proportion parameters
  alpha <- theta[2]; #target-based
  # log likelihood
  logl <- sum(-log((alpha*dvm(TargetError,0,kr)  + (1-alpha)/(2*pi))));
  
  return(logl)
  
}

## Fit mixture model function
# with or without r squared calculation
# one starting value
# the MultiFit function below uses this function

FitMix <- function(subdata, # one subject's data
                   start_vals = c(20,0.9), # starting values (kappa, pmem)
                   kei_low = c(0.001,0), # lower bound for kei parameter
                   kei_high = c(1000,1), # upper bound for kei parameter
                   rsquared = FALSE) { # whether or not to calculate (and return) rsquared
  
  ## Fit mixture model
  TError <-wrap(rad(subdata$error),-pi,pi) # get error
  
  MixtureFit <-optim(start_vals, MixMod, y = TError, method="L-BFGS-B", 
                     lower=kei_low, upper=kei_high, control=list(maxit=2000))
  
  ## Get various parameters
  EstKappa <- as.numeric(MixtureFit$par[1]) # precision
  EstPmem <- as.numeric(round(MixtureFit$par[2],2)) # made it into memory
  EstLikelihood <- as.numeric(MixtureFit$value) # likelihood
  nTrials <- as.numeric(length(TError)) # N of trials used
  
  # Get average error (not actually used for anything here, but can be useful to output)
  avError <- mean(abs(wrap(subdata$error, -180,180)))
  
  if (rsquared == FALSE){
    
    # Output data
    output <- list(Kappa = EstKappa,
                   Pmem = EstPmem,
                   AvError = avError,
                   Likelihood = EstLikelihood)
    
    return(output)
  } # else function continues -> r squared will be calculated and output
  
  ## Calculate r squared (observed vs predicted)
  
  # Use histogram density for observed
  histSteps <- seq(-180,180,length=60)
  xspace <- seq(-pi,pi,length = length(histSteps)-1) # x axis
  binsize <- deg(xspace[2])-deg(xspace[1])  # bin size in degree
  
  histplot = hist(subdata$error, breaks= histSteps, plot = F)
  
  observed <- histplot$density
  
  # Generate model prediction
  predict <- EstPmem * dvm(xspace,0,EstKappa) + (1 - EstPmem)/(2*pi)
  predictNorm <- predict/sum(predict)/binsize
  
  # compute r-squared
  r <- cor(predictNorm,observed)
  rsquared <- r^2
  
  # Make output
  
  # Output data
  output <- list(Kappa = EstKappa,
                 Pmem = EstPmem,
                 AvError = avError,
                 Likelihood = EstLikelihood,
                 Rsqr = rsquared)
  
  return(output)
  
}

## Wrapper for above function
# fits runs multiple times with gridsearch of different starting values
# passes output for highest likelihood

MultiFit <- function(subdata, # subset of larger data 
                     kappa_startvals, # list of kappa starting values
                     pmem_startvals, # list of pmem starting values
                     kei_low = c(0.001,0), # lower bound for kei parameter
                     kei_high = c(1000,1), # upper bound for kei parameter
                     rsquared = FALSE) { # whether or not to calculate (and return) rsquared
  
  # number of starting value combos
  if (rsquared == TRUE){
    fits <- data.frame(matrix(0, nrow = length(kappa_startvals) * length(pmem_startvals), ncol = 5))
    colnames(fits) <- c('Kappa','Pmem','AvError', 'Rsqr','Likelihood')
  }
  if (rsquared == FALSE){
    fits <- data.frame(matrix(0, nrow = length(kappa_startvals) * length(pmem_startvals), ncol = 4))
    colnames(fits) <- c('Kappa','Pmem','AvError','Likelihood')
  }
  
  # loop over kappa start vals
  nfit = 1
  for (this_kappa in kappa_startvals){
    
    # loop over pmem starting values
    for (this_pmem in pmem_startvals){
      
      this_start_vals <- c(this_kappa, this_pmem)
      
      # try fit
      fit <- try(FitMix(subdata,
                        start_vals = this_start_vals,
                        kei_low = kei_low,
                        kei_high = kei_high,
                        rsquared = rsquared)) # dont supress error?
      
      if (class(fit) == "try-error"){ next } # skip if error

      # add data
      if (rsquared == TRUE){ 
        row <- c(fit$Kappa, fit$Pmem, fit$AvError, fit$Rsqr, fit$Likelihood)
      }
      if (rsquared == FALSE){ 
        row <- c(fit$Kappa, fit$Pmem, fit$AvError, fit$Likelihood)
      }
      
      fits[nfit,] <- row
      
      nfit = nfit + 1
    } # end pmem loop
    
  } # end kappa loop
  
  fits <- fits[fits$Likelihood != 0, ] # exclude 0 likelihood
  
  # get best fit... (highest likelihood)
  ml <- max(fits$Likelihood)
  bestFit <- fits[fits$Likelihood == ml,]
  
  # take just one... (in case identical likelihood value)
  if (length(bestFit$Kappa) > 1){
    bestFit <- bestFit[1,]
  }
  
  if (rsquared == FALSE){
    output <- list(Kappa = bestFit$Kappa,
                   Pmem = bestFit$Pmem,
                   AvError = bestFit$AvError)
  }
  
  if (rsquared == TRUE){
    output <- list(Kappa = bestFit$Kappa,
                   Pmem = bestFit$Pmem,
                   AvError = bestFit$AvError,
                   Rsqr = bestFit$Rsqr)
  }

  return(output)
  
}

#### Fit example ####

# load data (here its just one file)
dat <- read_excel("WM_Capacity_BEH_2023_May_03_1045_000.csv.xlsx")

# calculate error, must be done and named error 
dat$error <- wrap(dat$probedAngle - dat$respAngle, -180,180)

# Split by set size
dat_ss1 <- dat[dat$setSize == 1, ]
dat_ss5 <- dat[dat$setSize == 5, ]

# different starting values to try
# here its 3 kappas and 3 pmems, so MultiFit will try 3x3 fits and take the best one
kappas <- c(5,10,20)
pmems <- c(0.5, 0.7, 0.9)

# or you could just use the FitMix function, with default values or set your own

# fit data
# Set size 1
fit_ss1 <- MultiFit(dat_ss1, rsquared = TRUE, kappa_startvals = kappas, pmem_startvals = pmems)
print(fit_ss1) # these are the fit values

# Set size 5
fit_ss5 <- MultiFit(dat_ss5, rsquared = TRUE, kappa_startvals = kappas, pmem_startvals = pmems)
print(fit_ss5) # these are the fit values


#### Demo to make a histogram with fit line ####
histSteps <- seq(-180,180,length=60)

## Set size 1

# make a histogram 
histplot = hist(dat_ss1$error, breaks= histSteps,probability=T, plot=T,xlim=c(-180,180),ylim=c(0,0.1), 
                xlab="ReponseError", cex=0.1, main = "test_subject_SS1")

# get parameters from fit
xspace <- seq(-pi,pi,length = length(histSteps)-1) # x axis
pguess <- as.numeric(1 - fit_ss1$Pmem) # guess% (1 - pmem)
kr <- as.numeric( fit_ss1$Kappa) # kappa - precision
alpha <- as.numeric(fit_ss1$Pmem) # mixture ratio - pmem
binsize <- deg(xspace[2])-deg(xspace[1])  # bin size in degrees

# generate model prediction (the line)
predict <- alpha*dvm(xspace,0,kr)+ (pguess)/(2*pi)
predictNorm <- predict/sum(predict)/binsize

# plot the line
points(deg(xspace), predictNorm, type="l",lwd=2, col="red")


## Set size 5

# make a histogram 
histplot = hist(dat_ss5$error, breaks= histSteps,probability=T, plot=T,xlim=c(-180,180),ylim=c(0,0.1), 
                xlab="ReponseError", cex=0.1, main = "test_subject_SS5")

# get parameters from fit
xspace <- seq(-pi,pi,length = length(histSteps)-1) # x axis
pguess <- as.numeric(1 - fit_ss5$Pmem) # guess% (1 - pmem)
kr <- as.numeric( fit_ss5$Kappa) # kappa - precision
alpha <- as.numeric(fit_ss5$Pmem) # mixture ratio - pmem
binsize <- deg(xspace[2])-deg(xspace[1])  # bin size in degrees

# generate model prediction (the line)
predict <- alpha*dvm(xspace,0,kr)+ (pguess)/(2*pi)
predictNorm <- predict/sum(predict)/binsize

# plot the line
points(deg(xspace), predictNorm, type="l",lwd=2, col="red")

