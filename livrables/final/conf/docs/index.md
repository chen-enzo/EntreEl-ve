
# **Projet EntreÉlève**

## **Description** 

Le projet EntreElève a pour but d'éveiller la curiosité scientifique des plus jeunes tout en contribuant à réduire les stéréotypes de genre dans les domaines scientifiques. En encourageant les élèves aux questionnement et la participation, ce projet vise à rendre les sciences plus accessibles et plus attrayantes pour tous, indépendamment du genre, et à promouvoir une image positive et inclusive des sciences dès le plus jeune âge.

Dans cette optique, nous avons conçu une séance interactive de deux heures destinée à une classe de CM1/CM2, autour de notions d’astronomie. Cette séance a pour objectif d'aider les élèves à prendre conscience de l’immensité de l’univers, à connaître les grandes étapes de la vie d’une étoile et à identifier quelques objets célestes importants. 

Plusieurs contraintes ont guidé la conception de cette intervention. Le contenu doit être adapté au niveau CM1/CM2 ainsi qu'au contexte socio-économique de l’école. La séance doit proposer des activités ludiques et ne pas être uniquement un cours magistral. L’ensemble des supports et expériences doit être reproductible à partir des ressources du projet, dans le respect d’un budget limité. Enfin, une trace écrite synthétique doit être fournie aux élèves à l’issue de la séance.



---
## **Matériel**

**Fresque / Carte mentale:** 

- Une grande feuille CANSON (50cm x 70cm) ∼ 2-5€ 
- 11 de cartes pour compléter la fresque 
- Plastifieuse ∼ 20-30€ 
- Pochette de plastifications ∼ 15€ 
- Carte (papier) 
- Scotch double face 

	**Total : 50€** 

> *<font color="#7f7f7f">Une partie du matériel décrit nous a été fourni par CentraleSupélec.</font>*


---
## **Déroulement de la séance**
### **Situation** 

Cette intervention est une séance de médiation scientifique ayant pour ambition de faire découvrir à une classe de CM2 les différents types étoiles et leur évolution. Pour ce faire elle aborde la formation des étoiles à partir de nuages de gaz, l'évolution de ces nuages en naine rouge, naine jaune ou géante bleu puis la trajectoire de ces différentes étoiles qui évoluent en des naines blanches, des géantes rouges, des étoiles à neutrons et des trous noirs. L'objectif recherché est d'émerveiller les élèves en leur faisant prendre conscience que l'univers contient de nombreux corps célestes fondamentalement différent des objets avec lesquels nous interagissons sur Terre. 


### **Conditions matérielles requises** 

Au minimum un ordinateur par paire d'élèves. Avoir un ordinateur par élève est préférable. Sur chacun de ces ordinateurs doit être installé le programme python effectuant la simulation.
Un vidéo-projecteur est nécessaire pour la projection des diapositives. 
La fresque doit pouvoir être accrochée sur le tableau (ou un mur s'il n'y a pas de tableau) pour faire , par exemple avec des aimants.

### **Plan de la Séance** 

Concrètement, la séance, d'une durée totale de deux heures, comprendra une présentation d'environ 45 minutes avec des diapositives projetées au tableau, une activité sur ordinateur d'environ 35 minutes durant laquelle les élèves interagiront avec une simulation de la vie des étoiles, une activité d'environ 30 minutes durant laquelle la classe devra compléter une fresque synthétisant les rapports entre les différents types d'étoiles vus précédemment puis d'une trace écrite consistant en la complétion d'un texte à trou en une dizaine de minutes.

Pour le plan détaillé de la séance, voir la rubrique «[Plan détaillé](plan.md)»


### **Simulation Informatique**
#### **Choix de Conception** 

Le programme python simule l'évolution d'une masse de gaz initiale dans un univers fini en deux dimension.
La distribution de masse est donc représentée par un `array numpy` dont les cases correspondent à des densité de masse.
L'évolution de la répartition de masse se fait suivant selon un modèle simplifié de mécanique des fluides prenant en compte la diffusion et la gravité. La diffusion est calculée selon la deuxième loi de Fick. Pour calculer l'effet de la gravité, nous utilisons l'équation de continuité de la mécanique des fluides dans laquelle nous approximons la vitesse locale des particules par une valeur proportionnelle au champ gravitationnel.  
Lorsque que la densité dépasse un certain seuil dans une certain ensemble connexe de points, une étoile est formée. 
La matière à l'intérieur d'une étoile n'évolue plus suivant les équations décrite précédemment mais évolue d'une manière entièrement déterminée par le type de l'étoile. Ainsi, les étoiles n'ont pas de vitesse, elles sont fixes.

Pour plus d'informations sur la simulation, voir la rubrique «[Simulation Informatique](simulation.md)».

### **Extensions et Piste d'améliorations**

En fonction du déroulement de la séance il est possible de la compléter par une explication des phénomènes contre-intuitif se déroulant au voisinage des trou noirs, une présentation des études scientifiques ou  une introduction à la méthode scientifique, permettant ainsi de comprendre par quel processus les modèles présentés lors de la séance ont été établis. 

Pour aller plus loin, notre simulation peut être améliorée ... 

## Difficultés à prévoir

Faire attention à la version de `Powerpoint` disponible et au format de projection du vidéo-projecteur, le rendu des diapositives et de certaines animations peuvent être différent. 



---
## **Ressources** 

### **Nos Supports et Documents**

- [Présentation / diapositives](assets/ressource/presentation_entreeleve.pptx)
- [Fresque / Carte Mentale initiale](assets/ressource/fresque.png)
- [Cartes pour la frise](assets/ressource/cartes_frises.pdf)
- [Texte à trous](assets/ressource/texte-a-trou.pdf)
- [Simulation python](assets/ressource/simulation_final_version.py)
- [Simulation partie1](simulation_p1.png) : Interface de la première partie de notre simulation
- [Simulation partie2](simulation_p2.png) : Interface de la seconde partie de notre simulation 

### **Images utilisées** 

Pour plus de visibilité, voir la rubrique «[Galerie](galerie_photo.md)».

#### **Images**
- [Image Soleil](assets/image/sun.jpg) : Image du Soleil (*NASA/Goddard/SDO*)
- [Coupe du Soleil](assets/image/slice_sun.png) : Vue en coupe du Soleil générée par IA à partir de l'image du Soleil
- [Pilier de la création](assets/image/pillar_of_creation.jpeg) : Prise par le télescope Hubble (*NASA*, *ESA*)
- [Nébuleuse d'Orion](assets/image/Orion_Nebula.jpg) : Vue par le télescope spatial Hubble (*NASA*, *STScI*, *ESA*)
- [Naine Brune](assets/image/browndwarf.jpg) : Vue d'artiste inspirée d'image prise par Hubble (*Centre spatial Goddard*, *NASA*)
- [Naine rouge](assets/image/reddwarf.png) : image générée par IA
- [Naine blanche](assets/image/whitedwarf.jpg) : CC BY-NC-SA Eric Simon
- [Naine blanche dézoomée](assets/image/whitedwarf_unzoomed.png) : Image dézoomée par IA 
- [Géante rouge](assets/image/redgiant.jpg) : image retouchée à partir d'une [image du Soleil](assets/image/redgiant_original.jpg) de la *NASA/Goddard/SDO*
- [Nébuleuse planétaire](assets/image/planetary_nebula.jpg) : La nébuleuse de l'Hélice (*NGC 7293) (NASA, NOAO, ESA, the Hubble Helix Nebula Team, M. Meixner (STScI), and T.A. Rector (NRAO)*)
- [Géante bleu](assets/image/bluegiant.png) : image générée par IA
- [Comparaison des Géantes bleus](assets/image/blue_star_comparaison.jpg) : ESO/M. Kornmesser ([Lien](http://www.eso.org/public/images/eso1030c/))
- [Supernova](assets/image/supernova.jpeg) : Vue d'artiste de la supernova SN2016aps (*© M. Weiss, Center for Astrophysics Harvard & Smithsonian*)
- [Etoile à neutrons](assets/image/neutronstar.jpg) : Image de l'*ESA*
- [Trou noir](assets/image/black_hole_NASA.jpg) : Image composite du disque d'accrétion du trou noir M87* (*Event Horizon Telescope*) 
- [Trou noir Interstellar](assets/image/black_hole_interstellar.jpg) : Image issue du film *Interstellar* réalisé par Christopher Nolan
- [Proto-étoile](assets/image/Protostar.jpeg) : Image de *L1527 IRS*, prise par le télescope spatial James-Webb  en 2022 (*NASA, ESA, CSA, and STScI, J. DePasquale*)

#### Images exportées de Google Earth Pro
- [Maurice Barrès 2](ge_maurice-barres.jpg) : Image Google Earth de la zone urbaine autour de l'école où nous sommes intervenues (*Image © Google / Fournisseurs de données*)
- [Metz](ge_metz.jpg) : Image Google Earth de la ville de Metz (*Image © Google / Fournisseurs de données*)
- [Europe](ge_europe.jpg) : Image Google Earth de l'Europe (*Image © Google / Fournisseurs de données*)
- [Terrre](ge_terre.jpg) : Image Google Earth de la Terre (*Image © Google / Fournisseurs de données*)


---
## **Crédits**
### **Contributions** 
- **Auteurs** : Raphaël CADIER--GIARD, Enzo CHEN 
- **Professeur Encadrant** : Paul FRAUX 
- **Professeur des Ecoles** : Victor RENAUX 


---
## **Sélection commentée de notre ibliographie**
Aucunes des ressources mentionnées ci dessous ne pourra directement être utiles pour les élèves car ils ne les comprendraient pas.

-https://www.astronomy.ohio-state.edu/thompson.1847/1101/lecture_main_sequence.html justifie le choix effectué dans la simulation de prendre une durée de vie proportionelle à 1/M**3 pour les étoiles de la séquence principale :


L'article Kalirai, J. S. et al., Initial–Final Mass Relation from White Dwarfs in Open Clusters, The Astrophysical Journal, 676, 594 (2008) donne une relation empirique entre la masse d'une géante rouge et celle de la naine blanche qu'elle deviendra : 
M_final = 0.109  M_initial + 0.394 M_Soleil
Nous avons utilisés cette relation dans la simulation.

Proportion de masse ejectée lors d'une supernovae : self.massive_core_fraction = 0.15 
source : The initial mass-remnant mass relation for core collapse supernovae Cristiano Ugolini : https://www.aanda.org/articles/aa/full_html/2025/03/aa51483-24/aa51483-24.html


Les sources suivantes expliquent la 2ème loi de Fick, qui a été utilisé pour calculer l'évolution de la répartition de masse dans la simulation. 
https://nte.mines-albi.fr/SciMat/fr/co/SM5uc1-2.html et https://chem.libretexts.org/Bookshelves/ et Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Kinetics/09%3A_Diffusion#Fick.E2.80.99s_First_Law_of_Diffusion

-L'article suivant permet d'avoir une estimation des masses des différents types d'étoiles: THE ASTROPHYSICAL JOURNAL, 482:420–432, 1997 June 10 The End of the Main Sequence






