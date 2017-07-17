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
        self.freqMonitoring = 6

        #Variable de détection d'ajout de fichier.
        self.flagP          = False

        #Variable de détection de suppression de fichier.
        self.flagM          = False        
        
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

                    #Flag de détection.
                    self.flagM = True                    

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

                    #Flag de détection.
                    self.flagP = True

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
        
        if(val_freqMonitoring > 6):
            self._freqMonitoring = val_freqMonitoring
        else:
            self._freqMonitoring = 6            

    freqMonitoring = property(_get_freqMonitoring,_set_freqMonitoring)

    """
    Flag de détection d'ajout d'un fichier dans le répertoire virtuel.                                             
    """
        
    def _get_flagP(self):
        return(self._flagP)

    def _set_flagP(self,val_flagP):
        self._flagP = val_flagP

    flagP = property(_get_flagP,_set_flagP)

    """
    Flag de détection de suppression d'un fichier dans le répertoire virtuel.                                             
    """
        
    def _get_flagM(self):
        return(self._flagM)

    def _set_flagM(self,val_flagM):
        self._flagM = val_flagM

    flagM = property(_get_flagM,_set_flagM)      

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

    #Boucle permettant d'éxecuter une action après la détection d'un évènement.
    while 1 :

        #Attente tant qu'il n'y pas d'action (ajout ou de suppression de fichier).
        while ((module.flagP == False) and (module.flagM == False)):
            time.sleep(1)

        #Action détecté#
            
        #Initialisation du flag de détection.
        if(module.flagP == True):

            #Récupération des fichiers ajoutés.
            NewFile = module.lst_Modif

            #Routine de traitement sur le(s) fichier(s).
            for fic in NewFile :
                print("+ "+fic)
            
        #Initialisation du flag de détection.
        if(module.flagM == True):
            
            #Récupération des fichiers ajoutés.
            NewFile = module.lst_Modif

            #Routine de traitement sur le(s) fichier(s).
            for fic in NewFile :
                print("- "+fic)

        module.flagP = False
        module.flagM = False

    #Attente de la fin de la tâche.
    module.join()
    
if __name__ == '__main__':

    #Fonction de test
    testModule()
        
