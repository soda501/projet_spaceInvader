"""
    Groupe : SALL Soda, FORTIN Lison
    version : 14
"""
import json
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
    from tkinter import *
except:
    import Tkinter as tk
    import tkMessageBox


class Score(object):
    def __init__(self, nomJoueur, nbPoints):
        self.nomJoueur=nomJoueur  #nom du joueur
        self.nbPoints=nbPoints  #score du joueur
        
    #accesseurs des instances de Score:   
    def get_nomJoueur(self):
        return self.nomJoueur
    def set_nomJoueur(self, newName):
        self.nomJoueur=newName
    def get_nbPoints(self):
        return self.nbPoints
    def set_nbPoints(self, newScore):
        self.nbPoints=newScore

    def __str__(self):  #fonction pour "imprimer" les variables scores lorsque c'est demandé
        return str(self.nomJoueur)+" : "+str(self.nbPoints)+" points"

class Resultat(object):
    def __init__(self):
        self.LesScores = []  #initialisation d'une liste où stocker les scores
    
    def ajouter_Score(self, newScore):
        self.LesScores.append(newScore)  #fonction pour ajouter un score
        
    def __str__(self):
        chaine=str(self.LesScores[0])  #fonction pour imprimer la liste des scores enregistrés
        for e in self.LesScores[1:]:
            chaine=chaine+ str(e)
        return chaine
    
    @classmethod
    def fromFile(cls,nomFichier):  #méthode de classe pour afficher le contenu du fichier
        f = open(nomFichier,"r")   #on ouvre le fichier avec 'r' : read pour le lire
        #chargement
        liste = json.load(f)  #liste de dictionnaire trouvé dans le fichier
        
        L = []  #création d'une liste de scores, tirés du fichier
        for d in liste:
            s=Score(d["nomJoueur"],d["Score"]) #création d'instance pour chaque score trouvé dans le dictionnaire 
            #l'ajouter dans la liste
            L.append(s)
        Res=Resultat()  #on crée une instance résultat, pour mettre la liste trouvé dans la liste des scores
        Res.LesScores=L
        f.close()  #on referme le fichier 
        return Res  #on retourne la liste
    
    def toFile(self,nomFichier):  #fonction de stockage des scores dans un fichier json
        f = open(nomFichier,"w")  #on ouvre le fichier json avec l'intention "w" : write soit écrire dedans
        liste = []  #on créer une liste vide où mettre le dictionnaire
        for s in self.LesScores:
            d = {}  #initialisation du dictionnaire
            d["nomJoueur"] = s.nomJoueur  #on met nos instances de score dans le dictionnaire
            d["Score"] = s.nbPoints
            liste.append(d)  #on l'ajoute dans notre liste de dictionnaire
        json.dump(liste,f)  #on les encode dans le fichier json ouvert avant
        f.close();  #on referme le fichier




class Bullet(object):
    def __init__(self):
        self.bull_id = None  #instance du bullet
        self.diametre = 4  #diametre du bullet

    def install(self, canvas, x, y):  #on demande le canvas pour faire apparaitre le bullet, puis les coordonnees du defender pour que le bullet parte du bon endroit
        self.canvas = canvas
        self.y = y
        self.bull_id = self.canvas.create_oval(x, y, x+self.diametre, y+self.diametre, fill='white') #creation du bullet
        self.animation()  #appel de la fonction animation pour bouger la bullet

    def get_bullet(self):  #accesseur de la balle
        return self.bull_id

    def animation(self):
        self.canvas.move(self.bull_id, 0, -20) #deplace le bullet de 20 vers le haut
        self.canvas.after(100, self.animation)  #reitère l'animation toute les 100ms








class Alien(object):   #Alien
    alien_alive = None  #initialisation de l'image de l'alien vivant
    alien_dead = None  #initialisation de l'image de l'alien mort

    @classmethod
    def get_alien_still_alive(cls):  #méthode de classe, permettant de récupérer l'image de l'alien vivant
        if cls.alien_alive == None:  #on prend l'image initialisée de l'alien vivant,
            cls.alien_alive = tk.PhotoImage(file='alien.gif')  #on met l'image dedans
        return cls.alien_alive  #on retourne l'image

    @classmethod
    def get_alien_dead(cls):  #méthode de classe, permettant de récupérer l'image de l'alien mort
        if cls.alien_dead == None :  #on prend l'image initialisée de l'alien mort,
            cls.alien_dead = tk.PhotoImage(file='explosion.gif')   #on met l'image dedans (une explosion)
        return cls.alien_dead  #on retourne l'image
    
    def __init__(self):  #initialisation de l'image et de l'état de l'alien
        self.rect_id = None  #stockage de l'image
        self.alive = True  #état initial de l'alien : est vivant

    def get_image(self):
        return self.rect_id   #accesseur de l'image

    def alien_is_alive(self):
        return self.alive  #accesseur de l'état de l'alien

    def install_in(self, canvas, x, y, image, tag):
        # creation de l'alien
        self.canvas = canvas  #récupération du canvas
        self.canvas_width = int(canvas.cget("width"))  #on prends la largeur du canvas pour nos prochaines conditions 
        #apparition de l'alien
        self.rect_id = self.canvas.create_image(x, y, image=image, tags=tag)

    def install_alien_alive(self, canvas, x, y):   #appel de l'installation de l'alien lorsqu'il est vivant, pour chaque mouvement
        self.install_in(canvas, x, y, Alien.get_alien_still_alive(), "alien_alive") #installation de l'alien avec l'état (tag) vivant, afin que pour le mouvement, seul les aliens vivant bougent

    def install_alien_dead(self, x, y):   #appel de l'installation d'un alien mort (donc aucun) lorsqu'il est touché
        self.install_in(self.canvas, x, y, Alien.get_alien_dead(), "alien_dead") #installation de l'alien mort
        self.canvas.after(300, self.efface_explosion, self.get_image())  #appel de la fonction afin d'effacer l'explosion de l'impact après 300 millisecondes

    def efface_explosion(self, dead_id):
        self.canvas.delete(dead_id)  #fonction permettant d'enlever l'image d'impact, pour continuer le jeu tranquillement

    def move(self, canvas, x, y):
        if self.alien_is_alive():  #vérification de l'état "vivant" de l'alien
            canvas.move(self.get_image(), x, y)   #mouvement de l'alien

    def alien_touche(self, canvas, bullet):  #fonction supprimant l'alien lorsqu'il est touché par une balle
        self.alive = False  #l'etat de l'alien devient mort
        alien_coords = canvas.coords(self.get_image())  #on récupère les coordonnées de l'alien au moment de l'impact pour redessiner l'alien mort dessus
        canvas.delete(self.get_image())  #on supprime l'image de l'alien anciennement vivant
        self.install_alien_dead(alien_coords[0], alien_coords[1])  #on appel une fonction poour installer l'explosion de quelques millisecondes
        
        





class Defender(object):
    def __init__(self):
        self.rect_id = None  #instance du defender
        self.square_width = 50  #taille du defender
        self.x = 400  #nos coordonnees initials du defender
        self.y = 550
        self.rafale = []  #initialisation du nombre de bullet tirer dans une liste de bullet pour le controle

    def install(self, canvas):  #on demande le canvas afin de pouvoir faire apparaitre le defender dans la frame
        self.canvas = canvas
        self.rect_id = self.canvas.create_polygon(self.x, self.y, self.x-(self.square_width/2), self.y+self.square_width, self.x+(self.square_width/2), self.y+self.square_width, fill='red') #creation du defender
    

    def keypress(self, event):

        if event.keysym == 'Left':    #quand touche flèche gauche alors le defender se déplace à gauche
            self.canvas.move(self.rect_id, -10, 0)  #deplace de 10 le defender vers la gauche
            print('gauche')  #afin de déboguer si nos fonctions marche
            self.x = self.x -10   #mise à jour des coordonnees en fonction du mouvement
        elif event.keysym == 'Right':   #quand touche flèche droite alors le defender se déplace à droite
            self.canvas.move(self.rect_id, +10, 0)  #deplace de 10 le defender vers la droite
            print('droite')  #afin de déboguer si nos fonctions marche
            self.x = self.x +10  #mise à jour des coordonnees en fonction du mouvement
        elif (event.keysym == 'space' and len(self.rafale)<8):
            self.bullet = Bullet()  #creation d'une instance bullet lorsque l'on appuie sur espace pour tirer
            self.bullet.install(self.canvas, self.x, self.y)  #on installe les balles ici puis on les stocke dans la liste après
            self.rafale.append(self.bullet)  #appel de la fonction de creation de la bullet puis ajout dans la liste de bullet
            print('espace')  #afin de déboguer si nos fonctions marche

        self.recharge()  #appel de controle afin de voir si une recharge est possible

    def get_bullets_fired(self):
        return self.rafale  #accesseur des bullets tirés

    def recharge(self):
        for bullet in self.rafale :
            bullet_coords = self.canvas.coords(bullet.get_bullet())  #on prend les coordonnées pour chaque balle tirées, 
            if(bullet_coords[1] <=0):  #si elles atteignent l'extremité de la fenetre, 
                self.rafale.remove(bullet)  #alors elles sont supprimés de la liste et une recharge est faite







class Fleet(object):
    def __init__(self):
        self.lines = 4  #nombre de lignes dans la flotte
        self.columns = 8  #nombre de colonnes dans la flotte
        size_of_fleet = self.lines * self.columns    #taille de la flotte par lignes et colonnes
        self.nb_aliens = size_of_fleet  #le nombre d'alien pour le controle de mort
        self.fleet = [None]*size_of_fleet #initialisation de la flotte, par sa taille
        self.x = 20  #vitesse horizontale du mouvement de l'alien
        self.y = 0  #vitesse verticale du mouvement de l'alien
        self.score = 0  #initialisation du score

    def install_in(self, canvas):
        self.canvas = canvas  #récupération du canvas ->sert-il à quelque chose ?
        x = 50  #coordonnées initiales de la flotte
        y = 20
        for i in range(len(self.fleet)): #on parcourt la flotte, car il n'y a pas de disctonction entre colonnes et lignes,
            if (i%self.columns == 0):  #à chaque fois que le nombre de colonnes a été atteint, on fait retour à la ligne 20 'pixels' en dessous de la ligne précédente
                y = y + Alien.get_alien_still_alive().height() + 20  #modification du y pour chaque nouvelle ligne
                x = 50 #réinitialisation du x pour chaque nouvelle ligne
            alien = Alien()  #création d'une instance alien
            alien.install_alien_alive(canvas, x, y)  #installation de l'alien dans la canvas, pour un alien initialement vivant
            x = x+Alien.get_alien_still_alive().width() + 20  #modification du x pour chaque nouvel alien de la ligne
            self.fleet[i]=alien  #l'ajout de l'alien à la flotte

    def move(self, canvas):
        
        coords= canvas.bbox("alien_alive") #on prend les coordonnées de l'alien vivant
        if coords == None: return #pas de mouvement si y'a de coordonnées trouvées pour éviter des erreurs 
        cwidth = int(canvas.cget("width")) #on recupére la largeur du canvas
        self.y = 0 #réinitialisation de la vitesse en y pour chaque fois qu'il atteint un extrémité
        # calcul du deplacement dans self.x
        if(self.x>0): #condition pour le mouvement horizontal
            if(coords[2]>=cwidth):   #fais le chemin inverse quand il atteint l'extremité de la fenêtre
                self.x = self.x * -1; #mouvement inverse en x
                self.y = self.y + 10 #decalage en y pour chaque extrémité
        else :              #de même mais pour le mouvement inverse en x
            if (coords[0]<0):
                self.x = self.x * -1
                self.y = self.y + 10

        cheight = int(canvas.cget("height"))  #recupération de la taille du canvas
        if(coords[3]>= cheight-10):   #condition lorsque le dernier y de la flotte atteint l'extremité de la fenetre
            canvas.create_text(400, 300, text="game over", fill="white")  #apparition d'un message "game over" en blanc
            return  #arret total de tout mouvement
           
        # deplacement de l'alien
        for alien in self.fleet :
            alien.move(canvas, self.x, self.y)

    def controle_collision(self, canvas, defender):  #fonction appelé automatiquement pour controler les collisions
        balles = defender.get_bullets_fired() #on récupère les balles tirés
        for b in list(balles):
            x1, y1, x2, y2 = canvas.coords(b.get_bullet()) #on récupère les coordonées de chacune des balles tirées
            collisions = canvas.find_overlapping(x1, y1, x2, y2)  #on récupère les objets se trouvant dans la trajectoire de la balle, lorsqu'ils se touchent
            for alien in self.fleet :
                if alien.alien_is_alive() and alien.get_image() in collisions :  #condition : l'alien doit être en vie, et être dans la liste d'alien ayant été touché
                    alien.alien_touche(canvas, defender)  #on appel la fonction pour que l'alien soit effacé
                    balles.remove(b)  #on enlève la balle de la liste : recharge de 1 coup
                    canvas.delete(b.get_bullet())  #on supprime la balle du canvas
                    self.score = self.score + 15  #dès qu'un alien meurt, le score augmente de 15 points

    def flotte_detruite(self, canvas):  #fonction pour finir lorsque la flotte est detruite
        max_dead = 0  #on compte le nombre d'aliens mort
        for alien in self.fleet :  #on prend les aliens de la flotte
            if(alien.alive == False):  #essayé de le faire avec les accesseurs !  si les aliens sont morts, 
                max_dead = max_dead + 1  #alors on les rajoute dans le compte
                if(max_dead>=self.nb_aliens):  #on controle le nombre d'aliens morts (avec le nb d'aliens dans la flotte
                    canvas.create_text(400, 300, text="BRAVO", fill="white")  #on fait apparaitre un message
                    return "loser"  #si c'est le cas, on retourne cela dans game pour finir le jeu
            else :
                return "ok"  #sinon on continue



class Game(object):
    def __init__(self):
        self.defender = Defender()  #defender de la partie
        self.fleet = Fleet()  #flotte d'alien de la partie

    def install_in(self, canvas):  #on demande le canvas pour les autres classes
        self.defender.install(canvas)  #creation du defender dans le canvas
        self.fleet.install_in(canvas)   #création de la flotte d'alien dans le canvas
        self.canvas = canvas  #récupération du canvas
        self.canvas.after(10, self.animation)  #on effectue l'animation après 10 millisecondes

    def animation(self):  #les animations du jeu automatiques
        self.fleet.move(self.canvas)  #appel de la fonction du mouvement de la flotte
        self.canvas.after(300, self.animation)  #on réitère l'animation toutes les 300 millisecondes
        self.fleet.controle_collision(self.canvas, self.defender)  #automatiquement, on controle les collisions possibles
        etat = self.fleet.flotte_detruite(self.canvas)  #on récupère l'état de la flotte, automatiquement
        if etat == "loser":
            return  #pour finir le jeu




class SpaceInvader(object):  #classe initiale avec creation de la frame 
    def __init__(self):  #Création de la Frame avec le Canvas
        self.root = tk.Tk()
        self.root.title("Projet SpaceInvaders")  #nom du projet
        self.game = Game()  #instance pour appeler le jeu
        self.canvas_width = 1000  #largeur de la frame
        self.canvas_height = 600  #hauteur de la frame
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='black')  #creation du canvas
        self.canvas.pack()  #fonction d'apparition du canvas dans la frame
        self.name = input("Nom du joueur")  #un input pour donner le nom du joueur
        self.score = None #une intialisation d'une instance de classe Score
        self.results = Resultat()  #initialisation d'une instance résultat

    def install_in(self):
        self.game.install_in(self.canvas)  #appel pour debut de partie

    def start(self):
        self.install_in()  #appel afin de faire apparaitre le reste des objet du jeu
        self.root.bind("<Key>", self.game.defender.keypress)  #fonction pour appel depuis clavier
        self.root.mainloop()  #Apparition de la fenetre
        self.score = Score(self.name, self.game.fleet.score)  #création d'un score avec le nom trouvé et le score enregistré 
        self.results.ajouter_Score(self.score)  #on ajoute ce score dans la liste de score de resultat 
        self.results.toFile("Scores.json")  #on l'enregistre dans le fichier Scores.json
        self.results.fromFile("Scores.json")  #on veut lire le contenu du fichier
        print(self.score)  #on imprime le score indivduel
        print(self.results)  #puis on imprime les scores enregistré 
        

Jeu = SpaceInvader()  #création d'un jeu
Jeu.start()  #début du jeu
