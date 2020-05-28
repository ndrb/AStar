# -*- coding: utf-8 -*-
import math
import random
#####
# VotreNom (VotreMatricule) .~= À MODIFIER =~.
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np


########################
# Solution tic-tac-toe #
########################

#####
# joueur_tictactoe : Fonction qui calcule le prochain coup optimal pour gagner la
#                     la partie de Tic-tac-toe à l'aide d'Alpha-Beta Prunning.
#
# etat: Objet de la classe TicTacToeEtat indiquant l'état actuel du jeu.
#
# fct_but: Fonction qui prend en entrée un objet de la classe TicTacToeEtat et
#          qui retourne le score actuel tu plateau. Si le score est positif, les 'X' ont l'avantage
#          si c'est négatif ce sont les 'O' qui ont l'avantage, si c'est 0 la partie est nulle.
#
# fct_transitions: Fonction qui prend en entrée un objet de la classe TicTacToeEtat et
#                   qui retourne une liste de tuples actions-états voisins pour l'état donné.
#
# str_joueur: String indiquant c'est à qui de jouer : les 'X' ou 'O'.
#
# retour: Cette fonction retourne l'action optimal à joueur pour le joueur actuel c.-à-d. 'str_joueur'.
###
def joueur_tictactoe(etat, fct_but, fct_transitions, str_joueur):
    # Find the next best move
    # This function needs to find the most efficient NEXT STEP to the game depending on the player
    # Do we really need to go into depth or we only need to check the following function?
    # value = (alphabeta(-math.inf, math.inf, etat, fct_but, fct_transitions, str_joueur))
    values = [] # List avec des dictionnaire
    for i in fct_transitions(etat).items():
        values.append([i[0], (alphabeta(-math.inf, math.inf, i[1], fct_but, fct_transitions, str_joueur))])

    print(values)

    if str_joueur == 'X':
        best_value = -math.inf
    else:
        best_value = math.inf

    best_action = ""
    for i in values:
        if str_joueur == 'X' and i[1] > best_value:
            best_value = i[1]
            best_action = i[0]
        if str_joueur == 'O' and i[1] < best_value:
            best_value = i[1]
            best_action = i[0]

    print(best_value)
    print(best_action)
    print("Done")

    action = best_action
    # action = random.choice(list(fct_transitions(etat)))
    return action


def alphabeta(alpha, beta, etat, fct_but, fct_transitions, str_joueur):
    if fct_but(etat) is not None:
        return fct_but(etat)

    states = fct_transitions(etat).items()

    if str_joueur == 'X':
        maxEval = -math.inf
        for children in states:
            eval = alphabeta(alpha, beta, children[1], fct_but, fct_transitions, 'O')
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = math.inf
        for children in states:
            eval = alphabeta(alpha, beta, children[1], fct_but, fct_transitions, 'X')
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
