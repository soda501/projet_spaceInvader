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
    alien_alive = None
    alien_dead = None

    @classmethod
    def get_alien_still_alive(cls):
        if cls.alien_alive == None:
            cls.alien_alive = tk.PhotoImage(file='alien.gif')
        return cls.alien_alive

    @classmethod
    def get_alien_dead(cls):
        #if cls.alien_dead == None :
         #   cls.alien_dead = tk.PhotoImage
        return cls.alien_dead
    
    def __init__(self):
        self.rect_id = None
        self.id = None
        self.alive = True

    #def get_id(self):
    #    return self.id

    def install_in(self, canvas, x, y, image):
        # creation de l'alien
        self.canvas = canvas
        self.canvas_width = int(canvas.cget("width"))  #on prends la largeur du canvas pour nos prochaines conditions 
        #apparition de l'alien
        self.rect_id = self.canvas.create_image(x, y, image=image, tags="image")

    def install_alien_alive(self, canvas, x, y):
        self.install_in(canvas, x, y, Alien.get_alien_still_alive())

    #def install_alien_dead(self, x, y):
    #    self.install_in(self.canvas, x, y, Alien.get_alien_dead())
    #    self.canvas.after(300, self.canvas.delete(get_id))

    #def move(self):
        
        


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
        self.lines = 4
        self.columns = 8
        size_of_fleet = self.lines * self.columns
        self.fleet = [None]*size_of_fleet
        self.x = 20  #vitesse horizontale du mouvement de l'alien
        self.y = 0  #vitesse verticale du mouvement de l'alien

    def install_in(self, canvas):
        self.canvas = canvas
        x = 50
        y = 20
        #for m in self.fleet:
        #    m.install_in(canvas, x, y)
        #    x=x+80
        for i in range(len(self.fleet)):
            if (i%self.columns == 0):
                y = y + Alien.get_alien_still_alive().height() + 20
                x = 50
            alien = Alien()
            alien.install_alien_alive(canvas, x, y)
            x = x+Alien.get_alien_still_alive().width() + 20
            self.fleet[i]=alien

    def move(self, canvas):

        #self.x_min=self.fleet[0].coords
        #self.x_max=self.fleet[len(self.fleet)-1].coords
        #print(self.x_min)
        #print(self.x_max)
        
        bbox = canvas.bbox("alien_alive")
        if bbox == None: return
        cwidth = int(canvas.cget("width"))
        # calcul du deplacement dans self.x
        if(self.x>0):
            if(bbox[2]>=cwidth):   #fais le chemin inverse quand il atteint l
                self.x = self.x * -1;
                self.y = self.y + 10
        else :
            if (bbox[0]<0):
                self.x = self.x * -1
                self.y = self.y + 10
           
        # deplacement de l'alien
        self.canvas.move(canvas, self.x, self.y)
        self.y = 0
            


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
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)  #creation du canvas
        self.canvas.pack()  #fonction d'apparition du canvas dans la frame

    def install_in(self):
        self.game.install_in(self.canvas)  #appel pour debut de partie

    def start(self):
        self.install_in()  #appel afin de faire apparaitre le reste des objet du jeu
        self.root.bind("<Key>", self.game.defender.keypress)  #fonction pour appel depuis clavier
        self.root.mainloop()  #Apparition de la fenetre

Jeu = SpaceInvader()
Jeu.start()
