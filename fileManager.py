
from Doctor import Doctor as Doctor
from Mother import Mother as Mother
from schedule import Schedule as Schedule
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

    def saveHeader(self, filename, scheduleDay, scheduleTime):
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
        (newScheduleTime, newScheduleDay) = dateTime.computeNewTimes(self._fileTime, self._fileDay)

        header = []
        header.append("Organization:\n")
        header.append("SmartH\n")
        header.append("Hour:\n")
        header.append(newScheduleTime + "\n")
        header.append("Day:\n")
        header.append(newScheduleDay + "\n")
        if( filename.find("schedule") != -1):
            header.append("Schedule:\n")
        else :
            header.append("Doctors:\n")

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



        

class DoctorsHandler(FileManager):
    def __init__(self, fileName):
        super().__init__(fileName)
        self._doctors = []
       
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
        self._mothers.sort(key=lambda x: (x.getRisco(), -self.__color(x.getPulseira()), -int(x.getIdade()), x.getNome()))
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
    def __init__(self, fileName):
        super().__init__(fileName)
        self._schedules = []

    def loadAllSchedules(self):
        self._fileContents = []
        self._schedules = []
        self.loadData()
        self.removeHeader()
        for line in self._fileContents:
            line = line.strip()
            (time, motherName, doctorName) = line.split(", ")
            schedule = Schedule(time, motherName, doctorName)
            self._schedules.append(schedule)
        return self._schedules

    def __str__(self) -> str:
        result = ""
        for schedule in self._schedules :
            result += str(schedule).strip() + "\n"
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
    