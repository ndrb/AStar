# -*- coding: utf-8 -*-

import os
import argparse
import random
import copy
import numpy as np

# Enable command line history
# import readline
# readline.parse_and_bind('tab: complete')


class Joueur:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, etat, fct_but, fct_transitions, str_joueur):
        return self.func(etat, fct_but, fct_transitions, str_joueur)


def joueur_humain(etat, fct_but, fct_transitions, str_joueur):

    actions_str = '; '.join([a.__str__() for a in fct_transitions(etat).keys()])
    action = input('Entrer un choix d\'action puis appuyer sur Enter.\nChoisir parmi: {' + actions_str + '}\n')
    while True:
        try:
            action = eval(action)
            fct_transitions(etat)[action]
            break
        except:
            action = input('L\'action n\'est pas valide. Réessayer à nouveau, puis appuyer sur Enter\n')
    return action


def joueur_aleatoire(etat, fct_but, fct_transitions, str_joueur):
    action, etat = random.choice(list(fct_transitions(etat).items()))
    return action


class Jeu:

    """
    Classe de jeu.

    Initialize à partir de la fonction but,
    fonction transitions et l'état inital du jeu.

    La méthode "jouer_partie" simule une partie
    où un joueur Max (les 'X') et un joueur Min (les 'O')
    s'affrontent.
    """
    def __init__(self, etat_initial, fct_but, fct_transitions, verbose=True):
        self.but = fct_but
        self.transitions = fct_transitions
        self.etat_initial = etat_initial
        self.verbose = verbose
        self.resultat = None
        self.vainqueur = ''

    def resultat_partie(self):
        if self.resultat > 0:
            self.vainqueur = 'X'
            return 'Joueur X a gagné'

        if self.resultat < 0:
            self.vainqueur = 'O'
            return 'Joueur O a gagné'

        self.vainqueur = ''
        return 'Partie nulle'

    def afficher(self, str):
        if self.verbose:
            print(str)

    def jouer_partie(self, joueur_max, joueur_min):
        etat = copy.deepcopy(self.etat_initial)
        self.afficher(etat)
        while True:
            # X ###
            action = joueur_max(copy.deepcopy(etat), self.but, self.transitions, 'X')
            etat = self.transitions(etat)[action]
            self.afficher(etat)
            self.resultat = self.but(etat)

            if self.resultat is not None:
                self.afficher(self.resultat_partie())
                break

            # O ###
            action = joueur_min(copy.deepcopy(etat), self.but, self.transitions, 'O')
            etat = self.transitions(etat)[action]
            self.afficher(etat)
            self.resultat = self.but(etat)

            if self.resultat is not None:
                self.afficher(self.resultat_partie())
                break


#
# Etat, transitions et but pour le tic-tac-toe #
#
class TicTacToeEtat:

    def __init__(self):
        self.tableau = np.array([[' ', ' ', ' '],
                                 [' ', ' ', ' '],
                                 [' ', ' ', ' ']])

    def __str__(self):
        t = '''
   0   1   2
     |   |
0  {a} | {b} | {c}
     |   |
  ---+---+---
     |   |
1  {d} | {e} | {f}
     |   |
  ---+---+---
     |   |
2  {g} | {h} | {i}
     |   |
            '''.format(a=self.tableau[0, 0], b=self.tableau[0, 1], c=self.tableau[0, 2],
                       d=self.tableau[1, 0], e=self.tableau[1, 1], f=self.tableau[1, 2],
                       g=self.tableau[2, 0], h=self.tableau[2, 1], i=self.tableau[2, 2])
        return t


def tictactoe_transitions(etat):
    # Determiner c'est le tour à qui
    if np.sum(etat.tableau == 'X') > np.sum(etat.tableau == 'O'):
        # Tour de O
        symbol = 'O'
    else:
        # Tour de X
        symbol = 'X'
    positions_vides = np.nonzero(etat.tableau == ' ')
    actions = {}
    for i, j in zip(positions_vides[0], positions_vides[1]):
        nouvel_etat = copy.deepcopy(etat)
        nouvel_etat.tableau[i, j] = symbol
        actions[(i, j)] = nouvel_etat
    return actions


def tictactoe_but(etat):
    # Vérifie si X a gagné
    X_gagne = False
    X_gagne |= etat.tableau[0, 0] == 'X' and etat.tableau[0, 1] == 'X' and etat.tableau[0, 2] == 'X'
    X_gagne |= etat.tableau[1, 0] == 'X' and etat.tableau[1, 1] == 'X' and etat.tableau[1, 2] == 'X'
    X_gagne |= etat.tableau[2, 0] == 'X' and etat.tableau[2, 1] == 'X' and etat.tableau[2, 2] == 'X'
    X_gagne |= etat.tableau[0, 0] == 'X' and etat.tableau[1, 0] == 'X' and etat.tableau[2, 0] == 'X'
    X_gagne |= etat.tableau[0, 1] == 'X' and etat.tableau[1, 1] == 'X' and etat.tableau[2, 1] == 'X'
    X_gagne |= etat.tableau[0, 2] == 'X' and etat.tableau[1, 2] == 'X' and etat.tableau[2, 2] == 'X'
    X_gagne |= etat.tableau[0, 0] == 'X' and etat.tableau[1, 1] == 'X' and etat.tableau[2, 2] == 'X'
    X_gagne |= etat.tableau[0, 2] == 'X' and etat.tableau[1, 1] == 'X' and etat.tableau[2, 0] == 'X'

    if X_gagne:
        return 100000 + np.sum(etat.tableau == ' ')

    # Vérifie si O a gagné
    O_gagne = False
    O_gagne |= etat.tableau[0, 0] == 'O' and etat.tableau[0, 1] == 'O' and etat.tableau[0, 2] == 'O'
    O_gagne |= etat.tableau[1, 0] == 'O' and etat.tableau[1, 1] == 'O' and etat.tableau[1, 2] == 'O'
    O_gagne |= etat.tableau[2, 0] == 'O' and etat.tableau[2, 1] == 'O' and etat.tableau[2, 2] == 'O'
    O_gagne |= etat.tableau[0, 0] == 'O' and etat.tableau[1, 0] == 'O' and etat.tableau[2, 0] == 'O'
    O_gagne |= etat.tableau[0, 1] == 'O' and etat.tableau[1, 1] == 'O' and etat.tableau[2, 1] == 'O'
    O_gagne |= etat.tableau[0, 2] == 'O' and etat.tableau[1, 2] == 'O' and etat.tableau[2, 2] == 'O'
    O_gagne |= etat.tableau[0, 0] == 'O' and etat.tableau[1, 1] == 'O' and etat.tableau[2, 2] == 'O'
    O_gagne |= etat.tableau[0, 2] == 'O' and etat.tableau[1, 1] == 'O' and etat.tableau[2, 0] == 'O'

    if O_gagne:
        return -100000 - np.sum(etat.tableau == ' ')

    # Vérifie si c'est une partie nulle
    if np.sum(etat.tableau != ' ') == 9:
        return 0

    return None


def player_factory(player):
    if player == 'aleatoire':
        return joueur_aleatoire

    if player == 'humain':
        return joueur_humain

    if player.endswith('.py'):
        from importlib.machinery import SourceFileLoader

        player = os.path.abspath(player)
        name = player.replace('/', '.').replace('.', '_')
        solution = SourceFileLoader(name, player).load_module(name)

        return Joueur(player, solution.joueur_tictactoe)

    return None


DESCRIPTION = "Lancer une partie de Tic-Tac-Toe."


def buildArgsParser():
    p = argparse.ArgumentParser(description=DESCRIPTION,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Paramètres globaux
    p.add_argument('-joueur1', dest="player1", metavar="JOUEUR", action='store', type=str, required=False, default="solution_tictactoe.py",
                   help="'humain', 'aleatoire' ou le fichier contenant votre solution.")

    p.add_argument('-joueur2', dest="player2", metavar="JOUEUR", action='store', type=str, required=False, default="solution_tictactoe.py",
                   help="'humain', 'aleatoire' ou le fichier contenant votre solution.")

    p.add_argument('-v', dest='is_verbose', action='store_true', required=False,
                   help='activer le mode verbose')

    return p


#####
# Execution en tant que script
###
def main():
    parser = buildArgsParser()
    args = parser.parse_args()
    player1 = args.player1
    player2 = args.player2
    is_verbose = args.is_verbose

    if player1 == "humain" or player2 == "humain":
        is_verbose = True  # Afficher les grilles si c'est un joueur humain.

    if player1 not in ['aleatoire', 'humain'] and not player1.endswith('.py'):
        parser.error('Joueur 1 doit être [aleatoire, humain, solution_tictactoe.py]')

    if player2 not in ['aleatoire', 'humain'] and not player2.endswith('.py'):
        parser.error('Joueur 2 doit être [aleatoire, humain, solution_tictactoe.py]')

    if player1.endswith('.py') and not os.path.isfile(player1):
        parser.error("-joueur1 '{}' must be an existing file!".format(os.path.abspath(player1)))

    if player2.endswith('.py') and not os.path.isfile(player2):
        parser.error("-joueur2 '{}' must be an existing file!".format(os.path.abspath(player2)))

    # Jouer une partie de Tic-Tac-Toe
    tictactoe = Jeu(TicTacToeEtat(), tictactoe_but, tictactoe_transitions, verbose=is_verbose)
    tictactoe.jouer_partie(player_factory(player1), player_factory(player2))


if __name__ == "__main__":
    main()
