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
        self.y = None

    def install(self, canvas, x, y):  #on demande le canvas pour faire apparaitre le bullet, puis les coordonnees du defender pour que le bullet parte du bon endroit
        self.canvas = canvas
        self.y = y
        self.rect_id = self.canvas.create_oval(x, y, x+self.diametre, y+self.diametre, fill='white') #creation du bullet
        self.animation()  #appel de la fonction animation pour bouger la bullet
        

    def animation(self):
        self.canvas.move(self.rect_id, 0, -20) #deplace le bullet de 20 vers le haut
        self.y = self.y -20
        self.canvas.after(100, self.animation)  #reitère l'animation toute les 100ms


class Defender(object):
    def __init__(self):
        self.rect_id = None  #instance du defender
        self.square_width = 50  #taille du defender
        self.x = 400  #nos coordonnees initials du defender
        self.y = 550
        self.rafale = 0   #initialisation du nombre de bullet tirer

    def install(self, canvas):  #on demande le canvas afin de pouvoir faire apparaitre le defender dans la frame
        self.canvas = canvas
        self.rect_id = self.canvas.create_polygon(self.x, self.y, self.x-(self.square_width/2), self.y+self.square_width, self.x+(self.square_width/2), self.y+self.square_width, fill='red') #creation du defender




class Game(object):
    def __init__(self):
        self.defender = Defender()  #defender de la partie
        self.rafale = 0

    def install_in(self, canvas):  #on demande le canvas pour les autres classes
        self.canvas = canvas
        self.defender.install(canvas)  #creation du defender dans le canvas

    def keypress(self, event):

        self.defender.bullet = Bullet()  #creation d'une instance bullet lorsque l'on appuie sur espace pour tirer

        if event.keysym == 'Left':    #quand touche flèche gauche alors le defender se déplace à gauche
            self.canvas.move(self.defender.rect_id, -10, 0)  #deplace de 10 le defender vers la gauche
            print('gauche')  #afin de déboguer si nos fonctions marche
            self.defender.x = self.defender.x -10   #mise à jour des coordonnees en fonction du mouvement
        elif event.keysym == 'Right':   #quand touche flèche droite alors le defender se déplace à droite
            self.canvas.move(self.defender.rect_id, +10, 0)  #deplace de 10 le defender vers la droite
            print('droite')  #afin de déboguer si nos fonctions marche
            self.defender.x = self.defender.x +10  #mise à jour des coordonnees en fonction du mouvement
        elif (event.keysym == 'space' and self.rafale<8):
            self.defender.bullet.install(self.canvas, self.defender.x, self.defender.y)  #appel de la fonction de creation de la bullet
            self.rafale = self.rafale +1 #comptage du nombre de bullet tirer
            print('espace')  #afin de déboguer si nos fonctions marche

        if(self.defender.bullet.y == 0):
            self.rafale = self.rafale -1
       



class SpaceInvader(object):  #classe initiale avec creation de la frame 
    def __init__(self):  #Création de la Frame avec le Canvas
        self.root = tk.Tk()
        self.game = Game()  #instance pour appeler le jeu
        self.canvas_width = 800  #largeur de la frame
        self.canvas_height = 600  #hauteur de la frame
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)  #creation du canvas
        self.canvas.pack()  #fonction d'apparition du canvas dans la frame

    def install_in(self):
        self.game.install_in(self.canvas)  #appel pour debut de partie

    def start(self):
        self.install_in()  #appel afin de faire apparaitre le reste des objet du jeu
        self.root.bind("<Key>", self.game.keypress)  #fonction pour appel depuis clavier
        self.root.mainloop()  #Apparition de la fenetre

Jeu = SpaceInvader()
Jeu.start()
