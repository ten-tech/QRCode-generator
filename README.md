# 🎨 QR Code Generator Premium

Un générateur de QR codes moderne et puissant avec design neumorphique, offrant des fonctionnalités avancées de personnalisation et d'export.

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![Django](https://img.shields.io/badge/django-5.0+-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Fonctionnalités

### 🎯 Templates Spécialisés

- **Texte/URL** - QR codes classiques pour liens et textes
- **vCard** - Cartes de visite numériques
- **WiFi** - Connexion WiFi instantanée
- **Email** - Envoi d'emails pré-remplis
- **SMS** - Messages texte pré-configurés
- **Événement** - Ajout automatique au calendrier (iCalendar)
- **Géolocalisation** - Coordonnées GPS
- **Paiement** - PayPal et Bitcoin

### 🎨 Personnalisation Avancée

- **Couleurs personnalisées** - QR code et fond
- **Dégradés de couleurs** - Horizontal, vertical ou diagonal
- **Styles de modules** - Carrés, ronds ou coins arrondis
- **Formes globales** - Carrée ou circulaire
- **Cadre personnalisable** - Avec texte et couleurs
- **Logo central** - Insertion d'image au centre

### 🚀 Fonctionnalités Premium

- **Aperçu en temps réel** - Génération instantanée pendant la frappe
- **Export multiple formats** - PNG, SVG vectoriel, PDF haute résolution (600 DPI)
- **Génération en batch** - Upload CSV → ZIP de QR codes
- **Historique localStorage** - Sauvegarde des 10 derniers QR codes
- **Mode sombre** - Thème automatique selon les préférences système
- **Interface responsive** - Optimisée mobile, tablette et desktop

## 🖼️ Design

Interface moderne avec **neumorphisme** (soft UI) :

- Design élégant et intuitif
- Ombres et reliefs subtils
- Transitions fluides
- Support complet du mode sombre
- Sticky positioning sur desktop pour l'aperçu

## 📋 Prérequis

- Python 3.11+
- Django 5.0+
- Pillow (PIL)
- qrcode
- reportlab

## 🔧 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/qr-code-generator.git
cd qr-code-generator
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Migrations de la base de données

```bash
python manage.py migrate
```

### 5. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible sur `http://127.0.0.1:8000/`

## 🌐 Déploiement

### Déploiement sur Render (Gratuit avec HTTPS)

1. **Fork ou push le projet sur GitHub**

2. **Créer un compte sur [render.com](https://render.com)**

3. **Le projet est déjà configuré avec** :

   - `render.yaml` - Configuration automatique
   - Variables d'environnement sécurisées
   - Base de données PostgreSQL gratuite
   - SSL/HTTPS automatique

4. **Cliquer sur "New Web Service" et connecter votre repo GitHub**

5. **Render détectera automatiquement la configuration**

L'app sera live en ~5 minutes sur `https://votre-app.onrender.com`

### Variables d'environnement

Les variables suivantes sont générées automatiquement par Render :

- `SECRET_KEY` - Clé secrète Django (générée automatiquement)
- `DEBUG` - Mode debug (False en production)
- `DATABASE_URL` - URL de la base PostgreSQL

## 📁 Structure du Projet

```
qr-code-generator/
├── qr_code_generator/      # Configuration Django
│   ├── settings.py         # Settings (production ready)
│   ├── urls.py
│   └── wsgi.py
├── qr_code_app/            # Application principale
│   ├── views.py            # Logique métier et APIs
│   ├── forms.py            # Formulaires Django
│   ├── urls.py             # Routes
│   └── templates/          # Templates HTML
├── static/                 # Fichiers statiques
│   ├── css/
│   │   └── style.css       # Design neumorphique
│   └── js/
│       └── script.js       # Interactions client
├── requirements.txt        # Dépendances Python
├── render.yaml            # Config déploiement Render
└── README.md              # Ce fichier
```

## 🎯 Utilisation

### Générer un QR code simple

1. Sélectionner le template **"Texte/URL"**
2. Entrer votre texte ou URL
3. Personnaliser les couleurs (optionnel)
4. L'aperçu se génère automatiquement
5. Télécharger en PNG, SVG ou PDF

### Créer une carte de visite (vCard)

1. Sélectionner le template **"vCard"**
2. Remplir vos informations (nom, entreprise, téléphone, email, site web)
3. Personnaliser le design
4. Télécharger et partager

### Générer des QR codes en masse

1. Préparer un fichier CSV avec le format :
   ```csv
   text,filename
   https://example.com,site_web
   WIFI:T:WPA;S:MonWiFi;P:password123;;,wifi_bureau
   ```
2. Aller dans la section **"Génération en Batch"**
3. Uploader le CSV (drag & drop supporté)
4. Télécharger le ZIP contenant tous les QR codes

## 🔌 API Endpoints

### Aperçu en temps réel

```
POST /api/preview
Content-Type: application/json

{
  "template_type": "text",
  "text": "Hello World",
  "fill_color": "#000000",
  "bg_color": "#FFFFFF",
  "border_size": 4
}
```

### Génération en batch

```
POST /api/batch
Content-Type: multipart/form-data

csv_file: [fichier CSV]
```

### Export PDF

```
POST /api/export-pdf
Content-Type: application/json

{
  "template_type": "text",
  "text": "Hello World",
  "fill_color": "#667eea",
  "use_gradient": "true",
  ...
}
```

## 🎨 Personnalisation

### Modifier les couleurs du thème

Éditer `static/css/style.css` :

```css
:root {
  --bg-main: #e0e5ec;
  --shadow-light: #ffffff;
  --shadow-dark: #a3b1c6;
  --text-primary: #2c3e50;
  --accent: #667eea;
}

:root[data-theme="dark"] {
  --bg-main: #1a1a2e;
  --shadow-light: #252947;
  --shadow-dark: #0f1419;
  --text-primary: #e0e5ec;
  --accent: #818cf8;
}
```

### Ajouter un nouveau template

1. Ajouter les champs dans `qr_code_app/forms.py`
2. Créer la fonction de formatage dans `qr_code_app/views.py`
3. Ajouter les champs UI dans `templates/qr_code/generator.html`
4. Mettre à jour le JavaScript dans `static/js/script.js`

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.0+, Python 3.11+
- **QR Generation** : python-qrcode, Pillow
- **PDF Export** : ReportLab
- **Frontend** : Vanilla JavaScript, CSS3 (Neumorphism)
- **Déploiement** : Render, PostgreSQL
- **CI/CD** : GitHub Actions ready

## 📊 Statistiques du Projet

- **8 templates** spécialisés
- **15+ options** de personnalisation
- **3 formats** d'export (PNG, SVG, PDF)
- **Génération en batch** illimitée
- **100% responsive** (mobile, tablette, desktop)
- **Mode sombre** natif
- **Aperçu temps réel** (< 500ms)

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Ajout feature incredible'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Roadmap

### Version 1.3 (En cours)

- [x] Templates spécialisés (vCard, WiFi, Email, SMS, Event, Geo, Payment)
- [x] Personnalisation design avancée (gradient, modules, formes)
- [x] Export SVG et PDF haute résolution
- [x] Génération en batch (CSV → ZIP)
- [x] Mode sombre
- [x] Historique localStorage

### Version 2.0 (Futur)

- [ ] QR codes dynamiques (trackables)
- [ ] Analytics et statistiques de scans
- [ ] API publique avec authentification
- [ ] Système utilisateur et dashboard
- [ ] Plans Premium (Free/Pro)
- [ ] Intégration Cloud Storage (S3)

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Développé avec tant d'affection.

## 🔗 Liens Utiles

- [Documentation Django](https://docs.djangoproject.com/)
- [python-qrcode](https://github.com/lincolnloop/python-qrcode)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Neumorphism Design](https://neumorphism.io/)

## 🙏 Remerciements

- Design inspiré par [Neumorphism.io](https://neumorphism.io/)
- QR Code library par [lincolnloop](https://github.com/lincolnloop/python-qrcode)
- PDF generation par [ReportLab](https://www.reportlab.com/)

---

⭐ **Si ce projet vous a aidé, n'oubliez pas de donner une étoile !** ⭐
