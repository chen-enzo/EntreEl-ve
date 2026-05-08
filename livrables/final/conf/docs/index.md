




#### **Objectifs généraux** 

-  Éveiller l’intérêt et la curiosité des élèves pour les sciences. 
- Faire prendre conscience aux élèves de l’immensité de l’univers. 


#### **Objectifs spécifiques** 
À l’issue de la séance, les élèves doivent être capables de :

- Comprendre ce qu’est une étoile et que le Soleil en est une. 
- Connaître les grandes étapes de la vie d’une étoile. 
- Reconnaître certains objets célestes liés à la vie des étoiles. 


---
## **Matériel**


**Frise / Carte mentale:** 

- Une grande feuille CANSON en tant que support ∼ 2-5€ 
- 11 de cartes pour compléter la fresque 
- Plastifieuse ∼ 20-30€ 
- Pochette de plastification s ∼ 15€ 
- Carte (papier) 
- Scotch double face 

> Total : 50€ 


---
## **Déroulement de la séance**
### **Situation** 

Cette intervention est une séance de médiation scientifique ayant pour ambition de faire découvrir à une classe de CM2 les différents types étoiles et leur évolution. Pour ce faire elle aborde la formation des étoiles à partir de nuages de gaz, l'évolution de ces nuages en naine rouge, naine jaune ou géante bleu puis la trajectoire de ces différentes étoiles qui évoluent en des naines blanches, des géantes rouges, des étoiles à neutrons et des trous noirs. L'objectif recherché est d'émerveiller les élèves en leur faisant prendre conscience que l'univers contient de nombreux corps célestes fondamentalement différent des objets avec lesquels nous interagissons sur Terre. 
Concrètement, la séance d'une totale de deux heures comprendra une présentation d'environ 45 minutes avec des slides projetées au tableau, une activité sur ordinateur d'environ 30 minutes durant laquelle les élèves interagiront avec une simulation de la vie des étoiles, une activité d'environ 30 minutes durant laquelle la classe devra compléter une fresque synthétisant les rapports entre les différents types d'étoiles vus précédemment puis d'une trace écrite consistant en la complétion d'un texte à trou.
L'animation fonctionne bien avec une vingtaine d'élèves.

### **Conditions matérielles requise** 

Une salle de classe comprenant assez de tables et de chaise pour que chaque élève ait une place.
Au minimum un ordinateur par paire d'élèves. Avoir un ordinateur par élève est préférable. Sur chacun de ces ordinateurs doit être installé le programme python effectuant la simulation.
Un vidéo-projecteur connecté à ordinateur distinct de ceux utilisé par les élèves lors de la simulation.
De quoi faire tenir la fresque sur le tableau (ou un mur s'il n'y a pas de tableau), par exemple des aimants.

### **Plan de la Séance** 
Introduction (5 minutes)
— Installation des élèves.
— Présentation succinte des intervenants et de la séance.

6.2 Du quotidien à l’espace (15 minutes)
— Dézoom progressif (diapositives projettées) : de l’école à la Terre, puis au système solaire
puis zoom sur le Soleil.(1 minute)
— // Questionnement : Qu’est-ce que le Soleil ? Pourquoi semble-t-il plus gros et lumineux
que es autres étoiles ? ( 1 minute)
— // Réponse : Parce que les autres étoiles sont beaucoup plus loin de la Terre que ne l’est
le Soleil. Conséquence : l’univers est immense . (2 minutes)
— Explication succinte de ce qu’est une étoile : une étoile est une énorme boule de gaz/feu
très chaude qui produit de la lumière. (3 minutes)
- Notion de gaz
— Comparaisons de tailles et de durées de vie avec des grandeurs familières aux élèves. (5
minutes)
6.3 La vie des étoiles (30 minutes)
— Formation à partir de nuages de gaz qui s’effondrent sur eux-mêmes. (5 minutes)
— Équilibre entre l’effondrement et la pression interne. (5 minutes)
- Notion de gravité
- Notion de pression
2
— Reprise de l’effondrement lorsqu’il n’y a plus assez d’hydrogène à consommer. Puis différents devenirs possibles selon la masse de l’étoile : naine blanche, géante rouge, supernova,
étoile à neutrons et trou noir. (15 minutes)
— // Observation d’images et dézoom/zoom pour situer ces objets dans l’espace. (5 minutes)

6.4 Expérience : Simulation informatique (30 minutes)
    La simulation est divisée en deux partie. Dans un premier temps, les élèves observeront la formution puis l'évolution d'étoiles au sein d'une répartition initiale de masse. Puis dans un second temps, il rajouteront eux même des nuages de gas durant la simulation afin de créer les différents types d'étoiles vus pendant la présentation.
    6.4.1 Organisation :
    — Les élèves seront seuls ou en binome devant un ordinateur sur lequel la simulation est ouverte.
    — Les intervenants circuleront tout au long l’activité afin de veiller à son bon déroulement.
    6.4.2 Déroulement de l’activité :
        -Présentation de la simulation projetée au tableau et explication des consignes (voir slides). (3min)
        -Première partie : observation (10 min)
        -Consignes de la deuxième partie (voir slides). (2min)
        -Deuxième partie formation manuelle des étoiles (15 minutes)


 
6.5 Activité 2 : Fresque (30 minutes)
Une fresque sur laquelle sont inscrits des rectangles et des flèches reliant ces rectangles est présentée à la classe. Les intervenants présentent aux élèves des cartes correspondant aux différents objets célestes vus précédemment. Ces derniers doivent placer ces cartes dans le bon rectangle. Concrètement les élèves restent à leur place à lèvent la main quand ils ont une idée. Quand ils interrogent un élève, les intervenants l'écouteront puis lui demanderont d'expliquer les raisons de sa proposition.
Déroulement : 
— Rangement des ordinateurs et explication des consignes (5 min).
— Placement de cartes représentant des objets célestes sur une fresque suspendue au tableau (25 min).

6.6 Trace écrite (5 minutes)
— Distribution de la trace écrite (1 min).
— Collage de la trace écrite dans le cahier de science (4 min).



#### **Choix de Conception** 

Le programme python simule l'évolution d'une masse de gaz initiale dans un univers fini en deux dimension.
La distribution de masse est donc représentée par un `array numpy` dont les cases correspondent à des densité de masse.
L'évolution de la répartition de masse se fait suivant selon un modèle simplifié de mécanique des fluides prenant en compte la diffusion et la gravité. La diffusion est calculée selon la deuxième loi de Fick. Pour calculer l'effet de la gravité, nous utilisons l'équation de continuité de la mécanique des fluides dans laquelle nous approximons la vitesse locale des particules par une valeur proportionnelle au champ gravitationnel.  
Lorsque que la densité dépasse un certain seuil dans une certain ensemble connexe de points, une étoile est formée. 
La matière à l'intérieur d'une étoile n'évolue plus suivant les équations décrite précédemment mais évolue d'une manière entièrement déterminée par le type de l'étoile. Ainsi, les étoiles n'ont pas de vitesse, elles sont fixes.

### **Extensions **

En fonction du déroulement de la séance il est possible de la compléter par une explication des phénomènes contre-intuitif se déroulant au voisinage des trou noirs, une présentation des études scientifiques ou  une introduction à la méthode scientifique, permettant ainsi de comprendre par quel processus les modèles présentés lors de la séance ont été établis. 




---
## **Ressources** 

### **Nos Supports et Documents**


- [Simulation python](assets/ressource/simulation_final_version.py)
- [Présentation / diapositives](assets/ressource/presentation_entreeleve.pptx)
- [Frise / Carte Mentale initiale]()
- [Cartes pour la frise](assets/ressource/cartes_frises.pdf)
- [Texte à trous](assets/ressource/texte-a-trou.pdf)

### **Images utilisées** 

- [Image Soleil](assets/image/sun.png) : image du Soleil générée par IA 
- ? [Coupe du Soleil](assets/image/slice_sun.png) : Vue en coupe du Soleil, réalisé par C.P Rigel ([lien](https://www.orionpx.fr/project/blog/les-etoiles-qui-sont-elles/coupe-du-soleil/))
- [Pilier de la création](assets/image/pillar_of_creation.jpeg) : Prise par le télescope Hubble (*NASA*, *ESA*)
- [Nébuleuse d'Orion](assets/image/Orion_Nebula.jpg) : Vue par le télescope spatial Hubble (*NASA*, *STScI*, *ESA*)
- [Naine Brune](assets/image/browndwarf.jpg) : Vue d'artiste inspirée d'image prise par Hubble (*Centre spatial Goddard*, *NASA*)
- [Naine rouge](assets/image/reddwarf.png) : image générée par IA
- [Naine blanche](assets/image/whitedwarf.jpg) : CC BY-NC-SA Eric Simon
- [Naine blanche dézoomée](assets/image/whitedwarf_unzoomed.png) : Image dézoomée par IA 
- ? [Géante rouge](assets/image/redgiant.png) : réalisé par C.P Rigel ([lien](https://www.orionpx.fr/project/blog/les-etoiles-qui-sont-elles/geante-rouge/))
- [Nébuleuse planétaire](assets/image/planetary_nebula.jpg) : La nébuleuse de l'Hélice (*NGC 7293) (NASA, NOAO, ESA, the Hubble Helix Nebula Team, M. Meixner (STScI), and T.A. Rector (NRAO)*)
- [Géante bleu](assets/image/bluegiant.png) : image générée par IA
- [Comparaison des Géantes bleus](assets/image/blue_star_comparaison.jpg) : ESO/M. Kornmesser ([http://www.eso.org/public/images/eso1030c/](http://www.eso.org/public/images/eso1030c/))
- [Supernova](assets/image/supernova.jpeg) : Vue d'artiste de la supernova SN2016aps (*© M. Weiss, Center for Astrophysics Harvard & Smithsonian*)
- [Etoile à neutrons](assets/image/neutronstar.jpg) : Image de l'*ESA*
- [Trou noir](assets/image/black_hole_NASA.jpg) : Image composite du disque d'accrétion du trou noir M87* (*Event Horizon Telescope*) 
- [Trou noir Interstellar](assets/image/black_hole_interstellar.jpg) : Image issue du film *Interstellar* réalisé par Christopher Nolan
- [Proto-étoile](assets/image/Protostar.jpeg) : Image de [L1527 IRS](https://fr.wikipedia.org/wiki/L1527_IRS "L1527 IRS"), prise par le télescope spatial James-Webb  en 2022 (*NASA, ESA, CSA, and STScI, J. DePasquale*)



---
## **Crédits**
### **Contributions** 
- **Auteurs** : Raphaël CADIER--GIARD, Enzo CHEN 
- **Professeur Encadrant** : Paul FRAUX 
- **Professeur des Ecoles** : Victor RENAUX 


---
## **Bibliographie**

