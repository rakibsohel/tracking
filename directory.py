#################################################################################
# Projet : NetBook                                                              #
# Nom    : Module tracking                                                      #
# Auteur : R.BEPARI                                                             #
# Date   : 15/07/2017                                                           #
#################################################################################


#################################################################################
# Bibliothèques                                                                 #    
#################################################################################
    
import os
import time
from   threading import Thread, RLock
import datetime

verrou = RLock()

#################################################################################
# Définition de la classe Monitoring                                            #    
#################################################################################
class Monitoring(Thread):

    """
    Cette classe permet de surveiller l'activité d'un répertoire.
    Elle s'éxecute en arrière plan.
    """

    def __init__(self,folder = "C:/GitHub",extension = ".TXT", vFname = "vFname"):            
        """
        Constructeur de la classe.
        """
        
        #Intialisation de l'objet Thread.
        Thread.__init__(self)
        self.deamon         = True

        #Initialisation des attributs
        self.typeFile       = list(extension)
        self.path           = list(folder)
        self.vFname         = str(vFname)
        self.freqMonitoring = 60
        
        os.chdir(self.path[0])

        #Création du répertoire des logs s'il n'existe pas.
        if(os.path.isdir(self.path[0]+"/logs") == False):
            os.mkdir("logs")
    
    def getFiles(self):
        """
        Cette fonction renvoie une liste contenant le contenu du répertoire.              
        """

        self.lst_files = []

        #Récupération des éléments avec l'extension typeFile du répertoire.
        self.cDirectory = []

        for self.link in self.path:
            self.cDirectory.extend(os.listdir(self.link))

        #Recherche des fichiers avec les extensions.
        for self.fileName in self.cDirectory:        

            for self.ext in self.typeFile:
                
                if((self.fileName.endswith(self.ext.lower())) or (self.fileName.endswith(self.ext.upper()))):
                    self.lst_files.append(self.fileName)

        return(self.lst_files)

    def getNewElmt(self,lst_a, lst_b):
        """
        Cette fonction renvoie une liste des éléments différents entre deux listes.   
        """
        
        #Les deux listes à comparer.
        self.lst_a       = lst_a
        self.lst_b       = lst_b

        #Liste contenant la divergence entre les deux listes.
        self.lst_newElmt = []

        #Tri des éléments des listes.
        self.lst_a.sort()
        self.lst_b.sort()

        #Détections de la plus grande liste.
        if(len(self.lst_b) > len(self.lst_a)):
            for self.elm in self.lst_b:
                try:
                    self.lst_a.index(self.elm)
                except:
                    #Ajout de l'élément dans la nouvelle liste.
                    #Si l'élément n'existe pas dans la petite liste.
                    self.lst_newElmt.append(self.elm)
        else:
            for self.elm in self.lst_a:
                try:
                    self.lst_b.index(self.elm)
                except:
                    #Ajout de l'élément dans la nouvelle liste.
                    #Si l'élément n'existe pas dans la petite liste.
                    self.lst_newElmt.append(self.elm)

        return(self.lst_newElmt)

    def run(self):
        """
        Fonction de détection de l'activité dans le répertoire                       
        
        """
        with verrou:
            print("*********************************************")
            print("Monitoring -> ["+self.vFname+"] ["+"|".join(self.path)+"]")            
            print("Start...")
            self.lst_file = sorted((self.getFiles()))
            self.nPrev    = len(self.lst_file)
            time.sleep(5)
            print("Monitoring...")
            print("*********************************************")

        while 1:

            with verrou:                               
                
                self.ilst_file = sorted((self.getFiles()))
                self.iPrev    = len(self.ilst_file)                

                self.lst_Modif = self.getNewElmt(self.lst_file,self.ilst_file)
                self.nModif    = len(self.lst_Modif)                

                #Détection des fichiers supprimés.
                if(self.nPrev > self.iPrev) and (self.nModif != 0):

                    #Récupération de la date et uniquement de l'heure.
                    self.tmps = datetime.datetime.now()
                    self.logFileName = str(self.tmps.year)+"_"+str(self.tmps.month)+"_"+str(self.tmps.day)+"__"+str(self.tmps.hour)

                    #Création ou ouverture du fichier si existant log.
                    self.fileLog  = open(self.path[0]+"/logs/"+self.vFname+"_"+self.logFileName+"H.log","a")                    

                    #Écriture l'événement dans le fichier.
                    print("================================================")
                    for self.nElmt in self.lst_Modif:

                        #Ecriture dans le fichier log.
                        self.fileLog.write("- ["+str(self.tmps.year)+str(self.tmps.month)+str(self.tmps.day)
                                           +str(self.tmps.hour)+str(self.tmps.minute)+str(self.tmps.second)+"] ["+self.vFname+"] ["+self.nElmt+"]\n")

                        #Affichage dans la console.
                        print("- ["+str(self.tmps.year)+str(self.tmps.month)+str(self.tmps.day)
                              +str(self.tmps.hour)+str(self.tmps.minute)+str(self.tmps.second)+"] [["+self.vFname+"] ["+self.nElmt+"]")
                        
                    print("================================================")

                    self.fileLog.close()

                #Détection des fichiers ajoutés.            
                if(self.nPrev < self.iPrev) and (self.nModif != 0):

                    #Récupération de la date et uniquement de l'heure.
                    self.tmps = datetime.datetime.now()
                    self.logFileName = str(self.tmps.year)+"_"+str(self.tmps.month)+"_"+str(self.tmps.day)+"__"+str(self.tmps.hour)

                    #Création ou ouverture du fichier si existant log.
                    self.fileLog  = open(self.path[0]+"/logs/"+self.vFname+"_"+self.logFileName+"H.log","a")                      

                    #Écriture l'événement dans le fichier.
                    print("================================================")
                    for self.nElmt in self.lst_Modif:

                         #Ecriture dans le fichier log.                        
                         self.fileLog.write("+ ["+str(self.tmps.year)+str(self.tmps.month)+str(self.tmps.day)
                                            +str(self.tmps.hour)+str(self.tmps.minute)+str(self.tmps.second)+"] ["+self.vFname+"] ["+self.nElmt+"]\n")

                         #Affichage dans la console.
                         print("+ ["+str(self.tmps.year)+str(self.tmps.month)+str(self.tmps.day)
                               +str(self.tmps.hour)+str(self.tmps.minute)+str(self.tmps.second)+"] ["+self.vFname+"] ["+self.nElmt+"]")
                         
                    print("================================================")
                    
                    self.fileLog.close()

                #Détection de l'inactivité.
                if(self.nModif == 0):
                    print("nothing new...")

                self.lst_file = sorted((self.getFiles()))
                self.nPrev    = len(self.lst_file)

                time.sleep(self.freqMonitoring)

    """
    Attribut permettant de configurer les types de fichier à surveiller.          
    L'extension par défaut est ".TXT"                                             
    """
        
    def _get_typeFile(self):
        return(self._typeFile)

    def _set_typeFile(self,val_typeFile):
        self._typeFile = val_typeFile

    typeFile = property(_get_typeFile,_set_typeFile)

    """
    Attribut permettant de configurer la fréquence de surveillance du répertoire.  
    La durée minimum est de 60 secondes.                                          
    """

    def _get_freqMonitoring(self):
        return(self._freqMonitoring)
    
    def _set_freqMonitoring(self,val_freqMonitoring):
        
        if(val_freqMonitoring > 60):
            self._freqMonitoring = val_freqMonitoring
        else:
            self._freqMonitoring = 60            

    freqMonitoring = property(_get_freqMonitoring,_set_freqMonitoring)    

def testModule():
    """
    Fonction de test du module.    
    """

    #Listes des répertoires à surveiller.
    lst_dir       = ["C:/GitHub/gitRepTest","C:/GitHub/gitRepTest/prog","C:/GitHub/NetBook"]

    #Spécification des types de fichier à surveiller.
    lst_extension = [".txt",".psc",".py"]
    
    #Création de l'objet.
    module = Monitoring(folder=lst_dir, extension=lst_extension,vFname="MyProject") 
    
    #Lancement du thread en tâche de fond.
    module.start()

    #Attente de la fin de la tâche.
    module.join()
    
if __name__ == '__main__':

    #Fonction de test
    testModule()
        
