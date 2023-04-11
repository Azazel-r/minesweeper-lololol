#Hauptautor: Grischa Storch
#Datum: 02.03.2021
#Zweck: Klasse Bombencounter

import pygame
from pygame.locals import *
pygame.init()

"""Die Instanz der Klasse Bombencounter modelliert grafisch den Bombenzähler
     (oder auch: verbleibende-Markierungen-Anzeige :) oben links auf dem Spielfeld."""

class Bombencounter:
    def __init__(self, markierte: int, win: "pygame"):
        """ Vor.: -markierte- ist die Differenz zwischen der Anzahl der Bomben im Spielfeld
                  und der Anzahl der bereits markierten Felder. -win- ist das Pygame-Fenster in dem
                  der Bombencounter dargestellt werden soll.
            Eff.: Die Differenz zwischen der Anzahl der Bomben im Spielfeld und der Anzahl der bereits
                  markierten Felder wird in der oberen linken Ecke des Fensters -win- grafisch dargestellt.
            Erg.: - """
        self.__window = win
        self.__c = [pygame.image.load('C0.png'),pygame.image.load('C1.png'),pygame.image.load('C2.png'),pygame.image.load('C3.png'),pygame.image.load('C4.png'),pygame.image.load('C5.png'),
             pygame.image.load('C6.png'),pygame.image.load('C7.png'),pygame.image.load('C8.png'),pygame.image.load('C9.png'),]
        self.__groesse = self.__c[1].get_rect()
        self.__übrige = markierte
        if self.__übrige > 9:
            self.__bild2 = self.__c[int(str(self.__übrige)[0])]
            self.__bild1 = self.__c[int(str(self.__übrige)[1])]
        else:
            self.__bild2 = self.__c[0]
            self.__bild1 = self.__c[self.__übrige]
        self.__window.blit(self.__bild2, (0,0))
        self.__window.blit(self.__bild1, (self.__groesse.width, 0))
        
