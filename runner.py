import mae as m
import doctor as d
import schedule as s
import fileManager as fM
from planner import  * 
import dateTime as dT

class runner (object):
    def __init__(self, doctoFileName, maeFileName, scheduleFileName):
        self.doctorFileName = doctoFileName
        self.maeFileName = maeFileName
        self.scheduleFileName = scheduleFileName

    def run(self):
        doctors = fM.doctorReader(self.doctorFileName)
        maes = fM.maeReader(self.maeFileName)
        schedule = fM.scheduleReader(self.scheduleFileName)
        
        doctorPlanner = doctorPlanner(doctors)   ####  sort doctors

        sortedMothers = maePlanner(maes)   #### sort maes

        scheduleBeeingPlanned = schedulePlanner(doctorPlanner, sortedMothers, schedule)
        upadatedSchedule = scheduleBeeingPlanned.updateSchedule()


    
        fM.doctorWriter(doctors)
        fM.scheduleWriter(upadatedSchedule)




        

