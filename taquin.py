# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np
import random

# Enable command line history
# import readline
# readline.parse_and_bind('tab: complete')


def joueur_humain(
    etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique
):
    etat = etat_depart
    yield etat
    while not fct_estEtatFinal(etat):
        actions_str = '; '.join([a.__str__()
                                 for a in fct_transitions(etat).keys()])
        action = input(
            'Entrer un choix d\'action puis appuyer sur Enter.\nChoisir parmi: {' + actions_str + '}\n')
        while True:
            try:
                action = eval(action)
                fct_transitions(etat)[action]
                break
            except:
                action = input(
                    'L\'action n\'est pas valide. Réessayer à nouveau, puis appuyer sur Enter\n')

        etat = fct_transitions(etat)[action]
        yield etat


class Jeu:

    """
    Classe de jeu.

    Initialisation à partir de la fonction but,
    fonction transitions et l'état inital du jeu.

    La méthode "jouer_partie" simule une partie.
    """

    def __init__(self, etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique, verbose=False):
        self.etat_initial = etat_depart
        self.but = fct_estEtatFinal
        self.transitions = fct_transitions
        self.heuristique = fct_heuristique
        self.verbose = verbose

    def jouer_partie(self, joueur):
        etat = self.etat_initial
        nb_coups = 0

        for etat in joueur(etat, self.but, self.transitions, self.heuristique):
            self.afficher(etat)
            nb_coups += 1

        if taquin_estBut(etat):
            print('Vous avez gagné! ({0} coups)'.format(nb_coups))
        else:
            print('Vous avez perdu! ({0} coups)'.format(nb_coups))

    def afficher(self, msg):
        if self.verbose:
            print(msg)


#####
# Etat, transitions et but pour le Taquin #
###
class TaquinEtat:

    def __init__(self, seed=None, etat=None):
        self.largeur = 3
        self.hauteur = 3

        # Initialisation du casse-tête pour validation.
        self.tableau = np.array([['6', '2', '3'],
                                 ['7', ' ', '8'],
                                 ['4', '1', '5']]).astype(str)

        # Construction aléatoire du plateau.
        if seed is not None:
            self._randomize(seed)

        elif etat is not None:
            self._from_other(etat)

    def _from_other(self, etat):
        self.tableau = etat.astype(str)

    # Création d'un plateau généré aléatoirement.
    def _randomize(self, seed):
        self.tableau = np.array([['1', '2', '3'],
                                 ['4', '5', '6'],
                                 ['7', '8', ' ']])

        rnd = random.Random(seed)
        for i in range(1000):
            etat = rnd.choice(list(taquin_transitions(self).values()))
            self.tableau = etat.tableau

    # Trouve les coordonnées de la pièce désirée.
    def find(self, case):
        return np.array(np.where(self.tableau == case))

    # Calculer le facteur d'ordonnancement pour cet état.
    def calculer_ordre(self):
        txt = "".join(self.tableau.flat)
        txt = txt.replace(' ', '0')
        return 1 - (int(txt) / 876543210.)

    def __eq__(self, other):
        # dbg()
        # return np.array_equal(self.tableau, other.tableau)
        return np.array((self.tableau.astype(str) == other.tableau.astype(str))).all()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash("".join(self.tableau.flat))

    def __str__(self):
        self.tableau = self.tableau.astype(str)
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
                       d=self.tableau[1, 0], e=self.tableau[1,
                                                            1], f=self.tableau[1, 2],
                       g=self.tableau[2, 0], h=self.tableau[2, 1], i=self.tableau[2, 2])
        return t


def taquin_transitions(etat):
    # Déterminer l'emplacement de la case vide
    y, x = etat.find(' ')

    # Quatre choix sont théoriquement possibles
    actionsPossibles = [(y - 1, x), (y + 1, x),
                        (y, x - 1), (y, x + 1)]

    actions = {}
    for i, j in actionsPossibles:
        # Vérifier si la possible position se trouve à l'intérieur du tableau
        if 0 > i or i >= etat.hauteur or 0 > j or j >= etat.largeur:
            continue

        nouvelEtat = TaquinEtat()
        nouvelEtat.tableau = np.copy(etat.tableau)
        nouvelEtat.tableau[y, x] = nouvelEtat.tableau[i, j]
        nouvelEtat.tableau[i, j] = ' '
        actions[(i[0], j[0])] = nouvelEtat

    return actions


def taquin_transitions_agent(etat):
    return taquin_transitions(etat).values()


def taquin_but():
    but = TaquinEtat()
    but.tableau = np.array([['1', '2', '3'],
                            ['4', '5', '6'],
                            ['7', '8', ' ']])

    return but


def taquin_estBut(etat):
    return etat == g_etatFinal


def taquin_heuristique(etat):
    coutHeuristique = 0

    for i, pos in enumerate(g_positionsFinales, start=1):
        y1x1 = etat.find(str(i))
        y2x2 = pos
        coutHeuristique += np.sum(np.abs(y2x2 - y1x1))

    coutHeuristique -= etat.calculer_ordre()
    return max(coutHeuristique, 0)


#####
# Variable globale #
###
g_etatFinal = taquin_but()

# Position des cases 1 à 8 inclusivement.
g_positionsFinales = [np.array((0, 0)), np.array((0, 1)), np.array((0, 2)),
                      np.array((1, 0)), np.array((1, 1)), np.array((1, 2)),
                      np.array((2, 0)), np.array((2, 1))]

g_etats = []


def etats_cote_a_cote(e1, e2):
    lignes1 = str(e1).split('\n')
    lignes2 = str(e2).split('\n')

    msg = [l1 + '         ' + l2 for l1, l2 in zip(lignes1[:-1], lignes2[:-1])]
    return "\n".join(msg)


def evaluation(solution_file):
    import pickle
    # pickle.dump(g_etats, open(solution_file,'wb'))
    solutionEtats = pickle.load(open(solution_file, 'rb'))

    if solutionEtats[0] != g_etats[0]:
        print('Erreur: États initiaux incohérents. Avez-vous oublié de l\'ajouter à votre solution ?')
        return


    if len(g_etats) != len(solutionEtats):
        print("Erreur: votre solution comporte {0} coups, alors que vous devriez en avoir {1}!".format(
            len(g_etats), len(solutionEtats)))
        return

    no_etats_errones = []

    for i, (e1, e2) in enumerate(zip(g_etats, solutionEtats), start=1):
        if e1 != e2:
            print("État #{0}: Erreur l'état diffère de la solution.".format(i))
            no_etats_errones.append(i)
        else:
            print(
                "État #{0}: Votre joueur obtient bien l'état attendu, bravo!".format(i))

        print("  Votre coup     |       Solution  ")
        print("-----------------+-----------------")
        print(etats_cote_a_cote(e1, e2))
        print("")

    if len(no_etats_errones) > 0:
        print("Erreur: les états suivants ne correspondent pas à la solution: {0}".format(
            ",".join(map(str, no_etats_errones))))
    else:
        print("Bravo, vous n'avez pas d'erreur.")


#####
# Execution en tant que script
###
def player_factory(player):
    if player == 'humain':
        return joueur_humain

    if player.endswith('.py'):
        from importlib.machinery import SourceFileLoader

        player = os.path.abspath(player)
        name = player.replace('/', '.').replace('.', '_')
        solution = SourceFileLoader(name, player).load_module(name)

        # S'occupe de créer un générateur une fois la solution trouvée
        def joueurAgent(etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique):
            global g_etats
            g_etats = solution.joueur_taquin(
                etat_depart, fct_estEtatFinal, fct_transitions, fct_heuristique)
            return iter(g_etats)

        return joueurAgent

    return None


DESCRIPTION = "Lancer une partie de taquin."


def buildArgsParser():
    p = argparse.ArgumentParser(description=DESCRIPTION,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Paramètres globaux
    p.add_argument('-joueur', dest="player", metavar="JOUEUR", action='store', type=str, required=False, default="solution_taquin.py",
                   help="'humain' ou le fichier contenant votre solution.")

    p.add_argument('-no_partie', dest="no_partie", metavar="INT", action='store', type=int, required=False,
                   help="numéro de partie à jouer.")

    p.add_argument('-valider', dest="validation_file", metavar="FICHIER", action='store', type=str, required=False, default='taquin_validation.pkl',
                   help="fichier permettant de valider votre joueur pour un jeu donné.")

    p.add_argument('-v', dest='verbose', action='store_true', required=False,
                   help='activer le mode verbose')

    return p


#####
# Execution en tant que script
###
def main():
    parser = buildArgsParser()
    args = parser.parse_args()
    player = args.player
    no_partie = args.no_partie
    validation_file = args.validation_file
    verbose = args.verbose

    if player == "humain":
        verbose = True  # Afficher les grilles si c'est un joueur humain.

    if player not in ['humain'] and not player.endswith('.py'):
        parser.error('Joueur doit être [humain, solution_taquin.py]')

    if no_partie is None and not os.path.isfile(validation_file):
        parser.error("Fichier introuvable: '{0}'".format(validation_file))

    # Jouer une partie de taquin
    taquin = Jeu(TaquinEtat(no_partie), taquin_estBut,
                 taquin_transitions, taquin_heuristique, verbose)

    if player != "humain":
        taquin.transitions = taquin_transitions_agent

    taquin.jouer_partie(player_factory(player))

    if no_partie is None:
        evaluation(validation_file)


if __name__ == "__main__":
    main()
