import doctor as doctor
import mae as mae
import dateTime as dateTime
class fileManager ():
    def __init__(self):
        self





class reader(fileManager):
    def __init__(self):
       self  


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
        

        
        
        
class doctorReader(reader):
    def __init__(self, fileName):
        (inFile) = super.removeHeader(fileName)
        doctors = []
        for line in inFile:
            line = line.strip()
            nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso = line.split(" ")
            doctors.append(doctor(nome, int(experiencia), str(ultimoParto), int(minAcomulados), str(ultimoDescanso)))
        
        return doctors
       

class maeReader(reader):
    def __init__(self, fileName):
        maes = []
        (inFile) = super.removeHeader(fileName)
        for line in inFile:
            line = line.strip()
            nome, idade, pulseira, risco = line.split(" ")
            maes.append(mae(nome, int(idade), str(pulseira), str(risco)))
        return maes

class scheduleReader(reader):
    def __init__(self, fileName):

        schedule = []
        (inFile) = super.removeHeader(fileName)
        for line in inFile:
            line = line.strip()
            nome, idade, pulseira, risco = line.split(" ")
            schedule.append(mae(nome, int(idade), str(pulseira), str(risco)))
        return schedule



class writer(fileManager):
    def __init__(self):
        self


    
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
    
class doctorWriter(writer):
    def __init__(self, doctors, scheduleDay, scheduleTime):
        newDoctorsFileName = super.computeNewFileNames(scheduleTime, scheduleDay)[1]
        header = super.saveHeader(newDoctorsFileName, scheduleDay, scheduleTime)
        with open(newDoctorsFileName, "w") as file:
            for line in header:
                file.write(line)
            for doctor in doctors:
                file.write(str(doctor) + "\n")
        return newDoctorsFileName

class scheduleWriter(writer):
    def __init__(self, schedule, scheduleDay, scheduleTime):
        newScheduleFileName = super.computeNewFileNames(scheduleTime, scheduleDay)[0]
        header = super.saveHeader(newScheduleFileName, scheduleDay, scheduleTime)
        with open(newScheduleFileName, "w") as file:
            for line in header:
                file.write(line)
            for mae in schedule:
                file.write(str(mae) + "\n")
        return newScheduleFileName
    
