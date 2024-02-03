import os
import ast
import time
import string
import inspect
import importlib
import pandas as pd
from datetime import datetime
from types import FunctionType
from random import random,uniform,choice

def clear_terminal():
    if os.name == 'nt':  # Pour Windows
        os.system('cls')
    else:  # Pour Unix (Linux, macOS)
        os.system('clear')

DANGEROUS_MODULES = ['os', 'subprocess', 'shutil']
DANGEROUS_FUNCTIONS = ['exec', 'eval', 'open']

def is_function_safe(function):
    source_code =  inspect.getsource(function)
    module = ast.parse(source_code)

    for node in ast.walk(module):
        # Vérifier l'utilisation de modules dangereux
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in DANGEROUS_MODULES:
                    return False
        # Vérifier l'utilisation de fonctions dangereuses
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in DANGEROUS_FUNCTIONS:
                return False

    return True

def randint(mini:int,maxi:int)->int:return int(mini + random() * (maxi - mini))

# Initialiser le DataFrame pour stocker les scores
scores = pd.DataFrame(columns=['Algorithme', 'Temps d\'exécution', 'Statut', 'Épreuve'])

# Importer les algorithmes de tri du module sort_pack
# sys.path.insert(0, 'sort_pack')
sort_pack = importlib.import_module('sort_pack')

# Générer une liste aléatoire
def generate_random_list(size:int,type:str='int',sorted:bool=False,reverse:bool=False,duplicates:bool=False)->list[int|float|str]:
    if type == 'int':
        lst = [randint(1, 100) for _ in range(size)]
    elif type == 'float':
        lst = [uniform(1, 100) for _ in range(size)]
    elif type == 'str':
        lst = [choice(string.ascii_letters) for _ in range(size)]
    else :
        lst = []

    if sorted:
        lst.sort()
    if reverse:
        lst.reverse()
    if duplicates:
        lst = lst + lst

    return lst

# Vérifier si une liste est triée
def is_sorted(lst:list)->bool:
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

# Tester un algorithme de tri
def test_sorting_algorithm(algorithm:FunctionType,lst:list)->tuple[None|float,str]:
    if isinstance(algorithm, FunctionType) and is_function_safe(algorithm):  # Vérifier que l'attribut est une fonction
        start_time = time.time()
        sorted_lst = algorithm(lst)
        end_time = time.time()
        execution_time = end_time - start_time
        if is_sorted(sorted_lst):
            return execution_time, 'Qualifié'
    return None, 'Disqualifié'  # L'attribut n'est pas une fonction ou l'algorithme est disqualifié
# Le concours
def contest(scale:int=3)->pd.DataFrame:
    clear_terminal()
    print(f'-------------  contest results the {datetime.now().strftime("[%d-%m-%Y] at [%H-%M-%S]")}  -------------')
    # Définir les épreuves
    challenges = [
        {'name': f'Tri de liste d\'entiers de taille {10**scale}', 'size': 10**scale, 'type': 'int'},
        {'name': f'Tri de liste d\'entiers de taille {5*10**scale}', 'size': 5*10**scale, 'type': 'int'},
        {'name': f'Tri de liste d\'entiers de taille {10**(scale+1)}', 'size': 10**(scale+1), 'type': 'int'},
        {'name': f'Tri de liste de flottants de taille {10**scale}', 'size': 10**scale, 'type': 'float'},
        {'name': f'Tri de liste de chaînes de caractères de taille {10**scale}', 'size': 10**scale, 'type': 'str'},
        {'name': f'Tri de liste d\'entiers presque triée de taille {10**scale}', 'size': 10**scale, 'type': 'int', 'sorted': True},
        {'name': f'Tri de liste d\'entiers en ordre inverse de taille {10**scale}', 'size': 10**scale, 'type': 'int', 'reverse': True},
        {'name': f'Tri de liste d\'entiers avec beaucoup de doublons de taille {10**scale}', 'size': 10**scale, 'type': 'int', 'duplicates': True},
    ]

    # Tester chaque algorithme de tri pour chaque épreuve
    keys_to_exclude = ['name']
    for challenge in challenges:
        lst = generate_random_list(**{k: v for k, v in challenge.items() if k not in keys_to_exclude})
        for algorithm in dir(sort_pack):
            if algorithm.startswith('__'):
                continue
            execution_time, status = test_sorting_algorithm(getattr(sort_pack, algorithm), lst)
            # Ajouter le score et le statut à la DataFrame
            scores.loc[len(scores)] = [algorithm, execution_time, status, challenge['name']]

        # Trier la DataFrame par temps d'exécution et attribuer les rangs pour l'épreuve actuelle
        current_challenge_scores = scores[scores['Épreuve'] == challenge['name']]
        current_challenge_scores.sort_values(by='Temps d\'exécution', inplace=True, na_position='last')
        current_challenge_scores['Rang'] = current_challenge_scores['Temps d\'exécution'].rank(method='min')

        # Supprimer la colonne 'Épreuve'
        current_challenge_scores = current_challenge_scores.drop(columns=['Épreuve'])

        print(f"Tableau des scores pour l'épreuve de {challenge['name']} :")
        print(current_challenge_scores)

    # Calculer le temps d'exécution moyen pour chaque algorithme
    average_scores = scores.groupby('Algorithme')['Temps d\'exécution'].mean()

    # Créer le tableau de score final
    final_scores = pd.DataFrame(average_scores).reset_index()
    final_scores.columns = ['Algorithme', 'Temps d\'exécution moyen']
    final_scores.sort_values(by='Temps d\'exécution moyen', inplace=True)
    final_scores['Rang final'] = final_scores['Temps d\'exécution moyen'].rank(method='min')

    print("\n\nTableau de score final (classement définitif du concours) :")
    print(final_scores)
    return final_scores

# Lancer le concours
contest()

# Enregistrez le DataFrame dans un fichier CSV
scores.to_csv(f'results/contest_results{datetime.now().strftime("[%d-%m-%Y][%H-%M-%S]")}.csv', index=False)
