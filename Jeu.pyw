#!/usr/bin/env python3
#-*- coding:utf-8 -*-


# --- Importations --- #

from tkinter import *
from tkinter.messagebox import *
from tkinter import font

import pygame 

from PIL import Image, ImageTk

from random import randint, choice

import os
import os.path

from lxml import etree

import time


# --- Fenetre --- #

fenetre = Tk()
fenetre.title('SlapDash')
fenetre.configure(width=800, height=500)
fenetre.resizable(width=False, height=False)


# --- Fonds --- #

backforet = PhotoImage(file=os.path.join("Fonds", "Transition_foret1.png"), master=fenetre) #--- A enlever
parameters_back = PhotoImage(file=os.path.join("Menu_Images", "Parameters.png"), master=fenetre)


# --- Canvas --- #

canvas = Canvas(fenetre, width=800, height=500, background='white')
canvas.pack()


# --- Variables --- #

text2print = ""
i, b, rank = 0, 0, 0

sound_volume = 0.1
new_volume = None

story_state = 0
grotte_choice = ""


# --- Images --- #

Image_Jouer = PhotoImage(file=os.path.join("Menu_Images", "Bouton Jouer.png"), master=fenetre)
Image_Parametres = PhotoImage(file=os.path.join("Menu_Images", "Bouton paramètres.png"), master=fenetre)
Image_Quitter = PhotoImage(file=os.path.join("Menu_Images", "Bouton quitter.png"), master=fenetre)
Image_BackMenu = PhotoImage(file=os.path.join("Menu_Images", "Back2Menu.png"), master=fenetre)


# --- Redimensonnement --- #

exit = Image.open(os.path.join("Menu_Images", "croix_quitter.png"))
exit_resized = ImageTk.PhotoImage(exit.resize((10, 10)))

image_son = Image.open(os.path.join("Menu_Images", "son.png"))
image_son_resized = ImageTk.PhotoImage(image_son.resize((30, 30)))

image_mute = Image.open(os.path.join("Menu_Images", "mute.png"))
image_mute_resized = ImageTk.PhotoImage(image_mute.resize((30, 30)))

image_replay = Image.open(os.path.join("Menu_Images", "Replay.png"))
image_replay_resized = ImageTk.PhotoImage(image_replay.resize((75, 75)))


# --- Sons --- #

list_musics = ["Medieval_Music.ogg", "Medieval_Music_2.ogg"]

actual_music = choice(list_musics)

pygame.mixer.init()

son_principal = pygame.mixer.Sound(os.path.join("Menu_Sons", actual_music))
son_principal.set_volume(sound_volume)

son_principal.play()


# --- Police --- #

police = font.Font(fenetre, size=12, family='Gabriola')
police_bis = font.Font(fenetre, size=20, family='Gabriola')


# --- Fonctions --- #


def Creation_Menu():

	global back, canvas_back
	global text_histoire
	global Canvas_Bouton1, Canvas_Bouton2, Canvas_Bouton3
	global rbc1, rbc2, labeltext
	global police

	try:
		canvas.itemconfig(rbc1, state="hidden")
		canvas.itemconfig(rbc2, state="hidden")
		canvas.itemconfig(labeltext, state="hidden")
	except:
		pass

	canvas.itemconfig(Canvas_Bouton_Replay, state="hidden")
	canvas.itemconfig(Canvas_Bouton_Back, state="hidden")

	back = PhotoImage(file=os.path.join("Fonds", "Menu.png"), master=fenetre)
	canvas_back = canvas.create_image(400, 250, image=back)

	text_histoire = canvas.create_text(400, 450, font=police, text="")

	Bouton1 = Button(fenetre, image=Image_Jouer, cursor='hand1', width=300, height=80, bd=2, command=Jouer)
	Canvas_Bouton1 = canvas.create_window(200, 150, window=Bouton1)

	Bouton2 = Button(fenetre, image=Image_Parametres, cursor='hand1', width=300, height=80, bd=2, command=Settings)
	Canvas_Bouton2 = canvas.create_window(200, 250, window=Bouton2)

	Bouton3 = Button(fenetre, image=Image_Quitter, cursor='hand1', width=300, height=80, bd=2, command=Exit_Check)
	Canvas_Bouton3 = canvas.create_window(200, 350, window=Bouton3)


def Background(new_back):

	global back

	back = PhotoImage(file=os.path.join("Fonds", new_back), master=fenetre)
	canvas.itemconfig(canvas_back, image=back)


def Way_Choice_Performed():

	global grotte_choice
	global xml_part_location, xml_bg_location
	global xml_text_location, xml_game_location
	global count_xml, xml_part_basis, xml_search

	canvas.unbind("<Button-1>")

	if grotte_choice == "LEFT":

		if first_victory is True:

			count_xml = 1 # --- A voir
			xml_part_basis = 1
			xml_search = "/Main/PartA/Gauche/part"

		else:

			count_xml = 1
			xml_part_basis = 1
			xml_search = "/Main/PartB/Gauche/part"

	else:

		if first_victory is True:

			count_xml = 1
			xml_part_basis = 2
			xml_search = "/Main/PartA/Droite/part" 

		else:

			count_xml = 1
			xml_part_basis = 2
			xml_search = "/Main/PartB/Droite/part"

	Xml_Processing() # A completer/Ameliorer


def Way_Choice_Proposal(event):

	global grotte_choice

	print("Way_Choice_Proposal")

	if event.x in range(50, 350) and event.y in range(50, 450):

		grotte_choice = "LEFT"

		Way_Choice_Performed()

	elif event.x in range(450, 750) and event.y in range(50, 450):

		grotte_choice = "RIGHT"

		Way_Choice_Performed()


def Text_Animation(xml_text):

	global text2print
	global b, rank
	global xml_search

	len_text2print = 0

	for char in xml_text:
		rank += 1
		c = randint(10000, 100000) 

		while b != c:
			b += 1

		len_text2print += 1
		text2print += char

		if len_text2print >= 130 and char == " ":
			text2print += "\n"
			len_text2print = 0

		canvas.itemconfig(text_histoire, text=text2print)

		canvas.update()

		if char == "," or char == "!":
			time.sleep(0.5)

		b, rank = 0, 0


def Cls():

	global texts, xml_text, text2print
	global i

	blank = ""

	for char in xml_text:
		blank += " "

	canvas.itemconfig(text_histoire, text=blank)

	text2print = ""


def Log_Processing():

	global count_xml, xml_part_basis, xml_search
	global xml_part_location, xml_bg_location
	global xml_text_location, xml_game_location
	global xml_game_text, story_state
	global recent_victory, first_victory
	global log_content, grotte_choice, t

	print("Log_Processing")

	log_file = t + "\\" + t + "_Log.dat"

	print(log_file)

	with open(log_file, "r") as f:

		log_content = f.read()

	if story_state == 1:

		if log_content == "0":

			first_victory = True

			count_xml = 1
			xml_part_basis = 3
			xml_search = "/Main/PartA/part" 

		elif log_content == "1":

			first_victory = False

			count_xml = 1
			xml_part_basis = 3
			xml_search = "/Main/PartB/part" 

		else:

			fenetre.quit()

	elif story_state == 3:

		if log_content == "0":

			if first_victory is True:

				if grotte_choice == "LEFT":

					recent_victory = True

					count_xml = 1
					xml_part_basis = 1
					xml_search = "/Main/PartA/Gauche/PartA1/part"

				else:

					recent_victory = True

					count_xml = 1
					xml_part_basis = 1
					xml_search = "/Main/PartA/Droite/PartA11/part"

			else:

				if grotte_choice == "LEFT":

					recent_victory = True

					count_xml = 1
					xml_part_basis = 1
					xml_search = "/Main/PartB/Gauche/PartB1/part"

				else:

					recent_victory = True

					count_xml = 1
					xml_part_basis = 1
					xml_search = "/Main/PartB/Droite/PartB11/part" # --- ATTENTION B1

		elif log_content == "1":

			if first_victory is True:

				if grotte_choice == "LEFT":

					recent_victory = True

					count_xml = 1
					xml_part_basis = 2
					xml_search = "/Main/PartA/Gauche/PartA2/part"

				else:

					recent_victory = True

					count_xml = 1
					xml_part_basis = 1
					xml_search = "/Main/PartA/Droite/PartA21/part"

			else:

				if grotte_choice == "LEFT":

					recent_victory = True

					count_xml = 1
					xml_part_basis = 2
					xml_search = "/Main/PartB/Gauche/PartB2/part"

				else:

					recent_victory = True

					count_xml = 1
					xml_part_basis = 1
					xml_search = "/Main/PartB/Droite/PartB21/part"

		else:

			fenetre.quit()

	elif story_state == 4:

		if log_content == "0":

			if grotte_choice == "LEFT":

				if first_victory is True:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Gauche/PartA1/PartA11/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Gauche/PartA2/PartA21/part"

				else:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Gauche/PartB1/PartB11/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Gauche/PartB2/PartB21/part"

			else:

				if first_victory is True:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Droite/PartA1/PartA11/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Droite/PartA2/PartA12/part"

				else:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Droite/PartB1/PartB11/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Droite/PartB2/PartB21/part"

		elif log_content == "1":

			if grotte_choice == "LEFT":

				if first_victory is True:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Gauche/PartA1/PartA12/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Gauche/PartA2/PartA22/part"

				else:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Gauche/PartB1/PartB12/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Gauche/PartB2/PartB22/part"

			else:

				if first_victory is True:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Droite/PartA1/PartA11/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartA/Droite/PartA2/PartA12/part"

				else:

					if recent_victory is True:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Droite/PartB1/PartB11/part"

					else:

						count_xml = 1
						xml_part_basis = 1
						xml_search = "/Main/PartB/Droite/PartB2/PartB12/part"

		else:

			fenetre.quit()

	print("count_xml", count_xml, "basis", xml_part_basis, "search", xml_search)


def Xml_Processing():

	global count_xml, xml_part_basis, xml_search
	global xml_game_text, xml_text
	global story_state, t

	print("Xml_Processing") # ---
	print("count_xml", count_xml, "basis", xml_part_basis, "search", xml_search)

	story_state += 1

	tree = etree.parse("Script (bis).xml")

	for count_xml in range(xml_part_basis+1):

		print("while")

		xml_part_location = xml_search + str(count_xml)
		xml_bg_location = xml_part_location + "/background"
		xml_text_location = xml_part_location + "/text"
		xml_game_location = xml_part_location + "/game"

		for bg in tree.xpath(xml_bg_location):

			for texte in tree.xpath(xml_text_location):

				Background(bg.text + ".png")

				xml_text = texte.text

				Text_Animation(xml_text)

				time.sleep(len(xml_text)/50)

				Cls()

			for game in tree.xpath(xml_game_location):

				if game.text != "None" and game.text != "Choice":

					xml_game_text = game.text
					print(xml_game_text) #---

					t = ""

					for char in xml_game_text:
						if char != "\\":
							t += char
						else:
							break

					os_game = "python " + xml_game_text + " i"

					os.system(os_game + "1")

					Log_Processing()

					count_xml += 1

					Xml_Processing()

				elif game.text == "Choice":

					print("bind")

					canvas.bind("<Button-1>", Way_Choice_Proposal)

		count_xml += 1

	if len(xml_search) == 38:

		canvas.itemconfig(Canvas_Bouton_Replay, state="normal")


def Jouer():

	global xml_search, xml_part_basis, count_xml
	global story_state

	canvas.itemconfig(Canvas_Bouton1, state="hidden")
	canvas.itemconfig(Canvas_Bouton2, state="hidden")
	canvas.itemconfig(Canvas_Bouton3, state="hidden")

	try:
		canvas.itemconfig(tocome_area, state="hidden")
		canvas.itemconfig(tocome_text, state="hidden")
		canvas.itemconfig(Canvas_Bouton_Back, state="hidden")
	except:
		pass

	filemenu.delete(0)

	Background("Transition_foret1.png")

	count_xml = 1
	xml_part_basis = 3
	xml_search = "/Main" + "/part"
	Xml_Processing()


def Change_Musique():

	global son_principal, var_bis

	new_music = var_bis.get()

	if new_music != "":

		son_principal.stop()
		son_principal = pygame.mixer.Sound(os.path.join("Menu_Sons", new_music))

		son_principal.play()


def Settings():

	global parameters_back, var_bis, actual_music
	global rbc1, rbc2, labeltext, police_bis
	#global tocome_area, tocome_text

	canvas.itemconfig(Canvas_Bouton1, state="hidden")
	canvas.itemconfig(Canvas_Bouton2, state="hidden")
	canvas.itemconfig(Canvas_Bouton3, state="hidden")

	canvas.itemconfig(canvas_back, image=parameters_back)
	canvas.itemconfig(Canvas_Bouton_Back, state="normal")
	
	label = Label(fenetre, text="Choix de la musique", font=police_bis)
	labeltext = canvas.create_window(525, 200, window=label, state="normal")

	var_bis = StringVar() 
	rbouton1 = Radiobutton(fenetre, text="Musique 1", variable=var_bis, value="Medieval_Music.ogg", 
		width=50, height=3, indicatoron=0, command=Change_Musique)
	rbouton2 = Radiobutton(fenetre, text="Musique 2", variable=var_bis, value="Medieval_Music_2.ogg", 
		width=50, height=3, indicatoron=0, command=Change_Musique)

	rbc1 = canvas.create_window(525, 320, window=rbouton1)
	rbc2 = canvas.create_window(525, 375, window=rbouton2)


def Exit_Check():

	showinfo("Attention", "Vous êtes sur le point de fermer le jeu.")

	if askyesno('Fermer la fenêtre ?', 'Êtes-vous sûr de vouloir quitter ?'):
		
		fenetre.quit()
	else:
		pass

 
def Sound_Modification(var):

	global new_volume

	new_volume = int(var)

	son_principal.set_volume(new_volume/100)

	if son_principal.get_volume() == 0:

		Bouton_Son.configure(image=image_mute_resized)

	else:

		Bouton_Son.configure(image=image_son_resized)


def Open_Scale():

	canvas.itemconfig(Canvas_Bouton_Son, state="hidden")
	canvas.itemconfig(Canvas_Scale_Son, state="normal")
	canvas.itemconfig(Canvas_Bouton_Quitter_Son, state="normal")


def Close_Scale():

	canvas.itemconfig(Canvas_Bouton_Quitter_Son, state="hidden")
	canvas.itemconfig(Canvas_Scale_Son, state="hidden")
	canvas.itemconfig(Canvas_Bouton_Son, state="normal")


def Mute(event):

	global var

	if son_principal.get_volume() != 0:

		son_principal.set_volume(0.0)

		Bouton_Son.configure(image=image_mute_resized)

	else:

		Bouton_Son.configure(image=image_son_resized)

		Sound_Modification(scale_son.get())


def Credits():

	dev_crdt = "Développeurs :\n\nNicolas Lacroix\nFlore Andrieu\nCorentin Montiel"

	music_crdt = "Musiques (YouTube) : \n\nDerek & Brandon Fiechter\nMcKlingonsown"

	credits = dev_crdt + "\n\n\n" + music_crdt

	showinfo("Crédits", credits)


def Synopsis():

	syn_p1 = "Tout va pour le mieux dans le monde de spaldash, jusqu'à ce qu'un jour, "
	syn_p2 = "le méchant Boss Final vole l'épée légendaire !\n\nLe Héros accompagné de son ami "
	syn_p3 = "le Lutin et du Roi vont devoir surmonter de nombreux obstacles afin de la récupérer "
	syn_p4 = "des griffes du voleur et accomplir leur destinée."

	synopsis = syn_p1 + syn_p2 + syn_p3 + syn_p4

	showinfo("Synopsis", synopsis)


# --- Scale --- #

scale_son = Scale(fenetre, from_=100, to=0, command=Sound_Modification)
scale_son.set(son_principal.get_volume()*100)

Canvas_Scale_Son = canvas.create_window(775, 445, state="hidden", window=scale_son)


# --- Boutons --- #

Bouton_Son = Button(fenetre, image=image_son_resized, bg="grey", cursor='hand1', bd=2, command=Open_Scale)
Canvas_Bouton_Son = canvas.create_window(775, 475, window=Bouton_Son)

Bouton_Quitter_Son = Button(fenetre, image=exit_resized, bg="grey", cursor='hand1', bd=2, command=Close_Scale)
Canvas_Bouton_Quitter_Son = canvas.create_window(762, 402, state="hidden", window=Bouton_Quitter_Son)

Bouton_Replay = Button(fenetre, image=image_replay_resized, cursor='hand1', bd=2, command=Creation_Menu)
Canvas_Bouton_Replay = canvas.create_window(400, 400, state="hidden", window=Bouton_Replay)

Bouton_Back = Button(fenetre, image=Image_BackMenu, cursor='hand1', bd=2, command=Creation_Menu)
Canvas_Bouton_Back = canvas.create_window(50, 450, state="hidden", window=Bouton_Back)


# --- Menu --- #

menubar = Menu(fenetre)

filemenu = Menu(menubar, tearoff=0, font=police)
filemenu.add_command(label="Jouer", command=Jouer)
menubar.add_cascade(label="Options", menu=filemenu)
filemenu.add_separator()
filemenu.add_command(label="Quitter", command=Exit_Check)

filemenu_2 = Menu(menubar, tearoff=0, font=police)
filemenu_2.add_command(label="Synopsis", command=Synopsis)
menubar.add_cascade(label="A propos", menu=filemenu_2)
filemenu_2.add_separator()
filemenu_2.add_command(label="Crédits", command=Credits)

fenetre.config(menu=menubar)

canvas.bind("<Button-3>", Mute) # --- A modifier


# ---


Creation_Menu()
fenetre.mainloop()
