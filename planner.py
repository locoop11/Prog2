import doctor as d
import mae as m
import schedule as s
import fileManager as fM
import datetime as dT

    
# A comment
class schedulePlanner:
    def __init__(self, doctors, maes, schedule):
        self.doctors = doctors
        self.maes = maes
        self.schedule = schedule
        self.scheduleTime = schedule.getScheduleTime()
        self.scheduleDay = schedule.getScheduleDay()

    def updateSchedule(self): #  nextTime falta meter isto
        """
        Update birth assistance schedule assigning the given birth assistance requested
        to the given doctors, taking into account a previous schedule.
        
        Requires:
        doctors, a list of doctors already sorted, mothers, a list of mothers already sorted
        Ensures:
        a list of birth assistances, representing the schedule updated at
        the current update time (= previous update time + 30 minutes),
        assigned according to the conditions indicated in the general specification
        of the project (omitted here for the sake of readability).
        """
        # doctors exemple: ((Guilherme Gaspar, 2, weekly leave, 60, 40h10)(Horácio Horta, 3, 14h50, 140, 7h40)Ildefonso Inácio, 2, weekly leave, 60, 40h10)(José Justo, 2, 14h50, 60, 15h20))

        # request exemple: (Hortênsia Holmes, 22, yellow, low)
        # schedule exemple: (14h00, Eduarda Elói, Horácio Horta)


        # 1. Sort request by priority and doctors by skill
        newSchedule = self.createNewScheduleBasedOnPrevious(self.schedule, self.scheduleTime, self.scheduleDay)
        (newScheduleTime, newScheduleDay) = fM.computeNewTimes(self.scheduleTime, self.scheduleDay)

    

        for mae in self.maes:
            doctor  = self.getMatchingDoctor(mae, self.doctors) # get the doctor that is the best to do the request
            
            if( doctor != None):
                self.addDoctorToNewSchedule(doctor, mae, newSchedule, newScheduleTime, newScheduleDay) # Updates doctor and the new schedule 
            else:
                # If a suitable doctor is not found, send request to another hospital
                self.sendRequestToOtherHospital(mae, newSchedule, self.scheduleTime)

        return newSchedule
    
    
    def computeNewFileNames (self, scheduleTime, scheduleDay):
        """
        Computes the new file names for the schedule and doctors files. File names hour is increased by 30 minutes.
        Requires:
        scheduleTime is a string in the format HHhMM with the time of the current schedule
        scheduleDay is a string in the format DD-MM-YYYY with the day of the current schedule
        """
        (newScheduleTime, newScheduleDay) = dT.computeNewTimes(scheduleTime, scheduleDay)
        
        newScheduleFileName = "schedule" + newScheduleTime + ".txt"
        newDoctorsFileName = "doctors" + newScheduleTime + ".txt"

        return (newScheduleFileName, newDoctorsFileName)
    
    
    def createNewScheduleBasedOnPrevious(self, previousSched, scheduleTime, scheduleDay):
        """
        Creates a new schedule copying to the new schedule all requests that are not yet performed
        Requires:
        the previous schedule to copy schedules from, the time of the schedule and the day of the schedule
        Ensures:
        To return a new schedule containing all requests that are not yet performed
        """
        newScheduleTime = dT.updateHours(scheduleTime)
        if( newScheduleTime[:1] == "20"):
            newScheduleTime = "04h00"
            newScheduleDay = dT.updateDay(scheduleDay)
        else:
            newScheduleDay = scheduleDay

        newScheduleDate = newScheduleDay +"|"+newScheduleTime.replace("h", ":")
        newSchedule = []
        for oldSchedule in previousSched:
            oldScheduleDate = scheduleDay +"|"+oldSchedule[0].replace("h", ":")
            if( dT.biggestDate(oldScheduleDate, newScheduleDate) == oldScheduleDate):
                newSchedule.append(oldSchedule)

        return newSchedule
    
    def addDoctorToNewSchedule(self, doctor, request, newSchedule, scheduleTime, scheduleDay):
        """
        this funcion adds the doctor and the request in the newSchedule, and updates the doctor carcateristics
        Requires:
        The doctor to add to the schedule. The request to append to the schedule. The newSchedule to append the request to. The time of the schedule. The day of the schedule.

        Ensures:
        The doctor is added to the schedule and the doctor characteristics are updated.
        """
        scheduleDoctorName = doctor.getNome()
        scheduleMaeName = request.getNome()
        doctorScheduleTime = dT.biggestDate(scheduleDay +"|"+scheduleTime.replace("h", ":"), scheduleDay +"|"+doctor.getNome().replace("h", ":"))
        doctorScheduleTime = doctorScheduleTime.split("|")[1].replace(":", "h")
        if( doctorScheduleTime[:2] == "20" and scheduleTime[:2] == "04"):
            doctorScheduleTime = scheduleTime
        else:
            if( doctorScheduleTime[:2] == "20"):
                return self.sendRequestToOtherHospital(request, newSchedule, scheduleTime)
            
    


    def sendRequestToOtherHospital(self, mae, newSchedule, scheduleTime):
        """
        Writes a request in the newSchedule with the message "redirected to other network" which signals that the request was sent to another hospital either because there are no doctors available 
        or because there are no doctors with the required skill level or even if the doctor does not have available time to perform the request.

        Requires:
        request that should be sent to another hospital, the schedule to which append the request to and the time of the schedule
        """	
        newSchedule.append((scheduleTime, mae.getName(), "redirected to other network"))




    def getMatchingDoctor (self, mae, doctors):
        """
        Calculates the doctors that have the required skill and availability to perform the request given

        Requires:
        The request to be performed and the list of all doctors

        Ensures:
        A doctor that has the required skill and availability to perform the request given. The doctors are sorted by priority which means that when more than one doctor is available 
        to perform the request the doctor with the highest priority is returned. Priority is given by the lowest accumulated hours in the day, the lowest accumulated hours in the week,
        """	
        listOfMatchingDoctors = []
        for doctor in doctors:
            # A doctor is NOT availbale to do the request if:
            #    he is already fully booked for the day
            #    doctor has not enough hours free to do the request
            if( d.isDoctorSkillHigherOrEqual(doctor, mae) ):
                # If the doctor is available to do the request, check if he has the right skill
                # That is we need to check that the skill of the available doctor is equal or higher than the request
                if d.isDoctorAvailable(doctor):
                    listOfMatchingDoctors.append(doctor)
                #sort the doctors most qualifeid first in the list
        if len(listOfMatchingDoctors) == 0:
            return None
        else:
            self.prioritezeDoctors(listOfMatchingDoctors)
            return listOfMatchingDoctors[0]
        
    def custom_sort_key(self, arr):
        """
        Function to be used to sort doctors by priority
        """
        type = int(arr[const.DOCT_TYPE_IDX])
        accumHours = int(arr[const.DOCT_ACCUM_HOURS_DAY_IDX])
        accumTimeWeek = arr[const.DOCT_ACCUM_TIME_WEEK_IDX]
        
        match = re.match(r'(\d{2})h(\d{2})', accumTimeWeek)
        if match:
            hours, minutes = map(int, match.groups())
        else:
            hours, minutes = 0, 0
        
        return (-type, accumHours, hours, minutes)

        
    def color(self, color):
        """
        Converts a color to an integerr to be used in sorting
        """
        if color == 'red':
            return 3
        elif color == 'yellow':
            return 2
        elif color == 'green':
            return 1
        else:
            return 10

    def prioritezeDoctors(self, listOfMatchingDoctors):
        listOfMatchingDoctors.sort(key=self.custom_sort_key)

    def getDoctors(self):
        return self.doctors
    
    def getSchedule(self):
        return self.schedule