class ScheduleItem(object):
    def __init__(self, time, mae, doctor):
        self.time = time
        self.mae = mae
        self.doctor = doctor
        self.time = time
        


    

    def __str__(self):
        return self.time + ", " + str(self.mae) + ", " + str(self.doctor)
    
    def getTime(self):
        return self.time
    def getMae(self):
        return self.mae
    def getDoctor(self):
        return self.doctor
    def getScheduleDay(self):
        return self.day