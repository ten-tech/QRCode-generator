from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import QRCodeForm
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import zipfile
import csv


def qr_code_generator(request):
    form = QRCodeForm()

    context = {
        'form': form,
        'qr_image_data': None,
    }

    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupère le type de template
            template_type = form.cleaned_data.get('template_type', 'text')

            # Génère le texte selon le template
            if template_type == 'text':
                text = form.cleaned_data['text']
            elif template_type == 'vcard':
                text = format_vcard(
                    name=form.cleaned_data.get('vcard_name', ''),
                    org=form.cleaned_data.get('vcard_org', ''),
                    phone=form.cleaned_data.get('vcard_phone', ''),
                    email=form.cleaned_data.get('vcard_email', ''),
                    url=form.cleaned_data.get('vcard_url', '')
                )
            elif template_type == 'wifi':
                text = format_wifi(
                    ssid=form.cleaned_data.get('wifi_ssid', ''),
                    password=form.cleaned_data.get('wifi_password', ''),
                    security=form.cleaned_data.get('wifi_security', 'WPA')
                )
            elif template_type == 'email':
                text = format_email(
                    to=form.cleaned_data.get('email_to', ''),
                    subject=form.cleaned_data.get('email_subject', ''),
                    body=form.cleaned_data.get('email_body', '')
                )
            elif template_type == 'sms':
                text = format_sms(
                    phone=form.cleaned_data.get('sms_phone', ''),
                    message=form.cleaned_data.get('sms_message', '')
                )
            elif template_type == 'event':
                text = format_event(
                    title=form.cleaned_data.get('event_title', ''),
                    start=form.cleaned_data.get('event_start', ''),
                    end=form.cleaned_data.get('event_end', ''),
                    location=form.cleaned_data.get('event_location', ''),
                    description=form.cleaned_data.get('event_description', '')
                )
            elif template_type == 'geo':
                latitude = form.cleaned_data.get('geo_latitude', '')
                longitude = form.cleaned_data.get('geo_longitude', '')
                if latitude and longitude:
                    text = format_geo(latitude=latitude, longitude=longitude)
                else:
                    text = ''
            elif template_type == 'payment':
                text = format_payment(
                    payment_type=form.cleaned_data.get('payment_type', 'paypal'),
                    recipient=form.cleaned_data.get('payment_recipient', ''),
                    amount=form.cleaned_data.get('payment_amount', '')
                )
            else:
                text = form.cleaned_data.get('text', '')

            fill_color = form.cleaned_data.get('fill_color', 'black') or 'black'
            bg_color = form.cleaned_data.get('bg_color', 'white') or 'white'
            border_size = form.cleaned_data.get('border_size', 4)
            logo = form.cleaned_data.get('logo')
            enable_frame = form.cleaned_data.get('enable_frame', False)
            frame_width = form.cleaned_data.get('frame_width', 30)
            frame_color = form.cleaned_data.get('frame_color', '#FFFFFF') or '#FFFFFF'
            frame_text = form.cleaned_data.get('frame_text', '')
            use_gradient = form.cleaned_data.get('use_gradient', False)
            gradient_color_start = form.cleaned_data.get('gradient_color_start', '#667eea') or '#667eea'
            gradient_color_end = form.cleaned_data.get('gradient_color_end', '#764ba2') or '#764ba2'
            gradient_direction = form.cleaned_data.get('gradient_direction', 'diagonal') or 'diagonal'
            module_style = form.cleaned_data.get('module_style', 'square') or 'square'
            global_shape = form.cleaned_data.get('global_shape', 'square') or 'square'

            # Génère l'image QR
            qr_image_data = generate_qr_image(
                text=text,
                fill_color=fill_color,
                bg_color=bg_color,
                border_size=border_size,
                logo=logo,
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

            context['qr_image_data'] = qr_image_data
            context['form'] = form

    return render(request, 'qr_code/generator.html', context)


def format_vcard(name, org="", phone="", email="", url=""):
    """Format vCard 3.0"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
"""
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
    """Format WiFi MECARD"""
    wifi = f"WIFI:T:{security};S:{ssid};P:{password};;"
    return wifi


def format_email(to, subject="", body=""):
    """Format email mailto"""
    email = f"mailto:{to}"
    params = []
    if subject:
        params.append(f"subject={subject}")
    if body:
        params.append(f"body={body}")
    if params:
        email += "?" + "&".join(params)
    return email


def format_sms(phone, message=""):
    """Format SMS"""
    sms = f"smsto:{phone}"
    if message:
        sms += f":{message}"
    return sms


def format_event(title, start="", end="", location="", description=""):
    """Format iCalendar event"""
    event = f"""BEGIN:VEVENT
SUMMARY:{title}
"""
    if start:
        # Format attendu: YYYYMMDDTHHMMSS
        start_formatted = start.replace('-', '').replace(':', '')
        event += f"DTSTART:{start_formatted}\n"
    if end:
        end_formatted = end.replace('-', '').replace(':', '')
        event += f"DTEND:{end_formatted}\n"
    if location:
        event += f"LOCATION:{location}\n"
    if description:
        event += f"DESCRIPTION:{description}\n"
    event += "END:VEVENT"
    return event


def format_geo(latitude, longitude):
    """Format geolocation"""
    geo = f"geo:{latitude},{longitude}"
    return geo


def format_payment(payment_type, recipient, amount=""):
    """Format payment URI (PayPal or Bitcoin)"""
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
        error_correction=qrcode.constants.ERROR_CORRECT_H if logo else qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=border_size,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Crée l'image de base
    if use_gradient or module_style != 'square' or global_shape != 'square':
        # Mode personnalisé avec PIL
        img = Image.new('RGB', (qr.modules_count * 10 + border_size * 20,
                                 qr.modules_count * 10 + border_size * 20), bg_color)
        draw = ImageDraw.Draw(img)

        # Fonction pour calculer la couleur du gradient
        def get_gradient_color(row, col):
            if not use_gradient:
                return fill_color

            # Parse les couleurs hex
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

            start_rgb = hex_to_rgb(gradient_color_start)
            end_rgb = hex_to_rgb(gradient_color_end)

            # Calcule le ratio selon la direction
            if gradient_direction == 'horizontal':
                ratio = col / qr.modules_count
            elif gradient_direction == 'vertical':
                ratio = row / qr.modules_count
            else:  # diagonal
                ratio = (row + col) / (qr.modules_count * 2)

            # Interpole les couleurs
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

            return f'#{r:02x}{g:02x}{b:02x}'

        # Dessine les modules
        for row in range(qr.modules_count):
            for col in range(qr.modules_count):
                if qr.modules[row][col]:
                    color = get_gradient_color(row, col)
                    x = col * 10 + border_size * 10
                    y = row * 10 + border_size * 10

                    if module_style == 'rounded':
                        # Cercles
                        draw.ellipse([x, y, x + 10, y + 10], fill=color)
                    elif module_style == 'rounded-corners':
                        # Carrés avec coins arrondis
                        draw.rounded_rectangle([x, y, x + 10, y + 10], radius=2, fill=color)
                    else:
                        # Carrés normaux
                        draw.rectangle([x, y, x + 10, y + 10], fill=color)

        # Applique la forme globale circulaire si demandé
        if global_shape == 'circle':
            # Crée un masque circulaire
            mask = Image.new('L', img.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, img.size[0], img.size[1]], fill=255)

            # Applique le masque
            output = Image.new('RGBA', img.size, (0, 0, 0, 0))
            output.paste(img, (0, 0))
            output.putalpha(mask)
            img = output
    else:
        # Mode simple sans gradient
        img = qr.make_image(fill_color=fill_color, back_color=bg_color)
        img = img.convert('RGB')

    # Ajoute le logo au centre si fourni
    if logo:
        try:
            if hasattr(logo, 'read'):
                logo_img = Image.open(logo)
            else:
                logo_img = Image.open(io.BytesIO(logo.read()))

            # Redimensionne le logo (max 20% de la taille du QR)
            qr_width, qr_height = img.size
            logo_size = min(qr_width, qr_height) // 5
            logo_img.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Centre le logo
            logo_pos = ((qr_width - logo_img.size[0]) // 2,
                       (qr_height - logo_img.size[1]) // 2)

            # Colle le logo
            if img.mode == 'RGBA':
                img.paste(logo_img, logo_pos, logo_img if logo_img.mode == 'RGBA' else None)
            else:
                img = img.convert('RGBA')
                img.paste(logo_img, logo_pos, logo_img if logo_img.mode == 'RGBA' else None)
        except Exception as e:
            print(f"Erreur lors de l'ajout du logo: {e}")

    # Ajoute un cadre avec texte si demandé
    if enable_frame and frame_text:
        # Ajoute de l'espace pour le cadre
        frame_img = Image.new('RGB',
                             (img.width + frame_width * 2,
                              img.height + frame_width * 2),
                             frame_color)
        frame_img.paste(img, (frame_width, frame_width))

        # Ajoute le texte
        draw = ImageDraw.Draw(frame_img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), frame_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (frame_img.width - text_width) // 2
        text_y = frame_img.height - frame_width + 5

        draw.text((text_x, text_y), frame_text, fill=fill_color, font=font)
        img = frame_img

    # Convertit en base64
    buffer = io.BytesIO()
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


@csrf_exempt
@require_POST
def qr_preview_api(request):
    """
    Endpoint API pour l'aperçu en temps réel
    Accept JSON ou FormData POST et retourne l'image QR en base64
    """
    try:
        # Vérifie si c'est du FormData (avec fichier) ou du JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = request.POST.dict()
            logo_file = request.FILES.get('logo')
        else:
            data = json.loads(request.body)
            logo_file = None

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
            logo=logo_file,
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
    Retourne un fichier ZIP avec tous les QR codes
    """
    try:
        if 'csv_file' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'Fichier CSV requis'}, status=400)

        csv_file = request.FILES['csv_file']

        # Crée un buffer pour le ZIP
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Parse le CSV
            csv_content = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))

            for row in csv_reader:
                text = row.get('text', '')
                filename = row.get('filename', f'qr_{len(zip_file.namelist())}')

                if not text:
                    continue

                # Génère le QR code (simple, sans options)
                qr_image_data = generate_qr_image(text=text)

                # Extrait les données base64
                if qr_image_data.startswith('data:image/png;base64,'):
                    img_data = base64.b64decode(qr_image_data.split(',')[1])

                    # Ajoute au ZIP
                    zip_file.writestr(f'{filename}.png', img_data)

        # Prépare la réponse
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="qrcodes_batch.zip"'

        return response

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erreur: {str(e)}'}, status=500)


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

        # Génère le QR code haute résolution (600 DPI)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=25,  # Plus grand pour 600 DPI
            border=border_size,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Crée l'image
        if use_gradient or module_style != 'square' or global_shape != 'square':
            img = Image.new('RGB', (qr.modules_count * 25 + border_size * 50,
                                     qr.modules_count * 25 + border_size * 50), bg_color)
            draw = ImageDraw.Draw(img)

            def get_gradient_color(row, col):
                if not use_gradient:
                    return fill_color

                def hex_to_rgb(hex_color):
                    hex_color = hex_color.lstrip('#')
                    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

                start_rgb = hex_to_rgb(gradient_color_start)
                end_rgb = hex_to_rgb(gradient_color_end)

                if gradient_direction == 'horizontal':
                    ratio = col / qr.modules_count
                elif gradient_direction == 'vertical':
                    ratio = row / qr.modules_count
                else:
                    ratio = (row + col) / (qr.modules_count * 2)

                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

                return f'#{r:02x}{g:02x}{b:02x}'

            for row in range(qr.modules_count):
                for col in range(qr.modules_count):
                    if qr.modules[row][col]:
                        color = get_gradient_color(row, col)
                        x = col * 25 + border_size * 25
                        y = row * 25 + border_size * 25

                        if module_style == 'rounded':
                            draw.ellipse([x, y, x + 25, y + 25], fill=color)
                        elif module_style == 'rounded-corners':
                            draw.rounded_rectangle([x, y, x + 25, y + 25], radius=5, fill=color)
                        else:
                            draw.rectangle([x, y, x + 25, y + 25], fill=color)

            if global_shape == 'circle':
                mask = Image.new('L', img.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, img.size[0], img.size[1]], fill=255)
                output = Image.new('RGBA', img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)
                img = output
        else:
            img = qr.make_image(fill_color=fill_color, back_color=bg_color)
            img = img.convert('RGB')

        # Ajoute le cadre si demandé
        if enable_frame and frame_text:
            frame_img = Image.new('RGB',
                                 (img.width + frame_width * 2,
                                  img.height + frame_width * 2),
                                 frame_color)
            frame_img.paste(img, (frame_width, frame_width))

            draw = ImageDraw.Draw(frame_img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
            except:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), frame_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (frame_img.width - text_width) // 2
            text_y = frame_img.height - frame_width + 10

            draw.text((text_x, text_y), frame_text, fill=fill_color, font=font)
            img = frame_img

        # Crée le PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
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


@csrf_exempt
@require_POST
def export_business_card(request):
    """
    Export d'une carte de visite professionnelle avec QR code vCard
    Format: 85mm × 55mm (standard carte de visite)
    Résolution: 300 DPI pour impression professionnelle
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib import colors as reportlab_colors
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    try:
        data = json.loads(request.body)

        # Vérifie que c'est bien un vCard
        if data.get('template_type') != 'vcard':
            return JsonResponse({'success': False, 'error': 'Cette fonctionnalité est uniquement pour les vCard'}, status=400)

        # Récupère les données vCard
        vcard_name = data.get('vcard_name', '')
        vcard_org = data.get('vcard_org', '')
        vcard_phone = data.get('vcard_phone', '')
        vcard_email = data.get('vcard_email', '')
        vcard_url = data.get('vcard_url', '')

        if not vcard_name:
            return JsonResponse({'success': False, 'error': 'Le nom est requis pour la carte de visite'}, status=400)

        # Récupère les paramètres de design
        card_layout = data.get('card_layout', 'left')
        card_bg_color = data.get('card_bg_color', '#FFFFFF')
        card_text_color = data.get('card_text_color', '#2c3e50')
        card_accent_color = data.get('card_accent_color', '#667eea')

        # Génère le texte vCard pour le QR code
        vcard_text = format_vcard(
            name=vcard_name,
            org=vcard_org,
            phone=vcard_phone,
            email=vcard_email,
            url=vcard_url
        )

        # Génère le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(vcard_text)
        qr.make(fit=True)

        # Crée l'image QR
        qr_img = qr.make_image(fill_color=card_text_color, back_color=card_bg_color)
        qr_img = qr_img.convert('RGB')

        # Sauvegarde temporairement le QR code
        qr_temp_path = '/tmp/qr_business_card.png'
        qr_img.save(qr_temp_path, format='PNG', dpi=(300, 300))

        # Dimensions de la carte de visite (85mm × 55mm)
        card_width = 85 * mm
        card_height = 55 * mm

        # Crée le PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=(card_width, card_height))

        # Convertit les couleurs hex en RGB
        def hex_to_rgb_normalized(hex_color):
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return r/255.0, g/255.0, b/255.0

        bg_rgb = hex_to_rgb_normalized(card_bg_color)
        text_rgb = hex_to_rgb_normalized(card_text_color)
        accent_rgb = hex_to_rgb_normalized(card_accent_color)

        # Fond de la carte
        c.setFillColorRGB(*bg_rgb)
        c.rect(0, 0, card_width, card_height, fill=1, stroke=0)

        # Taille du QR code (20mm × 20mm)
        qr_size = 20 * mm

        # Position du QR code selon le layout
        if card_layout == 'left':
            qr_x = 5 * mm
            qr_y = (card_height - qr_size) / 2
            info_x_start = 30 * mm
        elif card_layout == 'right':
            qr_x = card_width - qr_size - 5 * mm
            qr_y = (card_height - qr_size) / 2
            info_x_start = 5 * mm
        else:  # center
            qr_x = (card_width - qr_size) / 2
            qr_y = card_height - qr_size - 3 * mm
            info_x_start = 5 * mm

        # Dessine le QR code
        c.drawImage(qr_temp_path, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=True)

        # Ajoute les informations textuelles
        c.setFillColorRGB(*text_rgb)

        # Nom (gros et gras)
        c.setFont("Helvetica-Bold", 14)
        if card_layout == 'center':
            y_offset = card_height - qr_size - 8 * mm
        else:
            y_offset = card_height - 10 * mm
        c.drawString(info_x_start, y_offset, vcard_name)

        # Titre/Organisation
        c.setFillColorRGB(*accent_rgb)
        c.setFont("Helvetica", 10)
        y_offset -= 5 * mm
        if vcard_org:
            c.drawString(info_x_start, y_offset, vcard_org)
            y_offset -= 5 * mm

        # Coordonnées
        c.setFillColorRGB(*text_rgb)
        c.setFont("Helvetica", 8)

        if vcard_phone:
            c.drawString(info_x_start, y_offset, f"📱 {vcard_phone}")
            y_offset -= 4 * mm

        if vcard_email:
            c.drawString(info_x_start, y_offset, f"✉  {vcard_email}")
            y_offset -= 4 * mm

        if vcard_url:
            c.setFillColorRGB(*accent_rgb)
            c.drawString(info_x_start, y_offset, f"🌐 {vcard_url}")

        # Ligne d'accent décorative (optionnelle)
        c.setStrokeColorRGB(*accent_rgb)
        c.setLineWidth(0.5 * mm)
        if card_layout != 'center':
            c.line(info_x_start, 8 * mm, card_width - 5 * mm, 8 * mm)

        # Finalise le PDF
        c.save()

        # Prépare la réponse
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        filename = f"carte_visite_{vcard_name.replace(' ', '_')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erreur lors de la génération de la carte: {str(e)}'}, status=500)
