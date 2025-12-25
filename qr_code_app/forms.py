from django import forms

class QRCodeForm(forms.Form):
    # Template selector
    TEMPLATE_CHOICES = [
        ('text', 'Texte/URL'),
        ('vcard', 'vCard'),
        ('wifi', 'WiFi'),
        ('email', 'Email'),
        ('sms', 'SMS'),
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