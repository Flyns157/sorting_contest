import time
import random
import importlib
import sys
import pandas as pd

# Importer les algorithmes de tri du module sort_pack
sys.path.insert(0, 'sort_pack')
sort_pack = importlib.import_module('sort_pack')

# Générer une liste aléatoire
def generate_random_list(size):
    return [random.randint(1, 100) for _ in range(size)]

# Vérifier si une liste est triée
def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))
import types
# Initialiser le DataFrame pour stocker les scores
scores = pd.DataFrame(columns=['Algorithme', 'Temps d\'exécution'])

# Tester un algorithme de tri
def test_sorting_algorithm(algorithm, lst):
    if isinstance(algorithm, types.FunctionType):  # Vérifier que l'attribut est une fonction
        start_time = time.time()
        sorted_lst = algorithm(lst)
        end_time = time.time()
        execution_time = end_time - start_time
        if is_sorted(sorted_lst):
            return execution_time
    return None  # L'attribut n'est pas une fonction ou l'algorithme est disqualifié

# Le concours
def contest():
    # Générer la liste à trier
    lst = generate_random_list(1000)

    # Tester chaque algorithme de tri
    for algorithm in dir(sort_pack):
        if algorithm.startswith('__'):
            continue
        execution_time = test_sorting_algorithm(getattr(sort_pack, algorithm), lst)
        if execution_time is not None:
            # Ajouter le score à la DataFrame
            scores.loc[len(scores)] = [algorithm, execution_time]
        else:
            print(f"L'algorithme {algorithm} est disqualifié ou n'est pas une fonction.")

    # Trier la DataFrame par temps d'exécution et attribuer les rangs
    scores.sort_values(by='Temps d\'exécution', inplace=True)
    scores['Rang'] = scores['Temps d\'exécution'].rank(method='min')
    print(scores)

# Lancer le concours
contest()