document.addEventListener('DOMContentLoaded', function() {
    // Color picker synchronization
    const fillColorInput = document.getElementById('id_fill_color');
    const bgColorInput = document.getElementById('id_bg_color');

    if (fillColorInput) {
        const fillPreview = document.getElementById('fill-color-preview');
        fillColorInput.addEventListener('input', function() {
            fillPreview.textContent = this.value.toUpperCase();
            fillPreview.style.background = this.value;
            fillPreview.style.color = getContrastColor(this.value);
        });
        // Initialize preview
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
        // Initialize preview
        bgPreview.textContent = bgColorInput.value.toUpperCase();
        bgPreview.style.background = bgColorInput.value;
        bgPreview.style.color = getContrastColor(bgColorInput.value);
    }

    // Border size input validation
    const borderInput = document.getElementById('id_border_size');
    if (borderInput) {
        borderInput.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (value < 0) this.value = 0;
            if (value > 20) this.value = 20;
        });
    }

    // Frame toggle functionality
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
        // Initialize on load
        toggleFrameOptions();

        frameToggle.addEventListener('change', toggleFrameOptions);
    }

    // Frame width validation
    const frameWidthInput = document.getElementById('id_frame_width');
    if (frameWidthInput) {
        frameWidthInput.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (value < 10) this.value = 10;
            if (value > 100) this.value = 100;
        });
    }

    // Frame color picker preview
    const frameColorInput = document.getElementById('id_frame_color');
    if (frameColorInput) {
        const frameColorPreview = document.getElementById('frame-color-preview');
        frameColorInput.addEventListener('input', function() {
            frameColorPreview.textContent = this.value.toUpperCase();
            frameColorPreview.style.background = this.value;
            frameColorPreview.style.color = getContrastColor(this.value);
        });
        // Initialize preview
        frameColorPreview.textContent = frameColorInput.value.toUpperCase();
        frameColorPreview.style.background = frameColorInput.value;
        frameColorPreview.style.color = getContrastColor(frameColorInput.value);
    }

    // File upload display
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

    // Download functionality
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const qrImage = document.getElementById('qr-img');
            if (qrImage) {
                const link = document.createElement('a');
                link.href = qrImage.src;
                link.download = 'qrcode_' + Date.now() + '.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Visual feedback
                this.textContent = 'Téléchargé !';
                setTimeout(() => {
                    this.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>Télécharger';
                }, 2000);
            }
        });
    }

    // Real-time preview with debounce
    const textInput = document.getElementById('id_text');
    const qrImage = document.getElementById('qr-img');
    const qrDisplay = document.querySelector('.qr-display');
    let previewTimeout = null;

    // Create loading spinner
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'loading-spinner';
    loadingSpinner.innerHTML = '<div class="spinner-ring"></div>';
    loadingSpinner.style.display = 'none';
    if (qrDisplay) {
        qrDisplay.appendChild(loadingSpinner);
    }

    function generatePreview() {
        const text = textInput?.value.trim();
        if (!text) return;

        // Show spinner
        if (loadingSpinner) loadingSpinner.style.display = 'flex';

        // Collect form data
        const formData = {
            text: text,
            fill_color: fillColorInput?.value || '#000000',
            bg_color: bgColorInput?.value || '#FFFFFF',
            border_size: borderInput?.value || '4',
            enable_frame: frameToggle?.checked ? 'true' : 'false',
            frame_width: frameWidthInput?.value || '30',
            frame_color: frameColorInput?.value || '#FFFFFF',
            frame_text: document.getElementById('id_frame_text')?.value || ''
        };

        // Call API
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

    // Add event listeners for real-time preview
    const previewInputs = [
        textInput,
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

// Function to get contrasting text color
function getContrastColor(hexcolor) {
    // Remove # if present
    hexcolor = hexcolor.replace('#', '');

    // Convert to RGB
    const r = parseInt(hexcolor.substr(0, 2), 16);
    const g = parseInt(hexcolor.substr(2, 2), 16);
    const b = parseInt(hexcolor.substr(4, 2), 16);

    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

    return luminance > 0.5 ? '#000000' : '#ffffff';
}
