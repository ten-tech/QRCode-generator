from django.apps import AppConfig


class QrCodeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qr_code_app'
    verbose_name = 'Générateur de QR Code'
