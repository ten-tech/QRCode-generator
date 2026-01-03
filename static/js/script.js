document.addEventListener('DOMContentLoaded', function() {
    // ========== GESTION DU THÈME SOMBRE ==========
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Détecte la préférence système
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Charge le thème sauvegardé ou utilise la préférence système
    const savedTheme = localStorage.getItem('theme') || (prefersDark ? 'dark' : 'light');
    htmlElement.setAttribute('data-theme', savedTheme);

    // Met à jour l'état du toggle
    if (savedTheme === 'dark') {
        themeToggle.classList.add('active');
    }

    // Toggle au clic
    themeToggle.addEventListener('click', function() {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        themeToggle.classList.toggle('active');
    });

    // ========== SWITCH DE TEMPLATES ==========
    const templateRadios = document.querySelectorAll('.template-radio');
    const templateFieldsSections = document.querySelectorAll('.template-fields');

    function switchTemplate() {
        const selectedTemplate = document.querySelector('.template-radio:checked')?.value || 'text';

        // Masque tous les champs de templates
        templateFieldsSections.forEach(section => {
            section.style.display = 'none';
        });

        // Affiche les champs du template sélectionné
        const selectedSection = document.querySelector(`.template-fields[data-template="${selectedTemplate}"]`);
        if (selectedSection) {
            selectedSection.style.display = 'block';
        }
    }

    templateRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Sauvegarde le template sélectionné dans localStorage
            localStorage.setItem('selectedTemplate', this.value);
            switchTemplate();
            // Déclenche la mise à jour de l'aperçu quand le template change
            debouncedPreview();
        });
    });

    // Restaure le template sauvegardé
    const savedTemplate = localStorage.getItem('selectedTemplate');
    if (savedTemplate) {
        const savedRadio = document.querySelector(`.template-radio[value="${savedTemplate}"]`);
        if (savedRadio) {
            savedRadio.checked = true;
        }
    }

    // Initialise l'affichage du template
    switchTemplate();

    // Synchronisation des sélecteurs de couleur
    const fillColorInput = document.getElementById('id_fill_color');
    const bgColorInput = document.getElementById('id_bg_color');

    if (fillColorInput) {
        const fillPreview = document.getElementById('fill-color-preview');
        fillColorInput.addEventListener('input', function() {
            fillPreview.textContent = this.value.toUpperCase();
            fillPreview.style.background = this.value;
            fillPreview.style.color = getContrastColor(this.value);
        });
        // Initialise l'aperçu
        fillPreview.textContent = fillColorInput.value.toUpperCase();
        fillPreview.style.background = fillColorInput.value;
        fillPreview.style.color = getContrastColor(fillColorInput.value);
    }

    if (bgColorInput) {
        const bgPreview = document.getElementById('bg-color-preview');
        bgColorInput.addEventListener('input', function() {
            bgPreview.textContent = this.value.toUpperCase();
            bgPreview.style.background = this.value;
            bgPreview.style.color = getContrastColor(this.value);
        });
        // Initialise l'aperçu
        bgPreview.textContent = bgColorInput.value.toUpperCase();
        bgPreview.style.background = bgColorInput.value;
        bgPreview.style.color = getContrastColor(bgColorInput.value);
    }

    // Validation de la taille de bordure
    const borderInput = document.getElementById('id_border_size');
    if (borderInput) {
        borderInput.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (value < 0) this.value = 0;
            if (value > 20) this.value = 20;
        });
    }

    // Fonctionnalité de toggle du cadre
    const frameToggle = document.getElementById('id_enable_frame');
    const frameOptions = document.getElementById('frame-options');

    function toggleFrameOptions() {
        if (frameToggle && frameOptions) {
            if (frameToggle.checked) {
                frameOptions.classList.remove('disabled');
            } else {
                frameOptions.classList.add('disabled');
            }
        }
    }

    if (frameToggle) {
        // Initialise au chargement
        toggleFrameOptions();

        frameToggle.addEventListener('change', toggleFrameOptions);
    }

    // Validation de la largeur du cadre
    const frameWidthInput = document.getElementById('id_frame_width');
    if (frameWidthInput) {
        frameWidthInput.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (value < 10) this.value = 10;
            if (value > 100) this.value = 100;
        });
    }

    // Aperçu du sélecteur de couleur du cadre
    const frameColorInput = document.getElementById('id_frame_color');
    if (frameColorInput) {
        const frameColorPreview = document.getElementById('frame-color-preview');
        frameColorInput.addEventListener('input', function() {
            frameColorPreview.textContent = this.value.toUpperCase();
            frameColorPreview.style.background = this.value;
            frameColorPreview.style.color = getContrastColor(this.value);
        });
        // Initialise l'aperçu
        frameColorPreview.textContent = frameColorInput.value.toUpperCase();
        frameColorPreview.style.background = frameColorInput.value;
        frameColorPreview.style.color = getContrastColor(frameColorInput.value);
    }

    // ========== GESTION DU GRADIENT ==========
    const gradientToggle = document.getElementById('id_use_gradient');
    const gradientOptions = document.getElementById('gradient-options');

    function toggleGradientOptions() {
        if (gradientToggle && gradientOptions) {
            if (gradientToggle.checked) {
                gradientOptions.style.display = 'block';
            } else {
                gradientOptions.style.display = 'none';
            }
        }
    }

    if (gradientToggle) {
        // Initialise au chargement
        toggleGradientOptions();
        gradientToggle.addEventListener('change', toggleGradientOptions);
    }

    // Aperçu des couleurs du dégradé
    const gradientStartInput = document.getElementById('id_gradient_color_start');
    const gradientEndInput = document.getElementById('id_gradient_color_end');

    if (gradientStartInput) {
        const gradientStartPreview = document.getElementById('gradient-start-preview');
        gradientStartInput.addEventListener('input', function() {
            gradientStartPreview.textContent = this.value.toUpperCase();
            gradientStartPreview.style.background = this.value;
            gradientStartPreview.style.color = getContrastColor(this.value);
        });
        // Initialise l'aperçu
        gradientStartPreview.textContent = gradientStartInput.value.toUpperCase();
        gradientStartPreview.style.background = gradientStartInput.value;
        gradientStartPreview.style.color = getContrastColor(gradientStartInput.value);
    }

    if (gradientEndInput) {
        const gradientEndPreview = document.getElementById('gradient-end-preview');
        gradientEndInput.addEventListener('input', function() {
            gradientEndPreview.textContent = this.value.toUpperCase();
            gradientEndPreview.style.background = this.value;
            gradientEndPreview.style.color = getContrastColor(this.value);
        });
        // Initialise l'aperçu
        gradientEndPreview.textContent = gradientEndInput.value.toUpperCase();
        gradientEndPreview.style.background = gradientEndInput.value;
        gradientEndPreview.style.color = getContrastColor(gradientEndInput.value);
    }

    // Affichage du fichier uploadé
    const fileInput = document.getElementById('id_logo');
    const fileName = document.getElementById('file-name');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileName.textContent = 'Fichier: ' + this.files[0].name;
                fileName.style.fontStyle = 'normal';
                fileName.style.color = '#2ecc71';
            } else {
                fileName.textContent = 'Aucun fichier choisi';
                fileName.style.fontStyle = 'italic';
                fileName.style.color = '#7f8c8d';
            }
        });
    }

    // ========== GESTION CARTE DE VISITE ==========
    const businessCardToggle = document.getElementById('id_enable_business_card');
    const businessCardOptions = document.getElementById('business-card-options');

    function toggleBusinessCardOptions() {
        if (businessCardToggle && businessCardOptions) {
            if (businessCardToggle.checked) {
                businessCardOptions.classList.add('active');
            } else {
                businessCardOptions.classList.remove('active');
            }
        }
    }

    if (businessCardToggle) {
        toggleBusinessCardOptions();
        businessCardToggle.addEventListener('change', toggleBusinessCardOptions);
    }

    // Synchronisation des color pickers pour la carte de visite
    const cardBgColorInput = document.getElementById('id_card_bg_color');
    const cardTextColorInput = document.getElementById('id_card_text_color');
    const cardAccentColorInput = document.getElementById('id_card_accent_color');

    if (cardBgColorInput) {
        const preview = document.getElementById('card-bg-color-preview');
        cardBgColorInput.addEventListener('input', function() {
            preview.textContent = this.value.toUpperCase();
            preview.style.background = this.value;
            preview.style.color = getContrastColor(this.value);
        });
        preview.textContent = cardBgColorInput.value.toUpperCase();
        preview.style.background = cardBgColorInput.value;
        preview.style.color = getContrastColor(cardBgColorInput.value);
    }

    if (cardTextColorInput) {
        const preview = document.getElementById('card-text-color-preview');
        cardTextColorInput.addEventListener('input', function() {
            preview.textContent = this.value.toUpperCase();
            preview.style.background = this.value;
            preview.style.color = getContrastColor(this.value);
        });
        preview.textContent = cardTextColorInput.value.toUpperCase();
        preview.style.background = cardTextColorInput.value;
        preview.style.color = getContrastColor(cardTextColorInput.value);
    }

    if (cardAccentColorInput) {
        const preview = document.getElementById('card-accent-color-preview');
        cardAccentColorInput.addEventListener('input', function() {
            preview.textContent = this.value.toUpperCase();
            preview.style.background = this.value;
            preview.style.color = getContrastColor(this.value);
        });
        preview.textContent = cardAccentColorInput.value.toUpperCase();
        preview.style.background = cardAccentColorInput.value;
        preview.style.color = getContrastColor(cardAccentColorInput.value);
    }

    // Téléchargement de la carte de visite
    const downloadBusinessCardBtn = document.getElementById('download-business-card');
    if (downloadBusinessCardBtn) {
        downloadBusinessCardBtn.addEventListener('click', async function() {
            // Vérifie que le template vCard est sélectionné
            const selectedTemplate = document.querySelector('.template-radio:checked')?.value;
            if (selectedTemplate !== 'vcard') {
                alert('La carte de visite est uniquement disponible pour le template vCard');
                return;
            }

            // Vérifie que les données vCard minimales sont présentes
            const vcardName = document.getElementById('id_vcard_name')?.value;
            if (!vcardName) {
                alert('Le nom est requis pour générer la carte de visite');
                return;
            }

            // Collecte les données
            const data = {
                template_type: 'vcard',
                vcard_name: vcardName,
                vcard_org: document.getElementById('id_vcard_org')?.value || '',
                vcard_phone: document.getElementById('id_vcard_phone')?.value || '',
                vcard_email: document.getElementById('id_vcard_email')?.value || '',
                vcard_url: document.getElementById('id_vcard_url')?.value || '',
                card_layout: document.getElementById('id_card_layout')?.value || 'left',
                card_bg_color: cardBgColorInput?.value || '#FFFFFF',
                card_text_color: cardTextColorInput?.value || '#2c3e50',
                card_accent_color: cardAccentColorInput?.value || '#667eea'
            };

            try {
                // Désactive le bouton pendant le téléchargement
                downloadBusinessCardBtn.disabled = true;
                downloadBusinessCardBtn.textContent = 'Génération en cours...';

                const response = await fetch('/api/export-business-card', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    // Télécharge le PDF
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `carte_visite_${vcardName.replace(' ', '_')}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } else {
                    const error = await response.json();
                    alert('Erreur: ' + (error.error || 'Erreur lors de la génération'));
                }
            } catch (error) {
                alert('Erreur lors de la génération de la carte: ' + error.message);
            } finally {
                // Réactive le bouton
                downloadBusinessCardBtn.disabled = false;
                downloadBusinessCardBtn.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Télécharger Carte PDF
                `;
            }
        });
    }

    // Fonctionnalité de téléchargement PNG
    const downloadPngBtn = document.getElementById('download-png-btn');
    if (downloadPngBtn) {
        downloadPngBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const qrImage = document.getElementById('qr-img');
            if (qrImage) {
                const link = document.createElement('a');
                link.href = qrImage.src;
                link.download = 'qrcode_' + Date.now() + '.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Feedback visuel
                const originalHTML = this.innerHTML;
                this.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9 12l2 2 4-4"></path></svg>OK';
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                }, 2000);
            }
        });
    }

    // Fonctionnalité de téléchargement SVG
    const downloadSvgBtn = document.getElementById('download-svg-btn');
    if (downloadSvgBtn) {
        downloadSvgBtn.addEventListener('click', function(e) {
            e.preventDefault();

            // Récupère le template sélectionné et collecte les données
            const selectedTemplate = document.querySelector('.template-radio:checked')?.value || 'text';
            let qrText = '';

            // Collecte les données selon le template
            if (selectedTemplate === 'text') {
                qrText = textInput?.value.trim() || '';
            } else if (selectedTemplate === 'vcard') {
                const name = document.getElementById('id_vcard_name')?.value || '';
                const org = document.getElementById('id_vcard_org')?.value || '';
                const phone = document.getElementById('id_vcard_phone')?.value || '';
                const email = document.getElementById('id_vcard_email')?.value || '';
                const url = document.getElementById('id_vcard_url')?.value || '';
                qrText = generateVCardText(name, org, phone, email, url);
            } else if (selectedTemplate === 'wifi') {
                const ssid = document.getElementById('id_wifi_ssid')?.value || '';
                const password = document.getElementById('id_wifi_password')?.value || '';
                const security = document.getElementById('id_wifi_security')?.value || 'WPA';
                qrText = `WIFI:T:${security};S:${ssid};P:${password};;`;
            } else if (selectedTemplate === 'email') {
                const to = document.getElementById('id_email_to')?.value || '';
                const subject = document.getElementById('id_email_subject')?.value || '';
                const body = document.getElementById('id_email_body')?.value || '';
                qrText = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            } else if (selectedTemplate === 'sms') {
                const phone = document.getElementById('id_sms_phone')?.value || '';
                const message = document.getElementById('id_sms_message')?.value || '';
                qrText = `sms:${phone}?body=${encodeURIComponent(message)}`;
            }

            if (!qrText) return;

            // Génère le QR code SVG
            const qr = qrcode(0, 'H');
            qr.addData(qrText);
            qr.make();

            // Récupère les couleurs
            const fillColor = fillColorInput?.value || '#000000';
            const bgColor = bgColorInput?.value || '#FFFFFF';

            // Crée le SVG avec les couleurs personnalisées
            const cellSize = 10;
            const moduleCount = qr.getModuleCount();
            const borderSize = parseInt(borderInput?.value || '4');
            const svgSize = (moduleCount + borderSize * 2) * cellSize;

            let svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}" height="${svgSize}" viewBox="0 0 ${svgSize} ${svgSize}">`;
            svgContent += `<rect width="100%" height="100%" fill="${bgColor}"/>`;

            for (let row = 0; row < moduleCount; row++) {
                for (let col = 0; col < moduleCount; col++) {
                    if (qr.isDark(row, col)) {
                        const x = (col + borderSize) * cellSize;
                        const y = (row + borderSize) * cellSize;
                        svgContent += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" fill="${fillColor}"/>`;
                    }
                }
            }
            svgContent += '</svg>';

            // Télécharge le SVG
            const blob = new Blob([svgContent], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'qrcode_' + Date.now() + '.svg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);

            // Feedback visuel
            const originalHTML = this.innerHTML;
            this.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9 12l2 2 4-4"></path></svg>OK';
            setTimeout(() => {
                this.innerHTML = originalHTML;
            }, 2000);
        });
    }

    // Fonctionnalité de téléchargement PDF
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', async function(e) {
            e.preventDefault();

            // Récupère le template sélectionné et collecte les données
            const selectedTemplate = document.querySelector('.template-radio:checked')?.value || 'text';

            // Collecte les données communes
            const formData = {
                template_type: selectedTemplate,
                fill_color: fillColorInput?.value || '#000000',
                bg_color: bgColorInput?.value || '#FFFFFF',
                border_size: borderInput?.value || '4',
                enable_frame: frameToggle?.checked ? 'true' : 'false',
                frame_width: frameWidthInput?.value || '30',
                frame_color: frameColorInput?.value || '#FFFFFF',
                frame_text: document.getElementById('id_frame_text')?.value || '',
                use_gradient: gradientToggle?.checked ? 'true' : 'false',
                gradient_color_start: gradientStartInput?.value || '#667eea',
                gradient_color_end: gradientEndInput?.value || '#764ba2',
                gradient_direction: document.getElementById('id_gradient_direction')?.value || 'diagonal',
                module_style: document.getElementById('id_module_style')?.value || 'square',
                global_shape: document.getElementById('id_global_shape')?.value || 'square',
                timestamp: Date.now()
            };

            // Collecte les données spécifiques au template
            if (selectedTemplate === 'text') {
                formData.text = textInput?.value.trim() || '';
            } else if (selectedTemplate === 'vcard') {
                formData.vcard_name = document.getElementById('id_vcard_name')?.value || '';
                formData.vcard_org = document.getElementById('id_vcard_org')?.value || '';
                formData.vcard_phone = document.getElementById('id_vcard_phone')?.value || '';
                formData.vcard_email = document.getElementById('id_vcard_email')?.value || '';
                formData.vcard_url = document.getElementById('id_vcard_url')?.value || '';
            } else if (selectedTemplate === 'wifi') {
                formData.wifi_ssid = document.getElementById('id_wifi_ssid')?.value || '';
                formData.wifi_password = document.getElementById('id_wifi_password')?.value || '';
                formData.wifi_security = document.getElementById('id_wifi_security')?.value || 'WPA';
            } else if (selectedTemplate === 'email') {
                formData.email_to = document.getElementById('id_email_to')?.value || '';
                formData.email_subject = document.getElementById('id_email_subject')?.value || '';
                formData.email_body = document.getElementById('id_email_body')?.value || '';
            } else if (selectedTemplate === 'sms') {
                formData.sms_phone = document.getElementById('id_sms_phone')?.value || '';
                formData.sms_message = document.getElementById('id_sms_message')?.value || '';
            } else if (selectedTemplate === 'event') {
                formData.event_title = document.getElementById('id_event_title')?.value || '';
                formData.event_start = document.getElementById('id_event_start')?.value || '';
                formData.event_end = document.getElementById('id_event_end')?.value || '';
                formData.event_location = document.getElementById('id_event_location')?.value || '';
                formData.event_description = document.getElementById('id_event_description')?.value || '';
            } else if (selectedTemplate === 'geo') {
                formData.geo_latitude = document.getElementById('id_geo_latitude')?.value || '';
                formData.geo_longitude = document.getElementById('id_geo_longitude')?.value || '';
            } else if (selectedTemplate === 'payment') {
                formData.payment_type = document.getElementById('id_payment_type')?.value || 'paypal';
                formData.payment_recipient = document.getElementById('id_payment_recipient')?.value || '';
                formData.payment_amount = document.getElementById('id_payment_amount')?.value || '';
            }

            try {
                // Envoie la requête au backend
                const response = await fetch('/api/export-pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    throw new Error('Erreur lors de la génération du PDF');
                }

                // Télécharge le fichier PDF
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'qrcode_' + Date.now() + '.pdf';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);

                // Feedback visuel
                const originalHTML = this.innerHTML;
                this.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9 12l2 2 4-4"></path></svg>OK';
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                }, 2000);

            } catch (error) {
                alert('Erreur lors du téléchargement du PDF: ' + error.message);
            }
        });
    }

    // Aperçu en temps réel avec debounce
    const textInput = document.getElementById('id_text');
    const qrImage = document.getElementById('qr-img');
    const qrDisplay = document.querySelector('.qr-display');
    let previewTimeout = null;

    // Crée le spinner de chargement
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'loading-spinner';
    loadingSpinner.innerHTML = '<div class="spinner-ring"></div>';
    loadingSpinner.style.display = 'none';
    if (qrDisplay) {
        qrDisplay.appendChild(loadingSpinner);
    }

    function generatePreview() {
        // Récupère le type de template sélectionné
        const selectedTemplate = document.querySelector('.template-radio:checked')?.value || 'text';

        // Affiche le spinner
        if (loadingSpinner) loadingSpinner.style.display = 'flex';

        // Récupère le fichier logo s'il existe
        const logoInput = document.getElementById('id_logo');
        const hasLogo = logoInput && logoInput.files && logoInput.files.length > 0;

        // Utilise FormData si un logo est présent, sinon utilise JSON
        let formData;
        let isFormData = hasLogo;

        if (isFormData) {
            // Utilise FormData pour supporter le fichier
            formData = new FormData();
            formData.append('template_type', selectedTemplate);
            formData.append('fill_color', fillColorInput?.value || '#000000');
            formData.append('bg_color', bgColorInput?.value || '#FFFFFF');
            formData.append('border_size', borderInput?.value || '4');
            formData.append('enable_frame', frameToggle?.checked ? 'true' : 'false');
            formData.append('frame_width', frameWidthInput?.value || '30');
            formData.append('frame_color', frameColorInput?.value || '#FFFFFF');
            formData.append('frame_text', document.getElementById('id_frame_text')?.value || '');
            formData.append('use_gradient', gradientToggle?.checked ? 'true' : 'false');
            formData.append('gradient_color_start', gradientStartInput?.value || '#667eea');
            formData.append('gradient_color_end', gradientEndInput?.value || '#764ba2');
            formData.append('gradient_direction', document.getElementById('id_gradient_direction')?.value || 'diagonal');
            formData.append('module_style', document.getElementById('id_module_style')?.value || 'square');
            formData.append('global_shape', document.getElementById('id_global_shape')?.value || 'square');
            formData.append('logo', logoInput.files[0]);
        } else {
            // Utilise JSON comme avant
            formData = {
                template_type: selectedTemplate,
                fill_color: fillColorInput?.value || '#000000',
                bg_color: bgColorInput?.value || '#FFFFFF',
                border_size: borderInput?.value || '4',
                enable_frame: frameToggle?.checked ? 'true' : 'false',
                frame_width: frameWidthInput?.value || '30',
                frame_color: frameColorInput?.value || '#FFFFFF',
                frame_text: document.getElementById('id_frame_text')?.value || '',
                use_gradient: gradientToggle?.checked ? 'true' : 'false',
                gradient_color_start: gradientStartInput?.value || '#667eea',
                gradient_color_end: gradientEndInput?.value || '#764ba2',
                gradient_direction: document.getElementById('id_gradient_direction')?.value || 'diagonal',
                module_style: document.getElementById('id_module_style')?.value || 'square',
                global_shape: document.getElementById('id_global_shape')?.value || 'square'
            };
        }

        // Helper pour ajouter des données (compatible FormData et objet)
        const addData = (key, value) => {
            if (isFormData) {
                formData.append(key, value);
            } else {
                formData[key] = value;
            }
        };

        // Collecte les données spécifiques au template
        if (selectedTemplate === 'text') {
            const textValue = textInput?.value.trim() || '';
            addData('text', textValue);
            if (!textValue) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'vcard') {
            const vcardName = document.getElementById('id_vcard_name')?.value || '';
            const vcardEmail = document.getElementById('id_vcard_email')?.value || '';
            const vcardPhone = document.getElementById('id_vcard_phone')?.value || '';
            addData('vcard_name', vcardName);
            addData('vcard_org', document.getElementById('id_vcard_org')?.value || '');
            addData('vcard_phone', vcardPhone);
            addData('vcard_email', vcardEmail);
            addData('vcard_url', document.getElementById('id_vcard_url')?.value || '');
            if (!vcardName && !vcardEmail && !vcardPhone) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'wifi') {
            const wifiSsid = document.getElementById('id_wifi_ssid')?.value || '';
            addData('wifi_ssid', wifiSsid);
            addData('wifi_password', document.getElementById('id_wifi_password')?.value || '');
            addData('wifi_security', document.getElementById('id_wifi_security')?.value || 'WPA');
            if (!wifiSsid) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'email') {
            const emailTo = document.getElementById('id_email_to')?.value || '';
            addData('email_to', emailTo);
            addData('email_subject', document.getElementById('id_email_subject')?.value || '');
            addData('email_body', document.getElementById('id_email_body')?.value || '');
            if (!emailTo) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'sms') {
            const smsPhone = document.getElementById('id_sms_phone')?.value || '';
            addData('sms_phone', smsPhone);
            addData('sms_message', document.getElementById('id_sms_message')?.value || '');
            if (!smsPhone) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'event') {
            const eventTitle = document.getElementById('id_event_title')?.value || '';
            addData('event_title', eventTitle);
            addData('event_start', document.getElementById('id_event_start')?.value || '');
            addData('event_end', document.getElementById('id_event_end')?.value || '');
            addData('event_location', document.getElementById('id_event_location')?.value || '');
            addData('event_description', document.getElementById('id_event_description')?.value || '');
            if (!eventTitle) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'geo') {
            const geoLat = document.getElementById('id_geo_latitude')?.value || '';
            const geoLon = document.getElementById('id_geo_longitude')?.value || '';
            addData('geo_latitude', geoLat);
            addData('geo_longitude', geoLon);
            if (!geoLat || !geoLon) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'payment') {
            const paymentRecipient = document.getElementById('id_payment_recipient')?.value || '';
            addData('payment_type', document.getElementById('id_payment_type')?.value || 'paypal');
            addData('payment_recipient', paymentRecipient);
            addData('payment_amount', document.getElementById('id_payment_amount')?.value || '');
            if (!paymentRecipient) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        }

        // Appelle l'API avec le bon format
        const fetchOptions = {
            method: 'POST',
            body: isFormData ? formData : JSON.stringify(formData)
        };

        // N'ajoute le header Content-Type que pour JSON (FormData le gère automatiquement)
        if (!isFormData) {
            fetchOptions.headers = {
                'Content-Type': 'application/json',
            };
        }

        fetch('/api/preview', fetchOptions)
        .then(response => response.json())
        .then(data => {
            if (data.success && qrImage) {
                qrImage.src = data.image;
                qrImage.style.opacity = '0';
                setTimeout(() => {
                    qrImage.style.opacity = '1';
                }, 50);

                // Sauvegarde dans l'historique
                addToHistory(data.image, formData);
            }
        })
        .catch(error => {
            console.error('Preview error:', error);
        })
        .finally(() => {
            if (loadingSpinner) loadingSpinner.style.display = 'none';
        });
    }

    function debouncedPreview() {
        if (previewTimeout) clearTimeout(previewTimeout);
        previewTimeout = setTimeout(generatePreview, 500);
    }

    // Ajoute les event listeners pour l'aperçu en temps réel
    const previewInputs = [
        // Template texte
        textInput,
        // Template vCard
        document.getElementById('id_vcard_name'),
        document.getElementById('id_vcard_org'),
        document.getElementById('id_vcard_phone'),
        document.getElementById('id_vcard_email'),
        document.getElementById('id_vcard_url'),
        // Template WiFi
        document.getElementById('id_wifi_ssid'),
        document.getElementById('id_wifi_password'),
        document.getElementById('id_wifi_security'),
        // Template Email
        document.getElementById('id_email_to'),
        document.getElementById('id_email_subject'),
        document.getElementById('id_email_body'),
        // Template SMS
        document.getElementById('id_sms_phone'),
        document.getElementById('id_sms_message'),
        // Template Event
        document.getElementById('id_event_title'),
        document.getElementById('id_event_start'),
        document.getElementById('id_event_end'),
        document.getElementById('id_event_location'),
        document.getElementById('id_event_description'),
        // Template Geolocation
        document.getElementById('id_geo_latitude'),
        document.getElementById('id_geo_longitude'),
        // Template Payment
        document.getElementById('id_payment_type'),
        document.getElementById('id_payment_recipient'),
        document.getElementById('id_payment_amount'),
        // Champs communs
        fillColorInput,
        bgColorInput,
        borderInput,
        frameToggle,
        frameWidthInput,
        frameColorInput,
        document.getElementById('id_frame_text'),
        // Personnalisation avancée
        gradientToggle,
        gradientStartInput,
        gradientEndInput,
        document.getElementById('id_gradient_direction'),
        document.getElementById('id_module_style'),
        document.getElementById('id_global_shape'),
        // Logo
        document.getElementById('id_logo')
    ];

    previewInputs.forEach(input => {
        if (input) {
            const eventType = (input.type === 'checkbox' || input.type === 'file') ? 'change' : 'input';
            input.addEventListener(eventType, debouncedPreview);
        }
    });

    // Génère l'aperçu initial au chargement
    debouncedPreview();
});

// ========== GÉNÉRATION EN BATCH ==========
document.addEventListener('DOMContentLoaded', function() {
    const batchFileInput = document.getElementById('batch-csv-file');
    const batchUploadZone = document.getElementById('batch-upload-zone');
    const batchFileInfo = document.getElementById('batch-file-info');
    const batchFilename = document.getElementById('batch-filename');
    const batchRemove = document.getElementById('batch-remove');
    const batchGenerateBtn = document.getElementById('batch-generate-btn');
    const batchProgress = document.getElementById('batch-progress');

    let selectedFile = null;

    // Gestion du changement de fichier
    if (batchFileInput) {
        batchFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.name.endsWith('.csv')) {
                selectedFile = file;
                batchFilename.textContent = file.name;
                batchFileInfo.style.display = 'flex';
                batchGenerateBtn.disabled = false;
            }
        });
    }

    // Drag & Drop
    if (batchUploadZone) {
        batchUploadZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.add('dragover');
        });

        batchUploadZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.remove('dragover');
        });

        batchUploadZone.addEventListener('drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.remove('dragover');

            const file = e.dataTransfer.files[0];
            if (file && file.name.endsWith('.csv')) {
                selectedFile = file;
                batchFilename.textContent = file.name;
                batchFileInfo.style.display = 'flex';
                batchGenerateBtn.disabled = false;
            }
        });
    }

    // Bouton de suppression du fichier
    if (batchRemove) {
        batchRemove.addEventListener('click', function() {
            selectedFile = null;
            batchFileInput.value = '';
            batchFileInfo.style.display = 'none';
            batchGenerateBtn.disabled = true;
        });
    }

    // Génération du ZIP
    if (batchGenerateBtn) {
        batchGenerateBtn.addEventListener('click', async function() {
            if (!selectedFile) return;

            // Affiche la barre de progression
            batchProgress.style.display = 'block';
            batchGenerateBtn.disabled = true;

            try {
                // Prépare le FormData
                const formData = new FormData();
                formData.append('csv_file', selectedFile);

                // Envoie la requête
                const response = await fetch('/api/batch', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Erreur lors de la génération');
                }

                // Télécharge le fichier ZIP
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'qrcodes_batch.zip';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);

                // Réinitialise
                selectedFile = null;
                batchFileInput.value = '';
                batchFileInfo.style.display = 'none';

                // Feedback visuel
                const originalHTML = batchGenerateBtn.innerHTML;
                batchGenerateBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9 12l2 2 4-4"></path></svg>Terminé !';
                setTimeout(() => {
                    batchGenerateBtn.innerHTML = originalHTML;
                }, 2000);

            } catch (error) {
                alert('Erreur: ' + error.message);
            } finally {
                batchProgress.style.display = 'none';
                batchGenerateBtn.disabled = false;
            }
        });
    }
});
// Fonction pour obtenir une couleur de texte contrastée
function getContrastColor(hexcolor) {
    // Retire le # si présent
    hexcolor = hexcolor.replace('#', '');

    // Convertit en RGB
    const r = parseInt(hexcolor.substr(0, 2), 16);
    const g = parseInt(hexcolor.substr(2, 2), 16);
    const b = parseInt(hexcolor.substr(4, 2), 16);

    // Calcule la luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

    return luminance > 0.5 ? '#000000' : '#ffffff';
}

// Fonction pour générer le texte vCard
function generateVCardText(name, org, phone, email, url) {
    let vcard = "BEGIN:VCARD\n";
    vcard += "VERSION:3.0\n";
    if (name) vcard += `FN:${name}\n`;
    if (org) vcard += `ORG:${org}\n`;
    if (phone) vcard += `TEL:${phone}\n`;
    if (email) vcard += `EMAIL:${email}\n`;
    if (url) vcard += `URL:${url}\n`;
    vcard += "END:VCARD";
    return vcard;
}

// ========== GESTION DE L'HISTORIQUE ==========
const MAX_HISTORY = 10;

// Charge l'historique depuis localStorage
function loadHistory() {
    const history = localStorage.getItem('qr_history');
    return history ? JSON.parse(history) : [];
}

// Sauvegarde l'historique dans localStorage
function saveHistory(history) {
    localStorage.setItem('qr_history', JSON.stringify(history));
}

// Ajoute un QR code à l'historique
function addToHistory(image, config) {
    const history = loadHistory();
    const newItem = {
        id: Date.now(),
        image: image,
        config: config,
        timestamp: Date.now()
    };
    
    // Ajoute en début de liste
    history.unshift(newItem);
    
    // Limite à MAX_HISTORY items
    if (history.length > MAX_HISTORY) {
        history.pop();
    }
    
    saveHistory(history);
}

// Supprime un item de l'historique
function deleteHistoryItem(id) {
    let history = loadHistory();
    history = history.filter(item => item.id !== id);
    saveHistory(history);
    displayHistory();
}

// Vide tout l'historique
function clearHistory() {
    localStorage.removeItem('qr_history');
    displayHistory();
}

// Affiche l'historique dans le modal
function displayHistory() {
    const history = loadHistory();
    const grid = document.getElementById('history-grid');
    const emptyState = document.getElementById('history-empty');
    
    if (history.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    grid.innerHTML = '';
    
    history.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'history-item';
        
        const date = new Date(item.timestamp);
        const dateStr = date.toLocaleDateString('fr-FR', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric'
        });
        
        itemDiv.innerHTML = `
            <button class="history-item-delete" onclick="deleteHistoryItem(${item.id}); event.stopPropagation();">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
            <img src="${item.image}" alt="QR Code">
            <div class="history-item-date">${dateStr}</div>
        `;
        
        itemDiv.addEventListener('click', () => {
            restoreFromHistory(item.config);
            closeHistoryModal();
        });
        
        grid.appendChild(itemDiv);
    });
}

// Restaure une configuration depuis l'historique
function restoreFromHistory(config) {
    // Restaure le type de template
    if (config.template_type) {
        const templateRadio = document.querySelector(`input[name="template_type"][value="${config.template_type}"]`);
        if (templateRadio) {
            templateRadio.checked = true;
            switchTemplate();
        }
    }
    
    // Restaure les champs selon le template
    if (config.template_type === 'text' && config.text) {
        const textInput = document.getElementById('id_text');
        if (textInput) textInput.value = config.text;
    } else if (config.template_type === 'vcard') {
        if (config.vcard_name) document.getElementById('id_vcard_name').value = config.vcard_name;
        if (config.vcard_org) document.getElementById('id_vcard_org').value = config.vcard_org;
        if (config.vcard_phone) document.getElementById('id_vcard_phone').value = config.vcard_phone;
        if (config.vcard_email) document.getElementById('id_vcard_email').value = config.vcard_email;
        if (config.vcard_url) document.getElementById('id_vcard_url').value = config.vcard_url;
    } else if (config.template_type === 'wifi') {
        if (config.wifi_ssid) document.getElementById('id_wifi_ssid').value = config.wifi_ssid;
        if (config.wifi_password) document.getElementById('id_wifi_password').value = config.wifi_password;
        if (config.wifi_security) document.getElementById('id_wifi_security').value = config.wifi_security;
    } else if (config.template_type === 'email') {
        if (config.email_to) document.getElementById('id_email_to').value = config.email_to;
        if (config.email_subject) document.getElementById('id_email_subject').value = config.email_subject;
        if (config.email_body) document.getElementById('id_email_body').value = config.email_body;
    } else if (config.template_type === 'sms') {
        if (config.sms_phone) document.getElementById('id_sms_phone').value = config.sms_phone;
        if (config.sms_message) document.getElementById('id_sms_message').value = config.sms_message;
    } else if (config.template_type === 'event') {
        if (config.event_title) document.getElementById('id_event_title').value = config.event_title;
        if (config.event_start) document.getElementById('id_event_start').value = config.event_start;
        if (config.event_end) document.getElementById('id_event_end').value = config.event_end;
        if (config.event_location) document.getElementById('id_event_location').value = config.event_location;
        if (config.event_description) document.getElementById('id_event_description').value = config.event_description;
    } else if (config.template_type === 'geo') {
        if (config.geo_latitude) document.getElementById('id_geo_latitude').value = config.geo_latitude;
        if (config.geo_longitude) document.getElementById('id_geo_longitude').value = config.geo_longitude;
    } else if (config.template_type === 'payment') {
        if (config.payment_type) document.getElementById('id_payment_type').value = config.payment_type;
        if (config.payment_recipient) document.getElementById('id_payment_recipient').value = config.payment_recipient;
        if (config.payment_amount) document.getElementById('id_payment_amount').value = config.payment_amount;
    }

    // Restaure les couleurs
    if (config.fill_color) {
        const fillInput = document.getElementById('id_fill_color');
        if (fillInput) {
            fillInput.value = config.fill_color;
            const fillPreview = document.getElementById('fill-color-preview');
            if (fillPreview) {
                fillPreview.textContent = config.fill_color.toUpperCase();
                fillPreview.style.background = config.fill_color;
                fillPreview.style.color = getContrastColor(config.fill_color);
            }
        }
    }
    
    if (config.bg_color) {
        const bgInput = document.getElementById('id_bg_color');
        if (bgInput) {
            bgInput.value = config.bg_color;
            const bgPreview = document.getElementById('bg-color-preview');
            if (bgPreview) {
                bgPreview.textContent = config.bg_color.toUpperCase();
                bgPreview.style.background = config.bg_color;
                bgPreview.style.color = getContrastColor(config.bg_color);
            }
        }
    }
    
    // Restaure la bordure
    if (config.border_size !== undefined) {
        const borderInput = document.getElementById('id_border_size');
        if (borderInput) borderInput.value = config.border_size;
    }
    
    // Restaure le cadre
    if (config.enable_frame !== undefined) {
        const frameToggle = document.getElementById('id_enable_frame');
        if (frameToggle) {
            frameToggle.checked = config.enable_frame === 'true';
            toggleFrameOptions();
        }
    }
    
    if (config.frame_width) {
        const frameWidthInput = document.getElementById('id_frame_width');
        if (frameWidthInput) frameWidthInput.value = config.frame_width;
    }
    
    if (config.frame_color) {
        const frameColorInput = document.getElementById('id_frame_color');
        if (frameColorInput) {
            frameColorInput.value = config.frame_color;
            const frameColorPreview = document.getElementById('frame-color-preview');
            if (frameColorPreview) {
                frameColorPreview.textContent = config.frame_color.toUpperCase();
                frameColorPreview.style.background = config.frame_color;
                frameColorPreview.style.color = getContrastColor(config.frame_color);
            }
        }
    }
    
    if (config.frame_text) {
        const frameTextInput = document.getElementById('id_frame_text');
        if (frameTextInput) frameTextInput.value = config.frame_text;
    }
    
    // Déclenche l'aperçu
    debouncedPreview();
}

// Ouvre le modal historique
function openHistoryModal() {
    const modal = document.getElementById('history-modal');
    modal.classList.add('active');
    displayHistory();
}

// Ferme le modal historique
function closeHistoryModal() {
    const modal = document.getElementById('history-modal');
    modal.classList.remove('active');
}

// Event listeners pour l'historique
document.addEventListener('DOMContentLoaded', function() {
    const historyBtn = document.getElementById('history-btn');
    const historyClose = document.getElementById('history-close');
    const historyClear = document.getElementById('history-clear');
    const historyModal = document.getElementById('history-modal');
    
    if (historyBtn) {
        historyBtn.addEventListener('click', openHistoryModal);
    }
    
    if (historyClose) {
        historyClose.addEventListener('click', closeHistoryModal);
    }
    
    if (historyClear) {
        historyClear.addEventListener('click', () => {
            if (confirm('Voulez-vous vraiment vider tout l\'historique ?')) {
                clearHistory();
            }
        });
    }
    
    // Ferme le modal en cliquant en dehors
    if (historyModal) {
        historyModal.addEventListener('click', (e) => {
            if (e.target === historyModal) {
                closeHistoryModal();
            }
        });
    }
});

