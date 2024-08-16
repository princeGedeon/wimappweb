# -*- coding: utf-8 -*-
from licenceapp.models import Classe, Matiere
from musicapp.models import StyleMusique

# Liste des classes à ajouter
classes = ['Terminale', 'Cinquième', 'Sixième', 'Quatrième', 'Première', 'Seconde', 'Troisième']

# Liste des styles de musique à ajouter
styles = ['RAP', 'POP', 'ZOUK']

# Liste des matières à ajouter
matieres = ['SVT', 'Philosophie', 'Mathematiques', 'Histoire', 'Geographie', 'Espagnol', 'Economie', 'Bonus', 'Anglais']

# Ajouter les classes
for classe_name in classes:
    Classe.objects.get_or_create(nom=classe_name)

# Ajouter les styles de musique
for style_name in styles:
    StyleMusique.objects.get_or_create(nom=style_name)

# Ajouter les matières
for matiere_name in matieres:
    Matiere.objects.get_or_create(nom=matiere_name)

print("Les classes, styles de musique, et matières ont été ajoutés avec succès.")
