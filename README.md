# EntreÉlève : Introduction aux étoiles

Projet de médiation scientifique destiné à faire découvrir à des élèves de CM1/CM2 les différents types d'étoiles et leur évolution, réalisé dans le cadre du projet EntreÉlève / CS Students.

Ce dépôt contient :

- une simulation informatique simplifiée de l'évolution stellaire (`simulation.py`) ;
- le site web de documentation du projet, généré avec MkDocs ;
- les supports pédagogiques utilisés pendant la séance.

Site publié : _lien à ajouter_

## Sommaire

- [Présentation de la séance](#présentation-de-la-séance)
- [Simulation](#simulation)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Organisation du dépôt](#organisation-du-dépôt)
- [Technologies](#technologies)
- [Ressources pédagogiques](#ressources-pédagogiques)
- [Crédits](#crédits)
- [Licence](#licence)

## Présentation de la séance

La séance, d'une durée totale d'environ 2 heures, aborde la formation des étoiles à partir de nuages de gaz, les différents types d'étoiles, leur évolution en fonction de leur masse, ainsi que les naines blanches, les géantes rouges, les étoiles à neutrons et les trous noirs.

| Activité | Durée approximative |
|---|---:|
| Présentation avec diapositives | 45 min |
| Activité avec la simulation informatique | 35 min |
| Réalisation de la fresque | 30 min |
| Trace écrite | 10 min |

Le déroulé détaillé, le matériel nécessaire et les contraintes sont décrits sur le site web du projet.

## Simulation

La simulation modélise l'évolution d'une répartition de gaz dans un univers bidimensionnel. La distribution de masse est représentée par un tableau NumPy, et son évolution repose sur :

- la diffusion, modélisée à partir de la deuxième loi de Fick ;
- la gravité ;
- une approximation de la vitesse locale des particules à partir du champ gravitationnel ;
- un seuil de densité déterminant la formation d'une étoile.

Une fois formée, l'évolution d'une étoile dépend de son type.

**Remarque :** il s'agit d'un modèle simplifié destiné à la médiation scientifique et à l'illustration des phénomènes étudiés. Il ne constitue pas une simulation astrophysique complète.

## Installation

Le projet nécessite Python 3.

```bash
# Récupérer le dépôt
git clone <url-du-depot>
cd <nom-du-depot>

# Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Installer les dépendances
python -m pip install -r requirements.txt
```

## Utilisation

### Lancer la simulation

```bash
python simulation.py
```

### Lancer le site en local

```bash
python -m mkdocs serve
```

Le site est accessible à l'adresse indiquée par MkDocs (généralement `http://127.0.0.1:8000/`) et se met à jour automatiquement à chaque modification des fichiers Markdown.

### Construire le site statique

```bash
python -m mkdocs build
```

Les fichiers générés sont placés dans le dossier `site/`.

## Organisation du dépôt

```text
.
├── mkdocs.yml            # Configuration du site
├── requirements.txt      # Dépendances Python
├── simulation.py         # Simulation de l'évolution stellaire
├── docs/
│   ├── index.md
│   ├── plan.md
│   ├── simulation.md
│   ├── galerie_photo.md
│   ├── assets/           # Images et ressources
│   └── stylesheets/
│       └── extra.css
└── README.md
```

## Technologies

- [NumPy](https://numpy.org/) : calcul numérique
- [Matplotlib](https://matplotlib.org/) : affichage et animation de la simulation
- [MkDocs](https://www.mkdocs.org/) et [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) : génération et thème du site
- [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/) : extensions Markdown (équations)

## Ressources pédagogiques

Les supports utilisés pendant la séance sont fournis dans le projet : présentation PowerPoint, fresque initiale et complétée, cartes pour la fresque, texte à trous destiné aux élèves, captures d'écran de la simulation et illustrations. Les sources et crédits des images sont indiqués dans la documentation du site, et les références scientifiques dans la section « Bibliographie commentée ».

## Crédits

**Auteurs :** Raphaël CADIER--GIARD, Enzo CHEN

**Encadrement :** Paul FRAUX (professeur encadrant), Victor RENAUX (professeur des écoles)

## Licence

Projet réalisé dans le cadre du projet EntreÉlève / CS Students. Les droits et conditions d'utilisation des images et ressources externes restent ceux de leurs auteurs et organismes respectifs.