# -*- coding: utf-8 -*-

#####
# VotreNom (VotreMatricule) .~= À MODIFIER =~.
###

# Utiliser dbg() pour faire un break dans votre code.
from pdb import set_trace as dbg


#
# AEtoileTuple : Classe représentant un tuple de TaquinEtat, score f et d'un parent
# AEtoileTuple.
# AEtoile Nodes
class AEtoileTuple:

    def __init__(self, etat, f, parent=None):
        self.etat = etat
        self.f = f
        self.parent = parent

    # Fonction de comparaison entre deux AEtoileTuple.
    def __lt__(self, autre):
        return self.f < autre.f

    # Fonctions d'équivalence entre deux AEtoileTuple.
    def __eq__(self, autre):
        return self.etat == autre.etat

    def __ne__(self, autre):
        return not (self == autre)


def AEtoile(start, isGoal, transitions, heuristique, cost):

    #Reminder: f(n) tries to calculate the optimal path between n and the goal
    #We separate the calculation of f(n) into two parts:
    #   g(n): cout du meilleur chemin du depart jusqua n
    #   h(n): estimated optimal cost from n to goal, the heuristique function

    n = None
    nPrime = None
    open = []
    closed = []

    starterNode = AEtoileTuple(start, heuristique(start), None)
    open.append(starterNode)
    print(isinstance(start, AEtoileTuple))
    while(1):
        #print("while lol")
        if not open:
            break
        n = open[-1]
        container = open.pop(-1)
        closed.append(container)

        if isGoal(n.etat):
           break

        nPrimes = transitions(n.etat)
        for etat in nPrimes:
            gn = n.f
            gnprime = gn + cost(n, etat)
            nodle = AEtoileTuple(etat, heuristique(etat)+gnprime, n)

            boolz = False;
            for i in range(len(open)):
                if open[i].__eq__(nodle) and nodle.f <= open[i].f:
                    open.append(open.pop(i))
                    boolz = True
            for i in range(len(closed)):
                if closed[i].__eq__(nodle) and nodle.f <= closed[i].f:
                    open.append(closed.pop(i))
                    boolz = True

            if boolz == False:
                open.append(nodle)






    #This is pretty much the only function you gotta touch
    #The heuristique funtion is already coded and you just call it to get the value from your current state to the final state, this is done with a recherche en largeur

    #print(start) # affiche l'etat de depart

    #We want to use the AEToileTuple which are our objects
    #start is an object of type TaquinEtat
    #Giving the first state this will give you all the possible and returns a list of neighbouring states

    #Now that I have all the next possible states, I must chose the most optimal one and then add it to my closed list

    #Has to be the optimal solution
    print("About to return")
    return closed # This juste returns a list with the first element, you need to return a list with all states
#
# joueur_taquin : Fonction qui calcule le chemin, suite d'états, optimal afin de complété
#                  le puzzle.
#
# etat_depart: Objet de la classe TaquinEtat indiquant l'état initial du jeu.
#
# fct_estEtatFinal: Fonction qui prend en entrée un objet de la classe TaquinEtat et
#                   qui vérifie si l'état passée en paramêtre est l'état final ou non.
#
# fct_transitions: Fonction qui prend en entrée un objet de la classe TaquinEtat et
#                   qui retourne la listes des états voisins pour l'état donné.
#
# fct_heuristique: Fonction qui prend en entrée un objet de la classe TaquinEtat et
#                   qui retourne le coût heuristique pour se rendre à l'état final.
#
# retour: Cette fonction retourne la liste des états de la solution triés en ordre chronologique
#          c'est-à-dire de l'état initial jusqu'à l'état final inclusivement.
#


def joueur_taquin(etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique):
    def fct_cout(x, y): return 1
    return AEtoile(etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique, fct_cout)