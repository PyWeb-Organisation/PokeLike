#-*-coding:utf-8-*-

# Importation des modules complémentaires nécéssaires :
from multiprocessing import Queue
import threading

# Création des variables de contenance :
WORKERS = []

# Création des objets du module :
class QueueWorker(threading.Thread):
    """
    Thread effectuant une tache a partir d'une file
    """

    def __init__(self, call_function):
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.call_function = call_function
        self.kill = False

    def run(self):
        while not self.kill:
            action = self.queue.get()
            self.call_function(action)

    def destroy(self):
        self.kill = True

    def put(self, action):
        self.queue.put(action)

# Lancement du module :
if __name__ == "__main__":
    print("Nothing to see There")
