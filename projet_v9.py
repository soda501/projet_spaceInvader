try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox


class Bullet(object):
    def __init__(self):
        self.rect_id = None  #instance du bullet
        self.diametre = 4  #diametre du bullet

    def install(self, canvas, x, y):  #on demande le canvas pour faire apparaitre le bullet, puis les coordonnees du defender pour que le bullet parte du bon endroit
        self.canvas = canvas
        self.y = y
        self.rect_id = self.canvas.create_oval(x, y, x+self.diametre, y+self.diametre, fill='white') #creation du bullet
        self.animation()  #appel de la fonction animation pour bouger la bullet
        

    def animation(self):
        self.canvas.move(self.rect_id, 0, -20) #deplace le bullet de 20 vers le haut
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
            cls.alien_dead = tk.PhotoImage   #on met l'image dedans
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

    #def install_alien_dead(self, x, y):
    #    self.install_in(self.canvas, x, y, Alien.get_alien_dead())
    #    self.canvas.after(300, self.canvas.delete(get_id))

    def move(self, canvas, x, y):
        if self.alien_is_alive():  #vérification de l'état "vivant" de l'alien
            canvas.move(self.get_image(), x, y)   #mouvement de l'alien
        
        


class Defender(object):
    def __init__(self):
        self.rect_id = None  #instance du defender
        self.square_width = 50  #taille du defender
        self.x = 400  #nos coordonnees initials du defender
        self.y = 550
        self.rafale = 0  #initialisation du nombre de bullet tirer

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
        elif (event.keysym == 'space' and self.rafale<8):
            self.bullet = Bullet()  #creation d'une instance bullet lorsque l'on appuie sur espace pour tirer
            self.bullet.install(self.canvas, self.x, self.y)  #appel de la fonction de creation de la bullet
            self.rafale = self.rafale +1 #comptage du nombre de bullet tirer
            print('espace')  #afin de déboguer si nos fonctions marche

class Fleet(object):
    def __init__(self):
        self.lines = 4  #nombre de lignes dans la flotte
        self.columns = 8  #nombre de colonnes dans la flotte
        size_of_fleet = self.lines * self.columns    #taille de la flotte par lignes et colonnes
        self.fleet = [None]*size_of_fleet #initialisation de la flotte, par sa taille
        self.x = 20  #vitesse horizontale du mouvement de l'alien
        self.y = 0  #vitesse verticale du mouvement de l'alien

    def install_in(self, canvas):
        self.canvas = canvas  #récupération du canvas
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
            


class Game(object):
    def __init__(self):
        self.defender = Defender()  #defender de la partie
        self.fleet = Fleet()  #flotte d'alien de la partie

    def install_in(self, canvas):  #on demande le canvas pour les autres classes
        self.defender.install(canvas)  #creation du defender dans le canvas
        self.fleet.install_in(canvas)
        self.canvas = canvas
        self.canvas.after(10, self.animation)

    def animation(self):
        self.fleet.move(self.canvas)
        self.canvas.after(300, self.animation)



class SpaceInvader(object):  #classe initiale avec creation de la frame 
    def __init__(self):  #Création de la Frame avec le Canvas
        self.root = tk.Tk()
        self.root.title("Projet SpaceInvaders")  #nom du projet
        self.game = Game()  #instance pour appeler le jeu
        self.canvas_width = 1000  #largeur de la frame
        self.canvas_height = 600  #hauteur de la frame
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='black')  #creation du canvas
        self.canvas.pack()  #fonction d'apparition du canvas dans la frame

    def install_in(self):
        self.game.install_in(self.canvas)  #appel pour debut de partie

    def start(self):
        self.install_in()  #appel afin de faire apparaitre le reste des objet du jeu
        self.root.bind("<Key>", self.game.defender.keypress)  #fonction pour appel depuis clavier
        self.root.mainloop()  #Apparition de la fenetre

Jeu = SpaceInvader()
Jeu.start()
