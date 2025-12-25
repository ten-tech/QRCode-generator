from django.urls import path
from . import views

urlpatterns = [
    path('', views.qr_code_generator, name='qr_code_generator'),
    path('api/preview', views.qr_preview_api, name='qr_preview_api'),
    path('api/batch', views.batch_generate, name='batch_generate'),
    path('api/export-pdf', views.export_pdf, name='export_pdf'),
]  