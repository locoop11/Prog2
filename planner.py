import Doctor as d
import Mother as m
import ScheduleItem as s
import dateTime as dT
import re
from fileManager import  *

    
# A comment
class schedulePlanner:
    def __init__(self, doctors, maes, scheduleHandler):
        self.doctors = doctors
        self.maes = maes
        self.schedule = scheduleHandler
        self.scheduleTime = scheduleHandler._headerTime
        self.scheduleDay = scheduleHandler._headerDay

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


        # 1. Create new schedule based on previous
        newSchedule = self.createNewScheduleBasedOnPrevious(self.schedule.getScheduleArray(), self.scheduleTime, self.scheduleDay)
        (newScheduleTime, newScheduleDay) = dT.computeNewTimes(self.scheduleTime, self.scheduleDay)
        newScheduleHandler = ScheduleHandler("", newSchedule, self.schedule._headerDay, self.schedule._headerTime)    

        for mae in self.maes:
            doctor  = self.getMatchingDoctor(mae, self.doctors) # get the doctor that is the best to do the request
            
            if( doctor != None):
                self.addToNewSchedule(doctor, mae, newScheduleHandler) # Updates doctor and the new schedule 
            else:
                # If a suitable doctor is not found, send request to another hospital
                self.sendRequestToOtherHospital(mae, newScheduleHandler, self.scheduleTime)

        return newScheduleHandler
    
    
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
            oldScheduleDate = scheduleDay +"|"+oldSchedule.getTime().replace("h", ":")
            if( dT.biggestDate(oldScheduleDate, newScheduleDate) == oldScheduleDate):
                newSchedule.append(oldSchedule)

        return newSchedule
    
    def addToNewSchedule(self, doctor, mae, newScheduleHandler):
        """
        this funcion adds the doctor and the request in the newSchedule, and updates the doctor carcateristics
        Requires:
        The doctor to add to the schedule. The request to append to the schedule. The newSchedule to append the request to. The time of the schedule. The day of the schedule.

        Ensures:
        The doctor is added to the schedule and the doctor characteristics are updated.
        """
        doctorScheduleTime = dT.biggestDate(newScheduleHandler.getScheduleDay() +"|"+newScheduleHandler.getScheduleTime().replace("h", ":"), newScheduleHandler.getScheduleDay() +"|"+doctor.getUltimoParto().replace("h", ":"))
        doctorScheduleTime = doctorScheduleTime.split("|")[1].replace(":", "h")
        if( doctorScheduleTime[:2] == "20" and newScheduleHandler.getScheduleTime()[:2] == "04"):
            newScheduleHandler.addScheduleItem(ScheduleItem(newScheduleHandler.getScheduleTime(), mae.getNome(), doctor.getNome()))
        elif ( doctorScheduleTime[:2] == "20"):
            return newScheduleHandler.addScheduleItem(ScheduleItem(doctorScheduleTime, mae.getNome(), "redirected to other network"))
        else:
            newScheduleHandler.addScheduleItem(ScheduleItem(doctorScheduleTime, mae.getNome(), doctor.getNome()))
        
        doctor.updateDoctor(doctorScheduleTime)
            
    


    def sendRequestToOtherHospital(self, mae, newScheduleHandler, scheduleTime):
        """
        Writes a request in the newSchedule with the message "redirected to other network" which signals that the request was sent to another hospital either because there are no doctors available 
        or because there are no doctors with the required skill level or even if the doctor does not have available time to perform the request.

        Requires:
        request that should be sent to another hospital, the schedule to which append the request to and the time of the schedule
        """	
        scheduleItem = ScheduleItem(scheduleTime, mae.getNome(), "redirected to other network")
        newScheduleHandler.addScheduleItem(scheduleItem)



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
            if( doctor.isDoctorSkillHigherOrEqual(mae) ):
                # If the doctor is available to do the request, check if he has the right skill
                # That is we need to check that the skill of the available doctor is equal or higher than the request
                if doctor.isAvailable():
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
        type = int(arr.getExperiencia())
        timeLastIntervention = int(arr.getUltimoParto().split("h")[0]) + int(arr.getUltimoParto().split("h")[1])
        print(timeLastIntervention + ", " + arr.getUltimoParto())
        accumHours = 999999
        if( arr.getMinAcomulados() != "weekly leave"):
            accumHours = int(arr.getMinAcomulados())
        accumTimeWeek = arr.getWeeklyWorkedHours()
        
        match = re.match(r'(\d{2})h(\d{2})', accumTimeWeek)
        if match:
            hours, minutes = map(int, match.groups())
        else:
            hours, minutes = 0, 0
        
        return (timeLastIntervention, -type, accumHours, hours, minutes)

        
    def prioritezeDoctors(self, listOfMatchingDoctors):
        listOfMatchingDoctors.sort(key=self.custom_sort_key)
        return listOfMatchingDoctors

    def getDoctors(self):
        return self.doctors
    
    def getSchedule(self):
        return self.schedule