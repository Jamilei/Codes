import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#funtio mita pyritaan optimoimaan - etsimaan arvo x mika palauttaa arvon 0
def funtio1(x):
    arvo=0
    for i in range(len(x)):
        arvo = arvo + x[i]**2
    return arvo


class Partikkeli:

    #partikkeleiden maarittely
    def __init__(self, lahtocord):

        #maaritellaan jokaiselle partikkelille tiedot mitka jokainen partikkeli tietaa itse
        self.nykpaikka = []         
        self.nopeus = []
        self.omaparas = []
        self.globaaliparas = []
        self.nykyinenparas = []

        
        #maaritellaan kaikille random nopeus ja asetetaan alku positio samaan paikkaan
        for i in range(0, num_dimensions):
            self.nopeus.append(random.uniform(-1, 1))
            self.nykpaikka.append(lahtocord[i])

    #partikkeleiden tietojen paivitys
    def vertaa(self, funktio):
        self.nykyinenparas = funktio(self.nykpaikka)
        #verrataan onko nykyinen paikka parempi kuin globaalisti loydetty paikka TAI ollaanko ensimmaisella suorituksella
        if self.nykyinenparas < self.globaaliparas or self.globaaliparas == -1:
            self.omaparas = self.nykpaikka
            self.globaaliparas = self.nykyinenparas
    
    def paivita_nopeus(self, porukan_positio):
        #maaritellaan painot kuinka paljon muut partikkelit vaikuttaa nopeuden muutokseen
        vakio_paino = 0.5
        oma_paino = 1
        yleinen_paino = 2.5

        #paivitetaan partikkelille uusi nopeus
        for i in range(0, num_dimensions):
            #random muuttuja jokaiselle jotta loydetaan uusia alueita
            random1 = random.random()
            random2 = random.random()

            #lasketaan painotukset erillaan ja lopussa lisataan yhteen luoden uuden nopeuden partikkelille
            oma_nopeus = oma_paino * random1 * (self.omaparas[i] - self.nykpaikka[i])
            yleinen_nopeus = yleinen_paino * random2 * (porukan_positio[i] - self.nykpaikka[i])
            self.nopeus[i] = vakio_paino * self.nopeus[i] + yleinen_nopeus + oma_nopeus

    def paivita_koord(self):
        for i in range(0, num_dimensions):
            #liikutaan nopeuden mukana uuteen paikkaan
            #print type(self.nopeus)
            self.nykpaikka[i] = self.nykpaikka[i] + self.nopeus[i]

            #reunat?
            if self.nykpaikka[i]>reunat[i][1]:
                self.nykpaikka[i]=reunat[i][1]

            if self.nykpaikka[i] < reunat[i][0]:
                self.nykpaikka[i]=reunat[i][0]


class PSO():
    def __init__(self, funktio, paikka, reunat, p_maara, maxiteraatiot):

        #jotta for loopit pysyy mukana
        global num_dimensions

        #maarittelya jotta pystyy viittaamaan myohemmin
        self.iteraatiot = 0
        self.maxiteraatiot = maxiteraatiot
        self.p_maara = p_maara
        self.reunat = reunat
        self.funktio = funktio

        #monta ulottuvuutta datalla on: x, y, z...
        num_dimensions = len(paikka)

        self.porukan_paras = -1
        self.porukan_positio = []

        #luodaan parvi
        self.parvi = []
        for i in range(0, p_maara):
            self.parvi.append(Partikkeli(paikka))

        i = 0

    def paivita(self, scat):
        #pyoritaan ennalta annetun maxiteraatio muuttujan verran
        if(self.iteraatiot < self.maxiteraatiot):
            print 'Run number:', self.iteraatiot, '. Best value found in this iteration: ', self.porukan_paras

        #jos haluaa katsoa hitaammin tyoskentelya
        #time.sleep(1)

        #katsotaan onko uudet paikat parempia kuin edelliset
        for j in range(0, self.p_maara):
            self.parvi[j].vertaa(self.funktio)
            #jos loydetaan uusi paras paikka
            if self.parvi[j].nykyinenparas < self.porukan_paras or self.porukan_paras == -1:
                self.porukan_paras = float(self.parvi[j].nykyinenparas)
                self.porukan_positio = list(self.parvi[j].nykpaikka)
                
        #alustetaan x ja y koordinaatit visualisoinnille
        parvi_xkoord = []
        parvi_ykoord = []

        #paivitetaan parven uudet paikat ja nopeudet
        for j in range(0, self.p_maara):
            self.parvi[j].paivita_nopeus(self.porukan_positio)
            self.parvi[j].paivita_koord()

            #napataan parven uudet koordinaatit
            parvi_xkoord.append(self.parvi[j].nykpaikka[0])
            parvi_ykoord.append(self.parvi[j].nykpaikka[1])

        #poistaa parven edellisen sijainnin piirroksesta
        plt.clf()

        #plotataan ymparisto uudella parvella
        plt.scatter(parvi_xkoord, parvi_ykoord)
        
        #luodaan reunat scatterplotille
        plt.xlim(self.reunat[0])
        plt.ylim(self.reunat[1])

        #yksi iteraatio suoritettu
        self.iteraatiot = self.iteraatiot + 1

if __name__ == "__PSO__":
    main()

#tasta voi valita mista koordinaatista lahdetaan liikkeelle
lahtopaikka = [-5, -5]

#reunat ei tarvii?
reunat = [(-10,10),(-10,10)]

thisrun = PSO(funtio1,lahtopaikka, reunat, p_maara=10,maxiteraatiot=25)
fig = plt.figure()
ani = animation.FuncAnimation(fig, thisrun.paivita)
plt.show()



            
        
        

        
            
            
        
            

        



