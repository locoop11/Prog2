# 2023-2024 Programação 1 (LTI)
# Grupo 26
# 60231 Tiago Carvalho
# 60253 Hugo Silva


import dateTime as dT


class Doctor:
    def __init__(self, nome, experiencia, ultimoParto, minAcomulados, weeklyWorkedHours):
        self.nome = nome
        self.experiencia = experiencia
        self.ultimoParto = ultimoParto
        self.minAcomulados = minAcomulados
        self.weeklyWorkedHours = weeklyWorkedHours

    def isAvailable(self):
        """
        Checks thast a doctor is available to perform a request, ie is not in weekly leave and has enough hours to perform the request
        Requires:
        The doctor to check if is available
        Ensures to return a boolean value True if the doctor is available and False otherwise
        """
        if self.getMinAcomulados() != "weekly leave" :
            hoursUpdated = dT.updateHours(self.getWeeklyWorkedHours())
            if hoursUpdated[0] == "4":
                return False
        return True

    def isDoctorSkillHigherOrEqual(self, mother):
        """
        Checks if a doctor skill is enough for a given request
        Requires: 
        The doctor to check if has the required skill and the request to be performed.
        Ensures:
        To return a boolean value True if the doctor has the required skill and False otherwise
        """
        if  mother.getRisco() == 'high' :
            if self.experiencia == 2 or self.experiencia == 3:
                return True
            else:
                return False
        return True


    def __str__(self):
        return self.nome + ", " + str(self.experiencia) + ", " + str(self.ultimoParto) + ", " + str(self.minAcomulados) + ", " + str(self.weeklyWorkedHours)
    



    def updateDoctor(self, newScheduleTime): 
        """
        Updates the doctor schedule with the new time
        Requires:
        The new time to be updated
        Ensures:
        The doctor schedule is updated with the new time
        """
        self.ultimoParto = dT.updateHours(newScheduleTime)
        self.minAcomulados = (int(self.minAcomulados) + 30)
        self.weeklyWorkedHours = dT.updateHours(self.weeklyWorkedHours)




    def getNome(self):
        return self.nome 
    def getExperiencia(self):
        return self.experiencia 
    def getUltimoParto(self):
        return self.ultimoParto 
    def getMinAcomulados(self):
        return self.minAcomulados 
    def getWeeklyWorkedHours(self):
        return self.weeklyWorkedHours
    
        