from tkinter import *
import random

table = {} # pour garder les valeurs des boutons( X ou O) 

def refraichir_table(clear=False):
    for row in range(3):
        for col in range(3):
            if clear: 
                table[(row,col)]["value"] = ""
            table[(row,col)]["button"]["text"] = table[(row,col)]["value"]

def bloquer_saisie(state):
    for row in range(3):
        for col in range(3):
            if state :
                table[(row,col)]["button"]["state"] = "normal"
            else :
                "disabled"

def nouvelle_partie():
    refraichir_table(clear=True)
    bloquer_saisie(True)
    text["text"] = "Ton tour"

def choix_joueur(row, col, who):  # returns True if game is finished
    table[(row,col)]["value"] = who
    refraichir_table()
    if test_de_fin(who):
        text["text"] = f"You {'Win' if who == 'X' else 'Loose'} !"
        bloquer_saisie(False)
        return True
    if all(table[(row,col)]["value"] for row in range(3) for col in range(3)):
        text["text"] = "Draw"
        bloquer_saisie(False)
        return True
    return False

def choix_ai():
    positions = [(row,col) for row in range(3) for col in range(3) if not table[(row,col)]["value"]]
    for pos in positions:
        for who in "XO":
            table[pos]["value"] = who
            win = test_de_fin(who)
            table[pos]["value"] = ""
            if win:
                return pos
    return random.choice(positions)

def test_de_fin(who):
    win  = all(table[(i,  i)]["value"] == who for i in range(3))
    win |= all(table[(i,2-i)]["value"] == who for i in range(3))
    for i in range(3):
        win |= all(table[(i,col)]["value"] == who for col in range(3))
        win |= all(table[(row,i)]["value"] == who for row in range(3))
    return win

def jeux(row, col):
    if table[(row,col)]["value"]:  # already occupied
        return
    if choix_joueur(row, col, "X"):
        return

    choix_joueur(*choix_ai(), "O")

def changer_taille_fenetre(event):
    fenetrep_principale["width"] = fenetrep_principale.winfo_height()


window = Tk()
window.title("Tic-Tac-Toe")
window.config(bg='#60D47C')
window.iconbitmap("logojeux.ico")

heading_frame = Frame(window, bg='#60D47C', highlightthickness=3, highlightbackground='silver', height=100)
heading_frame.pack(fill=X)
text = Label(heading_frame, text="ton tour !", bg='#60D47C', fg='white', font='Baskerville 16')
text.pack(anchor="center")

bottom_frame = Frame(window, bg='#60D47C')
bottom_frame.pack(fill=X, side=BOTTOM)
Button(bottom_frame, text='NOUVELLE PARTIE', bg='#299B45', fg='#60D47C', command=nouvelle_partie, font='Elephant 12').pack(side=LEFT)
Button(bottom_frame, text='SORTIR', bg='red', fg='#60D47C', command=window.destroy, font='Elephant 12').pack(side=RIGHT)

fenetrep_principale = Frame(window, bg='#60D47C', width=420, height=420)
fenetrep_principale.pack(side=RIGHT, fill=Y)
fenetrep_principale.columnconfigure(tuple(range(3)), minsize=140, weight=1, uniform="tableau")
fenetrep_principale.rowconfigure(tuple(range(3)), minsize=140, weight=1, uniform="tableau")
fenetrep_principale.bind("<Configure>", changer_taille_fenetre)
fenetrep_principale.grid_propagate(False)

for row in range(3):
    for col in range(3):
        table[(row,col)] = {"value":"", "button":Button(fenetrep_principale, border=0, font='CASTELLAR 48 bold', command=lambda r=row, c=col: jeux(r, c))}
        table[(row,col)]["button"].grid(row=row, column=col, sticky="news", padx=5, pady=5)

window.mainloop()


