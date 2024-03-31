import Doctor
from planner import *

class TestPlanner :
    def __init__(self) :
        pass

    def runTests (self) :
        pass

    def testPrioritizeDoctors() :
        doctorsString = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 3, 10h50, 100, 7h40\nCarlos Castro, 2, 11h55, 240, 32h20\nDuarte Dantas, 3, 11h00, 290, 15h20"
        doctorList = doctorsString.split("\n")
        objectList = []
        for line in doctorList :
            (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
            objectList.append(Doctor(nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso))
        planner = planner(objectList, [], [])
        planner.prioritizeDoctors()

    def testPlannerGetters() :
        # Create a planner and then
        # get doctors must return the given doctors
        # get scheddule must return the given schedule
        # get mothers must return the given mothers
        pass

    def testUpdateSchedule() :
        pass 



        

tests = TestPlanner()
tests.runTests()