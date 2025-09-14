import time
##import array

givenSongBPM = 70

print("\n\n\n\n\n")
#how long we want to record each period and 
# how often per second we listen
##RecordPeriod = 10
##SamplingRate = 10
#time between extends or time for delta BPM
playTime =30 


yn = "abcd"
while (yn != "y" and yn != "n"):
    print ("Is following mode on? (y/n)")
    yn = input()
    if (yn != "y" and yn != "n"):
        print("Sorry please answer 'y' or 'n'\n\n")
    if (yn == "y") :
        followingMode = True
    if (yn == "n"):
        followingMode = False




#psitive reinforcement for this cycle
yn = "abcd"
while (yn != "y" and yn != "n"):
    print ("Has the patient met a goal in this period? (y/n)")
    yn = input()
    if (yn != "y" and yn != "n"):
        print("Sorry please answer 'y' or 'n'\n\n")
    if (yn == "y") :
        EventFlagged = True
    if (yn == "n"):
        EventFlagged = False




#time events for frequency
#timeMarkers = []


if (not(followingMode)) :
    print ("What percent would you like to change BPM by:")
    PTIdeal = input()
    PTIdeal = int(PTIdeal)
    PTIdeal = givenSongBPM*(1+PTIdeal/100)



#running samplingRate per second for RecordPeriod
# seconds    time stuff will be fixed later

#add time control so this runs SamplingRate per second

print ("recording")
input ()
tStart = time.time()
steps = 1
while (steps<=4):
    input ()
    steps+=1

tFin = time.time()
#33% time increase reduction


timeCalibrate = 2/3
averageTime = 60*(steps+1)/((tFin-tStart)/timeCalibrate)
averageTime = round(averageTime)
#for i in RecordPeriod*SamplingRate :
#    if (keyispressed) :
#        timeMarkers.append(i)
#    if (Event Flagged) :
#        EventFlagged = True
print ("recording stopped")



# average time between timeMarkers in seconds
#averageT= ((timeMarkers(len(timeMarkers))-timeMarkers(0))/len(timeMarkers))/SamplingRate


prompt1 = "Extend song by "+str(playTime)+" seconds"
promptBPMFol = ", gradually change the BPM to "+str(averageTime)+" over a period of "+str(playTime)+" seconds"
promptEvent =", and add an upbeat flourish near the start of this section"
if (not(followingMode)) :
    promptBPMPT = ", gradually change the BPM to "+str(PTIdeal)+" over a period of "+str(playTime)+" seconds"

currentPromt = prompt1
if (followingMode) :
    currentPromt = currentPromt+promptBPMFol
else :
    currentPromt = currentPromt+promptBPMPT
if (EventFlagged) :
    currentPromt = currentPromt+promptEvent

print (currentPromt)