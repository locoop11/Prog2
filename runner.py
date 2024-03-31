import mae as m
import doctor as d
import schedule as s
from fileManager import  *
from planner import  * 
import dateTime as dT

class runner (object):
    def __init__(self, doctorsFileName, mothersFileName, scheduleFileName):
        self.doctorFileName = doctorsFileName
        self.maeFileName = mothersFileName
        self.scheduleFileName = scheduleFileName

    def computeNewFileNames (self, scheduleTime, scheduleDay):
        """
        Computes the new file names for the schedule and doctors files. File names hour is increased by 30 minutes.
        Requires:
        scheduleTime is a string in the format HHhMM with the time of the current schedule
        scheduleDay is a string in the format DD-MM-YYYY with the day of the current schedule
        """
        (newScheduleTime, newScheduleDay) = dT.computeNewTimes(scheduleTime, scheduleDay)
        
        newScheduleFileName = "schedule" + newScheduleTime + ".txt"
        newDoctorsFileName = "doctors" + newScheduleTime + ".txt"

        return (newScheduleFileName, newDoctorsFileName)
    
    

    def run(self):
        doctorsHandler = DoctorsHandler(self.doctorFileName)
        mothersHandler = RequestsHandler(self.maeFileName)
        scheduleHandler = ScheduleHandler(self.scheduleFileName)

        planner = schedulePlanner(doctorsHandler.loadAllDoctors(), 
                                  RequestsHandler.loadAllRequestsOrderedByPriority(), 
                                  scheduleHandler.loadAllSchedules())
        planner.updateSchedule()
        updatedDoctors = planner.getDoctors()
        newSchedule = planner.getSchedule()




        

