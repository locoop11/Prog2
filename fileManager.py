
from Doctor import Doctor as Doctor
from Mother import Mother as Mother
from ScheduleItem import ScheduleItem as ScheduleItem
import dateTime as dateTime


class FileManager ():
    def __init__(self, fileName):
        self._fileName = fileName
        if( fileName.find("schedule") != -1):
            self._fileType = "Schedule:"
        elif ( fileName.find("doctors") != -1):
            self._fileType = "Doctors:"
        elif ( fileName.find("requests") != -1):
            self._fileType = "Mothers:"  
        else:
            raise ValueError("File name error: file name does not contain any of the expected keywords.")     

        self._fileName = fileName
        self._fileContents = []
        self._fileTime = self._fileName.split("/")[-1].split(".")[0][-5:]
        time = self._fileTime.split("h")
        try: 
            if int(time[0]) > 24 or int(time[0]) < 0  :
               raise ValueError("Hour must be between 0 and 24")
            if int(time[1])  > 60 or int(time[0]) < 0 :
                raise ValueError("Monute must be between 0 and 60")
        except ValueError as e:
            raise ValueError(f"File time error: time format is not correct. Expected format is HHhMM. {e}")

    def generateHeader(self):
        """
        Saves the header of the file.
        Requires:
        filename is a string with the name of the file to write to
        scheduleDay is a string in the format DD-MM-YYYY with the day of the current schedule
        scheduleTime is a string in the format HHhMM with the time of the current schedule

        Ensures:
        header is a list of strings with the header of the file
        The header changes according to the filename (schedule or doctors)
        """
        #(newScheduleTime, newScheduleDay) = dateTime.computeNewTimes(self._fileTime, self._headerDay)

        header = []
        header.append("Organization:\n")
        header.append("SmartH\n")
        header.append("Hour:\n")
        header.append(self._fileTime + "\n")
        header.append("Day:\n")
        header.append(self._headerDay + "\n")
        if( self._fileType == "Schedule:"):
            header.append("Schedule:\n")
        elif ( self._fileType == "Doctors:"):
            header.append("Doctors:\n")
        else:
            raise ValueError(f"Save header error. File type {self._fileType} is unknown.")

        return header
    
    def loadData(self) :
        f = None
        try:
            # Read the file into contents
            f = open(self._fileName, "r")
            for line in f.readlines():
                self._fileContents.append(line.strip())
        except Exception as e:
                raise e
        finally:
            if( f != None): 
                f.close()

    def writeData(self):
        header = self.generateHeader()
        with open(self._fileName, "w") as file:
            for line in header:
                file.write(line)
            for line in self._fileContents:
                file.write(str(line) + "\n")

    def removeHeader(self):
        if (len(self._fileContents) == 0):
            self.loadData()
        """
        Removes the header from a file.
        Requires:
        filename is a string with the name of the file to write to
        Ensures:
        To raise an exception if the file does not exist or if the header is not correct
        """

        if( len(self._fileContents) <= 7):
            raise ValueError("File head error: file " + self._fileName + " does not contain the expected header.")
        
        # Extract information from header
        self._headerTime = self._fileContents[3]
        self._headerDay = self._fileContents[5]
        self._headerType = self._fileContents[6]

        # Remove header
        for line in self._fileContents[:7]:
            self._fileContents.remove(line)

        # Check if the header is correct
        if( self._headerType != self._fileType):
            raise ValueError("File head error: scope inconsistency between name and header in file " + self._fileName + ".")


    def computeNewFileNames (self, scheduleTime, scheduleDay):
        """
        Computes the new file names for the schedule and doctors files. File names hour is increased by 30 minutes.
        Requires:
        scheduleTime is a string in the format HHhMM with the time of the current schedule
        scheduleDay is a string in the format DD-MM-YYYY with the day of the current schedule
        """
        (newScheduleTime, newScheduleDay) = dateTime.computeNewTimes(scheduleTime, scheduleDay)
        self._headerTime = newScheduleTime
        self._headerDay = newScheduleDay
        
        if( self._headerType == "Schedule:"):
            return  "schedule" + newScheduleTime + ".txt"
        if( self._headerType == "Doctors:"):
            return  "doctors" + newScheduleTime + ".txt"

        raise ValueError(f"Compute Files error. The file type {self._fileType} is unknown.")
        

class DoctorsHandler(FileManager):
    def __init__(self, fileName = "", initialDoctors = [], scheduleDay = None, scheduleTime = None) :
        doctorsFileName = fileName
        if( fileName == "" ):
            if( scheduleDay == None or scheduleTime == None):
                raise ValueError("ScheduleHandler error: scheduleDay and scheduleTime must be provided when fileName is empty.")
            self._headerType = "Doctors:"
            self._fileTime = scheduleTime
            self._headerTime = scheduleTime
            self._headerDay = scheduleDay
            doctorsFileName = self.computeNewFileNames (scheduleTime, scheduleDay)
                
        super().__init__(doctorsFileName)
        self._doctors = initialDoctors

    def writeDoctors(self):
        for doctor in self._doctors:
            self._fileContents.append(str(doctor))
        super().writeData()

    def loadAllDoctors(self) :
        self._fileContents = []
        self._doctors = []
        self.loadData()
        self.removeHeader()
        
        for line in self._fileContents:
            line = line.strip()
            (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(", ")
            doc = Doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso))
            self._doctors.append(doc)
        return self._doctors
    
    def __str__(self) -> str:
        result = ""
        for doc in self._doctors :
            result += str(doc) + "\n"
        return result

class RequestsHandler(FileManager):
    def __init__(self, fileName):
        super().__init__(fileName)
        self._mothers = []
    
    def loadAllRequestsOrderedByPriority (self) :
        if( len(self._mothers) == 0 ) :
            self.loadAllRequests()
        
        # Sort mothers by priority then by color (red, yellow, green), then by age descending then by name
        #self._mothers.sort(key=lambda x: (x[3], -self.__color(x[2]), -int(x[1]), x[0]))
        self._mothers.sort(key=lambda x: (-self.__color(x.getPulseira()), -int(x.getIdade()), x.getNome()))
        return self._mothers

    def __color(self, color):
        """
        Converts a color to an integer to be used in sorting
        """
        if color == 'red':
            return 3
        elif color == 'yellow':
            return 2
        elif color == 'green':
            return 1
        else:
            return 10
    def loadAllRequests(self) :
        self._fileContents = []
        self._mothers = []
        self.loadData()
        self.removeHeader()

        for line in self._fileContents:
            line = line.strip()
            (nome, idade, pulseira, risco) = line.split(", ")
            mother = Mother(nome, int(idade), str(pulseira), str(risco))
            self._mothers.append(mother)

        return self._mothers

    def __str__(self) -> str:
        result = ""
        for mother in self._mothers :
            result += str(mother).strip() + "\n"
        return result
 
class ScheduleHandler(FileManager):
    def __init__(self, fileName = "", initialSchedule = [], scheduleDay = None, scheduleTime = None):
        scheduleFileName = fileName
        if( fileName == "" ):
            if( scheduleDay == None or scheduleTime == None):
                raise ValueError("ScheduleHandler error: scheduleDay and scheduleTime must be provided when fileName is empty.")
            self._headerType = "Schedule:"
            self._fileTime = scheduleTime
            self._headerTime = scheduleTime
            self._headerDay = scheduleDay
            scheduleFileName = self.computeNewFileNames (scheduleTime, scheduleDay)
        super().__init__(scheduleFileName)
        self._scheduleItems = initialSchedule

    def writeSchedule(self):
        for schedule in self._scheduleItems:
            self._fileContents.append(str(schedule))
        super().writeData()

    def getScheduleArray (self) :   
        arr = []
        for item in self._scheduleItems:
            arr.append(item)
        return arr
    
    def getScheduleTime(self):
        return self._headerTime
    
    def getScheduleDay(self):
        return self._headerDay
    
    def addScheduleItem(self, scheduleItem):
        self._scheduleItems.append(scheduleItem)

    def saveSchedule():
        pass

    def loadAllSchedules(self):
        self._fileContents = []
        self._scheduleItems = []
        self.loadData()
        self.removeHeader()
        for line in self._fileContents:
            line = line.strip()
            (time, motherName, doctorName) = line.split(", ")
            scheduleItem = ScheduleItem(time, motherName, doctorName)
            self._scheduleItems.append(scheduleItem)
        return self._scheduleItems
    
    def __str__(self) -> str:
        result = ""
        for scheduleItem in self._scheduleItems :
            result += str(scheduleItem).strip() + "\n"
        return result


# class Writer(FileManager):
#     def __init__(self, fileName):   
#         super(fileName) 


    
#     def saveHeader(filename, scheduleDay, scheduleTime):
#         """
#         Saves the header of the file.
#         Requires:
#         filename is a string with the name of the file to write to
#         scheduleDay is a string in the format DD-MM-YYYY with the day of the current schedule
#         scheduleTime is a string in the format HHhMM with the time of the current schedule

#         Ensures:
#         header is a list of strings with the header of the file
#         The header changes according to the filename (schedule or doctors)
#         """
#         (newScheduleTime, newScheduleDay) = dateTime.computeNewTimes(scheduleTime, scheduleDay)

#         header = []
#         header.append("Organization:\n")
#         header.append("SmartH\n")
#         header.append("Hour:\n")
#         header.append(newScheduleTime + "\n")
#         header.append("Day:\n")
#         header.append(newScheduleDay + "\n")
#         if( filename.find("schedule") != -1):
#             header.append("Schedule:\n")
#         else :
#             header.append("Doctors:\n")

#         return header
    
# class doctorWriter(Writer):
#     def __init__(self, fileName, doctors, scheduleDay, scheduleTime):
#         super(fileName)
#         newDoctorsFileName = super.computeNewFileNames(scheduleTime, scheduleDay)[1]
#         header = super.saveHeader(newDoctorsFileName, scheduleDay, scheduleTime)
#         with open(newDoctorsFileName, "w") as file:
#             for line in header:
#                 file.write(line)
#             for doctor in doctors:
#                 file.write(str(doctor) + "\n")
#         return newDoctorsFileName

# class scheduleWriter(Writer):
#     def __init__(self, fileName, schedule, scheduleDay, scheduleTime):
#         super(fileName)
#         newScheduleFileName = super.computeNewFileNames(scheduleTime, scheduleDay)[0]
#         header = super.saveHeader(newScheduleFileName, scheduleDay, scheduleTime)
#         with open(newScheduleFileName, "w") as file:
#             for line in header:
#                 file.write(line)
#             for mae in schedule:
#                 file.write(str(mae) + "\n")
#         return newScheduleFileName
    