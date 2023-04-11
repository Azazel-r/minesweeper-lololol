#Hauptautor: Nick Krause
#Datum: 28.02.2021
#Zweck: Klasse Feld

import pygame

""" Eine Feldinstanz ist das modellierte Feld auf dem Spielfeld, welches nicht aufgedeckt
      und nicht markiert, nicht aufgedeckt und markiert, nicht aufgedeckt und falsch markiert,
      aufgedeckt und leer, aufgedeckt und eine Zahl sowie aufgedeckt und eine Bombe sein kann.
      Mit rotem Hintergrund ist die Bombe, die man selbst aufgedeckt hat, alle anderen werden
      danach mit normalem Hintergrund aufgedeckt."""

class Feld:
    def __init__(self)-> "Feld":
        """   Vor.:
                Eff.: Die Eigenschaften sind nun mit Werten belegt.
                    Die Koordinaten werden noch zugeteilt, danach wird es gezeichnet.
                Erg.: Ein neues Feld ist geliefert."""
        self.__x = 0
        self.__y = 0
         #---------------------------Bilder-----------------------------
        self.__nA = pygame.image.load('nA.png') #nicht aufgedeckt
        self.__A = pygame.image.load('A.png') #aufgedecktes Feld (leer)
        self.__B1 = pygame.image.load('B1.png') #andere Bomben bei Niederlage
        self.__B2 = pygame.image.load('B2.png') #berührte Bombe
        self.__M1 = pygame.image.load('M1.png') #markiertes Feld
        self.__M2 = pygame.image.load('M2.png') #falsch markiertes Feld
        self.__Z = [pygame.image.load('Z1.png'),pygame.image.load('Z2.png'),pygame.image.load('Z3.png'),pygame.image.load('Z4.png'),pygame.image.load('Z5.png'),
                pygame.image.load('Z6.png'),pygame.image.load('Z7.png'),pygame.image.load('Z8.png')] #angrenzende Bombenfelderanzahl
         #---------------------------Bilder-----------------------------
        self.__seitenlänge = 30
        self.__istBombe = False
        self.__aufgedeckt = False
        self.__markiert = False
        self.__Zahl = 0
        self.__bild = self.__nA
        self.__verloren = False
        self.__gewonnen = False
        self.__wurde_geändert = True
        
    def zeichnen(self, window: "pygame"):
        """   Vor.: -.
                Eff.: Das Feld wurde im window nach den entsprechenden Eigenschaften gezeichnet/aktualisiert.
                Erg.: """

        if self.__wurde_geändert == True:
            window.blit(self.__bild,(self.__x, self.__y))
            pygame.display.update()
        
    def gibPos(self)-> int:
        """   Vor.: -
                Eff.: -
                Erg.: Die Koordinaten des Felds sind als Tupel geliefert."""
        return (self.__x, self.__y)

    def gib_istBombe(self)->bool:
        """   Vor.: -
                Eff.: -
                Erg.: Wenn das Feld eine Bombe ist, ist True geliefert. Andernfalls ist False geliefert"""
        return self.__istBombe

    def gib_aufgedeckt(self)-> bool:
        """   Vor.: -
                Eff.: -
                Erg.: Wenn das Feld aufgedeckt ist, ist True geliefert. Andernfalls ist False geliefert"""
        return self.__aufgedeckt

    def gib_markiert(self)->bool:
        """   Vor.: -
                Eff.: -
                Erg.: Wenn das Feld markiert ist, ist True geliefert. Andernfalls ist False geliefert"""
        return self.__markiert

    def gibBild(self)-> "pygame":
        """   Vor.: -
                Eff.: -
                Erg.: Das Attribut zum Aussehen des Feldes ist geliefert."""
        return self.__bild

    def gibZahl(self)-> int:
        """   Vor.: 
                Eff.: 
                Erg.: Die Anzahl der um den Feld umliegenden Bomben ist geliefert"""
        return self.__Zahl

    def gibSpielzustand(self)-> int:
        """   Vor.: 
                Eff.: 
                Erg.: Der Spielzustand, gemessen am Feld, ist geliefert (bedeutet, wenn eine Bombe aufgedeckt wird,
                ist der Spielzustand zuerst bei diesem Feld geändert)"""
        pass
        if self.__gewonnen and not self.__verloren:
            return 1 # gewonnen
        elif self.__verloren and not self.__gewonnen:
            return 2 # verloren
        else:
            return 3 # noch im Spielen

    def gib_verändert(self) -> bool:
        """   Vor.: -
                Eff.: -
                Erg.: Falls sich bei der letzten Bild-Aktualisierung das Bild geändert hat, ist True geliefert
                andernfalls ist False geliefert."""
        return self.__wurde_verändert

    def setzeSpielzustand(self, z: int):
        """  Vor.: -
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

    def setzePos(self,x,y: int):
        """  Vor.: -
                Eff.: Die Position des Feldes wurde auf die angegebenen Werte gesetzt.
                Erg.: - """
        self.__x, self.__y = x,y

    def setzeBombe(self):
        """   Vor.: -
                Eff.: Auf dem Feld wurde eine Bombe platziert.
                Erg.: -"""
        self.__istBombe = True

    def setze_aufgedeckt(self):
        """   Vor.: -
                Eff.: Das Feld wurde aufgedeckt.
                Erg.: -"""
        self.__aufgedeckt = True

    def setze_markiert(self,b: bool):
        """   Vor.: -
                Eff.: Das Feld wurde markiert.
                Erg.: -"""
        self.__markiert = b

    def setzeBild(self):
        """   Vor.: -
                Eff.: Das Attribut für das Bild des Feldes wurde anhand der Eigenschaften aktualisiert.
                Erg.: -"""
        if not self.__aufgedeckt and not self.__markiert and not self.__verloren and not self.__gewonnen:
            if self.__bild != self.__nA:
                self.__bild = self.__nA
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False
            
        elif self.__aufgedeckt and self.__Zahl == 0  and not self.__istBombe and not self.__markiert:
            if self.__bild != self.__A:
                self.__bild = self.__A
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False
                
        elif not self.__aufgedeckt and self.__istBombe and self.__verloren and not self.__markiert:
            if self.__bild != self.__B1:
                self.__bild = self.__B1
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False
                
        elif self.__aufgedeckt and self.__istBombe and not self.__markiert:
            if self.__bild != self.__B2:
                self.__bild = self.__B2
                self.setzeSpielzustand(2)
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False
            
        elif (not self.__aufgedeckt and self.__markiert and not self.__verloren) or (not self.__aufgedeckt and self.__gewonnen):
            self.__markiert = True
            if self.__bild != self.__M1:
                self.__bild = self.__M1
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False
                
        elif not self.__aufgedeckt and self.__markiert and self.__verloren and not self.__istBombe:
            if self.__bild != self.__M2:
                self.__bild = self.__M2
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False
            
        elif self.__aufgedeckt and self.__Zahl != 0 and not self.__istBombe and not self.__markiert:
            if self.__bild != self.__Z[self.__Zahl-1]:
                self.__bild = self.__Z[self.__Zahl-1]
                self.__wurde_geändert == True
            else:
                self.__wurde_geändert == False

    def setzeZahl(self,z:int):
        """   Vor.: -
                Eff.: Die Zahl der umliegenden Bomben um das Feld wurde auf den angegebenen Wert gesetzt.
                Erg.: -"""
        self.__Zahl = z
