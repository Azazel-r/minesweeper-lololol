# Hauptautor: René Richter
# Datum: 27.02.2021
# Zweck: Klasse Spielfeld

import pygame
from time import *
from random import randint as rnd

from Smiley import *
from Feld import *
from Timer import *
from Bombencounter import *

""" Eine Instanz der Klasse Spielfeld stellt im Pygame-Grafikfenster die gesamte
    Spielwelt dar. Durch bestimmte Ereignisse, wie z.B. Mausklicks, werden im
    Hauptprogramm Methoden dieser Klasse aufgerufen und das Spiel durch diese
    entsprechend verändert und kontrolliert. Die Spezifikationen der Methoden
    sind hier mit implementiert."""

class Spielfeld:

    """Für eine komplette Hilfe >>> help(Spielfeld) eingeben!
       Vor.: -difficulty- ist eine Zahl vom Typ int von 1 bis 3, welche die drei
             Schwierigkeitsgrade darstellen soll. -groesse- ist die Größe des
             Spielfeldes in Feldern und wird in einem Tupel (Länge, Breite) aus zwei int-
             Werten angegeben. -window- ist ein Fenster vom Pygame-Modul, in der das
             Spielfeld existieren soll.
       Eff.: Das Spielfeld ist entsprechend der angegebenen Werte gezeichnet und
             wartet auf Befehle durch das Hauptprogramm.
       Erg.: Ein neues Spielfeld ist geliefert."""
    
    def __init__(self, difficulty, groesse, window)-> "Spielfeld":
        self.__dif = difficulty - 1
        self.__win = window
        self.__starttime = int(time.perf_counter())
        self.__zeit = Timer(self.__win)
        self.__gewonnen = False
        self.__verloren = False
        self.__bomben = [10, 40, 99]
        self.__grs = groesse
        self.__felderNamen = []
        for i in range (self.__grs[0] * self.__grs[1]):
            self.__felderNamen.append("feld" + str(i))
        self.__felder = [Feld() for prop in self.__felderNamen]
        self.__x = 0
        self.__y = 40
        for obj in self.__felder:
            obj.setzePos(self.__x, self.__y)
            if self.__x + 30 < self.__grs[0]*30:
                self.__x += 30
                obj.zeichnen(self.__win)
            else:
                self.__x = 0
                self.__y += 30
                obj.zeichnen(self.__win)
        self.__Sm = Smiley(self.__grs[0]*30//2-15, 5, self.__win)
        self.__counter = Bombencounter(0, self.__win)

    def istBombe(self, feld)-> bool:
        """Vor.: -feld- ist ein Objekt von der Klasse Feld.
           Eff.: -
           Erg.: True/False ist geliefert, wenn das -feld- eine Bombe ist/keine Bombe ist."""
        return feld.gib_istBombe()
    
    def aktualisiereTimer(self):
        """Vor.: -
           Eff.: Der Timer wird aktualisiert.
           Erg.: -"""
        if self.__zeit.istGestartet() and self.gibZeit() < 999:
            Timer(self.__win).letsgo( self.__starttime)

    def aktualisiereBombencounter(self, markierte):
        """Vor.: -markierte- ist vom Typ int.
           Eff.: Der Bombencounter wird mit der übergebenen Zahl aktualisiert.
           Erg.: - """
        Bombencounter(markierte, self.__win)

    def starteTimer(self):
        """Vor.: -
           Eff.: Der Timer wird gestartet.
           Erg.: - """
        self.__starttime = int(time.perf_counter())
        self.__zeit.letsgo( self.__starttime)

    def nochNichtsAufgedeckt(self)-> bool:
        """Vor.: -
           Eff.: -
           Erg.: True/False ist geliefert, wenn noch kein Feld aufgedeckt ist/wenn
                 schon mindestens ein Feld aufgedeckt ist."""
        for obj in self.__felder:
            if obj.gib_aufgedeckt():
                return False
        return True

    def ist_markiert(self, feld:"Feld")-> bool:
        """Vor.: -
           Eff.: -
           Erg.: True ist geliefert, wenn das Feld markiert ist."""
        return feld.gib_markiert()

    def gibZahl(self, feld:"Feld")-> int:
        """Vor.: -
           Eff.: -
           Erg.: Die Zahl, die auf dem Feld steht, ist geliefert."""
        return feld.gibZahl()
    
    def istAufgedeckt(self, feld:"Feld")-> bool:
        """Vor.: -
           Eff.: -
           Erg.: True ist geliefert, wenn das Feld aufgedeckt ist."""
        return feld.gib_aufgedeckt()

    def aufdecken(self, feld:"Feld"):
        """Vor.: -
           Eff.: Das angegebene Feld wird aufgedeckt. Falls das Feld das allerste
                 Feld ist, was aufgedeckt wird, kann dieses keine Bombe sein und
                 beinhaltet die Zahl 0.
           Erg.: - """
        x = True
        if self.nochNichtsAufgedeckt() and x:
            self.verteileBombenUm(feld)
            for obj in self.__felder:
                obj.setzeZahl(self.anzBombenUmFeld(obj))
            x = False
        if not feld.gib_markiert():
            feld.setze_aufgedeckt()
            feld.setzeBild()
            feld.zeichnen(self.__win)

        
    def markieren(self, feld:"Feld"):
        """Vor.: -
           Eff.: Das angegebene Feld ist markiert. Falls das Feld schon markiert ist,
                 wird es wieder entmarkiert.
           Erg.: - """
        if self.gibBombenAnzahl() != 0 and not feld.gib_markiert() and not feld.gib_aufgedeckt():
            feld.setze_markiert(True)
            feld.setzeBild()
            feld.zeichnen(self.__win)
        elif feld.gib_markiert() and not feld.gib_aufgedeckt():
            feld.setze_markiert(False)
            feld.setzeBild()
            feld.zeichnen(self.__win)

    def überprüfen(self):
        """Vor.: - 
           Eff.: Alle Felder des Spielfelds werden durchlaufen und es wird dadurch geprüft, ob sich der Spielzustand
                   geändert hat. Falls das der Fall ist, werden alle Felder auf den geänderten Spielzustand gesetzt,
                   das Bild der Felder sowie der Bombencounter wird aktualisiert.
           Erg.: -"""
        x = True
        for obj in self.__felder:
            if obj.gibSpielzustand() == 2 and x:
                self.setzeSpielzustand(2)
                for obj2 in self.__felder:
                    obj2.setzeSpielzustand(2)
                    obj2.setzeBild()
                    obj2.zeichnen(self.__win)
                    self.aktualisiereBombencounter(self.gibBombenAnzahl())
                x = False
            if self.ist_gewonnen() and x:
                self.setzeSpielzustand(1)
                for obj3 in self.__felder:
                    obj3.setzeSpielzustand(1)
                    obj3.setzeBild()
                    obj3.zeichnen(self.__win)
                    self.aktualisiereBombencounter(self.gibBombenAnzahl())
                x = False

    def angrenzende_aufdecken(self):
        """Vor.: -
           Eff.: Solange freie Felder (aufgedeckte Felder ohne Zahl) existieren, dessen angrenzende
                   Felder nicht alle aufgedeckt sind, werden alle angrenzenden Felder der freien Felder aufgedeckt
           Erg.:"""
        while self.überprüfe_Leerfelder():
            for obj in self.__felder:
                if  obj.gib_aufgedeckt() and obj.gibZahl() == 0 and not obj.gib_istBombe():                            
                    self.deckeFelderAufUm(obj)

    def überprüfe_Leerfelder(self)->bool:
        for obj in self.__felder:
            for obj2 in self.getFelderUmFeld(obj):
                if obj2 != None and obj != None:
                    if ((not obj2.gib_aufgedeckt() and not obj2.gib_istBombe()) and (obj.gib_aufgedeckt() and obj.gibZahl() == 0 and not obj.gib_istBombe())):
                        return True
        return False

    def ist_gewonnen(self)-> bool:
        """Vor.: -
           Eff.: -
           Erg.: True ist geliefert, wenn das Spiel gewonnen ist. Andernfalls
                 ist False geliefert."""
        for obj in self.__felder:
            if not obj.gib_aufgedeckt() and not obj.gib_istBombe():
                return False
        return True

    def gibPos(self, feld:"Feld")-> (int, int):
        """Vor.: -
           Eff.: -
           Erg.: Die Position des Feldes ist geliefert."""
        return feld.gibPos()

    def gibBombenAnzahl(self)-> int:
        """Vor.: -
           Eff.: -
           Erg.: Die gesamte Anzahl der Bomben minus der Anzahl der markierten Felder ist geliefert."""
        x = self.__bomben[self.__dif]
        for obj in self.__felder:
            if obj.gib_markiert():
                x -= 1
        return x

    def gibZeit(self)-> int:
        """Vor.: -
           Eff.: -
           Erg.: Die bisher vergangene Zeit ist geliefert."""
        a = perf_counter()
        return int(a - self.__starttime)

    def gibGenaueZeit(self):
        a = perf_counter()
        return a - self.__starttime

    def gibSpielzustand(self)-> int:
        """Vor.: -
           Eff.: -
           Erg.: 1 ist geliefert, wenn das Spiel gewonnen ist, 2 ist geliefert,
                 wenn das Spiel verloren ist und 3 ist geliefert wenn das Spiel noch läuft."""
        if self.__gewonnen and not self.__verloren:
            return 1 # gewonnen
        elif self.__verloren and not self.__gewonnen:
            return 2 # verloren
        else:
            return 3 # noch im Spielen

    def setzeSpielzustand(self, z: int):
        """Vor.: -z- ist vom Typ int und ist entweder 1, 2 oder 3. Diese Zahlen stellen
                 die Spielzustände Gewonnen, Verloren und noch-im-Spiel dar.
           Eff.: Der Smiley verändert sein Aussehen entsprechend der Eingabe.
           Erg.: -"""
        if z == 1:
            self.__gewonnen = True
            self.__verloren = False
            self.__Sm.setzeSpielzustand(1)
            self.__Sm.setzeBild(self.__grs, self.__win)
        elif z == 2:
            self.__gewonnen = False
            self.__verloren = True
            self.__Sm.setzeSpielzustand(2)
            self.__Sm.setzeBild(self.__grs, self.__win)
        else:
            self.__gewonnen = False
            self.__verloren = False
            self.__Sm.setzeSpielzustand(3)
            self.__Sm.setzeBild(self.__grs, self.__win)

    def getFeldByCoords(self,x,y:int)-> "Feld":
        """Vor.: -x- und -y- stellen Koordinaten dar.
           Eff.: -
           Erg.: Das Feld-Objekt mit den angegebenen Koordinaten ist geliefert."""
        for obj in self.__felder:
            if obj.gibPos()[0] <= x < obj.gibPos()[0] + 30 and obj.gibPos()[1] <= y < obj.gibPos()[1] + 30:
                return obj

    def istFeldLetzteSpalte(self, feld:"Feld"):
        """Vor.: -
           Eff.: -
           Erg.: True ist geliefert, wenn das Feld in der letzten Spielfeldspalte ist."""
        if feld.gibPos()[0] == self.__grs[0]*30-30:
            return True
        return False
    
    def verteileBombenUm(self, feld:"Feld"):
        """Vor.: -feld- ist ein Objekt von der Klasse Feld.
           Eff.: Es werden je nach Schwierigkeitsgrad eine bestimmte Anzahl an
                 Bomben zufällig über alle Felder - außer auf das angegebene und die
                 umliegenden Felder - verteilt.
           Erg.: - """
        umfeld = self.getFelderUmFeld(feld)
        anzBomben = self.__bomben[self.__dif]
        if feld == self.__felder[-1]:
            anzFelder = self.__grs[0]*self.__grs[1] - len(umfeld)+1
        elif self.istFeldLetzteSpalte(feld):
            anzFelder = self.__grs[0]*self.__grs[1] - len(umfeld)
        else:
            anzFelder = self.__grs[0]*self.__grs[1] - len(umfeld) - 1
        for obj in self.__felder:
            if not ((obj in umfeld) or (obj == feld)):
                r = rnd(1, anzFelder)
                if r <= anzBomben:
                    obj.setzeBombe()
                    anzBomben -= 1
                anzFelder -= 1

    def getFelderUmFeld(self, feld:"Feld")-> ["Feld"]:
        """Vor.: -
           Eff.: -
           Erg.: Eine Liste an Felder-Objekten, die direkt um das angegebene Feld liegen, ist geliefert."""
        felderL = []
        x, y = feld.gibPos()
        for fx in range (-30, 60, 30):
            for fy in range (-30, 60, 30):
                if (0 <= x + fx <= self.__grs[0]*30) and (40 <= y + fy <= self.__grs[1]*30+40):
                    felderL.append(self.getFeldByCoords(x + fx, y + fy))
        if feld in felderL:
            felderL.remove(feld)
        for obj in felderL:
            if obj == None:
                felderL.remove(obj)
        return felderL

    def anzBombenUmFeld(self, feld:"Feld")-> int:
        """Vor.: -
           Eff.: -
           Erg.: Die Anzahl an Bomben, die um das angegebene Feld liegen, ist geliefert."""
        erg = 0
        for obj in self.getFelderUmFeld(feld):
            if obj != None:
                if self.istBombe(obj):
                    erg += 1
        return erg

    def deckeFelderAufUm(self, feld:Feld):
        """Vor.: -
           Eff.: Alle umliegenden Felder um das angegebene Feld werden aufgedeckt.
           Erg.: - """
        for obj in self.getFelderUmFeld(feld):
            if obj != None:
                self.aufdecken(obj)

    def SmileyGeklickt(self, x, y: int)-> bool:
        """Vor.: -x- und -y- stellen Koordinaten dar.
           Eff.: -
           Erg.: Falls die angegebenen Koordinaten auf dem Smiley liegen, ist True geliefert.
                 Andernfalls ist False geliefert."""
        smps = self.__Sm.gibPos()
        if smps[0] <= x <= smps[0]+30 and smps[1] <= y <= smps[1]+30:
            return True
        return False


