#!/usr/bin/python3

import time
import os

from   threading import Thread, RLock

verrou = RLock()

class Monitoring(Thread):
    
    def __init__(self,name):
        
        Thread.__init__(self)

        self._flagAdd      = False
        self.name          = name
        self.lst_diffFiles = []

        print("Monitoring "+self.name+"\n")

    def run(self):
        self.GetDiffDir()

    def GetDiffDir(self):        

        while 1 :

            self.lst_prev  = self.GetAllDir()       
            self.n_lstPrev = len(self.lst_prev)

            time.sleep(2)

            self.lst_after  = self.GetAllDir()
            self.n_lstAfter = len(self.lst_after)
            
            if(self.n_lstPrev < self.n_lstAfter):
                self.lst_diffFiles = self.getNewElmt(self.lst_prev, self.lst_after)
                self._flagAdd = True                

            if(self.n_lstPrev > self.n_lstAfter):
                print("Delete file(s) from "+self.name+"\n")               

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

    def GetAllDir(self):

        with verrou :
        
            os.chdir(self.name)
            
            self.lst_oneShoot     = []        

            for self.root, self.dirs, self.files in os.walk(self.name, topdown=False):
            
                for self.fName in self.files:
                    self.lst_oneShoot.append(str(os.path.join(self.root,self.fName)).replace("\\","/"))

            return(self.lst_oneShoot)            
        
            del self.lst_oneShoot            

    def _get_flagAdd(self):
        return(self._flagAdd)

    def _set_flagAdd(self,flagAdd):

        #Suppression des listes.
        del self.lst_prev
        del self.lst_after

        self._flagAdd = flagAdd

    flagAdd = property(_get_flagAdd,_set_flagAdd)

def main():
    
    # Create new threads
    thread1 = Monitoring("C:/GitHub/testA")
    thread2 = Monitoring("C:/GitHub/testB")

    # Start new Threads
    thread1.start()
    thread2.start()

    while 1 :
    
        while (thread1.flagAdd == False) and (thread2.flagAdd == False):
            time.sleep(1)

        if(thread1.flagAdd == True):
            print(thread1.lst_diffFiles)
            thread1.flagAdd = False

        if(thread2.flagAdd == True):
            print(thread2.lst_diffFiles)
            thread2.flagAdd = False        

    thread1.join()
    thread2.join()

if __name__=='__main__':
    main()
