# Générateur de QR Code Moderne - Design Neumorphisme

Une application web Django pour générer des QR codes personnalisés avec un design élégant et une expérience utilisateur exceptionnelle.

## Démarrage Rapide

### Lancement en 3 étapes

#### 1. Activer l'environnement virtuel

```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

#### 2. Lancer le serveur

```bash
python manage.py runserver
```

#### 3. Ouvrir dans le navigateur

Allez sur : **http://localhost:8000**

---

## Fonctionnalités

- **Design Neumorphisme** : Interface avec effet 3D subtil et ombres réalistes
- **100% Responsive** : S'adapte parfaitement à tous les types d'écrans (mobile, tablette, desktop)
- **Personnalisation complète** :
  - Couleur du QR code
  - Couleur du fond
  - **Taille de la bordure** (0-20 pixels)
  - **Cadre personnalisable** avec couleur et épaisseur (10-100 pixels)
  - **Zone de texte entre le QR et le cadre** (ex: "Scan me!", "Suivez-nous")
  - Logo personnalisé au centre
- **Téléchargement facile** : Export en PNG haute qualité
- **Temps réel** : Prévisualisation instantanée des couleurs et validations
- **Feedback visuel** : Animations fluides et retours utilisateur clairs

---

## Installation Complète

### Prérequis

- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. Clonez le dépôt ou naviguez vers le dossier du projet

2. Créez un environnement virtuel :

```bash
python -m venv venv
```

3. Activez l'environnement virtuel :

   - Linux/Mac :
     ```bash
     source venv/bin/activate
     ```
   - Windows :
     ```bash
     venv\Scripts\activate
     ```

4. Installez les dépendances :

```bash
pip install -r requirements.txt
```

5. Lancez le serveur de développement :

```bash
python manage.py runserver
```

6. Ouvrez votre navigateur et accédez à :

```
http://localhost:8000
```

---

## Guide d'Utilisation

### Créer un QR code basique

1. Entrez votre texte ou URL dans le champ "Texte ou URL" (jusqu'à 500 caractères)
2. Cliquez sur "Générer le QR Code"
3. Votre QR code apparaît à droite
4. Cliquez sur "Télécharger" pour le sauvegarder

### Personnaliser les couleurs

1. **Couleur du QR** : Cliquez sur le sélecteur de couleur et choisissez votre couleur préférée
2. **Couleur de fond** : Sélectionnez la couleur d'arrière-plan
3. Prévisualisation en temps réel avec code hexadécimal
4. Générez votre QR code

### Ajuster la bordure

- Définissez la taille de la bordure (0 = sans bordure, 20 = bordure maximale)
- Valeur par défaut : 4 pixels

### Ajouter un cadre personnalisé

1. **Activer le cadre** : Cliquez sur le toggle switch "Ajouter un cadre"
2. **Épaisseur du cadre** : Choisissez entre 10 et 100 pixels
3. **Couleur du cadre** : Sélectionnez la couleur souhaitée
4. **Texte personnalisé** : Ajoutez un texte entre le QR et le cadre (ex: "Scan me!", "Suivez-nous")
   - Le texte apparaît dans une zone contrastante pour une meilleure lisibilité
   - La couleur du texte s'ajuste automatiquement selon la couleur du cadre

### Ajouter un logo

1. Cliquez sur "Ajouter une image/logo"
2. Sélectionnez votre fichier image (PNG, JPG, GIF, etc.)
3. Le nom du fichier s'affiche sous le bouton
4. Le logo sera centré et redimensionné automatiquement (1/5 de la taille du QR)

### Télécharger

Cliquez sur "Télécharger" pour sauvegarder en PNG (nom unique avec timestamp)

---

## Exemples de Couleurs Populaires

- **Classique** : Noir (#000000) sur Blanc (#FFFFFF)
- **Moderne** : Violet (#764ba2) sur Blanc (#FFFFFF)
- **Tech** : Bleu (#2563eb) sur Gris clair (#f3f4f6)
- **Nature** : Vert (#16a34a) sur Crème (#fef3c7)

---

## Structure du Projet

```
qr-code-generator/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── qr_code_generator/       # Configuration Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── qr_code_app/             # Application principale
│   ├── __init__.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/               # Templates HTML
│   └── qr_code/
│       └── generator.html
└── static/                  # Fichiers statiques
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

---

## Technologies Utilisées

- **Backend** : Django 6.0
- **Génération QR** : qrcode avec PIL/Pillow
- **Frontend** : HTML5, CSS3 (Grid, Flexbox, Variables CSS), JavaScript ES6+
- **Design** : Neumorphisme avec ombres multiples et effets 3D
- **Responsive** : Media queries pour tous les breakpoints (360px à 4K)

---

## Fonctionnalités Techniques

### Design & UI

- **Neumorphisme** : Ombres doubles (light/dark) pour effet 3D
- Variables CSS pour personnalisation facile
- Animations avec cubic-bezier pour fluidité
- Typography responsive avec clamp()
- Color pickers natifs HTML5 stylisés
- Toggle switch neumorphique non-clickable sur le label

### Performance

- Grid CSS pour layout optimisé
- Transitions GPU-accelerated
- Media queries spécifiques (portrait, landscape, small screens)
- Images optimisées avec base64

### Backend

- Génération QR en mémoire (BytesIO)
- Support bordure personnalisable (0-20px)
- Support cadre avec zone de texte contrastante
- Validation formulaire côté client et serveur
- Gestion sécurisée des uploads
- Contraste automatique pour la lisibilité du texte

### JavaScript

- Validation en temps réel
- Feedback visuel immédiat
- Contraste automatique pour lisibilité
- Download avec timestamp unique
- Toggle functionality pour options de cadre

---

## Conseils d'Utilisation

- Utilisez des couleurs contrastées pour une meilleure lisibilité
- Gardez le logo petit (il sera automatiquement redimensionné à 1/5 de la taille du QR)
- Testez toujours votre QR code avec un scanner avant utilisation
- Pour les logos, utilisez des images avec fond transparent (PNG) pour un meilleur rendu
- Le texte sur la zone entre le QR et le cadre s'ajuste automatiquement pour rester lisible

---

## Dépannage

### Le serveur ne démarre pas ?

Assurez-vous que l'environnement virtuel est activé et que les dépendances sont installées :

```bash
pip install -r requirements.txt
```

### Les styles CSS ne se chargent pas ?

Vérifiez que le dossier `static/` existe et contient `css/style.css` et `js/script.js`

### Erreur lors de l'upload du logo ?

Vérifiez que votre fichier est une image valide (PNG, JPG, GIF, etc.)

### Le texte n'apparaît pas sur le cadre ?

Assurez-vous que :
1. Le toggle "Ajouter un cadre" est activé
2. Vous avez saisi du texte dans le champ "Texte sur le cadre"
3. La largeur du cadre est suffisante (minimum 10 pixels)

---

## Licence

Ce projet est libre d'utilisation pour vos projets personnels et commerciaux.
