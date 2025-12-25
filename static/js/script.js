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
            switchTemplate();
            // Déclenche la mise à jour de l'aperçu quand le template change
            debouncedPreview();
        });
    });

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

        // Collecte les données communes
        const formData = {
            template_type: selectedTemplate,
            fill_color: fillColorInput?.value || '#000000',
            bg_color: bgColorInput?.value || '#FFFFFF',
            border_size: borderInput?.value || '4',
            enable_frame: frameToggle?.checked ? 'true' : 'false',
            frame_width: frameWidthInput?.value || '30',
            frame_color: frameColorInput?.value || '#FFFFFF',
            frame_text: document.getElementById('id_frame_text')?.value || ''
        };

        // Collecte les données spécifiques au template
        if (selectedTemplate === 'text') {
            formData.text = textInput?.value.trim() || '';
            if (!formData.text) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'vcard') {
            formData.vcard_name = document.getElementById('id_vcard_name')?.value || '';
            formData.vcard_org = document.getElementById('id_vcard_org')?.value || '';
            formData.vcard_phone = document.getElementById('id_vcard_phone')?.value || '';
            formData.vcard_email = document.getElementById('id_vcard_email')?.value || '';
            formData.vcard_url = document.getElementById('id_vcard_url')?.value || '';
            if (!formData.vcard_name && !formData.vcard_email && !formData.vcard_phone) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'wifi') {
            formData.wifi_ssid = document.getElementById('id_wifi_ssid')?.value || '';
            formData.wifi_password = document.getElementById('id_wifi_password')?.value || '';
            formData.wifi_security = document.getElementById('id_wifi_security')?.value || 'WPA';
            if (!formData.wifi_ssid) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'email') {
            formData.email_to = document.getElementById('id_email_to')?.value || '';
            formData.email_subject = document.getElementById('id_email_subject')?.value || '';
            formData.email_body = document.getElementById('id_email_body')?.value || '';
            if (!formData.email_to) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        } else if (selectedTemplate === 'sms') {
            formData.sms_phone = document.getElementById('id_sms_phone')?.value || '';
            formData.sms_message = document.getElementById('id_sms_message')?.value || '';
            if (!formData.sms_phone) {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                return;
            }
        }

        // Appelle l'API
        fetch('/api/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && qrImage) {
                qrImage.src = data.image;
                qrImage.style.opacity = '0';
                setTimeout(() => {
                    qrImage.style.opacity = '1';
                }, 50);
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
        // Champs communs
        fillColorInput,
        bgColorInput,
        borderInput,
        frameToggle,
        frameWidthInput,
        frameColorInput,
        document.getElementById('id_frame_text')
    ];

    previewInputs.forEach(input => {
        if (input) {
            const eventType = input.type === 'checkbox' ? 'change' : 'input';
            input.addEventListener(eventType, debouncedPreview);
        }
    });
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
