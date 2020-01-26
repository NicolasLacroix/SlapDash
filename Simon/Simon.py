#!/usr/bin/env python3
#-*- coding:utf-8 -*-


# --- Importations --- #


from tkinter import *
import tkinter.messagebox

import pygame

from random import choice

import os


# --- Parametrage de la Fenetre --- #


fenetre = Tk()
fenetre.title('jeu du Simon')
fenetre.configure(width=800, height=500)
fenetre.resizable(width=False, height=False)


# --- Variables et Listes --- #


possibilites = ['Rouge', 'Vert', 'Bleu', 'Jaune']
computer = []
user = []

count = 0
turn = 0
state = True
result_state = None


# --- Canvas --- #

back = PhotoImage(file=os.path.join("Simon\Simon_Images", "simonfond.png"), master=fenetre)
back_bis = PhotoImage(file=os.path.join("Simon\Simon_Images", "simonfond (bis).png"), master=fenetre)

canvas = Canvas(fenetre, width=800, height=500, cursor="hand2", relief="flat", bg='grey')
canvas.grid(row=1, column=1, padx=10, pady=10, rowspan=2)
canvas.grid_propagate(1)

canvas.pack()

canvas_image = canvas.create_image(400, 250, image=back)


# --- Rectangle --- #


fond_noir = canvas.create_rectangle(25, 25, 340, 340, fill="Black")


# --- Images --- #


image_rouge = PhotoImage(file=os.path.join("Simon\Simon_Images", "Rouge(main).png"))
rouge = canvas.create_image(30, 30, anchor=NW, image=image_rouge)

image_vert = PhotoImage(file=os.path.join("Simon\Simon_Images", "Vert(potion).png"))
vert = canvas.create_image(185, 30, anchor=NW, image=image_vert)

image_bleu = PhotoImage(file=os.path.join("Simon\Simon_Images", "Bleu(pied).png"))
bleu = canvas.create_image(185, 185, anchor=NW, image=image_bleu)

image_jaune = PhotoImage(file=os.path.join("Simon\Simon_Images", "Jaune(bouclier).png"))
jaune = canvas.create_image(30, 185, anchor=NW, image=image_jaune)


# --- Rectangle et Texte --- #


text = ""

result_text = canvas.create_text(400, 450, text=text, state="hidden")


# --- Sons --- #


pygame.mixer.init()

son_rouge = pygame.mixer.Sound(os.path.join("Simon\Simon_Sons", "son_poing.ogg"))
son_rouge.set_volume(0.1)

son_vert = pygame.mixer.Sound(os.path.join("Simon\Simon_Sons", "son_potion.ogg"))
son_vert.set_volume(0.1)

son_bleu = pygame.mixer.Sound(os.path.join("Simon\Simon_Sons", "son_pied.ogg"))
son_bleu.set_volume(0.1)

son_jaune = pygame.mixer.Sound(os.path.join("Simon\Simon_Sons", "son_bouclier.ogg"))
son_jaune.set_volume(0.1)


# --- Log --- #

try:
	open("Simon\Simon_Log.dat", "r").read()
except:
	open("Simon\Simon_Log.dat", "w").write('')
finally:
	open("Simon\Simon_Log.dat", "r").close()


# --- Fonctions --- #


def Result():

	global computer, user
	global result_text, canvas_image
	global BC_w, BQ_w , BCH_w
	global result_state, back_bis

	canvas.itemconfig(canvas_image, image=back_bis)


	if computer == user:

		text = 'Victoire'
		canvas.itemconfig(BC_w, state="normal")
		result_state = True

		canvas.itemconfig(result_text, text=text, state="normal")

		canvas.itemconfig(BQ_w, state="normal")

	else:

		text = 'Défaite'
		result_state = False
		
		with open("Simon\Simon_Log.dat", "w") as f:
   			f.write("1")
   			f.close()
		
		canvas.itemconfig(result_text, text=text, state="normal")

		canvas.itemconfig(BCH_w, state="normal")


def User_Event(event):

	global computer, user

	if event.x in range(30, 180) and event.y in range(30, 180) and len(computer) != len(user):

		son_rouge.play()
		
		user.append('Rouge')


	elif event.x in range(185, 335) and event.y in range(30, 180) and len(computer) != len(user):

		son_vert.play()
		
		user.append('Vert')

	
	elif event.x in range(185, 335) and event.y in range(185, 335) and len(computer) != len(user):

		son_bleu.play()
		
		user.append('Bleu')


	elif event.x in range(30, 180) and event.y in range(185, 335) and len(computer) != len(user):

		son_jaune.play()
		
		user.append('Jaune')


	if len(computer) == len(user):

		Result()


def Cases():

	global canvas
	global rouge, vert, bleu, jaune

	canvas.bind("<Button-1>", User_Event)


def Motif():

	global possibilites, computer
	global rouge, vert, bleu, jaune
	global defined_count, count, timer

	canvas.itemconfig(rouge, state="normal")
	canvas.itemconfig(vert, state="normal")
	canvas.itemconfig(bleu, state="normal")
	canvas.itemconfig(jaune, state="normal")

	if count != defined_count:

		couleur_motif = choice(possibilites)

		computer.append(couleur_motif)

		if couleur_motif == 'Rouge':

			canvas.itemconfig(vert, state="hidden")
			canvas.itemconfig(bleu, state="hidden")
			canvas.itemconfig(jaune, state="hidden")

			son_rouge.play()

		elif couleur_motif == 'Vert':

			canvas.itemconfig(rouge, state="hidden")
			canvas.itemconfig(bleu, state="hidden")
			canvas.itemconfig(jaune, state="hidden")

			son_vert.play()

		elif couleur_motif == 'Bleu':

			canvas.itemconfig(rouge, state="hidden")
			canvas.itemconfig(vert, state="hidden")
			canvas.itemconfig(jaune, state="hidden")

			son_bleu.play()


		elif couleur_motif == 'Jaune':

			canvas.itemconfig(rouge, state="hidden")
			canvas.itemconfig(vert, state="hidden")
			canvas.itemconfig(bleu, state="hidden")

			son_jaune.play()

		timer = canvas.after(1000, Motif)

		count += 1

	else:

		canvas.after_cancel(timer)

		count = 0

		Cases()


def Parameters():

	global turn, defined_count
	global state, result_state
	global BC_w, BQ_w, BCH_w
	global text_result_location, result_text
	global canvas_image, back_bis

	try:
		canvas.itemconfig(text_result_location, state="hidden")
		canvas.itemconfig(result_text, state="hidden")
		
	except:
		pass

	canvas.itemconfig(result_text, text="", state="normal")

	if result_state is True:

		canvas.itemconfig(BC_w, state="hidden")

		canvas.itemconfig(BQ_w, state="hidden")

	elif result_state is False:

		canvas.itemconfig(BQ_w, state="hidden")

	if state is True:

		turn += 1

		if turn == 1:

			defined_count = 4
			Motif()

		elif turn == 2:

			defined_count = 6
			Motif()

		elif turn == 3:

			defined_count = 8
			Motif()

		elif turn == 4:

			canvas.itemconfig(canvas_image, image=back_bis)
			
			with open("Simon\Simon_Log.dat", "w") as f:
   				f.write("0")
   				f.close()

			final = 'Bravo, vous avez effectués tous les niveaux de ce mini-jeu !\nVous pouvez poursuivre votre quete !'

			canvas.itemconfig(result_text, text=final, state="normal")

			canvas.itemconfig(BCH_w, state="normal")

	else:

		computer = []
		user = []

		count = 0
		turn = 0
		state = True

		Parameters()


def Regles():

	regles = ("Le jeu du simon affiche aléatoirement quatre images, produisant simultanément les sons respectifs de ces images."
	  "\n\nC'est ensuite le tour du joueur qui doit appuyer sur ces images dans le même ordre."
	  "\n\nSi le joueur reproduit correctement cette suite, alors le joueur passe à l'étape suivante."
	  "\n\nDans le cas contraire, le joueur recommence le jeu depuis le début."
	  "\n\nIl y a 3 étapes correspondant respectivement à 4, 6 puis 8 images à retrouver dans le bon ordre.")

	tkinter.messagebox.showinfo("Règles du jeu", regles)


def Credits():

	credits_dev = "Développeurs :\n\nNicolas Lacroix\nFlore Andrieu\nCorentin Montiel\n\n"

	credits_son = "Son : \n\nhttps://lasonotheque.org/"

	credits = credits_dev + credits_son

	tkinter.messagebox.showinfo("Crédits", credits)


# ---  Boutons --- #


Bouton_Continuer = Button(fenetre, width=20, text="Continuer", background="#9D9696", cursor="hand1", command=Parameters)
BC_w = canvas.create_window(685, 300, state="hidden", window=Bouton_Continuer)

Bouton_Quitter = Button(fenetre, width=20, text="Quitter", background="#9D9696", cursor="pirate", command=fenetre.quit)
BQ_w = canvas.create_window(685, 355, state="hidden", window=Bouton_Quitter)

Bouton_Continuer_Histoire = Button(fenetre, width=20, text="Continuer l'histoire", background="#9D9696", cursor="hand1", command=fenetre.quit)
BCH_w = canvas.create_window(685, 325, state="hidden", window=Bouton_Continuer_Histoire)

# --- Menu --- #


menubar = Menu(fenetre)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quitter", command=fenetre.quit)

menubar.add_cascade(label="Options", menu=filemenu)

filemenu_2 = Menu(menubar, tearoff=0)
filemenu_2.add_command(label="Règles du jeu", command=Regles)
filemenu_2.add_separator()
filemenu_2.add_command(label="Crédits", command=Credits)

menubar.add_cascade(label="A propos", menu=filemenu_2)

fenetre.config(menu=menubar)


# ---


Parameters()

fenetre.mainloop()
