import doctor as doctor
import mae as mae
import dateTime as dateTime
class FileManager ():
    def __init__(self, fileName):
        self.fileName = fileName
        self.fileContents = []
        self.fileHeader = []


class Reader(FileManager):
    def __init__(self, fileName):
       super(fileName)


    def removeHeader(filename):
        """
        Removes the header from a file.
        Requires:
        filename is a string with the name of the file to write to
        Ensures:
        To raise an exception if the file does not exist or if the header is not correct
        """
        l=[]
        i = 0
        f = None
        fileTime = filename.split(".")[0][-5:]
        fileType = ""
        if( filename.find("schedule") != -1):
            fileType = "Schedule:"
        if ( filename.find("doctors") != -1):
            fileType = "Doctors:"
        if ( filename.find("requests") != -1):
            fileType = "Mothers:"


        try:
            f = open(filename, "r")
            for line in f.readlines():
                l.append(line.strip())
            scheduleTime = l[3]
            scheduleDay = l[5]
            fileHeaderType = l[6]
            for i in l[:7]:
                l.remove(i)
        except Exception as e:
            raise e
        finally:
            if( f != None): 
                f.close()

        r=[]
        for line in l:
            r.append(line)
        
        if( fileHeaderType != fileType):
            raise ValueError("File head error: scope inconsistency between name and header in file " + filename + ".")
        

        return r, scheduleTime, scheduleDay
        

class doctorReader(Reader):
    def __init__(self, fileName):
        super(fileName)
        (inFile) = super.removeHeader(fileName)
        self.fileContents = []
        for line in inFile:
            line = line.strip()
            (nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso) = line.split(" ")
            self.fileContents.append(doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso)))
       

class maeReader(Reader):
    def __init__(self, fileName):
        super(fileName)
        self.fileContents = []
        (inFile) = super.removeHeader(fileName)
        for line in inFile:
            line = line.strip()
            nome, idade, pulseira, risco = line.split(" ")
            self.fileContents.append(mae(nome, int(idade), str(pulseira), str(risco)))

class scheduleReader(Reader):
    def __init__(self, fileName):

        self.fileContents = []
        (inFile) = super.removeHeader(fileName)
        for line in inFile:
            line = line.strip()
            nome, idade, pulseira, risco = line.split(" ")
            self.fileContents.append(mae(nome, int(idade), str(pulseira), str(risco)))



class Writer(FileManager):
    def __init__(self, fileName):   
        super(fileName) 


    
    def saveHeader(filename, scheduleDay, scheduleTime):
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
        (newScheduleTime, newScheduleDay) = dateTime.computeNewTimes(scheduleTime, scheduleDay)

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
    
class doctorWriter(Writer):
    def __init__(self, fileName, doctors, scheduleDay, scheduleTime):
        super(fileName)
        newDoctorsFileName = super.computeNewFileNames(scheduleTime, scheduleDay)[1]
        header = super.saveHeader(newDoctorsFileName, scheduleDay, scheduleTime)
        with open(newDoctorsFileName, "w") as file:
            for line in header:
                file.write(line)
            for doctor in doctors:
                file.write(str(doctor) + "\n")
        return newDoctorsFileName

class scheduleWriter(Writer):
    def __init__(self, fileName, schedule, scheduleDay, scheduleTime):
        super(fileName)
        newScheduleFileName = super.computeNewFileNames(scheduleTime, scheduleDay)[0]
        header = super.saveHeader(newScheduleFileName, scheduleDay, scheduleTime)
        with open(newScheduleFileName, "w") as file:
            for line in header:
                file.write(line)
            for mae in schedule:
                file.write(str(mae) + "\n")
        return newScheduleFileName
    
