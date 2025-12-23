import qrcode
from io import BytesIO
import base64  # Pour encoder en base64
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from .forms import QRCodeForm

def qr_code_generator(request):
    qr_image_data = None  # Variable pour stocker l'image QR en base64

    if request.method == "POST":
        # Récupère les données du formulaire (texte, couleurs, logo)
        form = QRCodeForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Récupère les données nettoyées
            text = form.cleaned_data["text"]
            fill_color = form.cleaned_data["fill_color"] or "black"
            bg_color = form.cleaned_data["bg_color"] or "white"
            border_size = form.cleaned_data.get("border_size", 4)
            logo = form.cleaned_data["logo"]  # Logo optionnel

            # Génère le code QR avec les couleurs choisies et bordure personnalisée
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=border_size)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color=fill_color, back_color=bg_color).convert("RGBA")

            # Si un logo est fourni, il est ajouté au centre du QR
            if logo:
                logo_img = Image.open(logo).convert("RGBA")
                logo_size = img.size[0] // 5  # Taille du logo = 1/5 de l'image
                logo_img = logo_img.resize((logo_size, logo_size))
                # Position centrée
                pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
                img.paste(logo_img, pos, logo_img)  # Colle avec transparence

            # Si un cadre est activé, on l'ajoute autour du QR code
            enable_frame = form.cleaned_data.get("enable_frame", False)
            if enable_frame:
                frame_width = form.cleaned_data.get("frame_width", 30)
                frame_color = form.cleaned_data.get("frame_color", "#FFFFFF")
                frame_text = form.cleaned_data.get("frame_text", "")

                # Si du texte est fourni, réserver de l'espace supplémentaire pour la zone de texte
                text_zone_height = 0
                if frame_text:
                    text_zone_height = max(40, frame_width)  # Zone de texte entre QR et cadre

                # Calcul de la nouvelle taille avec le cadre et la zone de texte
                new_width = img.size[0] + (2 * frame_width)
                new_height = img.size[1] + (2 * frame_width) + text_zone_height

                # Création d'une nouvelle image avec le cadre
                framed_img = Image.new("RGBA", (new_width, new_height), frame_color)

                # Position du QR code au centre horizontal, en haut avec le cadre
                qr_position = (frame_width, frame_width)
                framed_img.paste(img, qr_position)

                # Ajouter une zone de texte entre le QR et le cadre du bas
                if frame_text:
                    draw = ImageDraw.Draw(framed_img)

                    # Calculer la couleur de fond pour la zone de texte (contraste avec le cadre)
                    frame_rgb = tuple(int(frame_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    luminance = (0.299 * frame_rgb[0] + 0.587 * frame_rgb[1] + 0.114 * frame_rgb[2]) / 255
                    text_zone_bg = "#FFFFFF" if luminance < 0.5 else "#000000"
                    text_color = "#000000" if luminance < 0.5 else "#FFFFFF"

                    # Dessiner la zone de texte entre le QR et le cadre du bas
                    text_zone_y_start = frame_width + img.size[1]
                    draw.rectangle(
                        [(frame_width, text_zone_y_start),
                         (new_width - frame_width, text_zone_y_start + text_zone_height)],
                        fill=text_zone_bg
                    )

                    # Essayer de charger une police
                    try:
                        font_size = max(14, min(text_zone_height - 10, 32))
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                    except:
                        font = ImageFont.load_default()

                    # Obtenir la taille du texte
                    bbox = draw.textbbox((0, 0), frame_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    # Position du texte centré dans la zone de texte
                    text_x = (new_width - text_width) // 2
                    text_y = text_zone_y_start + (text_zone_height - text_height) // 2

                    # Dessiner le texte
                    draw.text((text_x, text_y), frame_text, fill=text_color, font=font)

                # Remplacer l'image originale par celle avec cadre
                img = framed_img

            # Sauvegarde l'image en mémoire (BytesIO)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)  # Remet le pointeur au début

            # Encode l'image en base64 pour l'afficher dans le HTML
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            qr_image_data = f"data:image/png;base64,{img_base64}"

    else:
        # Si méthode GET, affiche un formulaire vide
        form = QRCodeForm()

    # Renvoie le formulaire et l'image (si générée) au template
    return render(request, "qr_code/generator.html", {"form": form, "qr_image_data": qr_image_data})   