class fileManager ():
    def __init__(self):
        self

class fileManager ():
    def __init__(self):
        self

    def readDoctors(self):
        doctors = []
        with open("doctors.txt", "r") as file:
            for line in file:
                line = line.strip()
                nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso = line.split(" ")
                doctors.append(doctor(nome, int(experiencia), int(ultimoParto), int(minAcomulados), int(ultimoDescanso))
        return doctors

    def readMaes(self):
        maes = []
        with open("maes.txt", "r") as file:
            for line in file:
                line = line.strip()
                nome, idade, pulseira, risco = line.split(" ")
                maes.append(mae(nome, int(idade), int(pulseira), int(risco))
        return maes


    def writeDoctors(self, doctors):
        with open("doctors.txt", "w") as file:
            for doctor in doctors:
                file.write(str(doctor) + "\n")

    def writeMaes(self, maes):
        with open("maes.txt", "w") as file:
            for mae in maes:
                file.write(str(mae) + "\n")