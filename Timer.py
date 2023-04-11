#Hauptautor: Grischa Storch
#Datum: 01.03.2021
#Zweck: Klasse Timer

import pygame
from pygame.locals import *
import time
pygame.init()

"""Die Klasse Timer initialisiert den oben rechts auf dem Spielfeld angezeigten Zeitzähler.
     Der Timer startet erst, sobald ein Feld im Spielfeld aufgedeckt wurde."""

class Timer:
    """Für eine komplette Hilfe >>> help(Spielfeld) eingeben!
       Vor.: -win- ist das Fenster des Pygame-Moduls, in dem der Timer dargestellt werden soll..
       Eff.: Der Timer ist in der oberen rechten Ecke des Fensters -win- durch drei Nullen grafisch dargestellt.
       Erg.: Ein neues Spielfeld ist geliefert."""
    
    def __init__(self, win: "pygame")-> "Timer":
        self.__letsGO = False
        self.__window = win
        self.__c = [pygame.image.load('C0.png'),pygame.image.load('C1.png'),pygame.image.load('C2.png'),pygame.image.load('C3.png'),pygame.image.load('C4.png'),pygame.image.load('C5.png'),
             pygame.image.load('C6.png'),pygame.image.load('C7.png'),pygame.image.load('C8.png'),pygame.image.load('C9.png'),]
        self.__x = self.__window.get_width()
        self.__groesse = self.__c[1].get_rect()
        self.__window.blit(self.__c[0], (self.__x-self.__groesse.width, 0))
        self.__window.blit(self.__c[0], (self.__x-2 * self.__groesse.width, 0))
        self.__window.blit(self.__c[0], (self.__x- 3 * self.__groesse.width, 0))
        
        
    def letsgo(self, starttime: "time"):
       """Vor.: -window- ist das Pygame-Fenster in dem der Timer angezeigt und aktualisiert werden soll. -starttime- ist die Zeit die zwischen dem Öffnen des Spiels und
                dem Aufdecken des ersten Feldes vergangen ist.
          Eff.: Die Zeit in Sekunden, die seit dem ersten Spielzug vergangen ist, wird im Fenster -win- in der oberen rechten Ecke grafisch dargestellt.
          Erg.: -"""
       self.__letsGO = True
       self.__starttime = starttime
       jetzt = int(time.perf_counter())
       counter = int(jetzt) - int(self.__starttime)
       counter1 = int(str(counter)[len(str(counter))-1])
       if counter > 9:
           counter2 = int(str(counter)[len(str(counter))-2])
           if counter > 99:
               counter3 = int(str(counter)[len(str(counter))-3])
           else:
               counter3 = 0
       else:
           counter2 = 0
           counter3 = 0
       self.__window.blit(self.__c[counter1], (self.__x-self.__groesse.width, 0))
       self.__window.blit(self.__c[counter2], (self.__x-2 * self.__groesse.width, 0))
       self.__window.blit(self.__c[counter3], (self.__x- 3 * self.__groesse.width, 0))

    def istGestartet(self)-> bool:
        """Vor.: -
           Eff.: -
           Erg.: True ist geliefert wenn der Timer gestartet ist. False ist geliefert wenn er noch nicht gestartet ist."""
        return self.__letsGO
