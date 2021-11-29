Ce projet contient plusieurs scripts d'analyse de lisibilité de texte (et permet d'en développer de nouveaux).
Pour ce faire, il utilise le logiciel Trombrone, un outil logiciel qui permet de d'analyser des textes.
Notez que Trombone est utilisé par une autre application plus conviviale d'utilisation,
Voyant-Tools (https://voyant-tools.org/).
Voyant-Tools possède cependant quelques limitations, l'application ne peut pas par exemple traiter de larges corpus.
Certains outils au sein de Trombone ne sont également pas accessibles à partir de Voyant-tools,
notamment les mesures de lisibilité. 
Ce projet a donc été développé afin de traiter de larges corpus et 
permettre l'utilisation de tous les outils dont Trombone dispose.


# Utilisation
L'application s'exécute à partir d'un terminal et d'une machine Linux/Unix.
Dans cet exemple, les serveurs de Calcul Canada sont utilisés,
il est néanmoins possible d'utiliser une autre machine/serveur.

### Connexion aux serveurs de Calcul Canada
Dans cet exemple, nous nous connectons au serveur Beluga de Calcul Canada par _ssh_.
Pour ce faire, il est nécessaire d'avoir accès à un terminal et d'avoir l'application ssh d'installée.
Cette étape dépend du système d'exploitation de votre ordinateur.
Il existe plusieurs ressources sur internet selon votre situation.

Du terminal, il est possible de se connecter avec la commande suivante :
```
ssh <votre-nom-d'utilisateur>@beluga.calculcanada.ca
```

### Cloner le répertoire Github
Cloner le répertoire Github https://github.com/ulaval-rs/andreanne-tremblay-simard
afin d'avoir les fichiers et scripts nécessaires aux analyses :
```
git clone https://github.com/ulaval-rs/andreanne-tremblay-simard.git
```
Entrez par la suite dans le dossier du projet :
```
cd andreanne-tremblay-simard
```

## Analyses
Maintenant les scripts récupérés, il est possible de lancer des analyses.
Notons que les scripts ne couvrent pas toutes les analyses possibles avec Trombone.
En effet, il est possible d'utiliser toutes les fonctionnalités de Trombone à partir
de scripts Python grâce à la librairie Python https://pypi.org/project/pytrombone/. Ici, on ne calcul que les indices de lisibilité
et la fréquence des termes.

### Calcul des indices/mesures
`scripts/calculate_indices_batch.py` est un script qui calcul les indices de lisibilité pour de grande quantité de PDF.
Il effectue un calcul en lot (par batch) et conserve une mémoire des PDF qui ont déjà
été analysés (ils stockés dans ce qu'on appelle la cache ici.).
Ainsi, même si la première exécution du script s'interrompt avant la fin, il est possible de le réexécuter sans avoir à
recommencer à zéro.

Les indices/mesure de lisibilité calculés par ce script sont les suivants :

- Mesure de Dale Chall (utilise par défaut la liste de mots simples suivante : https://github.com/voyanttools/trombone/blob/master/src/main/resources/org/voyanttools/trombone/readability/easywords.en.txt)
- Indice de Coleman Liau
- Indice SMOG
- Indice de LIX
- Indice de lisibilité automatique (Automated Readability Index)
- Indice FOG

Pour l'exécuter, il est nécessaire de lui fournir les paramètres suivants:
```shell
python ./scripts/calculate_indices_batch.py --pdf_path_pattern=./path/to/pdfs/*.pdf --csv_file=./path/to/results-indices.csv --cache_path=./path/to/cache-indices.db
```

Ici, `pdf_path_pattern` correspond au patron pour récupérer les PDF.
Par exemple, si l'objectif est de calculer tous les fichiers pdfs PDF qui finissent avec `_F.pdf`,
le paramètre devrait être : `--pdf_path_pattern=./path/pdfs/*_F.pdf`.
`csv_file` correspond au fichier où les résultats seront stockés.
Finalement, `cache_path` correspond à la "cache", c'est à dire l'endroit où la
mémoire de si un document a déjà été traité ou non se trouve.

#### Exécuter le script sur les serveurs de Calcul Canada via une tâche
Pour soumettre un calcul sur les serveurs de Calcul Canada via l'ordonnanceur de tâches,
il est nécessaire de faire un script bash et de le lancer avec la commande `sbatch`.
(voir https://docs.computecanada.ca/wiki/Running_jobs/fr pour plus d'information).

Il faut d'abord faire un script bash.
Pour ce faire, vous pouvez utiliser votre éditeur préféré, un exemple est _nano_.
Vous pouvez ainsi créer le script bash de cette façon : 
```shell
nano job_indices.sh
```
Et y copier-coller le contenu suivant :
```shell
#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --account=<nom-compte>
#SBATCH --mem=8G
#SBATCH --job-name=calcul-indices
#SBATCH --output=./data/output/%x-%j.out
#SBATCH --mail-user=<idul>@ulaval.ca
#SBATCH --mail-type=ALL

module load java
module load python/3.9
module load scipy-stack

python ./scripts/calculate_indices_batch.py --pdf_path_pattern=./data/pdfs/*_F.pdf --csv_file=./data/results-indices_F.csv --cache_path=./data/cache-indices_F.db
```
Vous pouvez finalement lancer cette tâche avec la commande :
```shell
sbatch job_indices.sh
```
Il est possible de consulter le statut de vos tâches avec la commande
```shell
sq
```

### Calcul de la fréquence des termes
Cette section est à propos des scripts Python `scripts/find_terms_frequency.py`
et `scripts/regroup_terms_results.py`.
`scripts/find_terms_frequency.py` permet d'abord d'obtenir tous les termes
de chaque document un à un.
Ces résultats sont tous rassemblés dans un seul fichier csv (qui peut devenir très volumineux!).
Le script `scripts/regroup_terms_results.py` permet quant à lui de regrouper les résultats des termes
obtenus par document afin d'obtenir des statistiques pour le corpus en entier.

Prenons par exemple de plusieurs documents PDF.
`scripts/find_terms_frequency.py` nous permet d'obtenir la fréquence de chacun des termes dans chacun des documents.
Ces résultats sont tous rassemblés dans le même fichier csv.
`scripts/regroup_terms_results.py` nous permet ensuite d'avoir ces statistique pour le corpus entier.
Par exemple, en moyenne dans tous les documents, à quel fréquence tel terme se retrouve.

L'exécution est très similaire à celle du script du calcul des indices de lisibilité.
Il suffit de lancer le script Python avec les paramètres suivants : 
```shell
python ./scripts/find_terms_frequency.py --pdf_path_pattern=./path/to/pdfs/*.pdf --csv_file=./path/to/results-terms.csv --cache_path=./path/to/cache-terms.db
```

Dans ce cas-ci, les résultats se trouve dans `./path/to/results-terms.csv`. 
__Pour lancer ce script sur un large volume de documents sur les serveurs de Calcul Canada,
référez-vous à la section "Exécuter le script sur les serveurs de Calcul Canada via une tâche"__

Il est ensuite possible de regrouper ces résultats afin d'obtenir des statistiques sur le corpus entier
avec le script `scripts/regroup_terms_results.py`. Il s'agit simplement d'exécuter cette commande avec ces paramètres :
```shell
python ./scripts/regroup_terms_results.py  --csv_file=./path/to/results-corpus-terms.csv --all_terms_filepath=./path/to/results-terms.csv
```
Les résultats se trouvent dans le fichier `./path/to/results-corpus-terms.csv`.
Le paramètre `all_terms_results` réfère au fichier résultant de la commande précédente.
__Pour lancer ce script sur un large volume de documents sur les serveurs de Calcul Canada,
référez-vous à la section "Exécuter le script sur les serveurs de Calcul Canada via une tâche"__

