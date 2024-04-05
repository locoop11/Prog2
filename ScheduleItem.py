# 2023-2024 Programação 1 (LTI)
# Grupo 26
# 60231 Tiago Carvalho
# 60253 Hugo Silva



class ScheduleItem(object):
    def __init__(self, time, mae, doctor):
        self.time = time
        self.mae = mae
        self.doctor = doctor
        self.time = time
        


    

    def __str__(self):
        return str(self.time) + ", " + str(self.mae) + ", " + str(self.doctor) 
    
    def getTime(self):
        return self.time
    def getMae(self):
        return self.mae
    def getDoctor(self):
        return self.doctor
    def getScheduleDay(self):
        return self.day