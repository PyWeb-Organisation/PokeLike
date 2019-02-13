#-*- coding: utf-8 -*-

# Importation des modules complémentaires nécéssaires :
import os
import sys
import time

# Création des variables globales du module :
LOGS = {"Info": [], "System": [], "Warning": [], "Error": []}

LOGS_COLORS = {"Info": "", "System": "", "Warning": "", "Error": "", "Reset": ""}

# Création des objets du module
class Log:
    """
    """
    def __init__(self, message, level="System", worker="MAIN-THREAD"):
        self.texte = "[{}][{}][{}] - {}".format(time.ctime(), worker, level, message)
        self.level = level
        LOGS[level].append(self)

    def log(self):
        log_file = "GameData\\Logs\\last_logs.log"
        with open(log_file, "a") as file:
            file.write(self.texte + "\n")
            file.close()

        print(LOGS_COLORS[self.level] + self.texte + LOGS_COLORS["Reset"])

# Création des fonctions du module
def log(message, level="System", worker="MAIN-THREAD"):
    Log(message, level, worker).log()

# Lancement du module :
log("========== New logs ==========")
