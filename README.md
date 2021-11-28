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
`script/calculate_indices_batch.py`

### Calcul de la fréquence des termes
`script/calculate_indices_batch.py`
