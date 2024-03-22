class doctor:
    def __init__(self, nome, experiencia, ultimoParto, minAcomulados, ultimoDescanso):
        self.nome = nome
        self.experiencia = experiencia
        self.ultimoParto = ultimoParto
        self.minAcomulados = minAcomulados
        self.ultimoDescanso = ultimoDescanso

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
    
        