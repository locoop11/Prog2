from Doctor import Doctor as Doctor
from fileManager import ScheduleHandler as ScheduleHandler
from fileManager import RequestsHandler as RequestsHandler
from planner import *
from Mother import Mother as Mother

class TestPlanner :
    def __init__(self) :
        pass

    def runTests (self) :
        self.testPrioritizeDoctors()
        self.testGetMatchingDoctors()
        self.testGetMatchingDoctorsWeeklyLeave()
        self.testGetMatchingDoctorsWeeklyHoursExceeded()
        self.testGetMatchingDoctorsMartchMinAccumMins()
        self.testaddToNewSchedule()
        self.testsendRequestToOtherHospital()

    def testsendRequestToOtherHospital(self) :
        scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
        scheduleH.loadAllSchedules()
        planner = schedulePlanner([], [], scheduleH)
        oldScheduleSize = len(scheduleH._scheduleItems)
        mother = Mother('Isabel Sofia', 30, 'red', 'low')
        planner.sendRequestToOtherHospital(mother, scheduleH, '11h00')
        newScheduleSize = len(scheduleH._scheduleItems)
        assert newScheduleSize == oldScheduleSize +1, "The schedule should have increased by 1"
        assert str(scheduleH._scheduleItems[3]) == '11h00, Isabel Sofia, redirected to other network', "The last item in the schedule should be Isabel Sofia, redirected to other network"



    def testaddToNewSchedule(self) :
        carlotaCunha = Mother('Carlota Cunha', 30, 'red', 'low') #Carlota Cunha, 30, red, low
        abilioAmaral = Doctor('Abílio Amaral', 1, '11h05', 180, '28h00') #Abílio Amaral, 1, 11h05, 180, 28h00
        scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
        scheduleH.loadAllSchedules()
        numItemsBefore = len(scheduleH._scheduleItems)
        

        planner = schedulePlanner([], [], scheduleH)
        planner.addToNewSchedule(abilioAmaral, carlotaCunha, scheduleH)
        numItemsAfter = len(scheduleH._scheduleItems)
        assert numItemsAfter == numItemsBefore + 1, "The number of items in the schedule should have increased by 1"
        assert abilioAmaral.getUltimoParto() == '11h35', "The doctor's last birth should have been updated to 11h35"
        message = "The doctor's accumulated minutes should have been updated to 210, but is " + str(abilioAmaral.getMinAcomulados())
        assert abilioAmaral.getMinAcomulados() == 210, message
        message = "The doctor's worked hours since last break should have been updated to 28h30, but is " + abilioAmaral.getWeeklyWorkedHours()
        assert abilioAmaral.getWeeklyWorkedHours() == '28h30', message



    def testCreatePlannerWithEmptySchedule(self) :
        pass

    def testGetMatchingDoctorsWeeklyLeave(self) :  
        try :
            doctorsString = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 1, 10h50, 100, 7h40\nCarlos Castro, 0, 11h55, 240, 32h20\nDuarte Dantas, 3, 11h00, weekly leave, 15h20"
            doctorList = doctorsString.split("\n")
            objectList= []
            for line in doctorList :
                (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
                doc = Doctor(nome, int(experiencia), str(ultimoParto), str(minAcomulados), str(ultimoDescanso))
                objectList.append(doc)
            
            scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleH.loadAllSchedules()
            mothersH = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            planner = schedulePlanner(objectList, mothersH.loadAllRequestsOrderedByPriority(), scheduleH)
            matchedDoctor = planner.getMatchingDoctor(Mother('Carlota Cunha', 30, 'red', 'high'), objectList)
            assert matchedDoctor == None, "The only available doctor is in weekly leave therefore no doctor should be matched"
        except AssertionError as error:
            print(f"testGetMatchingDoctorsWeeklyLeave: failed. {error}")      

        print("testGetMatchingDoctorsWeeklyLeave: passed.")

    def testGetMatchingDoctorsMartchMinAccumMins(self) :  
        try :
            doctorsString = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 1, 10h50, 100, 7h40\nDuarte Dantas, 3, 11h00, 290, 39h30"
            doctorList = doctorsString.split("\n")
            objectList= []
            for line in doctorList :
                (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
                doc = Doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso))
                objectList.append(doc)
            
            scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleH.loadAllSchedules()
            mothersH = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            planner = schedulePlanner(objectList, mothersH.loadAllRequestsOrderedByPriority(), scheduleH)
            matchedDoctor = planner.getMatchingDoctor(Mother('Carlota Cunha', 30, 'red', 'low'), objectList)
            assert matchedDoctor.getNome() == 'Bernardo Biscaia', "From the two doctors available, the one with less accum mins should be matched"
        except AssertionError as error:
            print(f"testGetMatchingDoctorsMartchMinAccumMins: failed. {error}")      

        print("testGetMatchingDoctorsMartchMinAccumMins: passed.")

    def testGetMatchingDoctorsWeeklyHoursExceeded(self) :  
        try :
            doctorsString = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 1, 10h50, 100, 7h40\nCarlos Castro, 0, 11h55, 240, 32h20\nDuarte Dantas, 3, 11h00, 290, 39h30"
            doctorList = doctorsString.split("\n")
            objectList= []
            for line in doctorList :
                (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
                doc = Doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso))
                objectList.append(doc)
            
            scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleH.loadAllSchedules()
            mothersH = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            planner = schedulePlanner(objectList, mothersH.loadAllRequestsOrderedByPriority(), scheduleH)
            matchedDoctor = planner.getMatchingDoctor(Mother('Carlota Cunha', 30, 'red', 'high'), objectList)
            assert matchedDoctor == None, "The only available doctor has worked all the hours available in the week"
        except AssertionError as error:
            print(f"testGetMatchingDoctorsWeeklyHoursExceeded: failed. {error}")      

        print("testGetMatchingDoctorsWeeklyHoursExceeded: passed.")

    def testGetMatchingDoctors(self) :
        try :
            doctorsString = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 2, 10h50, 100, 7h40\nCarlos Castro, 0, 11h55, 240, 32h20\nDuarte Dantas, 3, 11h00, 290, 15h20"
            doctorList = doctorsString.split("\n")
            objectList= []
            for line in doctorList :
                (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
                doc = Doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso))
                objectList.append(doc)
            
            scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleH.loadAllSchedules()
            mothersH = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            planner = schedulePlanner(objectList, mothersH.loadAllRequestsOrderedByPriority(), scheduleH)
            matchedDoctor = planner.getMatchingDoctor(Mother('Carlota Cunha', 30, 'red', 'low'), objectList)
            assert matchedDoctor.getNome() == 'Duarte Dantas', "The doctor should be the one with the highest experience"
        except AssertionError as error:
            print(f"testGetMatchingDoctors: failed. {error}")      

        print("testGetMatchingDoctors: passed.")


    def testPrioritizeDoctors(self) :
        try :
            doctorsString = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 2, 10h50, 100, 7h40\nCarlos Castro, 0, 11h55, 240, 32h20\nDuarte Dantas, 3, 11h00, 290, 15h20"
            doctorList = doctorsString.split("\n")
            objectList= []
            for line in doctorList :
                (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
                doc = Doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso))
                objectList.append(doc)
            
            scheduleH = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleH.loadAllSchedules()
            mothersH = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            planner = schedulePlanner(objectList, mothersH.loadAllRequestsOrderedByPriority(), scheduleH)
            planner.prioritezeDoctors(objectList)
            assert objectList[0].getNome() == 'Duarte Dantas', "The first doctor should be the one with the highest experience"
            assert objectList[1].getNome() == 'Bernardo Biscaia', "The second doctor should be the one with the second highest experience"
            assert objectList[2].getNome() == 'Abílio Amaral', "The second doctor should be the one with the second highest experience"
            assert objectList[3].getNome() == 'Carlos Castro', "The second doctor should be the one with the second highest experience"
        except AssertionError as error:
            print(f"testPrioritizeDoctors: failed. {error}")
        print("testPrioritizeDoctors: passed.")

    def testPlannerGetters(self) :
        # Create a planner and then
        # get doctors must return the given doctors
        # get scheddule must return the given schedule
        # get mothers must return the given mothers
        pass

    def testUpdateSchedule(self) :
        pass 



        

tests = TestPlanner()
tests.runTests()