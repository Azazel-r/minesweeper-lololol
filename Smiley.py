#Hauptautor: Nick Krause
#Datum: 28.02.2021
#Zweck: Klasse Smiley

import pygame

""" Der Smiley ist der modellierte Neustart-Button auf dem Spielfeld, welcher
        durch Betätigen ein neues Spiel auf demselben Schwierigkeitsgrad startet und außerdem
        den Spielzustand anzeigt."""

class Smiley:
    def __init__(self, x, y: int, window: "pygame")-> "Smiley":
        """   Vor.: x und y sind die Koordinaten des Smileys, die natürlich je nach Schwierigkeitsgrad anders sind.
                Eff.: Die Eigenschaften sind nun  mit den übergebenen Werten belegt.
                     Wenn es gültig ist, wurde es im Grafikfenster gezeichnet.
                Erg.: Ein neuer, normal schauender Smiley ist geliefert."""
        self.__x = x
        self.__y = y
        #-----------------------------Bilder----------------------------------
        self.__Sm1 = pygame.image.load('Sm1.png') #normaler Smiley
        self.__Sm2 = pygame.image.load('Sm2.png') #toter Smiley
        self.__Sm3 = pygame.image.load('Sm3.png') #cooler Smiley
        #-----------------------------Bilder----------------------------------
        self.__gewonnen = False
        self.__verloren = False
        self.__bild  = self.__Sm1
        window.blit(self.__bild, (x, y))

    def gibPos(self)-> (int, int):
        """   Vor.: -
                Eff.: -
                Erg.: Die Koordinaten des Smileys sind geliefert."""
        return (self.__x, self.__y)

    def setzeSpielzustand(self, z: int):
        """   Vor.: -
                Eff.: Der Spielzustand des Smileys wurde auf den zu -z- zugehörigen Wert gesetzt.
                    Dabei steht 1 für gewonnen, 2 für verloren und 3 für noch im Spiel.
                Erg.: - """

        if z == 1:
            self.__gewonnen = True
            self.__verloren = False
        elif z == 2:
            self.__gewonnen = False
            self.__verloren = True
        else:
            self.__gewonnen = False
            self.__verloren = False

    def setzeBild(self, Spielfeldgröße: (int, int), window: "pygame"):
        """   Vor.: -.
                Eff.: Der Smiley wird je nach Spielzustand auf des dazu entsprechende Bild gesetzt.
                Erg.: - """

        if self.__verloren == True:
            self.__bild = self.__Sm2
            window.blit(self.__bild, ((Spielfeldgröße[0]*30//2-15), 5))
            pygame.display.update()
        elif self.__gewonnen == True:
            self.__bild = self.__Sm3
            window.blit(self.__bild, ((Spielfeldgröße[0]*30//2-15), 5))
            pygame.display.update()
