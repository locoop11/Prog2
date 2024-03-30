class schedule(object):
    def __init__(self, time, day, mae, doctor):
        self.time = time
        self.mae = mae
        self.doctor = doctor
        self.day = day
        


    

    def __str__(self):
        return self.hora + " " + str(self.mae) + " " + str(self.doctor)
    
    def getScheduleTime(self):
        return self.time
    def getMae(self):
        return self.mae
    def getDoctor(self):
        return self.doctor
    def getScheduleDay(self):
        return self.day