from django import forms

class QRCodeForm(forms.Form):
    # Template selector
    TEMPLATE_CHOICES = [
        ('text', 'Texte/URL'),
        ('vcard', 'vCard'),
        ('wifi', 'WiFi'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('event', 'Événement'),
        ('geo', 'Localisation'),
        ('payment', 'Paiement'),
    ]

    template_type = forms.ChoiceField(
        choices=TEMPLATE_CHOICES,
        initial='text',
        label="Type de QR Code",
        widget=forms.RadioSelect(attrs={
            'class': 'template-radio'
        })
    )

    # Text/URL fields (default)
    text = forms.CharField(
        label="Texte ou URL",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Entrez votre texte ou URL...',
            'class': 'neumorphic-input',
            'data-template': 'text'
        })
    )

    # vCard fields
    vcard_name = forms.CharField(
        label="Nom complet",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: Jean Dupont',
            'data-template': 'vcard'
        })
    )
    vcard_org = forms.CharField(
        label="Organisation",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: Mon Entreprise',
            'data-template': 'vcard'
        })
    )
    vcard_phone = forms.CharField(
        label="Téléphone",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: +33 6 12 34 56 78',
            'data-template': 'vcard'
        })
    )
    vcard_email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: contact@exemple.fr',
            'data-template': 'vcard'
        })
    )
    vcard_url = forms.URLField(
        label="Site web",
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: https://www.exemple.fr',
            'data-template': 'vcard'
        })
    )

    # WiFi fields
    wifi_ssid = forms.CharField(
        label="Nom du réseau (SSID)",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: MonWiFi',
            'data-template': 'wifi'
        })
    )
    wifi_password = forms.CharField(
        label="Mot de passe",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Mot de passe WiFi',
            'data-template': 'wifi'
        })
    )
    wifi_security = forms.ChoiceField(
        label="Sécurité",
        choices=[
            ('WPA', 'WPA/WPA2'),
            ('WEP', 'WEP'),
            ('', 'Aucune'),
        ],
        initial='WPA',
        required=False,
        widget=forms.Select(attrs={
            'class': 'neumorphic-input',
            'data-template': 'wifi'
        })
    )

    # Email fields
    email_to = forms.EmailField(
        label="Destinataire",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: contact@exemple.fr',
            'data-template': 'email'
        })
    )
    email_subject = forms.CharField(
        label="Sujet",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Objet de l\'email',
            'data-template': 'email'
        })
    )
    email_body = forms.CharField(
        label="Message",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'neumorphic-input',
            'placeholder': 'Contenu de l\'email...',
            'data-template': 'email'
        })
    )

    # SMS fields
    sms_phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: +33 6 12 34 56 78',
            'data-template': 'sms'
        })
    )
    sms_message = forms.CharField(
        label="Message",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'neumorphic-input',
            'placeholder': 'Votre message...',
            'data-template': 'sms'
        })
    )

    # Event/Calendar fields
    event_title = forms.CharField(
        label="Titre de l'événement",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: Réunion équipe',
            'data-template': 'event'
        })
    )
    event_start = forms.DateTimeField(
        label="Date et heure de début",
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'neumorphic-input',
            'type': 'datetime-local',
            'data-template': 'event'
        })
    )
    event_end = forms.DateTimeField(
        label="Date et heure de fin",
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'neumorphic-input',
            'type': 'datetime-local',
            'data-template': 'event'
        })
    )
    event_location = forms.CharField(
        label="Lieu",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: Salle de conférence A',
            'data-template': 'event'
        })
    )
    event_description = forms.CharField(
        label="Description",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'neumorphic-input',
            'placeholder': 'Description de l\'événement...',
            'data-template': 'event'
        })
    )

    # Geolocation fields
    geo_latitude = forms.DecimalField(
        label="Latitude",
        max_digits=9,
        decimal_places=6,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: 48.856614',
            'step': '0.000001',
            'data-template': 'geo'
        })
    )
    geo_longitude = forms.DecimalField(
        label="Longitude",
        max_digits=9,
        decimal_places=6,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: 2.352222',
            'step': '0.000001',
            'data-template': 'geo'
        })
    )

    # Payment fields
    payment_type = forms.ChoiceField(
        label="Type de paiement",
        choices=[
            ('paypal', 'PayPal'),
            ('bitcoin', 'Bitcoin'),
        ],
        initial='paypal',
        required=False,
        widget=forms.Select(attrs={
            'class': 'neumorphic-input',
            'data-template': 'payment'
        })
    )
    payment_recipient = forms.CharField(
        label="Destinataire",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: username ou adresse BTC',
            'data-template': 'payment'
        })
    )
    payment_amount = forms.DecimalField(
        label="Montant",
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: 10.00',
            'step': '0.01',
            'data-template': 'payment'
        })
    )

    fill_color = forms.CharField(
        label="Couleur du QR",
        initial="#000000",
        widget=forms.TextInput(attrs={
            'type': 'color',
            'value': '#000000',
            'class': 'neumorphic-color'
        })
    )
    bg_color = forms.CharField(
        label="Couleur de fond",
        initial="#FFFFFF",
        widget=forms.TextInput(attrs={
            'type': 'color',
            'value': '#FFFFFF',
            'class': 'neumorphic-color'
        })
    )

    # Personnalisation design avancée
    use_gradient = forms.BooleanField(
        label="Utiliser un dégradé",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'neumorphic-checkbox'
        })
    )
    gradient_color_start = forms.CharField(
        label="Couleur de départ",
        initial="#667eea",
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'value': '#667eea',
            'class': 'neumorphic-color'
        })
    )
    gradient_color_end = forms.CharField(
        label="Couleur de fin",
        initial="#764ba2",
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'value': '#764ba2',
            'class': 'neumorphic-color'
        })
    )
    gradient_direction = forms.ChoiceField(
        label="Direction du dégradé",
        choices=[
            ('horizontal', 'Horizontal'),
            ('vertical', 'Vertical'),
            ('diagonal', 'Diagonal'),
        ],
        initial='diagonal',
        required=False,
        widget=forms.Select(attrs={
            'class': 'neumorphic-input'
        })
    )

    module_style = forms.ChoiceField(
        label="Style des modules",
        choices=[
            ('square', 'Carrés'),
            ('rounded', 'Ronds'),
            ('rounded-corners', 'Coins arrondis'),
        ],
        initial='square',
        required=False,
        widget=forms.Select(attrs={
            'class': 'neumorphic-input'
        })
    )

    global_shape = forms.ChoiceField(
        label="Forme globale",
        choices=[
            ('square', 'Carrée'),
            ('circle', 'Ronde'),
        ],
        initial='square',
        required=False,
        widget=forms.Select(attrs={
            'class': 'neumorphic-input'
        })
    )
    border_size = forms.IntegerField(
        label="Taille de la bordure",
        initial=4,
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': '4',
            'min': '0',
            'max': '20'
        })
    )
    enable_frame = forms.BooleanField(
        label="Ajouter un cadre",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'neumorphic-checkbox'
        })
    )
    frame_width = forms.IntegerField(
        label="Épaisseur du cadre",
        initial=30,
        min_value=10,
        max_value=100,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': '30',
            'min': '10',
            'max': '100'
        })
    )
    frame_color = forms.CharField(
        label="Couleur du cadre",
        initial="#FFFFFF",
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'value': '#FFFFFF',
            'class': 'neumorphic-color'
        })
    )
    frame_text = forms.CharField(
        label="Texte sur le cadre",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'neumorphic-input',
            'placeholder': 'Ex: Scan me! ou Suivez-nous...'
        })
    )
    logo = forms.ImageField(
        label="Logo (optionnel)",
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'neumorphic-file'
        })
    )

    # Champs pour la génération de carte de visite (vCard uniquement)
    enable_business_card = forms.BooleanField(
        label="Générer carte de visite complète",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'neumorphic-checkbox'
        })
    )
    card_layout = forms.ChoiceField(
        label="Position du QR code",
        required=False,
        initial='left',
        choices=[
            ('left', 'QR à gauche'),
            ('right', 'QR à droite'),
            ('center', 'QR centré')
        ],
        widget=forms.Select(attrs={
            'class': 'neumorphic-input'
        })
    )
    card_bg_color = forms.CharField(
        label="Couleur de fond carte",
        required=False,
        initial='#FFFFFF',
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'neumorphic-color'
        })
    )
    card_text_color = forms.CharField(
        label="Couleur du texte",
        required=False,
        initial='#2c3e50',
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'neumorphic-color'
        })
    )
    card_accent_color = forms.CharField(
        label="Couleur d'accent",
        required=False,
        initial='#667eea',
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'neumorphic-color'
        })
    )


class BatchQRCodeForm(forms.Form):
    """Formulaire pour la génération en batch"""
    csv_file = forms.FileField(
        label="Fichier CSV",
        required=True,
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'class': 'neumorphic-file'
        })
    )