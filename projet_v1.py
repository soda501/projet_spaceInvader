try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox


class Defender(object):
    def __init__(self):
        self.rect_id = None  #instance du defender
        self.square_width = 50  #taille du defender

    def install(self, canvas):  #on demande le canvas afin de pouvoir faire apparaitre le defender dans la frame
        x, y=375, 550  #coordonnees initials
        self.canvas = canvas
        self.rect_id = self.canvas.create_rectangle(x, y, x+self.square_width, y+self.square_width, fill='red') #creation du defender

    def keypress(self, event):
        
        if event.keysym == 'Left':    #quand touche flèche gauche alors le defender se déplace à gauche
            self.canvas.move(self.rect_id, -10, 0)  #deplace de 10 le defender vers la gauche
            print('gauche')  #afin de déboguer si nos fonctions marche
        elif event.keysym == 'Right':   #quand touche flèche droite alors le defender se déplace à droite
            self.canvas.move(self.rect_id, +10, 0)  #deplace de 10 le defender vers la droite
            print('droite')  #afin de déboguer si nos fonctions marche
        #elif event.keysym == 'space':
            #self.canvas.move(self.rect_id, 0, -10)
            #print('espace')



class Game(object):
    def __init__(self):
        self.defender = Defender()  #defender de la partie

    def install_in(self, canvas):  #on demande le canvas pour les autres classes
        self.defender.install(canvas)  #creation du defender dans le canvas



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
        self.root.bind("<Key>", self.game.defender.keypress)  #fonction pour appel depuis clavier
        self.root.mainloop()  #Apparition de la fenetre

Jeu = SpaceInvader()
Jeu.start()
        
