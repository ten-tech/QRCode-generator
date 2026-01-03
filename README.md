# 🎨 QR Code Generator Premium

Une application web moderne de génération de QR codes avec design neumorphique, offrant 8 templates spécialisés, personnalisation avancée et export multi-formats.

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)

## 🌐 Démo Live

**✨ Application déployée en production**: **[https://qrcode-generator-if7o.onrender.com/](https://qrcode-generator-if7o.onrender.com/)** ✨

- Production-ready avec PostgreSQL
- HTTPS automatique (SSL)
- Déploiement continu via Render
- Performance optimisée avec WhiteNoise

---

## 📋 Vue d'ensemble

QR Code Generator Premium est une application Django full-stack qui combine puissance backend et interface utilisateur moderne. Le projet démontre l'implémentation de patterns modernes de développement web avec un focus sur l'expérience utilisateur et la performance.

### Stack Technologique

- **Backend**: Django 6.0 avec architecture MVC
- **Database**: PostgreSQL (production) / SQLite (développement)
- **Static Files**: WhiteNoise avec compression Brotli
- **QR Generation**: python-qrcode + Pillow
- **PDF Export**: ReportLab (600 DPI)
- **Frontend**: Vanilla JavaScript ES6+ + CSS3
- **Deployment**: Render avec auto-scaling

### Statistiques Clés

- **8 templates** spécialisés
- **15+ options** de personnalisation
- **3 formats** d'export (PNG, SVG, PDF)
- **3 APIs** REST
- **~2000 lignes** Python
- **~1700 lignes** CSS
- **~900 lignes** JavaScript
- **< 500ms** génération temps réel

---

## 🏗️ Architecture & Design Patterns

### 1. Neumorphisme (Soft UI)

Design système avec ombres duales pour créer l'illusion de profondeur:

```css
/* Design system neumorphique */
:root {
  --bg-main: #e0e5ec;
  --shadow-light: #ffffff;
  --shadow-dark: #a3b1c6;
  --accent: #667eea;
}

.neumorphic-input {
  background: var(--bg-main);
  box-shadow: inset 6px 6px 12px var(--shadow-dark),
              inset -6px -6px 12px var(--shadow-light);
  border-radius: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Mode sombre automatique */
:root[data-theme="dark"] {
  --bg-main: #1a1a2e;
  --shadow-light: #252947;
  --shadow-dark: #0f1419;
  --accent: #818cf8;
}
```

### 2. Configuration Production-Ready

Settings Django optimisés avec support multi-environnements:

```python
# qr_code_generator/settings.py
import os
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database avec fallback SQLite pour dev
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,  # Connection pooling
        conn_health_checks=True,  # Auto-reconnect
    )
}

# WhiteNoise pour static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

### 3. Interface Accordéon Mobile-First

Organisation intelligente du contenu avec progressive disclosure:

```javascript
// static/js/script.js - Gestion accordéons
const accordionHeaders = document.querySelectorAll('.accordion-header');

accordionHeaders.forEach(header => {
    header.addEventListener('click', function() {
        const accordionId = this.getAttribute('data-accordion');
        const accordionBody = document.getElementById(accordionId);

        this.classList.toggle('active');
        accordionBody.classList.toggle('active');
    });
});
```

---

## ✨ Fonctionnalités Principales

### 1. Templates Spécialisés (8 types)

Chaque template génère un format de données optimisé:

```python
# qr_code_app/views.py - Exemples de formats
def format_vcard(name, org, phone, email, url):
    """vCard conforme RFC 2426"""
    return f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
ORG:{org}
TEL:{phone}
EMAIL:{email}
URL:{url}
END:VCARD"""

def format_wifi(ssid, password, security='WPA'):
    """QR WiFi pour connexion automatique"""
    return f"WIFI:T:{security};S:{ssid};P:{password};;"

def format_event(title, start, end, location, description):
    """Événement iCalendar scannable"""
    return f"""BEGIN:VEVENT
SUMMARY:{title}
DTSTART:{start}
DTEND:{end}
LOCATION:{location}
DESCRIPTION:{description}
END:VEVENT"""
```

**Templates disponibles**:
- **Texte/URL** - Liens web, texte brut
- **vCard** - Cartes de visite numériques
- **WiFi** - Connexion réseau instantanée
- **Email** - Email pré-rempli (mailto:)
- **SMS** - Messages pré-configurés
- **Event** - Événements calendrier (iCalendar)
- **Geo** - Coordonnées GPS (geo:lat,lon)
- **Payment** - PayPal et Bitcoin

### 2. Aperçu Temps Réel

API de preview avec génération asynchrone:

```javascript
// static/js/script.js - Preview temps réel
async function updateLivePreview() {
    const formData = {
        template_type: document.querySelector('.template-radio:checked').value,
        text: document.getElementById('id_text').value,
        fill_color: document.getElementById('id_fill_color').value,
        // ...
    };

    const response = await fetch('/api/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(formData)
    });

    const data = await response.json();
    document.getElementById('qr-img').src = data.qr_image;
}

// Debouncing pour optimiser
let previewTimeout;
document.querySelectorAll('input').forEach(el => {
    el.addEventListener('input', () => {
        clearTimeout(previewTimeout);
        previewTimeout = setTimeout(updateLivePreview, 300);
    });
});
```

### 3. Export Multi-formats

#### Export PDF Haute Résolution (600 DPI)

```python
# qr_code_app/views.py - Export PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@require_POST
def export_pdf(request):
    data = json.loads(request.body)

    # QR haute résolution
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,  # 20x pour 600 DPI
        border=4,
    )
    qr.add_data(data['text'])
    qr_img = qr.make_image(
        fill_color=data['fill_color'],
        back_color=data['bg_color']
    )

    # Génération PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawImage(ImageReader(qr_img), x, y, width, height)
    c.save()

    return HttpResponse(
        buffer.getvalue(),
        content_type='application/pdf'
    )
```

### 4. Génération en Batch (CSV → ZIP)

Traitement en masse avec streaming optimisé:

```python
# qr_code_app/views.py - Batch generation
import zipfile
import csv

@csrf_exempt
@require_POST
def batch_generate(request):
    csv_file = request.FILES['csv_file']
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        csv_reader = csv.DictReader(
            io.TextIOWrapper(csv_file, encoding='utf-8')
        )

        for row in csv_reader:
            qr_img = generate_qr_code(
                text=row['text'],
                fill_color='#000000'
            )

            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format='PNG')

            filename = f"{row.get('filename', 'qr')}.png"
            zip_file.writestr(filename, img_buffer.getvalue())

    return HttpResponse(
        zip_buffer.getvalue(),
        content_type='application/zip'
    )
```

**Format CSV**:
```csv
text,filename
https://example.com,site_web
WIFI:T:WPA;S:MonWiFi;P:pass123;;,wifi_bureau
```

### 5. Carte de Visite avec Preview

Génération PDF format standard (85mm × 55mm):

```python
# qr_code_app/views.py - Business card
from reportlab.lib.units import mm

@require_POST
def export_business_card(request):
    data = json.loads(request.body)

    # Format carte standard
    card_width = 85 * mm
    card_height = 55 * mm

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(card_width, card_height))

    # QR Code + informations
    layout = data.get('card_layout', 'left')
    qr_size = 40 * mm

    # Positionnement selon layout
    if layout == 'left':
        c.drawImage(qr_img, 5*mm, 7.5*mm, qr_size, qr_size)
    # ...

    c.save()
    return HttpResponse(buffer.getvalue())
```

---

## 🔌 API Endpoints

### POST /api/preview
Génération temps réel pour aperçu.

**Request**:
```json
{
  "template_type": "text",
  "text": "Hello",
  "fill_color": "#667eea",
  "use_gradient": true,
  "module_style": "rounded"
}
```

**Response**:
```json
{
  "success": true,
  "qr_image": "data:image/png;base64,..."
}
```

### POST /api/batch
Génération en masse depuis CSV.

**Request**: `multipart/form-data` avec `csv_file`

**Response**: Fichier ZIP

### POST /api/export-pdf
Export PDF haute résolution.

### POST /api/export-business-card
Export carte de visite PDF.

---

## ⚡ Performance & Optimisations

### Backend

```python
# Connection pooling
DATABASES = {
    'default': {
        'conn_max_age': 600,  # 10min
        'conn_health_checks': True,
    }
}
```

### Frontend

```javascript
// Debouncing
let timeout;
input.addEventListener('input', () => {
    clearTimeout(timeout);
    timeout = setTimeout(updatePreview, 300);
});
```

### Métriques

- Génération QR: < 100ms
- Preview API: < 500ms
- Export PDF: < 2s
- CSS bundle: 32KB (minified)
- First Paint: < 1.5s

---

## 💻 Installation Locale

```bash
git clone https://github.com/votre-username/qr-code-generator.git
cd qr-code-generator

python -m venv venv
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Accès: `http://127.0.0.1:8000/`

---

## 🚀 Déploiement

### Production sur Render

Configuration automatique via `render.yaml`:

```yaml
services:
  - type: web
    name: qr-code-generator
    runtime: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn qr_code_generator.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False

databases:
  - name: qr-code-db
    plan: free
```

**Build script** (`build.sh`):
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## 📝 Roadmap

### Version 1.3 ✅ (Production)
- [x] 8 templates spécialisés
- [x] Personnalisation avancée
- [x] Export SVG + PDF 600 DPI
- [x] Génération batch
- [x] Mode sombre
- [x] Accordéon mobile-first
- [x] Déploiement Render

### Version 2.0 🔮 (Planifiée)
- [ ] QR codes dynamiques trackables
- [ ] Dashboard analytics
- [ ] API publique avec authentification
- [ ] Système utilisateur
- [ ] Plans Premium (Free/Pro)
- [ ] Intégrations cloud

---

## 🛠️ Technologies

**Backend**: Django 6.0, python-qrcode 8.2, Pillow 12.0, ReportLab 4.4, gunicorn 23.0, dj-database-url 3.0, psycopg2-binary 2.9, whitenoise 6.6

**Frontend**: Vanilla JavaScript ES6+, CSS3 Custom Properties

**Infrastructure**: Render, PostgreSQL 15, Let's Encrypt SSL

---

## 📊 Structure du Projet

```
qr-code-generator/
├── qr_code_generator/      # Configuration Django
│   ├── settings.py         # Production-ready avec env vars
│   └── wsgi.py             # WSGI entry point
├── qr_code_app/            # Application principale
│   ├── views.py            # 8 templates + 3 APIs REST
│   ├── forms.py            # QRCodeForm avec validation
│   └── templates/          # Interface neumorphique
├── static/
│   ├── css/style.css       # 1674 lignes - Design system
│   └── js/script.js        # 900 lignes - Preview + UI
├── requirements.txt        # Dépendances Python
├── render.yaml            # Blueprint Render
└── build.sh              # Build script
```

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/Feature`)
3. Commit (`git commit -m 'feat: Add feature'`)
4. Push (`git push origin feature/Feature`)
5. Pull Request

---

## 📄 License

MIT License - Voir [LICENSE](LICENSE)

---

## 👨‍💻 Auteur

Développé avec ❤️

**Contact**:
- 🌐 **Demo Live**: [https://qrcode-generator-if7o.onrender.com/](https://qrcode-generator-if7o.onrender.com/)

---

## 🔗 Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [python-qrcode](https://github.com/lincolnloop/python-qrcode)
- [ReportLab](https://www.reportlab.com/docs/)
- [Neumorphism.io](https://neumorphism.io/)
- [Render Docs](https://render.com/docs)

---

## 🙏 Remerciements

- Design inspiré par [Neumorphism.io](https://neumorphism.io/)
- QR Library par [Lincoln Loop](https://github.com/lincolnloop/python-qrcode)
- PDF generation par [ReportLab](https://www.reportlab.com/)
- Hosting par [Render](https://render.com/)

---

<div align="center">

**⭐ Si ce projet vous a aidé, n'oubliez pas de donner une étoile ! ⭐**

[![Live Demo](https://img.shields.io/badge/Demo-Live-success?logo=google-chrome&logoColor=white)](https://qrcode-generator-if7o.onrender.com/)
[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)](https://render.com)

**Made with ❤️ using Django, PostgreSQL, and modern web technologies**

</div>
