# **Informations générales**

## **Plan du site web**

Notre site web est réparti en 4 onglets : 

- Celui-ci où vous trouverez les informations générales concernant notre projet, 
- l'onglet «[Déroulé de la séance](plan.md)» présentant la séance que nous avons réalisée,
- l'onglet «[Simulation informatique](simulation.md)» expliquant le code de la simulation plus en détail,
- l'onglet «[Galerie](galerie_photo.md)» montrant l'ensemble des images utilisées pour ce projet.

<br>
### **Description** 

Cette intervention est une séance de médiation scientifique ayant pour ambition de faire découvrir à une classe de CM2 les différents types étoiles et leur évolution. Pour ce faire elle aborde la formation des étoiles à partir de nuages de gaz, l'évolution de ces nuages en naine rouge, naine jaune ou géante bleu puis la trajectoire de ces différentes étoiles qui évoluent en des naines blanches, des géantes rouges, des étoiles à neutrons et des trous noirs. L'objectif recherché est d'émerveiller les élèves en leur faisant prendre conscience que l'univers contient de nombreux corps célestes fondamentalement différent des objets avec lesquels nous interagissons sur Terre. 

<br>

## **Matériel requis**

**Fresque / Carte mentale:** 

- Une grande feuille CANSON (50cm x 70cm) ∼ 2-5€ 
- 11 de cartes pour compléter la fresque 
- Plastifieuse ∼ 20-30€ 
- Pochette de plastifications ∼ 15€ 
- Cartes (papier) 
- Scotch double face 

	**Total : 50€** 

> *<font color="#7f7f7f">Une partie du matériel décrit nous a été fourni par CentraleSupélec.</font>*

<br>

### **Conditions matérielles requises** 

Au minimum un ordinateur par paire d'élèves. Avoir un ordinateur par élève est préférable. Sur chacun de ces ordinateurs doit être installé le programme python effectuant la simulation.
Un vidéo-projecteur est nécessaire pour la projection des diapositives. 
La fresque doit pouvoir être accrochée sur le tableau (ou un mur s'il n'y a pas de tableau), par exemple avec des aimants, pour pouvoir la compléter tous ensemble.

<br>
### **Plan de la Séance** 

Concrètement, la séance, d'une durée totale de deux heures, comprendra une présentation d'environ 45 minutes avec des diapositives projetées au tableau, une activité sur ordinateur d'environ 35 minutes durant laquelle les élèves interagiront avec une simulation de la vie des étoiles, une activité d'environ 30 minutes durant laquelle la classe devra compléter une fresque synthétisant les rapports entre les différents types d'étoiles vus précédemment puis d'une trace écrite consistant en la complétion d'un texte à trou en une dizaine de minutes.

Pour le plan détaillé de la séance, voir la rubrique «[Déroulé de la Séance](plan.md)»

<br>
## **Contraintes ayant guidé la conception de cette intervention** 

Plusieurs contraintes ont dû être respectées lors de la conception de cette intervention. Le contenu de la séance doit être adapté au niveau CM1/CM2 ainsi qu'au contexte socio-économique de l’école. La séance doit proposer des activités ludiques et ne pas être uniquement un cours magistral. L’ensemble des supports et expériences doit être reproductible à partir des ressources du projet, dans le respect d’un budget limité. Enfin, une trace écrite synthétique doit être fournie aux élèves à l’issue de la séance.

<br>
### **Simulation Informatique**
#### **Choix de Conception** 

Le programme python simule l'évolution d'une masse de gaz initiale dans un univers fini en deux dimension.
La distribution de masse est donc représentée par un `array numpy` dont les cases correspondent à des densité de masse.
L'évolution de la répartition de masse se fait suivant selon un modèle simplifié de mécanique des fluides prenant en compte la diffusion et la gravité. La diffusion est calculée selon la deuxième loi de Fick. Pour calculer l'effet de la gravité, nous utilisons l'équation de continuité de la mécanique des fluides dans laquelle nous approximons la vitesse locale des particules par une valeur proportionnelle au champ gravitationnel.  
Lorsque que la densité dépasse un certain seuil dans une certain ensemble connexe de points, une étoile est formée. 
La matière à l'intérieur d'une étoile n'évolue plus suivant les équations décrite précédemment mais évolue d'une manière entièrement déterminée par le type de l'étoile. Ainsi, les étoiles n'ont pas de vitesse, elles sont fixes.

Pour plus d'informations sur la simulation, voir la rubrique «[Simulation Informatique](simulation.md)».

<br>
### **Extensions**

En fonction du déroulement de la séance il est possible de la compléter par une explication des phénomènes contre-intuitif se déroulant au voisinage des trou noirs, une présentation des études scientifiques ou  une introduction à la méthode scientifique, permettant ainsi de comprendre par quel processus les modèles présentés lors de la séance ont été établis. 

<br>
## **Difficultés à prévoir**

Faire attention à la version de `Powerpoint` disponible et au format de projection du vidéo-projecteur, le rendu des diapositives et de certaines animations peuvent être différent. 

<br>

## **Ressources** 

### **Nos Supports et Documents**

- [Présentation / diapositives](assets/ressource/presentation_entreeleve.pptx)
- [Fresque initiale](assets/ressource/fresque.png)
- [Fresque complétée](assets/ressource/fresque_complete.png)
- [Cartes pour la frise](assets/ressource/cartes_frises.pdf)
- [Texte à trous](assets/ressource/texte-a-trou.pdf)
- [Simulation python](assets/ressource/simulation_final_version.py)
- [Simulation partie1](assets/image_perso/simulation_p1.png) : Interface de la première partie de notre simulation
- [Exemple pour la première partie](assets/image_perso/simulation_p1-ex.png)
- [Simulation partie2](assets/image_perso/simulation_p2.png) : Interface de la seconde partie de notre simulation 

<br>

### **Images utilisées** 

Pour plus de visibilité, voir la rubrique «[Galerie](galerie_photo.md)».

#### **Images**
- [Image Soleil](assets/image/sun.jpg) : Image du Soleil (*NASA/Goddard/SDO*)
- [Coupe du Soleil](assets/image/slice_sun.png) : Vue en coupe du Soleil générée par intelligence artificielle à partir de l'image du Soleil
- [Pilier de la création](assets/image/pillar_of_creation.jpeg) : Prise par le télescope Hubble (*NASA*, *ESA*)
- [Nébuleuse d'Orion](assets/image/Orion_Nebula.jpg) : Vue par le télescope spatial Hubble (*NASA*, *STScI*, *ESA*)
- [Naine Brune](assets/image/browndwarf.jpg) : Vue d'artiste inspirée d'image prise par Hubble (*Centre spatial Goddard*, *NASA*)
- [Naine rouge](assets/image/reddwarf.png) : image générée par intelligence artificielle
- [Naine blanche](assets/image/whitedwarf.jpg) : CC BY-NC-SA Eric Simon
- [Naine blanche dézoomée](assets/image/whitedwarf_unzoomed.png) : Image dézoomée par intelligence artificielle
- [Géante rouge](assets/image/redgiant.jpg) : image retouchée à partir d'une [image du Soleil](assets/image/redgiant_original.jpg) de la *NASA/Goddard/SDO*
- [Nébuleuse planétaire](assets/image/planetary_nebula.jpg) : La nébuleuse de l'Hélice (*NGC 7293) (NASA, NOAO, ESA, the Hubble Helix Nebula Team, M. Meixner (STScI), and T.A. Rector (NRAO)*)
- [Géante bleue](assets/image/bluegiant.png) : image générée par intelligence artificielle
- [Comparaison des Géantes bleus](assets/image/blue_star_comparaison.jpg) : ESO/M. Kornmesser ([Lien](http://www.eso.org/public/images/eso1030c/))
- [Supernova](assets/image/supernova.jpeg) : Vue d'artiste de la supernova SN2016aps (*© M. Weiss, Center for Astrophysics Harvard & Smithsonian*)
- [Etoile à neutrons](assets/image/neutronstar.jpg) : Image de l'*ESA*
- [Trou noir](assets/image/black_hole_NASA.jpg) : Image composite du disque d'accrétion du trou noir M87* (*Event Horizon Telescope*) 
- [Trou noir Interstellar](assets/image/black_hole_interstellar.jpg) : Image issue du film *Interstellar* réalisé par Christopher Nolan
- [Proto-étoile](assets/image/Protostar.jpeg) : Image de *L1527 IRS*, prise par le télescope spatial James-Webb  en 2022 (*NASA, ESA, CSA, and STScI, J. DePasquale*)

#### Images exportées de Google Earth Pro
- [Maurice Barrès 2](assets/image/ge_maurice-barres.jpg) : Image Google Earth de la zone urbaine autour de l'école où nous sommes intervenues (*Image © Google / Fournisseurs de données*)
- [Metz](assets/image/ge_metz.jpg) : Image Google Earth de la ville de Metz (*Image © Google / Fournisseurs de données*)
- [Europe](assets/image/ge_europe.jpg) : Image Google Earth de l'Europe (*Image © Google / Fournisseurs de données*)
- [Terre](assets/image/ge_terre.jpg) : Image Google Earth de la Terre (*Image © Google / Fournisseurs de données*)

<br>

## **Crédits**
### **Contributions** 
- **Auteurs** : Raphaël CADIER--GIARD, Enzo CHEN 
- **Professeur Encadrant** : Paul FRAUX 
- **Professeur des Ecoles** : Victor RENAUX 

<br>

## **Bibliographie commentée**
Les ressources mentionnées ci-dessous ont été principalement utilisées pour la simulation informatique et ne seront pas directement utiles pour les élèves, ils correspondent à un niveau post-BAC.  

- Relation entre durée de vie d'une étoile de la séquence principale avec un facteur $1/M^3$.  
	**<u>Source :</u>** *[https://www.astronomy.ohio-state.edu/thompson.1847/1101/lecture_main_sequence.html](https://www.astronomy.ohio-state.edu/thompson.1847/1101/lecture_main_sequence.html)*
- Relation empirique entre la masse d'une géante rouge et celle de la naine blanche qu'elle deviendra : $M_{final} = 0.109  M_{initial} + 0.394 M_{Soleil}$.  
	**<u>Source :</u>** *L'article Kalirai, J. S. et al., Initial–Final Mass Relation from White Dwarfs in Open Clusters, The Astrophysical Journal, 676, 594 (2008)*
- Proportion de masse éjectée lors d'une supernova : `self.massive_core_fraction = 0.15 `   
	**<u>Source :</u>** *[The initial mass-remnant mass relation for core collapse supernovae Cristiano Ugolini](https://www.aanda.org/articles/aa/full_html/2025/03/aa51483-24/aa51483-24.html)*
- 2ème loi de Fick utilisé pour calculer l'évolution de la répartition de masse dans la simulation.   
	**<u>Source :</u>**
	
	- *[https://nte.mines-albi.fr/SciMat/fr/co/SM5uc1-2.html](https://nte.mines-albi.fr/SciMat/fr/co/SM5uc1-2.html)* 
	- *[https://chem.libretexts.org/Bookshelves/ ](https://chem.libretexts.org/Bookshelves/)*
	- *Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Kinetics/09%3A_Diffusion#Fick.E2.80.99s_First_Law_of_Diffusion*

- Estimation des masses des différents types d'étoiles.  
	**<u>Source :</u>** *THE ASTROPHYSICAL JOURNAL, 482:420–432, 1997 June 10 The End of the Main Sequence*
