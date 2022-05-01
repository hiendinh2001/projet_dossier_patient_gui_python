# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:34:56 2022

@author: hien2
"""

import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QMainWindow, QWidget, QLabel, QTextEdit, QRadioButton,
                             QFormLayout, QGridLayout, QToolTip, QMessageBox)
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from paramiko import client

hote_path = ('patients_hote.csv') #le fichier .csv de la machine hote pour stocker les informations saisies
vm_path = ('patients_vm.csv') #vm  #le fichier.csv de la machine virtuelle pour stocker les informations saisies

class MVCView(QWidget): #La classe « MVCView » qui hérite de QWidget et représente notre fenêtre.

    def __init__(self, ctrl): #La méthode s'appelle le « constructeur » de la classe pour initialiser certaines variables (ctrl)
        super().__init__() #La constructeur de la classe « QWidget »

        self.myCtrl = ctrl #C’est l’objet type Controller passé en argument, la liaison entre View (client) et Controller (serveur)

        #logo
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('sante_logo.png')) #ajoute l'image logo
        self.logo.setStyleSheet("margin: 0px") #style de logo
        self.logo.setAlignment(QtCore.Qt.AlignCenter) #met le logo au milieu de la fenetre
        
        #nom de plateforme
        self.nom_pe = QLabel("ParaSanté")
        self.nom_pe.setStyleSheet("font-family: 'Roboto', sans-serif; font-size: 20pt; font-weight: bold; margin: 0px 50px")
        self.nom_pe.setAlignment(QtCore.Qt.AlignCenter)
        
        #Message de bienvenue
        self.mess = QLabel("Bienvenue à notre application!")
        self.mess.setStyleSheet("font-family: 'Roboto', sans-serif; font-size: 12pt; margin: 0px 50px")
        self.mess.setAlignment(QtCore.Qt.AlignCenter)
        
        #bouton "Créer un dossier"
        self.btn_creer = QPushButton('Créer un dossier')
        self.btn_creer.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 0px 80px 5px")

        #bouton "Importer un dossier"
        self.btn_import = QPushButton('Importer un dossier')
        self.btn_import.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 0px 80px 20px")


        self.init_ui() #La fonction pour organiser notre layout

        self.show() #L’affichage des widgets organisés en init_ui() (Classe QWidget)

    def init_ui(self):
        v_box = QVBoxLayout() #La création du layout principal de la fenêtre (vertical)
        v_box.addWidget(self.logo) #logo
        v_box.addWidget(self.nom_pe) #nom de platforme
        v_box.addWidget(self.mess) #Message de bienvenue
        v_box.addWidget(self.btn_creer) #bouton "Créer un dossier"
        v_box.addWidget(self.btn_import) #bouton "Importer un dossier"

        self.setLayout(v_box) #Le placement du layout dans la fenêtre (Classe QWidget)
        self.setWindowTitle("Fenêtre d'accueil") #Le titre de la fenêtre, affiché en haut
        self.setFixedSize(335, 380) #fixe la taille de la fenetre
        self.setStyleSheet("background-color: #f0ecec; border-radius: 5px") #style de la fenetre
        self.setWindowIcon(QIcon('sante_logo.png'))  #Le logo de la fenêtre, affiché en haut

        self.btn_creer.clicked.connect(self.btn_creer_click) #La fonction liée au bouton "Créer un dossier"
        #self.btn_import.clicked.connect(self.btn_import_click)

    #la fonction permet d'entrer à la fenetre de dossier
    @pyqtSlot()
    def btn_creer_click(self):
        self.trans = MVCViewDossier(self.myCtrl) #la classe de la fenetre de dossier
        self.close()

    """"@pyqtSlot()
    def bouton_ouvrirDossier_click(self):
        self.trans = MVCViewImporter(self.myCtrl)
        self.close()"""

# %%
class MVCViewDossier(QWidget): #La classe « MVCView » qui hérite de QWidget et représente notre fenêtre

    def __init__(self, ctrl, nom_e=None, prenom_e=None, age_e=None, sexe_e=None, sym_e=None, ordo_e=None):
        super().__init__() #La constructeur de la classe « QWidget »
        self.myCtrl = ctrl #C’est l’objet type Controller passé en argument, la liaison entre View (client) et Controller (serveur)

        # nom saisi
        self.nom_label = QLabel("Nom")
        self.nom_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin: 10px 0px 5px 15px")
        self.nom_text = QLineEdit(nom_e)
        self.nom_text.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; background-color: #fff; margin: 10px 0px 5px 5px")

        # prenom saisi
        self.prenom_label = QLabel("Prénom")
        self.prenom_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-bottom: 5px")
        self.prenom_text = QLineEdit(prenom_e)
        self.prenom_text.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; background-color: #fff; margin-bottom: 5px")

        # age saisi
        self.age_label = QLabel("Âge")
        self.age_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-bottom: 5px")
        self.age_text = QLineEdit(age_e)
        self.age_text.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; background-color: #fff; margin-bottom: 5px")

        # sexe choisi
        self.sexe_label = QLabel("Sexe")
        self.sexe_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px")
        self.sexe_m = QRadioButton("M", self)
        self.sexe_f = QRadioButton("F", self)
        self.sexe_m.setChecked(True) if sexe_e == "M" else None
        self.sexe_f.setChecked(True) if sexe_e == "F" else None

        # button historique
        self.btn_h = QPushButton('Historique')
        self.btn_h.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 0px 20px 5px 50px")

        # button enregistrer
        self.btn_e = QPushButton("Enregistrer")
        self.btn_e.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 20px")

        #button fermer
        self.btn_f = QPushButton("Fermer")
        self.btn_f.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 20px")

        #symptomes saisies
        self.sym_label = QLabel("Symptômes")
        self.sym_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-top: 15px")
        self.sym = QTextEdit(sym_e)
        self.sym.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; background-color: #fff; padding: 10px; margin: 0px 20px 5px 15px")
        self.sym.textChanged.connect(self.propo_connect)

        #ordonnaces saisies
        self.ordo_label = QLabel("Ordonnances")
        self.ordo_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-top: 5px")
        self.ordo = QTextEdit(ordo_e)
        self.ordo.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; background-color: #fff; padding: 10px; margin: 0px 20px 5px 15px")

        #zone de texte proposition des médicaments
        self.propo = QTextEdit("")
        self.propo.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; padding: 10px; margin: 20px 20px 5px")

        #creation de la liste des médicaments, chaque médicament lié aux symptomes
        self.list_medica = {"Doliprane": ["Douleur", "Fievre", "Nausee"],
                           "Dafalgan": ["Douleur", "Fievre", "Sudation", "Naussee"],
                           "Efferalgant": ["Douleur", "Fievre"],
                           "Kardegic": ["Hypertension", "Douleur", "Depression"],
                           "Spasfon": ["Douleur", "Digestif"],
                           "Gaviscon": ["Estomac", "Brulures"],
                           "Dexeryl": ["Douleur", "Irritation", "Urticaire"],
                           "Meteospasmyl": ["Ballonement", "Digestif"],
                           "Biseptine": ["Infectées", "Infection"],
                           "Eludril": ["Infecion", "Bouche"]}

        self.init_ui()

        self.show()

    def init_ui(self):
        #passe le souris sur les boutons pour voir le texte
        QToolTip.setFont(QFont('Roboto', 14))
        self.btn_f.setToolTip('Cliquez ici pour retourner à la fenêtre de accueil')
        self.btn_e.setToolTip('Cliquez ici pour enregistrer les informations dans la fiche du patient')
        self.btn_h.setToolTip('Cliquez ici pour enregistrer les informations dans la fiche du patient')

        #Le placement des widgets dans le layout form
        h_box = QHBoxLayout()
        f_box = QFormLayout()
        f_box.addRow(self.nom_label, self.nom_text)  #ajoute une ligne
        f_box.addRow(self.prenom_label, self.prenom_text) #ajoute une ligne
        f_box.addRow(self.age_label, self.age_text) #ajoute une ligne
        h_box.addWidget(self.sexe_label)
        h_box.addWidget(self.sexe_m)
        h_box.addWidget(self.sexe_f)
        f_box.addRow(h_box) #ajoute une ligne

        #Le placement des widgets dans le layout vertical
        k_box = QVBoxLayout()
        k_box.addWidget(self.sym_label)
        k_box.addWidget(self.sym)
        k_box.addWidget(self.ordo_label)
        k_box.addWidget(self.ordo)

        #Le placement des widgets dans le layout de la grille
        layout = QGridLayout()
        layout.addLayout(f_box, 0, 0)
        layout.addWidget(self.btn_h, 0, 1)
        layout.addLayout(k_box, 1, 0)
        layout.addWidget(self.propo, 1, 1)
        layout.addWidget(self.btn_e, 2, 0)
        layout.addWidget(self.btn_f, 2, 1)

        self.setLayout(layout) #Le placement du layout dans la fenêtre
        self.setWindowTitle("Fenêtre de doissier") #Le titre de la fenêtre, affiché en haut
        self.setFixedSize(450, 450) #fixer la taille de la fenetre
        self.setStyleSheet("background-color: #f0ecec") #style de la fenetre
        self.setWindowIcon(QIcon('sante_logo.png')) #L'icon de la fenetre, affiché en haut

        self.propo.setDisabled(True) #désactiver l'écriture dans la zone de la saisie de proposition des médicaments
        self.btn_f.clicked.connect(self.btn_f_click) #La fonction liée au bouton fermer
        self.btn_e.clicked.connect(self.btn_e_click) #La fonction liée au bouton enregistrer
        self.btn_h.clicked.connect(self.btn_h_click) #La fonction liée au bouton historique
        self.sexe_m.toggled.connect(self.radiobtn_sexe_click) #La fonction liée au choix du sexe
        self.sexe_f.toggled.connect(self.radiobtn_sexe_click) #La fonction liée au choix du sexe

    # la fonction permet de revenir à la fenetre d'accueil
    @pyqtSlot()
    def btn_f_click(self):
        self.trans = MVCView(self.myCtrl) #La classe de la fenetre d'accueil
        self.close()

    # la fonction du choix du sexe
    def radiobtn_sexe_click(self):
        if self.sexe_m.isChecked(): #Si on choix "M"
            return self.sexe_m.text() #ça écrit "M"
        if self.sexe_f.isChecked(): #Si on choix "F"
            return self.sexe_f.text() #ça écrit "F"

    #la fonction permet d'enregistrer des informations saisies d'un patient
    def btn_e_click(self):
        #nom saisi
        nom_e = self.nom_text.text().upper()
        nom_e = " ".join(nom_e.split())

        #prenom saisi
        prenom_e = self.prenom_text.text().title()
        prenom_e = " ".join(prenom_e.split())

        #age saisi
        age_e = self.age_text.text()
        age_e = " ".join(age_e.split())

        #sexe choisi
        sexe_e = self.radiobtn_sexe_click()

        #symptomes saisies
        sym_e = self.sym.toPlainText().title()
        sym_e = " ".join(sym_e.split())

        #ordonnances saisies
        ordo_e = self.ordo.toPlainText().title()
        ordo_e = " ".join(ordo_e.split())

        #vérifier si tous les champs remplies avant de cliquer le bouton enregistrer
        if (nom_e == '' or prenom_e == '' or age_e == '' or sexe_e == '' or sym_e == '' or ordo_e == ''):
            self.btn_e.setToolTip("Veuillez remplir tous les champs avant de cliquer ce bouton") #passe le souris sur les boutons pour voir le texte
        else:
            self.myCtrl.save(nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e) #enregistrer les informations saisies et passée en argument au Contrôleur
            self.nom_text.setText("") #vider la ligne de la saisie de nom
            self.prenom_text.setText("") #vider la ligne de la saisie de prénom
            self.age_text.setText("") #vider la ligne de la saisie d'age
            self.sym.setText("") #vider la ligne de la saisie des symptomes
            self.ordo.setText("") #vider la ligne de la saisie des ordonnances

    #la fonction permet de vérifier si un patient existe déjà ou pas grace aux informations saisies
    @pyqtSlot()
    def btn_h_click(self):
        try:
            self.aux = self.myCtrl.show() #base de données : le fichier .csv, la liaison entre View (client) et Controller (serveur)
            nom_h = list(list(self.aux.values())[0].values()) #colonne de nom, ça c'est une liste
            nom_e = self.nom_text.text().upper() #nom saisi
            nom_e = " ".join(nom_e.split()) #nom saisi
            for i in range(len(nom_h)):
                if (nom_e == nom_h[i]): #vérifie si le nom saisi existe dans la liste des noms
                    self.nom_txt_h = nom_h[i]

            prenom_h = list(list(self.aux.values())[1].values()) #colonne de prenom, ça c'est une liste
            prenom_e = self.prenom_text.text().title() #prenom saisi
            prenom_e = " ".join(prenom_e.split()) #prenom saisi
            for i in range(len(prenom_h)):
                if (prenom_e == prenom_h[i]): #vérifie si le prenom saisi existe dans la liste des prenoms
                    self.prenom_txt_h = prenom_h[i]

            age_h = list(list(self.aux.values())[2].values()) #colonne d'age
            age_e = self.age_text.text() #age saisi
            age_e = " ".join(age_e.split()) #age saisi
            for i in range(len(age_h)):
                age_h[i] = str(age_h[i])
                if (age_e == age_h[i]):  #vérifie si l'age saisi existe dans la liste des ages
                    self.age_txt_h = str(age_h[i])

            sexe_h = list(list(self.aux.values())[3].values()) #colonne de sexe
            sexe_e = self.radiobtn_sexe_click()
            for i in range(len(sexe_h)):
                if (sexe_e == sexe_h[i]):
                    self.sexe_txt_h = sexe_h[i]

            sym_h = list(list(self.aux.values())[4].values()) #colonne de symptomes
            sym_e = self.sym.toPlainText().title()
            sym_e = " ".join(sym_e.split())
            for i in range(len(sym_h)):
                if (sym_e == sym_h[i]):
                    self.sym_txt_h = str(sym_h[i])

            ordo_h = list(list(self.aux.values())[5].values()) #colonne d'ordonnances
            ordo_e = self.ordo.toPlainText().title()
            ordo_e = " ".join(ordo_e.split())
            for i in range(len(ordo_h)):
                if (ordo_e == ordo_h[i]):
                    self.ordo_txt_h = ordo_h[i]

            if (nom_e == '' or prenom_e == '' or age_e == '' or sexe_e == '' or sym_e == '' or ordo_e == ''):
                self.btn_h.setToolTip("Veuillez remplir tous les champs avant de cliquer ce bouton")
            else:
                self.trans = MVCViewHistorique(self.myCtrl, self.nom_txt_h, self.prenom_txt_h, self.age_txt_h, self.sexe_txt_h, self.sym_txt_h, self.ordo_txt_h)
                self.close()
        except:
            QMessageBox.about(self, "Erreur", "Veuillez vérifier toutes les informations du patient que vous voulez chercher!!!")

    #la fonction permet de suggérer des médicaments
    def propo_connect(self):
        self.propo.clear()
        self.sym_connect = self.sym.toPlainText().split('\n')
        self.sym_list = [] #liste des symptomes saisies

        for i in self.sym_connect:
            self.sym_ligne = i.split(" ") #Après une espace, c'est un symptome
            for j in self.sym_ligne:
                self.sym_list.append(j)  #Ajoute chaque symptome dans la liste

        self.ordo_list = []
        for l in range(len(self.sym_list)): #l chaque symptome dans la liste des symptomes
            for m in self.list_medica.keys(): #m chaque médicament
                for n in self.list_medica[m]: #n liste des symptomes liée à chaque médicament
                    if self.sym_list[l] == n:     #On cherche symptome saisie dans n la liste des symptome
                        self.ordo_list.append(m) #on ajoute m médicement dans l'ordonnance

        self.ordo_list = list(set(self.ordo_list)) #convertir "list" en "set" pour éviter l'affichage des médicaments plusieurs fois, puis, revenir la list en "list"

        self.ordo_string = "\n".join(self.ordo_list) #convertir "list" en "str"

        self.propo.setText(self.ordo_string) #l'affichage des propositions des médicaments liés à ses symptomes

# %%
class MVCViewHistorique(QWidget):

    def __init__(self, ctrl, nom_txt_h="", prenom_txt_h="", age_txt_h="", sexe_txt_h="", sym_txt_h="", ordo_txt_h=""):
        super().__init__() #La constructeur de la classe « QWidget ».

        self.myCtrl = ctrl #C’est l’objet type Controller passé en argument, la liaison entre View (client) et Controller (serveur)

        #nom
        self.nom_label_h = QLabel("Nom")
        self.nom_label_h.setStyleSheet("font-family: 'Roboto'; margin: 10px 0px 5px 15px")
        self.nom_text_h = QLineEdit(nom_txt_h)
        self.nom_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin: 10px 0px 5px 5px; margin-right: 220px")

        #prenom
        self.prenom_label_h = QLabel("Prénom")
        self.prenom_label_h.setStyleSheet("font-family: 'Roboto'; margin-left: 15px; margin-bottom: 5px")
        self.prenom_text_h = QLineEdit(prenom_txt_h)
        self.prenom_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; margin-bottom: 5px; margin-right: 220px")

        #age
        self.age_label_h = QLabel("Âge")
        self.age_label_h.setStyleSheet("font-family: 'Roboto'; margin-left: 15px; margin-bottom: 5px")
        self.age_text_h = QLineEdit(age_txt_h)
        self.age_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; margin-bottom: 5px; margin-right: 220px")

        #sexe
        self.sexe_label_h = QLabel("Sexe")
        self.sexe_label_h.setStyleSheet("font-family: 'Roboto'; margin-left: 15px; margin-bottom: 5px")
        self.sexe_text_h = QLineEdit(sexe_txt_h)
        self.sexe_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; margin-bottom: 5px; margin-right: 220px")

        #button
        self.btn_f_h = QPushButton("Fermer")
        self.btn_f_h.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 5px; margin: 10px 150px")

        #zone de text
        self.sym_label_h = QLabel("Symptômes")
        self.sym_label_h.setStyleSheet("font-family: 'Roboto'; margin: 10px 0px 5px 15px")
        self.sym_h = QTextEdit(sym_txt_h)
        self.sym_h.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; padding: 5px; margin: 0px 10px 5px")

        self.ordo_label_h = QLabel("Ordonnances")
        self.ordo_label_h.setStyleSheet("font-family: 'Roboto'; margin: 10px 0px 5px 15px")
        self.ordo_h = QTextEdit(ordo_txt_h)
        self.ordo_h.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; padding: 5px; margin: 0px 10px 5px")

        self.init_ui()

        self.show()

    def init_ui(self):
        # passe le souris sur les boutons pour voir le texte
        QToolTip.setFont(QFont('Roboto', 14))
        self.btn_f_h.setToolTip('Cliquez ici pour retourner à la fenêtre de dossier')

        # Le placement des widgets dans le layout form
        f_box = QFormLayout()
        f_box.addRow(self.nom_label_h, self.nom_text_h)
        f_box.addRow(self.prenom_label_h, self.prenom_text_h)
        f_box.addRow(self.age_label_h, self.age_text_h)
        f_box.addRow(self.sexe_label_h, self.sexe_text_h)

        # Le placement des widgets dans le layout vertical
        v_box = QVBoxLayout()
        v_box.addLayout(f_box)
        v_box.addWidget(self.sym_label_h)
        v_box.addWidget(self.sym_h)
        v_box.addWidget(self.ordo_label_h)
        v_box.addWidget(self.ordo_h)
        v_box.addWidget(self.btn_f_h)

        self.setLayout(v_box) #Le placement du layout dans la fenêtre
        self.setWindowTitle("Fenêtre d'historique") #Le titre de la fenêtre, affiché en haut
        self.setFixedSize(450, 500) #fixer la taille de la fenetre
        self.setStyleSheet("background-color: #f0ecec") #style de la fenetre
        self.setWindowIcon(QIcon('sante_logo.png')) #L'icon de la fenetre, affiché en haut

        # désactiver l'écriture dans la zone de la saisie
        self.nom_text_h.setDisabled(True)
        self.prenom_text_h.setDisabled(True)
        self.age_text_h.setDisabled(True)
        self.sexe_text_h.setDisabled(True)
        self.sym_h.setDisabled(True)
        self.ordo_h.setDisabled(True)
        self.btn_f_h.clicked.connect(self.btn_f_h_click)

    # La fonction liée au bouton fermer
    @pyqtSlot()
    def btn_f_h_click(self):
        self.trans = MVCViewDossier(self.myCtrl) #La classe de la fenetre de dossier
        self.close()

# %%
class MVCController: #La classe « MVCController » reçoit les demandes des utilisateurs, puis obtient les données du modèle et les donne à la vue

    def __init__(self, model): #La méthode s'appelle le « constructeur » de la classe pour initialiser certaines variables (model)
        self.myModel = model #C’est l’objet type Model passé en argument, la liaison entre Controller (serveur) et Model (base de données)

    #La fonction « save » appelle le Model pour enregistrer les informations saisies en appuyant la bouton "enregistrer" (la fonction "btn_e_click" de la classe MVCViewDossier)
    def save(self, nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e):
        return self.myModel.savePatient(nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e) #la liaison entre Controller (serveur) et Model (base de données)

    #La fonction « show » appelle le Model pour afficher les informations vérifies en appuyant la bouton "historisque" dans la fenetre d'historique (la fonction "btn_h_click" de la classe MVCViewDossier)
    def show(self):
        self.aux = self.myModel.showPatient() #la liaison entre Controller (serveur) et Model (base de données)
        return self.aux #Retourne le message

# %%
class MVCModel: #La classe « MVCModel » est l'architecture de données de la base de données, qui fournit des fonctions de traitement à la base de données

    def __init__(self, ssh): #La méthode s'appelle le « constructeur » de la classe
        self.ssh = ssh #C’est l’objet type ssh passé en argument, la liaison entre Model (base de données de la machine hôte) et SSH (connexion à distance – base  de données de la machine virtuelle).
        self.file = pd.DataFrame({'Nom': [], 'Prenom': [], 'Age': [], 'Sexe': [], 'Symptomes': [], 'Ordonnances': []}) #DataFrame est une structure de données étiquetée bidimensionnelle avec des colonnes de types potentiellement différents. Ici, on a six colonnes.
        self.file = self.rcp() #c’est la fonction qui permet d’envoyer des données du fichier .csv de la machine virtuelle au fichier .csv de la machine hôte et d’afficher la courbe de ces données

    # La fonction « savePatient » pour enregistrer les informations saisies en appuyant la bouton "enregistrer" (la fonction "btn_e_click" de la classe MVCViewDossier)
    def savePatient(self, nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e):
        self.file.loc[len(self.file.index)] = [nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e] #Ajoute une entrée, un dictionnaire : une clé et les valeurs associées
        self.file.to_csv(hote_path, index=False) # lecture d'une table sans index, c’est-à-dire, on envoie les informations saisis au fichier .csv de la machine hôte
        self.ssh.envoi_fichier() #après, on envoie ces données du fichier .csv de la machine hôte au fichier .csv de la machine virtuelle

    #La fonction « showPatient » appelle le Model pour afficher les informations vérifies en appuyant la bouton "historisque" dans la fenetre d'historique (la fonction "btn_h_click" de la classe MVCViewDossier)
    def showPatient(self):
        self.aux = self.file.to_dict() #convertir une trame de données en un dictionnaire de série ou une liste
        return self.aux

    #La fonction « rcp » pour récupérer les données du fichier.csv de la machine virtuelle au fichier.csv de la machine hôte
    def rcp(self):
        self.ssh.rcp_fichier() #récupérer les données à distance
        try: #Si des données existent déjà dans le fichier .csv de la machine hôte
            data = pd.read_csv(hote_path) #lecture du fichier .csv de la machine hôte
            return data
        except: #Sinon, ça va afficher le message d’erreur
            print("Error!!!!!!! Le fichier est vide")
            return self.file

# %%
class ssh: #La classe « ssh » a pour but de faire la connexion à distance, d’échanger les données d’enregistrement entre le fichier.csv de la machine hôte et de la machine virtuelle.

    # On fait la connexion à la machine virtuelle avec son hostname, son port, son username, son password
    client = None

    def __init__(self, hostname, port, username, password):
        try:
            print("Connecting to server.")
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username, password=password)
            self.sftp = self.client.open_sftp() #Ouvre sftp client, SFTP signifie SSH File Transfer Protocol ou Secure File Transfer Protocol. Le client SFTP permet d'importer et d'exporter des comptes, de renommer et de supprimer des fichiers, de créer de nouveaux fichiers/répertoires...
        except:
            print("Exception raised!")

    # La fonction « envoi_fichier » pour envoyer le fichier modifié sur la machine virtuelle
    def envoi_fichier(self):
        self.sftp.put(hote_path, vm_path) #ici, on utilise la méthode « put » pour envoyer des données du fichier .csv de la machine hôte au fichier .csv de la machine virtuelle

    # La fonction « rcp_fichier » pour récupérer les données du fichier .csv de la machine virtuelle au fichier .csv de la machine hôte
    def rcp_fichier(self):
        open(hote_path, 'a').close() #ouvre le fichier .csv de la machine hôte et ferme après finir des étapes
        try:
            print(self.sftp.stat(vm_path)) #vérifie si le fichier .csv de la machine virtuelle existe déjà
            print("File already exists.")
            self.sftp.get(vm_path, hote_path) #récupérer les données du fichier .csv de la machine virtuelle au fichier .csv de la machine hôte
        except:
            print("Copying file.")
            self.sftp.put(hote_path, vm_path) #sinon, envoyer des données du fichier .csv de la machine hôte au fichier .csv de la machine virtuelle


print(__name__)

hostname = "192.168.1.38"  # votre destination
username = "etudiant"
password = "vitrygtr"
port = 22

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ssh = ssh(hostname, port, username, password)
    model = MVCModel(ssh)
    ctrl = MVCController(model)
    window_a = MVCView(ctrl)
    sys.exit(app.exec_())
