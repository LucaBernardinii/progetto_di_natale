import random
from termcolor import colored

class Carta:
    def __init__(self, seme, valore):
        self.seme = seme
        self.valore = valore

class Mazzo:
    def __init__(self, semi, valori):
        self.carte = self.crea_mazzo(semi, valori)
        self.mischia_mazzo()

    def crea_mazzo(self, semi, valori):
        mazzo = []
        for seme in semi:
            for valore in valori:
                mazzo.append(Carta(seme, valore))
        return mazzo

    def mischia_mazzo(self):
        for _ in range(random.randint(5, 10)):
            random.shuffle(self.carte)

    def estrai_carta(self):
        carta = random.choice(self.carte)
        self.carte.remove(carta)
        return carta

    def scelta_briscola(self):
        carta_briscola = random.choice(self.carte)
        self.carte.remove(carta_briscola)
        self.carte.append(carta_briscola)
        return carta_briscola

class Giocatore:
    def __init__(self, nome):
        self.nome = nome
        self.mano = []
        self.punteggio = 0

    def scegli_carta(self):
        if len(self.mano) == 3:
            print(colored(f"In mano hai 1 = {self.mano[0].valore} di {self.mano[0].seme}, 2 = {self.mano[1].valore} di {self.mano[1].seme}, 3 = {self.mano[2].valore} di {self.mano[2].seme}", "yellow"))
        elif len(self.mano) == 2:
            print(colored(f"In mano hai 1 = {self.mano[0].valore} di {self.mano[0].seme}, 2 = {self.mano[1].valore} di {self.mano[1].seme}", "yellow"))
        elif len(self.mano) == 1:
            print(colored(f"In mano hai 1 = {self.mano[0].valore} di {self.mano[0].seme}", "yellow"))
        carta_scelta = int(input(f"{self.nome}, scegli la carta da giocare 1/2/3: "))
        while carta_scelta not in [1, 2, 3][:len(self.mano)]:
            print("Errore, inserisci un numero valido 1/2/3:")
            carta_scelta = int(input(f"{self.nome}, scegli la carta da giocare 1/2/3: "))
        carta_scelta -= 1
        carta_giocata = self.mano[carta_scelta]
        self.mano.remove(carta_giocata)
        print(f"{self.nome} ha giocato {carta_giocata.valore} di {carta_giocata.seme}.")
        return carta_giocata

class Computer(Giocatore):
    def scegli_carta(self):
        carta_giocata = random.choice(self.mano)
        self.mano.remove(carta_giocata)
        print(f"Il computer ha giocato {carta_giocata.valore} di {carta_giocata.seme}.")
        return carta_giocata

class Partita:
    def __init__(self):
        self.mazzo = Mazzo(["denari", "coppe", "bastoni", "spade"], ["Asso", 2, 3, 4, 5, 6, 7, "Fante", "Cavallo", "Re"])
        self.giocatore = Giocatore(input("Inserisci il tuo nome: "))
        self.computer = Computer("Computer")
        self.seme_briscola = None
        self.primo_giocatore = "giocatore"
        self.distribuzione_iniziale(self.giocatore)
        self.distribuzione_iniziale(self.computer)
        self.scelta_briscola()

    def distribuzione_iniziale(self, giocatore):
        for _ in range(3):
            carta_estratta = self.mazzo.estrai_carta()
            giocatore.mano.append(carta_estratta)

    def scelta_briscola(self):
        carta_briscola = self.mazzo.scelta_briscola()
        self.seme_briscola = carta_briscola.seme
        print(colored(f"La briscola è {carta_briscola.seme}", "cyan"))

    def assegna_valori(self, carta):
        if carta.valore == "Asso":
            return 11
        elif carta.valore == "Fante":
            return 2
        elif carta.valore == "Cavallo":
            return 3
        elif carta.valore == "Re":
            return 4
        elif carta.valore == 3:
            return 10
        else:
            return 0

    def determina_vincitore(self, carta_giocata, carta_giocata_computer):
        valore_carta_giocatore = self.assegna_valori(carta_giocata)
        valore_carta_computer = self.assegna_valori(carta_giocata_computer)
        
        if self.primo_giocatore == "giocatore":
            seme_prioritario = carta_giocata.seme
        else:
            seme_prioritario = carta_giocata_computer.seme

        #casi con briscola
        if carta_giocata.seme == self.seme_briscola and carta_giocata_computer.seme != self.seme_briscola:
            print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
            self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
            self.primo_giocatore = "giocatore"
        elif carta_giocata.seme != self.seme_briscola and carta_giocata_computer.seme == self.seme_briscola:
            print(colored("Il computer ha vinto questa mano.", "red"))
            self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
            self.primo_giocatore = "computer"
        elif carta_giocata.seme == self.seme_briscola and carta_giocata_computer.seme == self.seme_briscola:
            if valore_carta_giocatore > valore_carta_computer:
                print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                self.primo_giocatore = "giocatore"
            elif valore_carta_giocatore < valore_carta_computer:
                print(colored("Il computer ha vinto questa mano.", "red"))
                self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                self.primo_giocatore = "computer"
        #casi con seme uguale
        else:
            if carta_giocata.seme == carta_giocata_computer.seme:
                if valore_carta_giocatore > valore_carta_computer:
                    print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                    self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                    self.primo_giocatore = "giocatore"
                elif valore_carta_giocatore < valore_carta_computer:
                    print(colored("Il computer ha vinto questa mano.", "red"))
                    self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                    self.primo_giocatore = "computer"
                else:
                    if carta_giocata.valore > carta_giocata_computer.valore:
                        print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                        self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "giocatore"
                    elif carta_giocata.valore < carta_giocata_computer.valore:
                        print(colored("Il computer ha vinto questa mano.", "red"))
                        self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "computer"
            #casi con seme diverso
            else:
                if seme_prioritario == "denari":
                    if carta_giocata.seme == "denari":
                        print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                        self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "giocatore"
                    else:
                        print(colored("Il computer ha vinto questa mano.", "red"))
                        self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "computer"

                elif seme_prioritario == "coppe":
                    if carta_giocata.seme == "coppe":
                        print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                        self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "giocatore"
                    else:
                        print(colored("Il computer ha vinto questa mano.", "red"))
                        self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "computer"

                elif seme_prioritario == "bastoni":
                    if carta_giocata.seme == "bastoni":
                        print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                        self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "giocatore"
                    else:
                        print(colored("Il computer ha vinto questa mano.", "red"))
                        self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "computer"

                elif seme_prioritario == "spade":
                    if carta_giocata.seme == "spade":
                        print(colored(f"{self.giocatore.nome} ha vinto questa mano.", "green"))
                        self.giocatore.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "giocatore"
                    else:
                        print(colored("Il computer ha vinto questa mano.", "red"))
                        self.computer.punteggio += valore_carta_giocatore + valore_carta_computer
                        self.primo_giocatore = "computer"
        print("_________________________________________________________________________")

        
    def fine_partita(self):
        print(f"Il punteggio è: {self.giocatore.punteggio} per {self.giocatore.nome} e {self.computer.punteggio} per il computer.")
        if self.giocatore.punteggio > self.computer.punteggio:
            print(f"{self.giocatore.nome} ha vinto la partita con {self.giocatore.punteggio}.")
        elif self.giocatore.punteggio < self.computer.punteggio:
            print(f"Il computer ha vinto la partita con {self.computer.punteggio}.")
        else:
            print(f"{self.giocatore.nome} e il computer hanno pareggiato totalizzando entrambi {self.giocatore.punteggio}.")

    def nuova_partita(self):
        scelta_partita = input("Vuoi fare un'altra partita? (s/n) ")
        while scelta_partita not in ["s", "n"]:
            print("Errore scelta non valida.")
            scelta_partita = input("Vuoi fare un'altra partita? (s/n) ")
        if scelta_partita == "s":
            print(f"{self.giocatore.nome} vuole giocare un'altra partita.")
            print("_________________________________________________________________________")
            return True
        elif scelta_partita == "n":
            print(f"{self.giocatore.nome} abbandona il tavolo.")
            print("Grazie per aver giocato a Briscola romagnola in Python!")
            return False

    def gioca(self):
        while len(self.mazzo.carte) > 0 or len(self.giocatore.mano) > 0:
            if self.primo_giocatore == "giocatore":
                carta_giocata = self.giocatore.scegli_carta()
                carta_giocata_computer = self.computer.scegli_carta()
            else:
                carta_giocata_computer = self.computer.scegli_carta()
                carta_giocata = self.giocatore.scegli_carta()
            self.determina_vincitore(carta_giocata, carta_giocata_computer)
            if len(self.mazzo.carte) > 0:
                self.giocatore.mano.append(self.mazzo.estrai_carta())
                self.computer.mano.append(self.mazzo.estrai_carta())

        self.fine_partita()
        if self.nuova_partita():
            self.__init__()
            self.gioca()

# Start the game
partita = Partita()
partita.gioca()