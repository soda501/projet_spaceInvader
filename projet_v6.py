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
    alien_alive = None  #initialisation de l'image d'un alien vivant
    alien_dead = None   #initialisation de l'image d'un alien mort

    @classmethod
    def get_alien_still_alive(cls):   #afin de retourner l'image de l'alien vivant
        if cls.alien_alive == None:
            cls.alien_alive = tk.PhotoImage(file='alien.gif')
        return cls.alien_alive
    
    def __init__(self):
        self.pim = tk.PhotoImage(file='alien.gif')  #stockage de l'image
        self.rect_id = None  #instance où sera stocké l'alien
        self.x = 20  #vitesse horizontale du mouvement de l'alien
        self.y = 0  #vitesse verticale du mouvement de l'alien

    def install_in(self, canvas, x, y):
        # creation de l'alien
        self.canvas = canvas
        self.canvas_width = int(canvas.cget("width"))  #on prends la largeur du canvas pour nos prochaines conditions 
        #apparition de l'alien
        self.rect_id = self.canvas.create_image(x, y, image=self.pim, tags="image")

    def move(self):
        # calcul du deplacement dans self.x
        if(self.x>0):
            if(self.canvas.coords(self.rect_id)>=[self.canvas_width-50, 0]):   #fais le chemin inverse quand il atteint l
                self.x = self.x * -1;   #modifie la vitesse en x pour qu'il fasse le chemin inverse
                self.y = self.y + 10     #lorsqu'il atteint l'extremité, il descend de 10 pixels (environ)
        else :
            if (self.canvas.coords(self.rect_id)<=[35, 0]):
                self.x = self.x * -1   #modifie la vitesse en x pour qu'il fasse le chemin inverse
                self.y = self.y + 10   #lorsqu'il atteint l'extremité, il descend de 10 pixels (environ)
           
        # deplacement de l'alien
        self.canvas.move(self.rect_id, self.x, self.y)  #effectue le mouvement aux vitesses self.x et self.y
        self.y = 0  #reinitialise afin qu'il ne descende pas à chaque mouvement effectué par l'alien
        


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
        self.fleet = []  #flotte contenant nos aliens
        self.fleet.append(Alien())
        self.fleet.append(Alien())
        self.fleet.append(Alien()) #Instances aliens

    def install_in(self, canvas):
        x = 50  #coordonnees initiales de l'alien
        y = 20
        for m in self.fleet:
            m.install_in(canvas, x, y)  #appel de la focntion de la classe Alien afin d'afficher l'alien
            x=x+80   #décalage des images

    def move(self):
        for m in self.fleet:
            m.move()  #appel pour mouvement des aliens dans le canvas
            


class Game(object):
    def __init__(self):
        self.defender = Defender()  #defender de la partie
        self.fleet = Fleet()  #flotte d'alien de la partie

    def install_in(self, canvas):  #on demande le canvas pour les autres classes
        self.defender.install(canvas)  #creation du defender dans le canvas
        self.fleet.install_in(canvas)
        self.canvas = canvas    #notre canvas
        self.canvas.after(10, self.animation)  #faire l'animation apres 10 ms

    def animation(self):
        self.fleet.move()  #appel de la fonction move() de la classe Fleet afin de faire bouger automatiquement la flotte
        self.canvas.after(300, self.animation)  #repeter l'animation toutes les 300 ms



class SpaceInvader(object):  #classe initiale avec creation de la frame 
    def __init__(self):  #Création de la Frame avec le Canvas
        self.root = tk.Tk()
        self.root.title("Projet SpaceInvaders")  #nom du projet
        self.game = Game()  #instance pour appeler le jeu
        self.canvas_width = 800  #largeur de la frame
        self.canvas_height = 600  #hauteur de la frame
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)  #creation du canvas
        self.canvas.pack()  #fonction d'apparition du canvas dans la frame

    def install_in(self):
        self.game.install_in(self.canvas)  #appel pour debut de partie

    def start(self):
        self.install_in()  #appel afin de faire apparaitre le reste des objet du jeu
        self.root.bind("<Key>", self.game.defender.keypress)  #fonction pour appel depuis clavier
        self.root.mainloop()  #Apparition de la fenetre

Jeu = SpaceInvader()  #initialisation de notre jeu
Jeu.start()  #debut du jeu
