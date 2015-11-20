import random, math, array, random
from psychopy import core,visual,event,parallel
from itertools import product

class Task:
    
    #speedTime = 0.5
    cueTime = 1.5
    fixTime = 0.5
    jitterTime = 1
    preFeedbackTime = .1
    feedbackTime = .4
    postFeedbackTime = .1
    
    
    def __init__(self,win,filename,nsubblocks,nblocks,blockSize,speedTime,trialTime):
        
        self.datafile = open(filename, 'a') #a simple text file with 'comma-separated-values'

        self.win = win
        self.nsubblocks = nsubblocks # this is the size of each block for trial randomization
        self.nblocks = nblocks # this is used to randomize trials
        self.blockSize = blockSize # this is the block size seen by participants.
        self.speedTime = speedTime
        self.trialTime = trialTime
        
        self.typeInstructions = visual.TextStim(win,text="Ac",pos=(0,0))
        
        self.feedback = visual.TextStim(win,text="",pos=(0,0))
        
        self.blockInstructions = visual.TextStim(win,text="",pos=(0,0))
        
        self.dotPatch = visual.DotStim(win, units='pix',color=(1.0,1.0,1.0), dir= 0,
            nDots=120, fieldShape='circle', fieldPos=(0.0,0.0),dotSize=3,fieldSize=250,
            dotLife=-1, #number of frames for each dot to be drawn
            signalDots='different', #are the signal and noise dots 'different' or 'same' popns (see Scase et al)
            noiseDots='direction', #do the noise dots follow random- 'walk', 'direction', or 'position'
            speed=1.00, coherence=0.5)
        
        self.fixation = visual.ShapeStim(win,
            units='pix',
            lineColor='white',
            lineWidth=2.0,
            vertices=((-25, 0), (25, 0), (0,0), (0,25), (0,-25)),
            closeShape=False,
            pos= [0,0])
        
        self.trialClock = core.Clock()
        
        # following returns a list with: id, type, coherence
        tids = list(product([0,1],[0,1],[.05,.1,.15,.25,.35,.5])) * self.nsubblocks
        
        self.tids = []
        #self.dirs = []
        #self.ttype = []
        #self.tcoherence = []
        
        for i in range(self.nblocks):
            random.shuffle(tids)
            #random.shuffle(tttype)
            
            self.tids += tids
            #self.ttype += tttype
            
            
        ## add 100% coherency block at the end
        tids = list(product([0,1],[0,1],[1.0])) * 30
        
        self.tids += tids
        
            
        #self.dirs = [0]*(self.ntrials/2) + [1]*(self.ntrials/2)
        #random.shuffle(self.dirs)
        
        #self.ttype = [0]*(self.ntrials/2) + [1]*(self.ntrials/2)
        #random.shuffle(self.ttype)
        
        self.tinstructions = ["ACCURATE","FAST"]
        
        self.datafile.write('trial,type(1=Ac,2=Sp),coherence,direction(1=L,2=R),response (1=L,2=R),responsetime,feedback (1=correct,2=incorrect,3=inTime,4=tooSlow,5=noResponse)\n')
        
    def Run(self):
        
        running = True
        trial = 1
        block = 1
        
        while running:#forever
            
            self.dotPatch._dotsXY = self.dotPatch._newDotsXY(self.dotPatch.nDots)
            # set direction
            self.dotPatch.setDir(180 - self.tids[trial - 1][0]*180)
            # set instructions
            self.typeInstructions.setText(self.tinstructions[self.tids[trial - 1][1]])
            # set coherence
            self.dotPatch.setFieldCoherence(self.tids[trial - 1][2])
            
            # show instruction for cueTime
            self.typeInstructions.draw()
            self.win.flip()
            
            core.wait(self.cueTime)
            # do nothing
                
            # draw jitter time
            jitter = random.random() * self.jitterTime
            self.win.flip()
            
            #core.wait(jitter)
            
            # show fixation 500 ms
            self.fixation.draw()
            self.win.flip()
            
            core.wait(self.fixTime)
                # do nothing
                
            # jitter with blank screen
            #self.win.flip()
            core.wait(self.jitterTime - jitter)
            
            # show stimulus 1500 ms
            self.trialClock.reset()
            ttime = -1.0
            rgiven = False
            response = -1
            event.clearEvents(eventType='keyboard')
            event.clearEvents('mouse')
            
            
            while (self.trialClock.getTime() < self.trialTime):
                if (rgiven == False):
                    self.dotPatch.draw()
                    self.win.flip()
                    for key in event.getKeys():
                        if key in ['a','b','escape']:
                            ttime = self.trialClock.getTime()
                            rgiven = True
                            if key in ['b']:
                                response = 0
                            if key in ['a']:
                                response = 1
                            if key in ['escape']:
                                self.win.close()
                                core.quit()
                            self.win.flip() # delete contents of window
                else:
                    break
                       
            # do nothing
            self.win.flip()
            core.wait(self.preFeedbackTime)
            
            feedcode = 0
            dfeed = 0
            # show feedback 400 ms
            if (ttime < 0):
                self.feedback.setColor("red")
                self.feedback.setText("No response")#
                #feedcode = codes.feedback_noResponse_on
                dfeed = 5
            else:
                if (self.tids[trial - 1][1] == 0):
                    # accuracy
                    if (response == self.tids[trial - 1][0]):
                        self.feedback.setText("correct")
                        self.feedback.setColor("green")
                        #feedcode = codes.feedback_correct_on
                        dfeed = 1
                    else:
                        self.feedback.setText("incorrect")
                        self.feedback.setColor("red")
                        #feedcode = codes.feedback_incorrect_on
                        dfeed = 2
                else:
                    if (ttime < self.speedTime):
                        self.feedback.setText("in time")
                        self.feedback.setColor("green")
                        #feedcode = codes.feedback_inTime_on
                        dfeed = 3
                    else:
                        self.feedback.setText("too slow")
                        self.feedback.setColor("red")
                        #feedcode = codes.feedback_tooSlow_on
                        dfeed = 4
            self.feedback.draw()
            self.win.flip()
            
            #while (self.trialClock.getTime() < 400):
            core.wait(self.feedbackTime)
                # do nothing
                
            self.datafile.write(
                str(trial) + ',' + 
                str(self.tids[trial - 1][0] + 1) + ',' + 
                str(self.tids[trial - 1][2]) + ',' + 
                str(self.tids[trial - 1][1] + 1) + ',' + 
                str(response + 1) + ',' +
                str(1000*ttime) +  ',' +
                str(dfeed) + '\n')
            
            if(trial == 6*self.nsubblocks*self.nblocks):
                running = False
            elif(trial == block*self.blockSize):
                # show end of block instructions and wait for response
                txt = "This is the end of block " 
                txt += str(block) + "\n\n" 
                txt += "You can now take a short rest. Please wait for the experimenter to continue the task."
                self.blockInstructions.setText(txt)
                self.blockInstructions.draw()
                self.win.flip()
                cont = False
                while (cont == False):
                    for key in event.getKeys():
                        if key in ['enter','return','escape']:
                            if key in ['enter','return']:
                                cont = True
                                block += 1
                            if key in ['escape']:
                                self.win.close()
                                core.quit()
             
            trial = trial + 1
            
            # remove feedback
            self.win.flip()
            
            core.wait(self.postFeedbackTime)
            
        
        self.datafile.close()
