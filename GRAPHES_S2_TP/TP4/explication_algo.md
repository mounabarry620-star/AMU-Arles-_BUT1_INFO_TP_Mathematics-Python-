# TP4 – Recherche de plus courte chaîne (Guide pas à pas)

Ce guide explique **chaque ligne de code** avec une logique simple pour un étudiant débutant.

---

## 🔧 Préparation : les graphes du TP

Le TP demande **deux graphes** pour tester les algorithmes.

### Graphe `g` (orienté, pondéré)

```python
g = DiGraph(weighted = True)
g.add_edges([(1, 2, 8), (1,3,2), (2,4,1), (3,2,5), (3,4, 11), (3,5,1), (5, 4, 9)])
g.show()
```

### Graphe `g2` (non orienté, pondéré) — ⚠️ à ajouter dans ton notebook

```python
g2 = Graph()
g2.add_edges([(0,1,2), (0,2,4), (0,3,3), (0,4,6), (1,2,7), (2,3,2), (2,4,8), (3,4,1)])
g2.show()
```

### Matrices de poids

```python
M = g.weighted_adjacency_matrix()
print(M)

M2 = g2.weighted_adjacency_matrix()
print(M2)
```

> [!IMPORTANT]
> Dans SageMath, la matrice d'adjacence met **0** là où il n'y a **pas d'arête**. Mais dans l'algorithme, on a besoin de **+∞** (infini). Il faudra gérer cette conversion dans notre code !

---

## Exercice 1 : Bellman-Ford (simplifié)

### 🧠 L'idée en français

Imagine que tu veux trouver la distance la plus courte **du sommet 0 vers tous les autres sommets**.

**Le principe est ultra simple :**
1. Au début, on dit : "la distance vers le sommet 0, c'est 0" (logique, on y est déjà !)
2. Pour tous les autres sommets, on dit : "la distance, c'est l'infini" (on ne sait pas encore comment y aller)
3. Ensuite, on **regarde chaque arc du graphe** et on se demande : "est-ce que passer par cet arc raccourcit le chemin ?"
4. On **répète** l'étape 3 jusqu'à ce que plus rien ne change

### 📝 Le pseudo-code du TP (traduit en français)

```
Fonction Bellman_Ford(M) :
    n = nombre de sommets

    # Étape 1 : Tout est à l'infini sauf le départ
    Dist = [Infinity, Infinity, Infinity, ..., Infinity]   # une case par sommet
    Dist[0] = 0                                             # distance vers soi-même = 0

    # Étape 2 : On répète tant que ça change
    TANT QUE Dist change :
        POUR chaque sommet i :
            POUR chaque sommet j :
                SI Dist[i] + M[i][j] < Dist[j] :
                    Dist[j] = Dist[i] + M[i][j]
                    # "Passer par i pour aller à j est plus court !"

    RETOURNER Dist
```

### 🔍 Explication ligne par ligne du code SageMath

```python
def Bellman_Ford(M):
```
> On **définit** une fonction qui prend `M` (la matrice de poids) en entrée.

---

```python
    n = M.nrows()
```
> `M.nrows()` donne le **nombre de lignes** de la matrice = le nombre de sommets. On le stocke dans `n`.

---

```python
    Dist = [Infinity] * n
```
> On crée une **liste** de taille `n` remplie de `Infinity`. Par exemple, si `n = 5`, ça donne : `[Infinity, Infinity, Infinity, Infinity, Infinity]`. C'est comme dire : "je ne sais pas encore comment aller à ces sommets".

---

```python
    Dist[0] = 0
```
> Le sommet 0 (le départ), sa distance est **0** : on y est déjà !

---

```python
    changement = True
```
> On crée une variable `changement` mise à `True`. C'est un **drapeau** (flag) : il sert à savoir si quelque chose a changé. On le met à `True` au début pour **entrer dans la boucle**.

---

```python
    while changement:
```
> **Tant que** quelque chose a changé, on continue. Si plus rien ne change, on s'arrête.

---

```python
        changement = False
```
> Au début de chaque tour de boucle, on suppose que **rien ne va changer**. Si quelque chose change plus bas, on remettra `changement = True`.

---

```python
        for i in range(n):
```
> On parcourt **chaque sommet** `i` (de 0 à n-1).

---

```python
            for j in range(n):
```
> Pour chaque sommet `i`, on regarde **tous les autres sommets** `j`.

---

```python
                poids = M[i][j]
```
> On récupère le **poids** de l'arc entre `i` et `j` dans la matrice.

---

```python
                if poids == 0 and i != j:
                    poids = Infinity
```
> ⚠️ **Piège de SageMath !** La matrice met `0` quand il n'y a **pas d'arc**. Mais `0` n'est pas l'infini ! Donc si le poids est `0` et que `i ≠ j` (ce n'est pas le même sommet), on remplace par `Infinity`. Si `i == j`, le poids 0 est normal (distance d'un sommet à lui-même).

---

```python
                if Dist[i] + poids < Dist[j]:
```
> **La question clé** : "Est-ce que passer par `i` pour aller à `j` est **plus court** que ce qu'on connaît déjà ?"
> - `Dist[i]` = distance connue pour aller au sommet `i`
> - `poids` = coût pour aller de `i` à `j`
> - `Dist[i] + poids` = coût total en passant par `i`
> - On compare avec `Dist[j]` (la meilleure distance connue pour `j`)

---

```python
                    Dist[j] = Dist[i] + poids
                    changement = True
```
> Si c'est plus court, on **met à jour** la distance et on note qu'il y a eu un changement (donc on refera un tour de boucle).

---

```python
    return Dist
```
> À la fin, on retourne la liste des distances.

### ✅ Code complet de Bellman-Ford

```python
def Bellman_Ford(M):
    n = M.nrows()                     # nombre de sommets
    Dist = [Infinity] * n             # tout à l'infini
    Dist[0] = 0                       # le départ est à distance 0

    changement = True                 # drapeau pour la boucle
    while changement:                 # tant que ça change
        changement = False            # on suppose que rien ne change
        for i in range(n):            # pour chaque sommet i
            for j in range(n):        # pour chaque sommet j
                poids = M[i][j]
                if poids == 0 and i != j:
                    poids = Infinity  # 0 = pas d'arc = infini
                if Dist[i] + poids < Dist[j]:
                    Dist[j] = Dist[i] + poids
                    changement = True # on a trouvé un raccourci !
    return Dist
```

### 🧪 Tests attendus

```python
print(Bellman_Ford(M))    # → [0, 7, 2, 8, 3]
print(Bellman_Ford(M2))   # → [0, 2, 4, 3, 4]
```

### 🎯 Vérification manuelle pour `M` (graphe `g`)

| Sommet | Distance | Chemin |
|--------|----------|--------|
| 0 (=1) | 0 | Départ |
| 1 (=2) | 7 | 1 → 3 → 2 (coût 2+5=7, mieux que 1→2 direct qui coûte 8) |
| 2 (=3) | 2 | 1 → 3 (coût 2) |
| 3 (=4) | 8 | 1 → 3 → 2 → 4 (coût 2+5+1=8) |
| 4 (=5) | 3 | 1 → 3 → 5 (coût 2+1=3) |

---

## Exercice 2 : Dijkstra (simplifié)

### 🧠 L'idée en français

Dijkstra est **plus malin** que Bellman-Ford. Au lieu de regarder tous les arcs à chaque fois, il :
1. Choisit le sommet **le plus proche** qu'on n'a pas encore traité
2. Le **marque** comme "terminé"
3. Met à jour les distances des voisins non marqués
4. Recommence jusqu'à ce que tous les sommets soient marqués

C'est comme explorer une carte : tu vas d'abord au village le plus proche, puis au suivant, etc.

### 📝 Le pseudo-code (traduit)

```
Fonction dijkstra(M) :
    n = nombre de sommets

    Dist = [Infinity, ..., Infinity]
    Dist[0] = 0
    marquage = [0, 0, 0, ..., 0]    # 0 = pas marqué, 1 = marqué

    TANT QUE il reste des sommets non marqués :
        i = le sommet non marqué avec la plus petite distance
        marquer i  (marquage[i] = 1)

        POUR chaque sommet j non marqué :
            SI Dist[i] + M[i][j] < Dist[j] :
                Dist[j] = Dist[i] + M[i][j]

    RETOURNER Dist
```

### 🔍 Explication ligne par ligne

```python
def dijkstra(M):
    n = M.nrows()
    Dist = [Infinity] * n
    Dist[0] = 0
    marquage = [0] * n
```
> Même début que Bellman-Ford, **plus** une liste `marquage` : chaque case vaut `0` (pas marqué) ou `1` (marqué/traité). Au début, **personne** n'est marqué.

---

```python
    while 0 in marquage:
```
> **Tant qu'il y a un `0`** dans la liste de marquage = tant qu'il reste des sommets pas encore traités.

---

```python
        mini = Infinity
        i = -1
        for k in range(n):
            if marquage[k] == 0 and Dist[k] < mini:
                mini = Dist[k]
                i = k
```
> **On cherche le sommet non marqué le plus proche.** On parcourt tous les sommets `k`. Si `k` n'est pas marqué ET que sa distance est la plus petite qu'on a vue, on le retient. À la fin, `i` contient le **numéro du sommet non marqué le plus proche**.

---

```python
        if i == -1:
            break
```
> **Sécurité** : si `i` est resté à `-1`, ça veut dire qu'on n'a trouvé aucun sommet accessible (tous les non-marqués sont à distance infinie). On arrête.

---

```python
        marquage[i] = 1
```
> On **marque** le sommet `i` : il est maintenant "traité", on ne le touchera plus.

---

```python
        for j in range(n):
            if marquage[j] == 0:
                poids = M[i][j]
                if poids == 0 and i != j:
                    poids = Infinity
                if Dist[i] + poids < Dist[j]:
                    Dist[j] = Dist[i] + poids
```
> Pour chaque sommet `j` **non marqué**, on vérifie si passer par `i` raccourcit le chemin. C'est exactement la même logique que Bellman-Ford, sauf qu'on ne regarde que les sommets pas encore traités.

---

```python
    return Dist
```

### ✅ Code complet de Dijkstra

```python
def dijkstra(M):
    n = M.nrows()                     # nombre de sommets
    Dist = [Infinity] * n             # tout à l'infini
    Dist[0] = 0                       # le départ à distance 0
    marquage = [0] * n                # personne n'est marqué

    while 0 in marquage:              # tant qu'il reste des non-marqués
        # Chercher le sommet non marqué le plus proche
        mini = Infinity
        i = -1
        for k in range(n):
            if marquage[k] == 0 and Dist[k] < mini:
                mini = Dist[k]
                i = k

        if i == -1:                   # sécurité : plus rien d'accessible
            break

        marquage[i] = 1               # on marque ce sommet

        for j in range(n):            # pour chaque voisin non marqué
            if marquage[j] == 0:
                poids = M[i][j]
                if poids == 0 and i != j:
                    poids = Infinity  # 0 = pas d'arc = infini
                if Dist[i] + poids < Dist[j]:
                    Dist[j] = Dist[i] + poids
    return Dist
```

### 🧪 Tests attendus

```python
print(dijkstra(M))    # → [0, 7, 2, 8, 3]
print(dijkstra(M2))   # → [0, 2, 4, 3, 4]
```

> [!NOTE]
> Les résultats sont les **mêmes** que Bellman-Ford ! C'est normal : les deux algorithmes trouvent les mêmes plus courts chemins, mais Dijkstra est plus rapide.

---

## 🌟 Bonus : Dijkstra avec affichage du chemin

Pour afficher le chemin, on ajoute une liste `predecesseur` qui retient **par quel sommet on est passé** pour arriver à chaque sommet.

```python
def dijkstra_chemin(M):
    n = M.nrows()
    Dist = [Infinity] * n
    Dist[0] = 0
    marquage = [0] * n
    predecesseur = [-1] * n           # -1 = pas de prédécesseur

    while 0 in marquage:
        mini = Infinity
        i = -1
        for k in range(n):
            if marquage[k] == 0 and Dist[k] < mini:
                mini = Dist[k]
                i = k

        if i == -1:
            break

        marquage[i] = 1

        for j in range(n):
            if marquage[j] == 0:
                poids = M[i][j]
                if poids == 0 and i != j:
                    poids = Infinity
                if Dist[i] + poids < Dist[j]:
                    Dist[j] = Dist[i] + poids
                    predecesseur[j] = i       # on retient d'où on vient

    # Afficher les chemins
    for sommet in range(n):
        chemin = []
        s = sommet
        while s != -1:
            chemin = [s] + chemin     # on ajoute au début
            s = predecesseur[s]
        print("Sommet", sommet, ": distance =", Dist[sommet], ", chemin =", chemin)

    return Dist
```

### Test

```python
dijkstra_chemin(M)
```

Résultat attendu :
```
Sommet 0 : distance = 0 , chemin = [0]
Sommet 1 : distance = 7 , chemin = [0, 2, 1]
Sommet 2 : distance = 2 , chemin = [0, 2]
Sommet 3 : distance = 8 , chemin = [0, 2, 1, 3]
Sommet 4 : distance = 3 , chemin = [0, 2, 4]
```

---

## 📊 Comparaison Bellman-Ford vs Dijkstra

| | Bellman-Ford | Dijkstra |
|---|---|---|
| **Principe** | Regarde TOUS les arcs, répète | Choisit le plus proche, marque |
| **Vitesse** | Plus lent (O(n³)) | Plus rapide (O(n²)) |
| **Poids négatifs** | ✅ Gère les poids négatifs | ❌ Ne marche PAS avec poids négatifs |
| **Quand l'utiliser** | Quand il y a des poids négatifs | Sinon (cas le plus courant) |
