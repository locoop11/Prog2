# 2023-2024 Programação 1 (LTI)
# Grupo 26
# 60231 Tiago Carvalho
# 60253 Hugo Silva


class Mother ():

    def __init__ (self, nome, idade, pulseira, risco):
        self.nome = nome
        self.idade = idade
        self.pulseira = pulseira
        self.risco = risco


    def __str__ (self):
        return self.nome + ", " + str(self.idade) + ", " + str(self.pulseira) + ", " + str(self.risco)
    
    



    def getNome(self):
        return self.nome
    def getIdade(self):
        return self.idade
    def getPulseira(self):
        return self.pulseira
    def getRisco(self):
        return self.risco