
import ScheduleItem as s
from fileManager import  *
from planner import  * 
import dateTime as dT


class Runner (object):
    def __init__(self, doctorsFileName, mothersFileName, scheduleFileName):
        self.doctorFileName = doctorsFileName
        self.maeFileName = mothersFileName
        self.scheduleFileName = scheduleFileName
    
    

    def run(self):
        doctorsHandler = DoctorsHandler(self.doctorFileName)
        mothersHandler = RequestsHandler(self.maeFileName)
        scheduleHandler = ScheduleHandler(self.scheduleFileName)
        scheduleHandler.loadAllSchedules()

        planner = schedulePlanner(doctorsHandler.loadAllDoctors(), 
                                  mothersHandler.loadAllRequestsOrderedByPriority(), 
                                  scheduleHandler)
        newScheduleHandler = planner.updateSchedule()
        updatedDoctors = planner.getDoctors()

        newScheduleHandler.writeSchedule()
        newDoctorsHandler = DoctorsHandler("", updatedDoctors, scheduleHandler.getScheduleDay(), scheduleHandler.getScheduleTime())
        newDoctorsHandler.writeDoctors()

def main():
    try :
        runner = Runner("./testSets_v1/testSet1/doctors10h70.txt", "./testSets_v1/testSet1/requests10h30.txt", "./testSets_v1/testSet1/schedule10h00.txt")
        runner.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


#if __name__ == "__main__":
#    main()