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




        

