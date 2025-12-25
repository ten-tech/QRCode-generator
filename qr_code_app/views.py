import qrcode
from io import BytesIO
import base64
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
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


def format_vcard(name, org="", phone="", email="", url=""):
    """Formate les données en vCard 3.0"""
    vcard = "BEGIN:VCARD\n"
    vcard += "VERSION:3.0\n"
    if name:
        vcard += f"FN:{name}\n"
    if org:
        vcard += f"ORG:{org}\n"
    if phone:
        vcard += f"TEL:{phone}\n"
    if email:
        vcard += f"EMAIL:{email}\n"
    if url:
        vcard += f"URL:{url}\n"
    vcard += "END:VCARD"
    return vcard


def format_wifi(ssid, password="", security="WPA"):
    """Formate les données en WiFi QR code"""
    # Format: WIFI:T:WPA;S:mynetwork;P:mypass;;
    wifi = f"WIFI:T:{security};S:{ssid};"
    if password:
        wifi += f"P:{password};"
    wifi += ";"
    return wifi


def format_email(to, subject="", body=""):
    """Formate les données en mailto URL"""
    from urllib.parse import quote
    email = f"mailto:{to}"
    params = []
    if subject:
        params.append(f"subject={quote(subject)}")
    if body:
        params.append(f"body={quote(body)}")
    if params:
        email += "?" + "&".join(params)
    return email


def format_sms(phone, message=""):
    """Formate les données en SMS URL"""
    from urllib.parse import quote
    sms = f"sms:{phone}"
    if message:
        sms += f"?body={quote(message)}"
    return sms


def format_event(title, start="", end="", location="", description=""):
    """Formate les données en événement iCalendar"""
    from datetime import datetime

    event = "BEGIN:VEVENT\n"
    if title:
        event += f"SUMMARY:{title}\n"
    if start:
        # Convertir format datetime-local vers iCal (YYYYMMDDTHHMMSS)
        try:
            dt = datetime.fromisoformat(start)
            event += f"DTSTART:{dt.strftime('%Y%m%dT%H%M%S')}\n"
        except:
            pass
    if end:
        try:
            dt = datetime.fromisoformat(end)
            event += f"DTEND:{dt.strftime('%Y%m%dT%H%M%S')}\n"
        except:
            pass
    if location:
        event += f"LOCATION:{location}\n"
    if description:
        event += f"DESCRIPTION:{description}\n"
    event += "END:VEVENT"
    return event


def format_geo(latitude, longitude):
    """Formate les données en géolocalisation"""
    # Format: geo:latitude,longitude
    return f"geo:{latitude},{longitude}"


def format_payment(payment_type, recipient, amount=""):
    """Formate les données en URL de paiement"""
    if payment_type == 'paypal':
        # PayPal.me format
        payment = f"https://paypal.me/{recipient}"
        if amount:
            payment += f"/{amount}"
    elif payment_type == 'bitcoin':
        # Bitcoin URI format
        payment = f"bitcoin:{recipient}"
        if amount:
            payment += f"?amount={amount}"
    else:
        payment = ""
    return payment


def generate_qr_image(text, fill_color="black", bg_color="white", border_size=4,
                     logo=None, enable_frame=False, frame_width=30,
                     frame_color="#FFFFFF", frame_text="",
                     use_gradient=False, gradient_color_start="#667eea", gradient_color_end="#764ba2",
                     gradient_direction="diagonal", module_style="square", global_shape="square"):
    """
    Fonction helper pour générer une image QR code
    Retourne l'image en base64 data URI
    """
    # Génère le code QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=border_size
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Si module personnalisé ou gradient, dessine manuellement
    if module_style != 'square' or use_gradient:
        # Récupère la matrice QR
        modules = qr.modules
        box_size = 10
        size = (len(modules) + border_size * 2) * box_size

        # Crée une image vide
        img = Image.new('RGBA', (size, size), bg_color)
        draw = ImageDraw.Draw(img)

        # Prépare les couleurs (avec ou sans gradient)
        def get_color_for_position(row, col, max_rows, max_cols):
            if not use_gradient:
                return fill_color

            # Parse les couleurs hex
            r1, g1, b1 = tuple(int(gradient_color_start.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            r2, g2, b2 = tuple(int(gradient_color_end.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

            # Calcule le ratio selon la direction
            if gradient_direction == 'horizontal':
                ratio = col / max_cols
            elif gradient_direction == 'vertical':
                ratio = row / max_rows
            else:  # diagonal
                ratio = (row + col) / (max_rows + max_cols)

            # Interpole les couleurs
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)

            return f'#{r:02x}{g:02x}{b:02x}'

        # Dessine chaque module
        max_rows = len(modules)
        max_cols = len(modules[0]) if modules else 0

        for row in range(len(modules)):
            for col in range(len(modules[row])):
                if modules[row][col]:
                    x = (col + border_size) * box_size
                    y = (row + border_size) * box_size
                    color = get_color_for_position(row, col, max_rows, max_cols)

                    if module_style == 'rounded':
                        # Modules ronds
                        draw.ellipse([x, y, x + box_size, y + box_size], fill=color)
                    elif module_style == 'rounded-corners':
                        # Modules avec coins arrondis
                        radius = box_size // 3
                        draw.rounded_rectangle([x, y, x + box_size, y + box_size], radius=radius, fill=color)
                    else:
                        # Modules carrés
                        draw.rectangle([x, y, x + box_size, y + box_size], fill=color)
    else:
        # Génération standard
        img = qr.make_image(fill_color=fill_color, back_color=bg_color).convert("RGBA")

    # Ajout du logo si fourni
    if logo:
        try:
            logo_img = Image.open(logo).convert("RGBA")
            logo_size = img.size[0] // 5
            logo_img = logo_img.resize((logo_size, logo_size))
            pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            img.paste(logo_img, pos, logo_img)
        except:
            pass  # Ignore logo errors in preview

    # Application de la forme globale circulaire
    if global_shape == 'circle':
        size = img.size[0]
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, size, size], fill=255)

        # Crée une nouvelle image avec fond transparent
        circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        circular_img.paste(img, (0, 0))
        circular_img.putalpha(mask)
        img = circular_img

    # Ajout du cadre si activé
    if enable_frame:
        text_zone_height = 0
        if frame_text:
            text_zone_height = max(40, frame_width)

        new_width = img.size[0] + (2 * frame_width)
        new_height = img.size[1] + (2 * frame_width) + text_zone_height
        framed_img = Image.new("RGBA", (new_width, new_height), frame_color)
        qr_position = (frame_width, frame_width)
        framed_img.paste(img, qr_position)

        if frame_text:
            draw = ImageDraw.Draw(framed_img)
            frame_rgb = tuple(int(frame_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            luminance = (0.299 * frame_rgb[0] + 0.587 * frame_rgb[1] + 0.114 * frame_rgb[2]) / 255
            text_zone_bg = "#FFFFFF" if luminance < 0.5 else "#000000"
            text_color = "#000000" if luminance < 0.5 else "#FFFFFF"

            text_zone_y_start = frame_width + img.size[1]
            draw.rectangle(
                [(frame_width, text_zone_y_start),
                 (new_width - frame_width, text_zone_y_start + text_zone_height)],
                fill=text_zone_bg
            )

            try:
                font_size = max(14, min(text_zone_height - 10, 32))
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), frame_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (new_width - text_width) // 2
            text_y = text_zone_y_start + (text_zone_height - text_height) // 2
            draw.text((text_x, text_y), frame_text, fill=text_color, font=font)

        img = framed_img

    # Encode en base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


@csrf_exempt
@require_POST
def qr_preview_api(request):
    """
    Endpoint API pour l'aperçu en temps réel
    Accept JSON POST et retourne l'image QR en base64
    """
    try:
        data = json.loads(request.body)

        # Récupère le type de template
        template_type = data.get('template_type', 'text')

        # Génère le texte selon le template
        text = ''
        if template_type == 'text':
            text = data.get('text', '')
        elif template_type == 'vcard':
            text = format_vcard(
                name=data.get('vcard_name', ''),
                org=data.get('vcard_org', ''),
                phone=data.get('vcard_phone', ''),
                email=data.get('vcard_email', ''),
                url=data.get('vcard_url', '')
            )
        elif template_type == 'wifi':
            text = format_wifi(
                ssid=data.get('wifi_ssid', ''),
                password=data.get('wifi_password', ''),
                security=data.get('wifi_security', 'WPA')
            )
        elif template_type == 'email':
            text = format_email(
                to=data.get('email_to', ''),
                subject=data.get('email_subject', ''),
                body=data.get('email_body', '')
            )
        elif template_type == 'sms':
            text = format_sms(
                phone=data.get('sms_phone', ''),
                message=data.get('sms_message', '')
            )
        elif template_type == 'event':
            text = format_event(
                title=data.get('event_title', ''),
                start=data.get('event_start', ''),
                end=data.get('event_end', ''),
                location=data.get('event_location', ''),
                description=data.get('event_description', '')
            )
        elif template_type == 'geo':
            latitude = data.get('geo_latitude', '')
            longitude = data.get('geo_longitude', '')
            if latitude and longitude:
                text = format_geo(latitude=latitude, longitude=longitude)
        elif template_type == 'payment':
            text = format_payment(
                payment_type=data.get('payment_type', 'paypal'),
                recipient=data.get('payment_recipient', ''),
                amount=data.get('payment_amount', '')
            )

        if not text:
            return JsonResponse({'success': False, 'error': 'Données requises'}, status=400)

        fill_color = data.get('fill_color', '#000000') or '#000000'
        bg_color = data.get('bg_color', '#FFFFFF') or '#FFFFFF'
        border_size = int(data.get('border_size', 4))
        enable_frame = data.get('enable_frame', 'false') == 'true'
        frame_width = int(data.get('frame_width', 30))
        frame_color = data.get('frame_color', '#FFFFFF') or '#FFFFFF'
        frame_text = data.get('frame_text', '')
        use_gradient = data.get('use_gradient', 'false') == 'true'
        gradient_color_start = data.get('gradient_color_start', '#667eea') or '#667eea'
        gradient_color_end = data.get('gradient_color_end', '#764ba2') or '#764ba2'
        gradient_direction = data.get('gradient_direction', 'diagonal') or 'diagonal'
        module_style = data.get('module_style', 'square') or 'square'
        global_shape = data.get('global_shape', 'square') or 'square'

        # Génère l'image QR
        qr_image = generate_qr_image(
            text=text,
            fill_color=fill_color,
            bg_color=bg_color,
            border_size=border_size,
            enable_frame=enable_frame,
            frame_width=frame_width,
            frame_color=frame_color,
            frame_text=frame_text,
            use_gradient=use_gradient,
            gradient_color_start=gradient_color_start,
            gradient_color_end=gradient_color_end,
            gradient_direction=gradient_direction,
            module_style=module_style,
            global_shape=global_shape
        )

        return JsonResponse({'success': True, 'image': qr_image})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def batch_generate(request):
    """
    Génération en batch de QR codes depuis un fichier CSV
    Format CSV: text,filename
    Retourne un fichier ZIP contenant tous les QR codes
    """
    import csv
    import zipfile
    from io import StringIO, BytesIO as ZipBytesIO

    try:
        # Vérifie qu'un fichier a été uploadé
        if 'csv_file' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'Aucun fichier CSV fourni'}, status=400)

        csv_file = request.FILES['csv_file']

        # Lit le contenu du CSV
        csv_content = csv_file.read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(csv_content))

        # Vérifie que le CSV a les colonnes requises
        if 'text' not in csv_reader.fieldnames:
            return JsonResponse({'success': False, 'error': 'Le CSV doit contenir une colonne "text"'}, status=400)

        # Crée un fichier ZIP en mémoire
        zip_buffer = ZipBytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            count = 0
            for row in csv_reader:
                text = row.get('text', '').strip()
                if not text:
                    continue

                # Nom du fichier (utilise le champ filename si présent, sinon utilise un compteur)
                filename = row.get('filename', f'qrcode_{count + 1}').strip()
                if not filename.endswith('.png'):
                    filename += '.png'

                # Génère le QR code (utilise les paramètres par défaut)
                qr_image_data = generate_qr_image(text=text)

                # Extrait les données base64 et les convertit en bytes
                if qr_image_data.startswith('data:image/png;base64,'):
                    base64_data = qr_image_data.split(',')[1]
                    image_bytes = base64.b64decode(base64_data)

                    # Ajoute au ZIP
                    zip_file.writestr(filename, image_bytes)
                    count += 1

        if count == 0:
            return JsonResponse({'success': False, 'error': 'Aucun QR code généré. Vérifiez le contenu du CSV.'}, status=400)

        # Prépare la réponse avec le fichier ZIP
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="qrcodes_batch.zip"'

        return response

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erreur lors de la génération: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def export_pdf(request):
    """
    Export du QR code en format PDF haute résolution (600 DPI)
    Idéal pour l'impression professionnelle
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch

    try:
        data = json.loads(request.body)

        # Récupère le type de template
        template_type = data.get('template_type', 'text')

        # Génère le texte selon le template (même logique que preview)
        text = ''
        if template_type == 'text':
            text = data.get('text', '')
        elif template_type == 'vcard':
            text = format_vcard(
                name=data.get('vcard_name', ''),
                org=data.get('vcard_org', ''),
                phone=data.get('vcard_phone', ''),
                email=data.get('vcard_email', ''),
                url=data.get('vcard_url', '')
            )
        elif template_type == 'wifi':
            text = format_wifi(
                ssid=data.get('wifi_ssid', ''),
                password=data.get('wifi_password', ''),
                security=data.get('wifi_security', 'WPA')
            )
        elif template_type == 'email':
            text = format_email(
                to=data.get('email_to', ''),
                subject=data.get('email_subject', ''),
                body=data.get('email_body', '')
            )
        elif template_type == 'sms':
            text = format_sms(
                phone=data.get('sms_phone', ''),
                message=data.get('sms_message', '')
            )
        elif template_type == 'event':
            text = format_event(
                title=data.get('event_title', ''),
                start=data.get('event_start', ''),
                end=data.get('event_end', ''),
                location=data.get('event_location', ''),
                description=data.get('event_description', '')
            )
        elif template_type == 'geo':
            latitude = data.get('geo_latitude', '')
            longitude = data.get('geo_longitude', '')
            if latitude and longitude:
                text = format_geo(latitude=latitude, longitude=longitude)
        elif template_type == 'payment':
            text = format_payment(
                payment_type=data.get('payment_type', 'paypal'),
                recipient=data.get('payment_recipient', ''),
                amount=data.get('payment_amount', '')
            )

        if not text:
            return JsonResponse({'success': False, 'error': 'Données requises'}, status=400)

        # Récupère les paramètres de personnalisation
        fill_color = data.get('fill_color', '#000000') or '#000000'
        bg_color = data.get('bg_color', '#FFFFFF') or '#FFFFFF'
        border_size = int(data.get('border_size', 4))
        enable_frame = data.get('enable_frame', 'false') == 'true'
        frame_width = int(data.get('frame_width', 30))
        frame_color = data.get('frame_color', '#FFFFFF') or '#FFFFFF'
        frame_text = data.get('frame_text', '')
        use_gradient = data.get('use_gradient', 'false') == 'true'
        gradient_color_start = data.get('gradient_color_start', '#667eea') or '#667eea'
        gradient_color_end = data.get('gradient_color_end', '#764ba2') or '#764ba2'
        gradient_direction = data.get('gradient_direction', 'diagonal') or 'diagonal'
        module_style = data.get('module_style', 'square') or 'square'
        global_shape = data.get('global_shape', 'square') or 'square'

        # Génère le QR code en haute résolution (600 DPI)
        # Pour 600 DPI, on utilise un box_size plus grand
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=25,  # Plus grand pour haute résolution
            border=border_size
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Génère l'image haute résolution
        if module_style != 'square' or use_gradient:
            modules = qr.modules
            box_size = 25
            size = (len(modules) + border_size * 2) * box_size
            img = Image.new('RGBA', (size, size), bg_color)
            draw = ImageDraw.Draw(img)

            def get_color_for_position(row, col, max_rows, max_cols):
                if not use_gradient:
                    return fill_color
                r1, g1, b1 = tuple(int(gradient_color_start.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(gradient_color_end.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                if gradient_direction == 'horizontal':
                    ratio = col / max_cols
                elif gradient_direction == 'vertical':
                    ratio = row / max_rows
                else:
                    ratio = (row + col) / (max_rows + max_cols)
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                return f'#{r:02x}{g:02x}{b:02x}'

            max_rows = len(modules)
            max_cols = len(modules[0]) if modules else 0
            for row in range(len(modules)):
                for col in range(len(modules[row])):
                    if modules[row][col]:
                        x = (col + border_size) * box_size
                        y = (row + border_size) * box_size
                        color = get_color_for_position(row, col, max_rows, max_cols)
                        if module_style == 'rounded':
                            draw.ellipse([x, y, x + box_size, y + box_size], fill=color)
                        elif module_style == 'rounded-corners':
                            radius = box_size // 3
                            draw.rounded_rectangle([x, y, x + box_size, y + box_size], radius=radius, fill=color)
                        else:
                            draw.rectangle([x, y, x + box_size, y + box_size], fill=color)
        else:
            img = qr.make_image(fill_color=fill_color, back_color=bg_color).convert("RGBA")

        # Application de la forme circulaire si demandée
        if global_shape == 'circle':
            size = img.size[0]
            mask = Image.new('L', (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, size, size], fill=255)
            circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            circular_img.paste(img, (0, 0))
            circular_img.putalpha(mask)
            img = circular_img

        # Ajout du cadre si activé
        if enable_frame:
            text_zone_height = 0
            if frame_text:
                text_zone_height = max(60, frame_width)
            new_width = img.size[0] + (2 * frame_width)
            new_height = img.size[1] + (2 * frame_width) + text_zone_height
            framed_img = Image.new("RGBA", (new_width, new_height), frame_color)
            qr_position = (frame_width, frame_width)
            framed_img.paste(img, qr_position)

            if frame_text:
                draw = ImageDraw.Draw(framed_img)
                frame_rgb = tuple(int(frame_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                luminance = (0.299 * frame_rgb[0] + 0.587 * frame_rgb[1] + 0.114 * frame_rgb[2]) / 255
                text_zone_bg = "#FFFFFF" if luminance < 0.5 else "#000000"
                text_color = "#000000" if luminance < 0.5 else "#FFFFFF"
                text_zone_y_start = frame_width + img.size[1]
                draw.rectangle(
                    [(frame_width, text_zone_y_start),
                     (new_width - frame_width, text_zone_y_start + text_zone_height)],
                    fill=text_zone_bg
                )
                try:
                    font_size = max(20, min(text_zone_height - 10, 48))
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                bbox = draw.textbbox((0, 0), frame_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = (new_width - text_width) // 2
                text_y = text_zone_y_start + (text_zone_height - text_height) // 2
                draw.text((text_x, text_y), frame_text, fill=text_color, font=font)

            img = framed_img

        # Sauvegarde l'image temporairement
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG', dpi=(600, 600))
        img_buffer.seek(0)

        # Crée le PDF
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Calcule les dimensions pour centrer le QR code
        page_width, page_height = letter
        # Taille du QR code sur la page (4 inches = environ 10cm)
        qr_display_size = 4 * inch
        x = (page_width - qr_display_size) / 2
        y = (page_height - qr_display_size) / 2

        # Sauvegarde l'image temporairement pour reportlab
        temp_img_path = '/tmp/qr_temp.png'
        img.save(temp_img_path, format='PNG', dpi=(600, 600))

        # Dessine l'image sur le PDF
        c.drawImage(temp_img_path, x, y, width=qr_display_size, height=qr_display_size, preserveAspectRatio=True)

        # Finalise le PDF
        c.save()

        # Prépare la réponse
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="qrcode_{int(data.get("timestamp", 0))}.pdf"'

        return response

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erreur lors de la génération PDF: {str(e)}'}, status=500)