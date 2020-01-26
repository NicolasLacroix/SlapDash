#!/usr/bin/env python3
#-*- coding:utf-8 -*-


# --- Importations --- #


from tkinter import * 

from PIL import Image, ImageTk

from random import randint

import os
import time


# --- Fenetre --- #

fenetre = Tk()
fenetre.title('SlapDash')
fenetre.configure(width=800, height=500)
fenetre.resizable(width=False, height=False)


# --- Score --- #

score = 0
total = 3
text = str(score) + "/" + str(total)

label_frame = LabelFrame(fenetre, text="Nombre de fois touché par une flèche :", padx=100, pady=1)
label_frame.pack(fill="both", expand="yes", side=TOP)

score_zone = Label(label_frame, text=text)
score_zone.pack()


# --- Minuteur --- #

label_frame_time = LabelFrame(fenetre, text="Chronomètre :", padx=100, pady=1)
label_frame_time.pack(fill="both", side=TOP)

temps = 0.0
chrono = str(round(temps, 1)) + "/" + str(1000)
temps_zone = Label(label_frame_time, text=chrono)
temps_zone.pack()

# --- Images --- #

Fond = PhotoImage(file=os.path.join("Esquive\Fleches_Images", "Salle.png"), master=fenetre)
Fond_bis = PhotoImage(file=os.path.join("Esquive\Fleches_Images", "Salle (bis).png"), master=fenetre)


# --- Redimensionnement --- #

Slapdash = Image.open(os.path.join("Esquive\Fleches_Images", "Homme.png"))
Slapdash_r = ImageTk.PhotoImage(Slapdash.resize((200, 200)))

Fleche = Image.open(os.path.join("Esquive\Fleches_Images", "Fleche.png"))
Fleche_r = ImageTk.PhotoImage(Fleche.resize((75, 75)))


# --- Variables et Listes --- #

coord_x_homme = 125
coord_y_homme = 225

x_r = 800
y_r = randint(0, 500)

liste = []
liste_x_f = []
liste_y_f = []

speed = 500


# --- Canvas --- #

canvas = Canvas(fenetre, width=800, height=500)

back = canvas.create_image(400, 250, image=Fond)
personnage = canvas.create_image(coord_x_homme, coord_y_homme, image=Slapdash_r)

result_area = canvas.create_rectangle(100, 10, 700, 100, fill="grey", state="hidden")
result_text = canvas.create_text(745, 20, text="", state="hidden")


# --- Log --- #

try:
	open("Esquive\Esquive_Log.dat", "r").read()
except:
	open("Esquive\Esquive_Log.dat", "w").write('')
finally:
	open("Esquive\Esquive_Log.dat", "r").close()


# --- Fonctions --- #

def Victoire():

	global result_area, result_text
	global goto_animation, goto_creation, goto_chrono
	global back, Fond_bis

	canvas.delete("all")

	back = canvas.create_image(400, 250, image=Fond_bis)

	fenetre.after_cancel(goto_animation)
	fenetre.after_cancel(goto_creation)
	fenetre.after_cancel(goto_chrono)

	with open("Esquive\Esquive_Log.dat", "w") as f:
   		f.write("0")
   		f.close()

	result_text = canvas.create_text(400, 450, text="Veni, vidi, vici")

	Bouton_Histoire = Button(fenetre, text='Poursuivre l\'Histoire', bg="grey", command=sys.exit)
	Bouton_Histoire_c = canvas.create_window(400, 350, state="normal", window=Bouton_Histoire)


def Defaite():

	global result_area, result_text
	global goto_animation, goto_creation, goto_chrono
	global back, Fond_bis

	canvas.delete("all")

	back = canvas.create_image(400, 250, image=Fond_bis)

	fenetre.after_cancel(goto_animation)
	fenetre.after_cancel(goto_creation)
	fenetre.after_cancel(goto_chrono)

	with open("Esquive\Esquive_Log.dat", "w") as f:
   		f.write("1")
   		f.close()

	result_text = canvas.create_text(400, 450, text="C'est un échec !")

	Bouton_Histoire = Button(fenetre, text='Poursuivre l\'Histoire', bg="grey", command=sys.exit)
	Bouton_Histoire_c = canvas.create_window(400, 350, state="normal", window=Bouton_Histoire)


def Chronometre():

	global temps, chrono
	global goto_chrono
	
	temps += 0.1
	chrono = str(round(temps, 1)) + "/" + str(60)
	temps_zone.config(text=chrono)

	if temps == 1000:

		fenetre.after_cancel(goto_chrono)

		Victoire()

	goto_chrono = fenetre.after(50, Chronometre)


def Mouvement_Personnage(event):

	global coord_x_homme, coord_y_homme

	code = event.keycode

	if code == 38 and coord_y_homme != 0:
		coord_y_homme -= 25
	elif code == 40 and coord_y_homme != 425:
		coord_y_homme += 25

	canvas.coords(personnage, coord_x_homme, coord_y_homme)


def Animation_Fleches():

	global x_r, y_r
	global new_fleche
	global score, text
	global goto_animation

	for i in range(0, len(liste)):

		try:
		
			liste_x_f[i] -= 50

			canvas.coords(liste[i], liste_x_f[i], liste_y_f[i])

			position_fleche_i = canvas.coords(liste[i])

			if position_fleche_i[1] < 0:

				canvas.delete(liste[i])
				liste.delete(i)

			if (position_fleche_i[0] in range(coord_x_homme-25, coord_x_homme+25)
				and position_fleche_i[1] in range(coord_y_homme-40, coord_y_homme+50)):

				score += 1

				text = str(score) + "/" + str(total)
				score_zone.config(text=text)

				if score != 3:

					canvas.delete(liste[i])
					liste.delete(i)

				else:

					Defaite()

		except:
			pass

	goto_animation = fenetre.after(speed, Animation_Fleches)


def Creation_Fleches():

	global x_r, y_r
	global new_fleche, total
	global goto_creation
	global speed, temps

	text = str(score) + "/" + str(total)
	score_zone.config(text=text)

	y_r = randint(25, 450)

	new_fleche = canvas.create_image(x_r, y_r, image=Fleche_r)
	liste.append(new_fleche)
	liste_x_f.append(x_r)
	liste_y_f.append(y_r)

	if speed != 100:

		speed -= 5

	if speed == 495:

		Animation_Fleches()
		Chronometre()

	goto_creation = fenetre.after(speed+1, Creation_Fleches)


# --- Menu --- #

menubar = Menu(fenetre)

filemenu = Menu(menubar, tearoff=0, bg="white")

filemenu.add_command(label="Quitter", command=fenetre.quit)

menubar.add_cascade(label="Options", menu=filemenu)

fenetre.config(menu=menubar)


# --- Call Fonctions --- #

Creation_Fleches()


# --- Initialisation --- #

canvas.focus_set()

canvas.bind('<KeyPress>', Mouvement_Personnage)

# ---

canvas.pack()
fenetre.mainloop()
