from mae import mae
import dateTime as dT

class doctor:
    def __init__(self, nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso):
        self.nome = nome
        self.experiencia = experiencia
        self.ultimoParto = ultimoParto
        self.minAcomulados = minAcomulados
        self.ultimoDescanso = ultimoDescanso

    def isDoctorAvailable(self):
        """
        Checks thast a doctor is available to perform a request, ie is not in weekly leave and has enough hours to perform the request
        Requires:
        The doctor to check if is available
        Ensures to return a boolean value True if the doctor is available and False otherwise
        """
        if self.getMinAcomulados != "weekly leave" :
            if dT.updateHours(self.getMinAcomulados == "4"):
                return False
        return True

    def isDoctorSkillHigherOrEqual(self, mae):
        """
        Checks if a doctor skill is enough for a given request
        Requires: 
        The doctor to check if has the required skill and the request to be performed.
        Ensures:
        To return a boolean value True if the doctor has the required skill and False otherwise
        """
        if mae.getRisco() == 'high':
            if self.getExperiencia == '2' or self.getExperiencia == '3':
                return True
            else:
                return False
        return True


    def __str__(self):
        return self.nome + " " + str(self.experiencia) + " " + str(self.ultimoParto) + " " + str(self.minAcomulados) + " " + str(self.ultimoDescanso)
    








    def getNome(self):
        return self.nome 
    def getExperiencia(self):
        return self.experiencia 
    def getUltimoParto(self):
        return self.ultimoParto 
    def getMinAcomulados(self):
        return self.minAcomulados 
    def getUltimoDescanso(self):
        return self.ultimoDescanso
    
        