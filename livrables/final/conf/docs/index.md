

## **Description** 

Cette intervention a pour objectif de faire découvrir aux élèves de CM2 les étoiles, leur nature et leur évolution, à travers une approche visuelle et interactive. La séance s’inscrit dans une démarche de médiation scientifique adaptée à un jeune public, et ne suppose aucune connaissance préalable en physique ou en astronomie. L’intervention privilégie l’émerveillement, la curiosité et la manipulation, tout en transmet- tant des notions scientifiques rigoureuses sous une forme accessible.

### **Besoins** 
- Augmenter l’intérêt des plus jeunes pour les filières scientifiques, en particulier chez les filles. 
- Lutter contre les stéréotypes. 
- Rendre accessible des notions scientifiques abstraites.


### **Objectifs pédagogiques** 

#### **Objectifs généraux** 

-  Éveiller l’intérêt et la curiosité des élèves pour les sciences. 
-  Faire rêver les élèves. 
- Faire prendre conscience aux élèves de l’immensité de l’univers. 


#### **Objectifs spécifiques** 
À l’issue de la séance, les élèves doivent être capables de :

- Comprendre ce qu’est une étoile et que le Soleil en est une. 
- Connaître les grandes étapes de la vie d’une étoile. 
- Reconnaître certains objets célestes liés à la vie des étoiles. 


### **Contraintes de l’intervention** 
- Public : Faire un cours adapté à des élèves de CM1/CM2. 
- Tenir compte du niveau socio-économique de l’école. 
- Durée totale : 2 heures. 
- Ne pas faire un cours magistrale pendant 2 heures mais proposer des activités ou expériences aux élèves. 
- L’ensemble de la séance, dont les supports utilisés lors des expériences, doit être reproductible à partir des ressources du projet. 
- Fournir aux élèves une trace écrite synthétique. 
- Respecter le budget alloué.


---
## **Matériel**
Une partie du matériel décrit ci-dessous nous a été fourni par CentraleSupélec.

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

Cette intervention a pour ambition de faire découvrir à une classe de CM2 les différents types étoiles et leur évolution. Pour ce faire elle aborde la formation des étoiles à partir de nuages de gaz, l'évolution de ces nuages en naine rouge, naine jaune ou géante bleu puis la trajectoire de ces différentes étoiles qui évoluent en des naines blanches, des géantes rouges, des étoiles à neutrons et des trous noirs. L'objectif recherché est d'émerveiller les élèves en leur faisant prendre conscience que l'univers contient de nombreux corps célestes fondamentalement différent des objets avec lesquels nous interagissons sur Terre. 
Concrètement, la séance d'une totale de deux heures comprendra une présentation d'environ 45 minutes avec des slides projetées au tableau, une activité sur ordinateur d'environ 30 minutes durant laquelle les élèves interagiront avec une simulation de la vie des étoiles, une activité d'environ 30 minutes durant laquelle la classe devra compléter une fresque synthétisant les rapports entre les différents types d'étoiles vus précédemment puis d'une trace écrite consistant en la complétion d'un texte à trou.
L'animation fonctionne bien avec une vingtaine d'élèves.

### **Conditions matérielles requise** 

Une salle de classe comprenant assez de tables et de chaise pour que chaque élève ait une place.
Au minimum un ordinateur par paire d'élèves. Avoir un ordinateur par élève est préférable. Sur chacun de ces ordinateurs doit être installé le programme python effectuant la simulation.
Un vidéo-projecteur connecté à ordinateur distinct de ceux utilisé par les élèves lors de la simulation.
De quoi faire tenir la fresque sur le tableau (ou un mur s'il n'y a pas de tableau), par exemple des aimants.

### **Plan de la Séance** 


### **Simulation Informatique**

#### **Choix de Conception** 

Le programme python simule l'évolution d'une masse de gaz initiale dans un univers fini en deux dimension.
La distribution de masse est donc représentée par un `array numpy` dont les cases correspondent à des densité de masse.
L'évolution de la répartition de masse se fait suivant selon un modèle simplifié de mécanique des fluides prenant en compte la diffusion et la gravité. La diffusion est calculée selon la deuxième loi de Fick. Pour calculer l'effet de la gravité, nous utilisons l'équation de continuité de la mécanique des fluides dans laquelle nous approximons la vitesse locale des particules par une valeur proportionnelle au champ gravitationnel.  
Lorsque que la densité dépasse un certain seuil dans une certain ensemble connexe de points, une étoile est formée. 
La matière à l'intérieur d'une étoile n'évolue plus suivant les équations décrite précédemment mais évolue d'une manière entièrement déterminée par le type de l'étoile. Ainsi, les étoiles n'ont pas de vitesse, elles sont fixes.

### **Extensions et Améliorations**

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

