# =============================================================================
# R2.07 - TP2 : Coloration de graphes
# BARRY Mamadou Bailo
# Année 2025/2026
#
# IMPORTANT : Ce fichier contient les solutions en Python pur (sans SageMath).
#             Copiez chaque section dans une cellule séparée de votre notebook.
# =============================================================================


# ======================= CELLULE 1 : Fonctions utiles ========================
# Fonctions du TP précédent, adaptées pour Python pur
# (on utilise des listes de listes au lieu de matrices SageMath)

def voisins(M, x):
    """
    Retourne la liste des voisins du sommet x
    dans le graphe représenté par la matrice d'adjacence M.

    M : liste de listes (matrice d'adjacence)
    x : numéro du sommet
    """
    p = len(M[x])       # nombre de colonnes = nombre de sommets
    res = []
    for j in range(p):
        if M[x][j] == 1:
            res.append(j)
    return res


def degre(M, x):
    """
    Retourne le degré du sommet x dans le graphe de matrice M.
    Si x est relié à lui-même (boucle), on compte +1.

    M : liste de listes (matrice d'adjacence)
    x : numéro du sommet
    """
    L = voisins(M, x)
    if x in L:
        return len(L) + 1   # boucle : on ajoute 1
    else:
        return len(L)


# Matrice d'adjacence M donnée dans le sujet (graphe à 6 sommets : 0 à 5)
M = [
    [0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0]
]

# Vérification rapide
print("=== Vérification de la matrice M ===")
for i in range(len(M)):
    print(f"Sommet {i} : voisins = {voisins(M, i)}, degré = {degre(M, i)}")
print()


# =================== CELLULE 2 : Exercice 1 =================================
# Construire une fonction color1(M, sommets) qui retourne une partition telle que :
#   - chaque sommet donné en paramètre reçoit une couleur distincte
#   - les autres sommets sont dans un groupe "autre couleur"
#
# Une "partition" est ici une liste de listes.
# Chaque sous-liste contient les sommets d'une même couleur.

def color1(M, sommets):
    """
    Retourne une partition permettant :
    - d'affecter des couleurs distinctes aux sommets donnés
    - de colorer les autres sommets d'une autre couleur

    M       : matrice d'adjacence (liste de listes)
    sommets : liste des sommets à colorer individuellement

    Retour : liste de listes (partition)
             Chaque sous-liste = un groupe de même couleur.
             Le dernier groupe contient les "autres" sommets.
    """
    n = len(M)
    partition = []

    # Chaque sommet donné reçoit sa propre couleur (sous-liste individuelle)
    for s in sommets:
        partition.append([s])

    # Les sommets restants vont dans un groupe "autre"
    autres = []
    for i in range(n):
        if i not in sommets:
            autres.append(i)

    if len(autres) > 0:
        partition.append(autres)

    return partition


# Test (comme dans le sujet : color1(M, [0, 2, 4]))
print("=== Exercice 1 ===")
C = color1(M, [0, 2, 4])
print("Partition :", C)
print("Explication :")
for i, groupe in enumerate(C):
    print(f"  Couleur {i + 1} : sommets {groupe}")
print()


# =================== CELLULE 3 : Exercice 2 =================================
# Construire une fonction color2(M, x) qui retourne une partition telle que :
#   - le sommet x et chacun de ses voisins reçoivent une couleur différente
#   - les autres sommets sont dans un groupe "autre couleur"

def color2(M, x):
    """
    Retourne une partition permettant :
    - de colorer le sommet x avec une couleur
    - de colorer chacun de ses voisins avec une couleur différente
    - de colorer les autres sommets d'une autre couleur

    M : matrice d'adjacence (liste de listes)
    x : numéro du sommet central

    Retour : liste de listes (partition)
    """
    n = len(M)

    # Le sommet x et ses voisins : chacun dans sa propre sous-liste
    sommets_colores = [x] + voisins(M, x)
    partition = []
    for s in sommets_colores:
        partition.append([s])

    # Les sommets restants dans un groupe "autre"
    autres = []
    for i in range(n):
        if i not in sommets_colores:
            autres.append(i)

    if len(autres) > 0:
        partition.append(autres)

    return partition


# Test (comme dans le sujet : color2(M, 2))
print("=== Exercice 2 ===")
P = color2(M, 2)
print("Partition pour le sommet 2 :", P)
print(f"Le sommet 2 a pour voisins : {voisins(M, 2)}")
print("Explication :")
for i, groupe in enumerate(P):
    print(f"  Couleur {i + 1} : sommets {groupe}")
print()


# =================== CELLULE 4 : Exercice 3 =================================
# Construire une fonction color3(M) qui retourne une partition telle que :
#   - une couleur pour le(s) sommet(s) de plus haut degré
#   - une couleur pour le(s) sommet(s) de plus bas degré
#   - une autre couleur pour les sommets restants

def color3(M):
    """
    Retourne une partition permettant :
    - de colorer le(s) sommet(s) de plus haut degré en une couleur
    - de colorer le(s) sommet(s) de plus bas degré en une autre couleur
    - de colorer les autres sommets d'une autre couleur

    M : matrice d'adjacence (liste de listes)

    Retour : liste de listes (partition)
    """
    n = len(M)

    # Calculer le degré de chaque sommet
    degres = []
    for i in range(n):
        degres.append(degre(M, i))

    # Trouver le degré max et le degré min
    degre_max = max(degres)
    degre_min = min(degres)

    # Grouper les sommets
    groupe_max = []    # sommet(s) de plus haut degré
    groupe_min = []    # sommet(s) de plus bas degré
    autres = []        # les autres

    for i in range(n):
        if degres[i] == degre_max:
            groupe_max.append(i)
        elif degres[i] == degre_min:
            groupe_min.append(i)
        else:
            autres.append(i)

    # Construire la partition
    partition = [groupe_max, groupe_min]
    if len(autres) > 0:
        partition.append(autres)

    return partition


# Test
print("=== Exercice 3 ===")
C = color3(M)
print("Partition :", C)
print("Explication :")
# Afficher les degrés de tous les sommets
for i in range(len(M)):
    print(f"  Sommet {i} -> degré {degre(M, i)}")
print()
for i, groupe in enumerate(C):
    if i == 0:
        print(f"  Plus haut degré  (couleur 1) : sommets {groupe}")
    elif i == 1:
        print(f"  Plus bas degré   (couleur 2) : sommets {groupe}")
    else:
        print(f"  Autres           (couleur 3) : sommets {groupe}")
print()


# ======================= CELLULE 2 : Exercice 4 =============================
# 1. Construire la matrice d'adjacence M1 du graphe G1
#
# Le graphe G1 a 5 sommets : 0, 1, 2, 3, 4
# Complétez cette matrice selon l'image du graphe G1 dans le sujet du TP.
#
# Chaque ligne i et chaque colonne j contiennent :
#   1 si les sommets i et j sont reliés
#   0 sinon
# La diagonale est toujours à 0 (pas de boucle)

M1 = [
    [0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0]
]
# NOTE : Adaptez M1 en regardant l'image du graphe G1 dans le sujet !

print("=== Exercice 4 ===")
print("Matrice M1 :")
for ligne in M1:
    print(ligne)
print()

# Vérification : voisins et degrés de chaque sommet
for i in range(len(M1)):
    print(f"Sommet {i} : voisins = {voisins(M1, i)}, degré = {degre(M1, i)}")
print()


# 2. Algorithme glouton simplifié
def glouton(M):
    """
    Retourne la liste des couleurs attribuées à chaque sommet
    du graphe de matrice M, en utilisant l'algorithme glouton simplifié.

    Algorithme :
    Pour chaque sommet x (dans l'ordre 0, 1, 2, ...),
    on lui attribue la première couleur (1, 2, 3, ...)
    qui n'est utilisée par aucun de ses voisins.

    Retour : liste de couleurs (index = sommet, valeur = couleur)
    """
    n = len(M)
    couleurs = [0] * n   # 0 signifie "pas encore coloré"

    for x in range(n):
        # Étape 1 : trouver les couleurs déjà utilisées par les voisins
        couleurs_voisins = set()
        for v in voisins(M, x):
            if couleurs[v] != 0:
                couleurs_voisins.add(couleurs[v])

        # Étape 2 : trouver la première couleur libre (1, 2, 3, ...)
        pc = 1
        while pc in couleurs_voisins:
            pc += 1

        # Étape 3 : attribuer cette couleur au sommet x
        couleurs[x] = pc

    return couleurs


# Test
coloration_g1 = glouton(M1)
print("Coloration glouton de G1 :", coloration_g1)
print(f"Nombre de couleurs utilisées : {max(coloration_g1)}")
print()

# 3. La coloration est-elle optimale ?
# Réponse : Pas forcément ! L'algorithme glouton simplifié ne garantit pas
# d'utiliser le nombre minimum de couleurs (le nombre chromatique).
# Le résultat dépend de l'ordre dans lequel on traite les sommets.


# ======================= CELLULE 3 : Exercice 5 =============================
# Tri des sommets par degré

def tri_degre(M, Bool):
    """
    Renvoie la liste des sommets triés suivant leur degré.

    M    : matrice d'adjacence (liste de listes)
    Bool : si True  -> ordre décroissant (du plus grand degré au plus petit)
           si False -> ordre croissant   (du plus petit degré au plus grand)

    On utilise la méthode sort() avec le paramètre key.
    """
    n = len(M)
    sommets = list(range(n))   # [0, 1, 2, ..., n-1]

    # Fonction qui retourne le degré d'un sommet
    def degre_sommet(x):
        return degre(M, x)

    # Tri avec la fonction degre_sommet comme clé
    sommets.sort(key=degre_sommet, reverse=Bool)

    return sommets


# Tests
print("=== Exercice 5 ===")
print("Sommets de G1 triés par degré décroissant :", tri_degre(M1, True))
print("Sommets de G1 triés par degré croissant :", tri_degre(M1, False))
print()

# Affichage détaillé
for s in tri_degre(M1, True):
    print(f"  Sommet {s} -> degré {degre(M1, s)}")
print()


# ======================= CELLULE 4 : Exercice 6 =============================
# Algorithme de Welsh-Powell (glouton amélioré)

def glouton2(M):
    """
    Amélioration de l'algorithme glouton en classant préalablement
    les sommets par ordre de degré décroissant (Welsh-Powell).

    Retour : liste de couleurs (index = sommet, valeur = couleur)
    """
    n = len(M)
    couleurs = [0] * n

    # On parcourt les sommets dans l'ordre de degré décroissant
    sommets_tries = tri_degre(M, True)

    for x in sommets_tries:
        # Trouver les couleurs utilisées par les voisins de x
        couleurs_voisins = set()
        for v in voisins(M, x):
            if couleurs[v] != 0:
                couleurs_voisins.add(couleurs[v])

        # Première couleur non utilisée
        pc = 1
        while pc in couleurs_voisins:
            pc += 1

        couleurs[x] = pc

    return couleurs


# Tests
print("=== Exercice 6 ===")
coloration_g1_v2 = glouton2(M1)
print("Coloration glouton amélioré (Welsh-Powell) de G1 :", coloration_g1_v2)
print(f"Nombre de couleurs utilisées : {max(coloration_g1_v2)}")
print()

# Comparaison
print("Comparaison :")
print(f"  Glouton simplifié  : {max(glouton(M1))} couleur(s)")
print(f"  Welsh-Powell       : {max(glouton2(M1))} couleur(s)")
print()


# ======================= CELLULE 5 : Exercice 7 =============================
# Résolution d'un mini-Sudoku 4×4 par coloration de graphe
#
# On considère un mini-sudoku de 16 cases.
# Chaque case est un sommet (0 à 15).
# Deux sommets sont reliés s'ils ne peuvent pas avoir la même couleur :
#   - même ligne
#   - même colonne
#   - même carré 2×2

# Matrice d'adjacence du mini-sudoku (donnée dans le sujet)
sud = [
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0]
]


def sudoku(sommets, couleurs):
    """
    Propose une coloration du mini-sudoku en respectant
    les contraintes initiales.

    sommets  : liste des numéros de sommets déjà colorés
    couleurs : liste des couleurs associées à ces sommets

    Retour : liste de 16 couleurs (une par case du sudoku)

    On utilise l'algorithme glouton modifié :
    à chaque étape, on choisit le sommet non coloré
    ayant le plus de voisins déjà colorés (le plus contraint).
    Cela permet d'obtenir une coloration optimale à 4 couleurs.

    Exemple :
        sudoku([0, 2, 4, 11, 13], [1, 2, 3, 4, 1])
        -> [1, 4, 2, 3, 3, 2, 4, 1, 2, 3, 1, 4, 4, 1, 3, 2]
    """
    n = len(sud)          # 16 sommets
    resultat = [0] * n    # 0 = pas encore coloré

    # Étape 1 : placer les couleurs initiales (contraintes du sudoku)
    for i in range(len(sommets)):
        resultat[sommets[i]] = couleurs[i]

    # Étape 2 : colorer les sommets restants un par un
    # À chaque tour, on choisit le sommet non coloré
    # ayant le plus de voisins déjà colorés (le plus contraint)
    for _ in range(n):
        # Chercher le sommet non coloré le plus contraint
        meilleur_sommet = -1
        meilleur_score = -1

        for x in range(n):
            if resultat[x] != 0:
                continue   # déjà coloré

            # Compter combien de voisins sont déjà colorés
            score = 0
            for v in voisins(sud, x):
                if resultat[v] != 0:
                    score += 1

            if score > meilleur_score:
                meilleur_score = score
                meilleur_sommet = x

        if meilleur_sommet == -1:
            break   # tous les sommets sont colorés

        x = meilleur_sommet

        # Trouver les couleurs utilisées par les voisins
        couleurs_voisins = set()
        for v in voisins(sud, x):
            if resultat[v] != 0:
                couleurs_voisins.add(resultat[v])

        # Première couleur non utilisée (1, 2, 3 ou 4)
        pc = 1
        while pc in couleurs_voisins:
            pc += 1

        resultat[x] = pc

    return resultat


# Test avec l'exemple du sujet
print("=== Exercice 7 ===")
solution = sudoku([0, 2, 4, 11, 13], [1, 2, 3, 4, 1])
print("Solution du sudoku :", solution)
print()


# ======================= CELLULE 6 : Exercice 8 =============================
# Affichage du sudoku sous forme de tableau 4×4

def sudoku_tableau(sommets, couleurs):
    """
    Affiche le sudoku résolu sous forme d'un tableau 4 par 4.

    sommets  : liste des sommets déjà colorés
    couleurs : liste des couleurs associées

    Les 16 cases sont numérotées de 0 à 15 :
        0  1  2  3     (ligne 0)
        4  5  6  7     (ligne 1)
        8  9  10 11    (ligne 2)
        12 13 14 15    (ligne 3)
    """
    solution = sudoku(sommets, couleurs)

    for i in range(4):
        # Extraire les 4 valeurs de la ligne i
        ligne = solution[i * 4 : (i + 1) * 4]
        print(ligne)


# Test
print("=== Exercice 8 ===")
print("Sudoku résolu sous forme de tableau :")
sudoku_tableau([0, 2, 4, 11, 13], [1, 2, 3, 4, 1])
