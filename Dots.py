#!/usr/bin/env python
from psychopy import visual, event, core, data, gui, misc, parallel
import Instructions, StartMainInstructions, Task

debug = False
speedTime = 500

if debug == True:
    nsubblocks = 1
    nblocks = 1
    blockSize = 6
    #speedTime = .4

    #ntrials2 = 12
    #nblocks2 = 1
    #blockSize2 = 6#

    #ntrials3 = 4
    #nblocks3 = 2
    #blockSize3 = 4
else:
    nsubblocks = 5
    nblocks = 4
    blockSize = 120
    #speedTime = .4

    #ntrials2 = 30
    #nblocks2 = 4
    #blockSize2 = 120

    #ntrials3 = 100
    #nblocks3 = 2
    #blockSize3 = 100

# uncomment for debug run
#ntrials = 4
#nblocks = 4
#blockSize = 4


#create a window to draw in
myWin =visual.Window((1280,1024), allowGUI=True,
    bitsMode=None, units='norm', winType='pyglet', color=(-1,-1,-1))

# Admin
expInfo = {'subject':'test','date':data.getDateStr(),'practice':True,'speed time':speedTime,'trial time':1500}
#expInfo['dateStr']= data.getDateStr() #add the current time
#expInfo['practice'] = True

#present a dialogue to change params
ok = False
while(not ok):
    dlg = gui.DlgFromDict(expInfo, title='Moving Dots', fixed=['dateStr'],order=['date','subject','practice','speed time','trial time'])
    if dlg.OK:
        misc.toFile('lastParams.pickle', expInfo)#save params to file for next time
        ok = True
    else:
        core.quit()#the user hit cancel so exit


# setup data file
fileName = 'Data/' + expInfo['subject'] + expInfo['date'] + '.csv'
dataFile = open(fileName, 'w') #a simple text file with 'comma-separated-values'
dataFile.write('subject = ' + str(expInfo['subject']) + "; date = " + str(expInfo['date']) + "; speed time = " + str(expInfo['speed time']) + "; trial time = " + str(expInfo['trial time']) + '\n')
dataFile.close()
   
trialClock = core.Clock()
speedTime = float(expInfo['speed time'])/1000
trialTime = float(expInfo['trial time'])/1000
practiceTask = expInfo['practice']

#myPort = parallel.ParallelPort(address=0x0378)
#myPort = parallel.ParallelPort()
instr = Instructions.Instructions(myWin,practiceTask)
instr.Run()


if practiceTask == True:
    practice = Task.Task(myWin,fileName,2,1,12,speedTime,trialTime)
    practice.Run()
    dataFile = open(fileName, 'a') #a simple text file with 'comma-separated-values'
    dataFile.write('End Practice\n')
    dataFile.close()

    instr = StartMainInstructions.Instructions(myWin)
    instr.Run()

task = Task.Task(myWin,fileName,nsubblocks,nblocks,blockSize,speedTime,trialTime)
task.Run()

endText = "This is the end of the experiment \n \n"
endText += "Thank your for your participation."
end = visual.TextStim(myWin, pos=[0,0],text=endText)
end.draw()
myWin.flip()

done = False
while not done:
    for key in event.getKeys():
        if key in ['escape','q']:
            done = True
            core.quit()
