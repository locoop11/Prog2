
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
    """
    Main program.
    Requires:
    Three command-line arguments, corresponding to the names of the files
    with the list of doctors, the list of birth assistances and the list of requests, respectively.
    """
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Error: invalid number of arguments.")
        print("Usage: python refresh.py <doctors filename> <schedule filename> <requests filename>")
        return
    
    # Extract the file names from the command-line arguments
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]

    doctorsFileName = ""
    requestsFilName = ""
    scheduleFileName = ""

    for file in sys.argv:
        if file.find("doctors") != -1:
            doctorsFileName = file
        if file.find("schedule") != -1:
            scheduleFileName = file
        if file.find("requests") != -1:
            requestsFilName = file
    if( doctorsFileName == "" or requestsFilName == "" or scheduleFileName == ""):
        print("Error: invalid file name.")
        print("Usage: python refresh.py <doctors filename> <schedule filename> <requests filename>")
        exit(1)
    try:
        #"Para os testes" runner = Runner("./testSets_v1/testSet1/doctors10h00.txt", "./testSets_v1/testSet1/requests10h30.txt", "./testSets_v1/testSet1/schedule10h00.txt")
        runner = Runner(doctorsFileName, scheduleFileName, requestsFilName)
        runner.run()
        

    except Exception as e:
        print(f"An error occurred: {e}")
    # Optionally, you can perform additional error handling here if needed
    # ...
    # Exit in a controlled way (e.g., with a specific exit code)
    exit(1)  # Exit with a non-zero exit code to indicate an error
    
    
    runner = Runner("./testSets_v1/testSet1/doctors10h00.txt", "./testSets_v1/testSet1/requests10h30.txt", "./testSets_v1/testSet1/schedule10h00.txt")
    runner.run()


if __name__ == "__main__":
    main()
        

