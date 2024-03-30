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
        doctorsReader = DoctorsReader(self.doctorFileName)
        mothersReader = MothersReader(self.maeFileName)
        scheduleReader = ScheduleReader(self.scheduleFileName)

        doctorsList = doctorsReader.getDoctorsList()
        mothersListByPriority = mothersReader.getMotherListByPriority()
        schedule = scheduleReader.getSchedule()
        
        planner = schedulePlanner(doctorsList, mothersListByPriority, schedule)
        doctors = planner.getDoctors()
        planner.updateSchedule()
        updatedDoctors = planner.getDoctors()
        newSchedule = planner.getSchedule()

        doctorsWriter = DoctorWriter(self.doctorFileName)
        mothersWriter = mothersWriter(self.maeFileName)
        scheduleWriter = scheduleWriter(self.scheduleFileName)



        

