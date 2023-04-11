#Hauptautor: Grischa Storch
#Datum: 27.02.2021
#Zweck: Minesweeper

#Oberleiste Breite: 40
#Feld: 30x30

import json
import pygame
from Spielfeld import *

pygame.init()

import tkinter as tk
from tkinter import simpledialog

""" Die Klasse Minesweeper dient vorallem dazu, die Mainloop des Spiels zu starten,
    aber auch um am Anfang und am Ende Fenster mit Mitteilungen zu öffnen.
    Die notwendigen Variablen werden zum größten Teil eigenständig zusammengeführt,
    aber es werden auch Userinputs gefordert. Um das Spiel zu starten, wird noch ein
    kleines Hauptprogramm benötigt, welches hier ganz unten mit angegeben ist."""

class Minesweeper:

    """Vor.: -
       Eff.: Es wird auf Befehle des Hauptprogramms gewartet, da diese die Klasse steuern.
       Erg.: Eine Instanz der Klasse Minesweeper ist geliefert."""
    
    def __init__(self)-> "Minesweeper":
        self.__ranked = ("j" in input("Ranked?: "))
        self.__wahl = 0
        self.__stats = [0,0,0,0,0] # Spiele: gespielt, gewonnen, verloren, Rekord, average
        with open("stats.json", "r") as datei:
            data = json.load(datei)
            self.__stats[0] = data["gespielt"]
            self.__stats[1] = data["gewonnen"]
            self.__stats[2] = data["verloren"]
            self.__stats[3] = data["rekord"]
            self.__stats[4] = data["average"]

    def abspeichern(self):
        if self.__ranked:
            data = {}
            data["gespielt"] = self.__stats[0]
            data["gewonnen"] = self.__stats[1]
            data["verloren"] = self.__stats[2]
            data["rekord"] = self.__stats[3]
            data["average"] = self.__stats[4]
            with open("stats.json", "w") as datei:
                json.dump(data, datei, indent=4)
        
    def schwierigkeit(self):
        """Vor.: -
           Eff.: Es entsteht ein Fenster, welches eine Eingabe für einen int-Wert fordert, welcher
                 den Schwierigkeitsgrad darstellt. Je nach Auswahl werden Werte für die
                 Fenstergröße festgelegt.
           Erg.: - """
        
        fenster = tk.Tk()
        fenster.withdraw()
        fenster.attributes("-topmost", True)
        self.__dif = simpledialog.askinteger("Schwierigkeit wählen", "Bitte wähle den Schwierigkeitsgrad:\n1 - Anfänger\n2 - Fortgeschritten\n3 - Experte")
        fenster.attributes("-topmost",False)
        if self.__dif == 1:
            
            self.__x = 240
            self.__y = 280
            
            self.__titel = "Minesweeper - Anfänger"
            self.__l = 8
            self.__b = 8
        elif self.__dif == 2:
            self.__x = 480
            self.__y = 520
            self.__titel = "Minesweeper - Fortgeschritten"
            self.__l = 16
            self.__b = 16
        else:
            self.__x = 900
            self.__y = 520
            self.__titel = "Minesweeper - Experte"
            self.__l = 30
            self.__b = 16


    def gewonnen(self)-> int:
        """Vor.: -
           Eff.: Es öffnet sich ein Fenster, welches mitteilt, dass man gewonnen hat.
                 Dort kann man auch wieder einen int-Wert eingeben, welcher darüber
                 entscheidet was als nächstes passiert.
           Erg.: Der eingegebene Wert ist geliefert."""

        self.__stats[4] = (self.__stats[4]*self.__stats[1] + self.__genaueZeit)/(self.__stats[1]+1)
        self.__stats[1] += 1
        if self.__stats[3] == None:
            self.__stats[3] = self.__genaueZeit
        elif self.__genaueZeit < self.__stats[3]:
            self.__stats[3] = self.__genaueZeit
        self.abspeichern()
        fenster = tk.Tk()
        fenster.withdraw()
        fenster.attributes("-topmost", True)
        wahl = simpledialog.askinteger("Glückwunsch!", "Herzlichen Glückwunsch, sie haben gewonnen!\nBenötigte Zeit: " + str(self.__zeit) + " Sekunden\nWollen Sie:\n1 - Neustarten\n2 - Neustarten und den Schwierigkeitsgrad wechseln\n3 - Verlassen")
        fenster.attributes("-topmost",False)
        return wahl

    def gibWahl(self)-> int:
        """Vor.: -
           Eff.: -
           Erg.: Das Attribut -wahl- ist geliefert."""
        return self.__wahl
        

        
    def mainLoop(self)-> bool:
        """Vor.: -
           Eff.: Zuallererst wird ein graues Fenster mit den vorher festgelegten Fenster-
                 größen erschaffen, dann ein Spielfeld initialisiert. Nun beginnt
                 der richtige mainLoop, der dauerhaft Dinge abfragt und das Spiel
                 kontrolliert.
           Erg.: True ist geliefert, wenn das Spiel mit gleichen Attributen
                 neustarten soll. False ist geliefert, wenn das Spiel aufhören
                 oder komplett neustarten soll."""
        self.__wahl = 0
        self.__gewonnenZeit = False
        self.__win = pygame.display.set_mode((self.__x,self.__y))
        pygame.display.set_caption(self.__titel)
        self.__win.fill((160,160,160))
        self.__Spielfeld = Spielfeld(self.__dif,(self.__l, self.__b),self.__win)
        spielaktiv = True
        nochNicht = True
        while spielaktiv:
            for event in pygame.event.get():
                if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                    spielaktiv = False
                if self.__Spielfeld.gibSpielzustand() == 3:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[1]> 40:
                        if self.__Spielfeld.nochNichtsAufgedeckt():
                            self.__Spielfeld.starteTimer()
                            self.__stats[0] += 1
                            self.abspeichern()
                        self.__Spielfeld.aufdecken(self.__Spielfeld.getFeldByCoords(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                        self.__Spielfeld.überprüfen()
                        self.__Spielfeld.angrenzende_aufdecken()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and pygame.mouse.get_pos()[1]> 40:
                        if self.__Spielfeld.gibSpielzustand()==3:
                            if not self.__Spielfeld.nochNichtsAufgedeckt():
                                self.__Spielfeld.markieren(self.__Spielfeld.getFeldByCoords(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                                self.__Spielfeld.überprüfen()                   
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[1] < 40:
                    if self.__Spielfeld.SmileyGeklickt(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        spielaktiv = False
                        pygame.quit()
                        return True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and pygame.mouse.get_pos()[1] < 40:
                    if self.__Spielfeld.SmileyGeklickt(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        #print("Made by GReNick GmbH & Co. KG Startup-Firma\nSie wollen Teil des Teams sein? Schicken Sie uns ihre Bewerbung hier:\nhttps://tinyurl.com/GReNickBewerbung")
                        print("------------------------")
                        print(f"Spiele gespielt: {self.__stats[0]}\nSpiele ez r3kt: {self.__stats[1]}\nMisclicks: {self.__stats[2]}\nBeste Zeit: {self.__stats[3]}\nAverage: {self.__stats[4]}")          
                        print("------------------------")
                    
            if self.__Spielfeld.gibSpielzustand() == 3 and self.__Spielfeld.gibZeit() < 1000:
                self.__Spielfeld.aktualisiereTimer()
            elif self.__Spielfeld.gibSpielzustand() == 1:
                if not self.__gewonnenZeit:
                    self.__genaueZeit = self.__Spielfeld.gibGenaueZeit()
                    self.__zeit = str(self.__Spielfeld.gibZeit())
                    self.__gewonnenZeit = True
                    self.__wahl = self.gewonnen()
                if self.__wahl == 1:
                    pygame.quit()
                    return True
                elif self.__wahl == 2:
                    pygame.quit()
                    return False
                elif self.__wahl == 3:
                    pygame.quit()
                    return False
            elif self.__Spielfeld.gibSpielzustand() == 2:
                if nochNicht:
                    self.__stats[2] += 1
                    self.abspeichern()
                    nochNicht = False
                    
            self.__Spielfeld.aktualisiereBombencounter(self.__Spielfeld.gibBombenAnzahl())
            pygame.display.update()
        
        pygame.quit()
        return False


        


#--------------------------
komplettneustart = 2
while komplettneustart == 2:
    komplettneustart = 0
    spielen = True
    dif = 0
    m = Minesweeper()
    m.schwierigkeit()
    while spielen:
        neustart = m.mainLoop()
        if not neustart:
            spielen = False
    komplettneustart = m.gibWahl()

        




