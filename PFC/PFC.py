#!/usr/bin/env python3
#-*- coding:utf-8 -*-


# --- Importations --- #


from tkinter import *
import tkinter.messagebox

from PIL import Image, ImageTk

from random import choice, randint

import os
import sys


# --- Parametrage de la Fenetre --- #


fenetre = Tk()
fenetre.title("epee - bouclier - arc")
fenetre.configure(width=800, height=500)
fenetre.resizable(width=False, height=False)


# --- Variables et Listes --- #


choix = ["epee", "bouclier", "arc", "puit"]

choixordi = ''
choixjoueur = ''

score_user = 0
score_computer = 0

back = PhotoImage(file=os.path.join("PFC\PFC_Images", "pfcfond.png"), master=fenetre)
back_bis = PhotoImage(file=os.path.join("PFC\PFC_Images", "pfcfond (bis).png"), master=fenetre)


# --- Canvas --- #


canvas = Canvas(fenetre, width=800, height=500, bg="white")

canvas.pack()

canvas_image = canvas.create_image(400, 250, image=back)


# --- Rectangle --- #


fond_score = canvas.create_rectangle(693, 10, 793, 110, fill="white")


# --- Score --- #


score_canvas_display_main = canvas.create_text(745, 20, text='Score : ')
score_canvas_display_user_1 = canvas.create_text(735, 60, text='Joueur =')
score_canvas_display_user_2 = canvas.create_text(767, 60, text=score_user)
score_canvas_display_computer_1 = canvas.create_text(740, 90, text='Ordinateur = ')
score_canvas_display_computer_2 = canvas.create_text(780, 90, text=score_computer)


# --- Images --- #


epee_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "epee.png"), master=fenetre)
bouclier_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "bouclier.png"), master=fenetre)
arc_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "arc.png"), master=fenetre)
puit_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "puit.png"), master=fenetre)

continuer_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "continuer.png"), master=fenetre)

joueur_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "joueur.png"), master=fenetre)
ordi_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "ordi.png"), master=fenetre)

joueurgagne_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "victoire.png"), master=fenetre)
ordigagne_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "defaite.png"), master=fenetre)
egalite_s = PhotoImage(file=os.path.join("PFC\PFC_Images", "egalite.png"), master=fenetre)


# --- Redimensonnement --- #


laurier = Image.open(os.path.join("PFC\PFC_Images", "laurier.png"))
laurier_resized = ImageTk.PhotoImage(laurier.resize((350, 250)))

laurier_c = canvas.create_image(215, 250, state="hidden", image=laurier_resized)


# --- Log --- #

try:
    open("PFC\PFC_Log.dat", "r").read()
except:
    open("PFC\PFC_Log.dat", "w").write('')
finally:
    open("PFC\PFC_Log.dat", "r").close()


# --- Fonctions --- #


def Rejouer():

    global score_user, score_computer
    
    try:
        canvas.itemconfig(laurier_c, state="hidden")
        canvas.itemconfig(Bouton_Histoire_c, state="hidden")
    
    except:
        pass
    
    canvas.itemconfig(Bouton_Replay_c, state="hidden")
    canvas.itemconfig(fond_score, fill="white")

    score_user = 0
    score_computer = 0

    canvas.itemconfig(score_canvas_display_user_2, text=score_user)
    canvas.itemconfig(score_canvas_display_computer_2, text=score_computer)

    Continuer()


def Continuer():

    global choixordi, choixjoueur

    try:
        canvas.delete(result_image)
    except:
        pass

    canvas.itemconfig(Bouton_Continuer_c, state="hidden")

    canvas.itemconfig(Bouton_epee_c, state="normal")
    canvas.itemconfig(Bouton_bouclier_c, state="normal")
    canvas.itemconfig(Bouton_arc_c, state="normal")
    canvas.itemconfig(Bouton_Puit_c, state="normal")

    choixordi = ''
    choixjoueur = ''


def Verification():

    global score_user, score_computer
    global canvas_image, back_bis

    if score_user == 5 or score_computer == 5:

        canvas.itemconfig(canvas_image, image=back_bis)

        Bouton_Histoire = Button(fenetre, text='Poursuivre l\'Histoire', bg="grey", command=sys.exit)
        Bouton_Histoire_c = canvas.create_window(212, 400, state="normal", window=Bouton_Histoire)

        if score_user == 5:

            canvas.itemconfig(Bouton_epee_c, state="hidden")
            canvas.itemconfig(Bouton_bouclier_c, state="hidden")
            canvas.itemconfig(Bouton_arc_c, state="hidden")
            canvas.itemconfig(Bouton_Puit_c, state="hidden")
            canvas.itemconfig(Bouton_Continuer_c, state="hidden")
            canvas.itemconfig(fond_score, state="hidden")
            canvas.itemconfig(score_canvas_display_main, state="hidden")
            canvas.itemconfig(score_canvas_display_user_1, state="hidden")
            canvas.itemconfig(score_canvas_display_user_2, state="hidden")
            canvas.itemconfig(score_canvas_display_computer_1, state="hidden")
            canvas.itemconfig(score_canvas_display_computer_2, state="hidden")

            with open("PFC\PFC_Log.dat", "w") as f:
                f.write("0")
                f.close()

            text = "Felicitation, c'est une victoire !"

            canvas.itemconfig(laurier_c, state="normal")

        elif score_computer == 5:

            canvas.itemconfig(Bouton_epee_c, state="hidden")
            canvas.itemconfig(Bouton_bouclier_c, state="hidden")
            canvas.itemconfig(Bouton_arc_c, state="hidden")
            canvas.itemconfig(Bouton_Puit_c, state="hidden")
            canvas.itemconfig(Bouton_Continuer_c, state="hidden")

            with open("PFC\PFC_Log.dat", "w") as f:
                f.write("1")
                f.close()

            text = "Vous avez échoué !"

        result_text = canvas.create_text(400, 450, text=text)


def Afficher(x, y, winner):

    global result_image
    global score_user, score_computer
    global fond_score

    result_image = canvas.create_image(x, y, image=winner)

    canvas.itemconfig(score_canvas_display_user_2, text=score_user)
    canvas.itemconfig(score_canvas_display_computer_2, text=score_computer)

    if score_user > score_computer:

        canvas.itemconfig(fond_score, fill="green")

    elif score_user < score_computer:

        canvas.itemconfig(fond_score, fill="red")

    else:

        canvas.itemconfig(fond_score, fill="white")

    canvas.itemconfig(Bouton_Continuer_c, state="normal")

    Verification()


def Resultats():

    global choixjoueur, choixordi
    global score_user, score_computer

    canvas.itemconfig(Bouton_epee_c, state="hidden")
    canvas.itemconfig(Bouton_bouclier_c, state="hidden")
    canvas.itemconfig(Bouton_arc_c, state="hidden")
    canvas.itemconfig(Bouton_Puit_c, state="hidden")

    if choixjoueur == "epee" and choixordi == "bouclier":

        score_computer += 1
        Afficher(200, 250, ordigagne_s)

    elif choixjoueur == "epee" and choixordi == "arc":

        score_user += 1
        Afficher(200, 250, joueurgagne_s)

    elif choixjoueur == "epee" and choixordi == "puit":

        score_computer += 1
        Afficher(200, 250, ordigagne_s)

    elif choixjoueur == "bouclier" and choixordi == "epee":

        score_user += 1
        Afficher(200, 250, joueurgagne_s)

    elif choixjoueur == "bouclier" and choixordi == "arc":

        score_computer += 1
        Afficher(200, 250, ordigagne_s)

    elif choixjoueur == "bouclier" and choixordi == "puit":

        score_user += 1
        Afficher(200, 250, joueurgagne_s)

    elif choixjoueur == "arc" and choixordi == "bouclier":

        score_user += 1
        Afficher(200, 250, joueurgagne_s)

    elif choixjoueur == "arc" and choixordi == "epee":

        score_computer += 1
        Afficher(200, 250, ordigagne_s)

    elif choixjoueur == "arc" and choixordi == "puit":

        score_computer += 1
        Afficher(200, 250, ordigagne_s)

    elif choixjoueur == "puit" and choixordi == "bouclier":

        score_computer += 1
        Afficher(200, 250, ordigagne_s)

    elif choixjoueur == "puit" and choixordi == "epee":

        score_user += 1
        Afficher(200, 250, joueurgagne_s)

    elif choixjoueur == "puit" and choixordi == "arc":

        score_user += 1
        Afficher(200, 250, joueurgagne_s)

    else:
        Afficher(200, 250, egalite_s)  


def Choixepee():

    global choixjoueur, choixordi

    choixjoueur = "epee"
    choixordi = choice(choix)

    Resultats()


def Choixbouclier():

    global choixjoueur, choixordi

    choixjoueur = "puit"
    choixordi = choice(choix)

    Resultats()


def Choixarc():

    global choixjoueur, choixordi

    choixjoueur = "arc" 
    choixordi = choice(choix)

    Resultats()


def Choixpuit():

    global choixjoueur, choixordi

    choixjoueur = "puit"
    choixordi = choice(choix)

    Resultats()


def Regles():

    regles = ("Le jeu du épée - bouclier - arc oppose le joueur à un ordinateur."
      "\n\nLe but est, à partir de 4 choix : épée, bouclier, arc, puit; de gagner l'adversaire suivant "
      "des rapports de force prédéfinis. Ainsi, on a :"
      "\n\n- L'épée gagne face à l'arc. Elle le casse."
      "\n- L'arc l’emporte face au bouclier qu’il transperse."
      "\n- Le bouclier bat l'épée et le puit respectivement en parant et recouvrant ceux-ci."
      "\n- Le puit gagne l'épée et l'arc en les faisant chutter."
      "\n\nCette version du jeu va en 5 points.")

    tkinter.messagebox.showinfo("Règles du jeu", regles)


def Credits():

    credits = "Développeurs :\n\nNicolas Lacroix\nFlore Andrieu\nCorentin Montiel"

    tkinter.messagebox.showinfo("Crédits", credits)


# --- Boutons --- #


Bouton_epee = Button(fenetre, image=epee_s, bg="grey", command=Choixepee)
Bouton_bouclier = Button(fenetre, image=bouclier_s, bg="grey", command=Choixbouclier)
Bouton_arc = Button(fenetre, image=arc_s, bg="grey", command=Choixarc)
Bouton_Puit = Button(fenetre, image=puit_s, bg="grey", command=Choixpuit)

Bouton_Continuer = Button(fenetre, image=continuer_s, bg="grey", command=Continuer)
Bouton_Continuer_c = canvas.create_window(430, 250, state="hidden", window=Bouton_Continuer)

Bouton_epee_c = canvas.create_window(85, 100, window=Bouton_epee)
Bouton_bouclier_c = canvas.create_window(240, 100, window=Bouton_bouclier)
Bouton_arc_c = canvas.create_window(85, 255, window=Bouton_arc)
Bouton_Puit_c = canvas.create_window(240, 255, window=Bouton_Puit)


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

fenetre.mainloop()
