'''
    framework for running behavioral N-back tests  
    
    TODO:
    
'''
        
#imports
from psychopy import visual,core, sound, event,logging,gui
from random import randint, shuffle
import csv
from datetime import datetime
from nback_tests import vNback, aNback, nInterleaved, nPaired, nUnpaired, infolooper


     
#structures
     
#list that holds introductory information for the subject
startInfo = ['press return to continue',
             'welcome subject '
             'in this experiment you will preform a series of N-back tests that involve visual and auditory components',
             'each test is prefaced by a short explanation',
             'if you have any remaining questions, or would no longer like to take part in this pilot study, please notify an experimenter now']
wnd = visual.Window([1024,768],fullscr=False,allowGUI=True,units='pix',color=(-1,-1,-1)) #psychopy window
funcLis = [] #list to hold all testing functions


#functions
def seqGen(length): #this is for generating test sequences, returns a list of int in range 0-3 of desired length
    seq = []    
    for i in range(length):
        seq.append(randint(0,3))
    return seq        

def popFuncLis(lis): #creates a list of test functions shuffled in a random order.
    '''
    within here all the test functions should be appeneded to the funcLis list, ie. all the tests we will run.
    if new functions are created, they need to be added here.
    '''
    lis.append(vNback)
    lis.append(aNback)
    lis.append(nInterleaved)
    lis.append(nPaired)
    lis.append(nUnpaired)
        
    shuffle(lis) #randomize order of tests performed


#main routine
if __name__ == '__main__':
    '''
    file output setup, creates a dictionary that holds participant information and timestamp,
    and creates an output writer that stores participant score.
    '''    
    data={}
    data['expname']='N-Back'
    data['expdate']=datetime.now().strftime('%Y%m%d_%H%M')
    data['participantid']=''
    dlg=gui.DlgFromDict(data,title='Input data',fixed=['expname','expdate'],order=['expname','expdate','participantid'])
    if not dlg.OK:
        core.quit()
        
    outName='P_%s_%s.csv'%(data['participantid'],data['expdate'])
    outFile = open(outName, 'wb')
    outWr = csv.writer(outFile)
    
    
    '''
    loop for presenting each test to participants
    '''
    popFuncLis(funcLis) #populate list of test functions 
    wnd.flip() #initialize window    
    infolooper(startInfo, wnd) #loop through initial information 
    #loop that executes test functions
    for test in funcLis:
        print str(test)+": test started"
        test(outWr, 2, wnd, seqGen(2)) #filled with the generic arguments for all our test functions, change the number in seqGen() to make the list longer/shorter
        print str(test)+": test ended"
        
    '''
    cleanup/file closing/participant thank you message
    '''
    outFile.close() #close the output file
    thanks=visual.TextStim(wnd,'thank you for your participation, all tests are concluded?', color=(1.0,1.0,1.0)) #thank the subject for their participation
    thanks.draw()
    wnd.flip()
    event.waitKeys(keyList=['return'])    
    wnd.close()     #close the psychopy windo
    print "all tests concluded"    
    
