from django import forms

class QRCodeForm(forms.Form):
    text = forms.CharField(
        label="Texte ou URL",
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Entrez votre texte ou URL...',
            'class': 'neumorphic-input'
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