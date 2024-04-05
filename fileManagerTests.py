# 2023-2024 Programação 1 (LTI)
# Grupo 26
# 60231 Tiago Carvalho
# 60253 Hugo Silva



from fileManager import * 
import os
class testReaders :
    def __init__(self) :
        pass

    def runTests (self) :
        self.testDoctorHandler()
        self.testRequestsHandler()
        self.testRequestsByPriority()
        self.testScheduleHandler()
        self.testReadingEmptyFile()
        self.testFileWithWrongName()
        self.testFileWithWrongDate()
        self.testReadNonExistingFile()
        self.testFileWithWrongDate2()
        self.testWriteDoctors()
        self.testGetScheduleArray()
        #testReaders.testMothersReader()
        #testReaders.testScheduleReader()

    def testGetScheduleArray(self):
        try:
            scheduleHandler = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleHandler.loadAllSchedules()
            arr = scheduleHandler.getScheduleArray()
            assert len(arr) == 3, "testGetScheduleArray: The array should have 3 elements, but has " + str(len(arr))
        except AssertionError as error:
            print(f"testGetScheduleArray: Failed. {error}")
        print("testGetScheduleArray: passed.")

    def testRequestsByPriority(self):
        try:
            reqHandler = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            reqHandler.loadAllRequestsOrderedByPriority()
            expected = "Alberta Asunção, 35, green, high\nBrunilde Bastos, 28, green, high\nCarlota Cunha, 30, red, low\n"
            assert str(reqHandler) == str(expected), "testRequestsByPriority: The Mothers in the file were not sorted correctly:\n" \
                + str(reqHandler) + "!=\n" + str(expected)
        except AssertionError as error:
            print(f"testRequestsByPriority: Failed. {error}")
        print("testRequestsByPriority: passed.")

    def testRequestsHandler(self) :
        try:
            reqHandler = RequestsHandler("./testSets_v1/testSet1/requests10h30.txt")
            reqHandler.loadAllRequests()
            expected = "Brunilde Bastos, 28, green, high\nCarlota Cunha, 30, red, low\nAlberta Asunção, 35, green, high\n"
            assert str(reqHandler) == str(expected), "testRequestsHandler: The Mothers in the file were not the same read by handler:\n" \
                + str(reqHandler) + "!=\n" + str(expected)
        except AssertionError as error:
            print(f"testRequestsHandler: Failed. {error}")
        print("testRequestsHandler: passed.")


    def testScheduleHandler (self) :
        try:
            scheduleHandler = ScheduleHandler("./testSets_v1/testSet1/schedule10h00.txt")
            scheduleHandler.loadAllSchedules()
            expected = "9h50, Maria Machado, Bernardo Biscaia\n10h10, Eduarda Elói, Bernardo Biscaia\n10h45, Fernanda Fonseca, Abílio Amaral\n"
            assert str(scheduleHandler) == str(expected), "testScheduleHandler: The Mothers in the file were not the same read by handler:\n" \
                + str(scheduleHandler) + "!=\n" + str(expected)
        except AssertionError as error:
            print(f"testScheduleHandler: Failed. {error}")
        print("testScheduleHandler: passed.")

    def testDoctorHandler(self):
        """
        Test the doctor reader.
        """
        docsHandler = DoctorsHandler("./testSets_v1/testSet1/doctors10h00.txt")
        docsHandler.loadAllDoctors()
        expected = "Abílio Amaral, 1, 11h05, 180, 28h00\nBernardo Biscaia, 3, 10h30, 80, 7h20\nCarlos Castro, 2, 10h35, 220, 32h00\nDuarte Dantas, 3, 10h40, 270, 15h00\n"        
        
        try:
           assert str(docsHandler) == str(expected), "testDoctorReader: The docs in the file were not the same read by handler:" + str(docsHandler) + "!=" + str(expected)
        except AssertionError as error:
            print(f"testDoctorHandler: failed. {error}")

        
        print("testDoctorReader: passed.")

    def testReadingEmptyFile(self):
        """
        Test the doctor reader.
        """
        docsHandler = DoctorsHandler("./testSets_v1/testSet0/Emptydoctors10h00.txt")
        try :
            docsHandler.loadAllDoctors()
            assert False, "testReadingEmptyFile: The file was empty and should have raised an exception."
        except ValueError as e:
            pass
        except AssertionError as error:
            print(f"testReadingEmptyFile: failed. {error}")

        print("testReadingEmptyFile: passed.")
    
    def testFileWithWrongName(self) :
        try :
            doctorsHandler = DoctorsHandler("./testSets_v1/testSet0/wrongFileName10h00.txt")
            assert False, "testFileWithWrongName: The file had a wrong name it should raise an exception"
        except ValueError as e :
            print(f"testFileWithWrongName: passed. {e}")
        except AssertionError as error:
            print(f"testFileWithWrongName: failed. {error}")

        
    
    def testFileWithWrongDate(self):
        try :
            doctorsHandler = DoctorsHandler("./testSets_v1/testSet0/wrongHourdoctors25h00.txt")
            assert False, "testFileWithWrongName: The file had a wrong name it should raise an exception"
        except ValueError as e :
            print(f"testFileWithWrongDate: passed. {e}")
        except AssertionError as error:
            print(f"testFileWithWrongDate: failed. {error}")

    def testFileWithWrongDate2(self):
        try :
            doctorsHandler = DoctorsHandler("./testSets_v1/testSet0/wrongHourdoctors23h61.txt")
            assert False, "testFileWithWrongName: The file had a wrong name it should raise an exception"
        except ValueError as e :
            print(f"testFileWithWrongDate: passed. {e}")
            return True
        except AssertionError as error:
            print(f"testFileWithWrongDate2: failed. {error}")

        

    def testReadNonExistingFile(self) :
        try :
            doctorsHandler = DoctorsHandler("./testSets_v1/testSet0/doctors23h55.txt")
            assert doctorsHandler != None , "testReadNonExistingFile: We should be able to create handlers even if file does not exist"
            doctorsHandler.loadAllDoctors()
            assert False, "testReadNonExistingFile: Reading doctors from a non existing file should raise exception"
        except FileNotFoundError as e :
            print(f"testFileWithWrongDate: passed. {e}")
            return True
        except AssertionError as error:
            print(f"testReadNonExistingFile: failed. {error}")

    def testWriteDoctors(self):
        try :
            expectedFileName = "doctors10h30.txt"
            doctorsHandler = DoctorsHandler("./testSets_v1/testSet1/doctors10h00.txt")
            doctorsHandler.loadAllDoctors()[2].updateDoctor("11h00")
            docsHandler2 = DoctorsHandler("", doctorsHandler._doctors, doctorsHandler._headerDay, doctorsHandler._headerTime)   
            docsHandler2.writeDoctors()
            
            doctorsHandler1 = DoctorsHandler(expectedFileName)
            doctorsHandler1.loadAllDoctors()
            assert doctorsHandler1.loadAllDoctors()[2].getUltimoParto() == "11h30", "testWriteDoctors: The doctors were not written correctly. Expected 11h30, got " + doctorsHandler1.loadAllDoctors()[2].getUltimoParto()
            assert doctorsHandler1.loadAllDoctors()[2].getMinAcomulados() == 250, "testWriteDoctors: The doctors were not written correctly. Expected 250, got " + str(doctorsHandler1.loadAllDoctors()[2].getMinAcomulados())
            assert doctorsHandler1.loadAllDoctors()[2].getWeeklyWorkedHours() == "32h30", "testWriteDoctors: The doctors were not written correctly. Expected 32h30, got " + doctorsHandler1.loadAllDoctors()[2].getWeeklyWorkedHours()
            os.remove(expectedFileName)
        except AssertionError as error:
            print(f"testWriteDoctors: failed. {error}")
        print("testWriteDoctors: passed.")

tests = testReaders()
tests.runTests()