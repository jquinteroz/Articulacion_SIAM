/**
 * Sistema de Matrículas - Articulación SENA
 * JavaScript principal
 */

// ============================================
// UTILIDADES GENERALES
// ============================================

/**
 * Muestra una alerta temporal
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

/**
 * Confirmar acción
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Formatear fecha
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// ============================================
// FUNCIONALIDAD DE MOSTRAR/OCULTAR CONTRASEÑA
// ============================================

/**
 * Toggle para mostrar/ocultar contraseña en campos de input
 */
function togglePasswordInput(inputId, iconElement) {
    const input = document.getElementById(inputId);
    if (!input) return;

    if (input.type === 'password') {
        input.type = 'text';
        iconElement.classList.remove('fa-eye');
        iconElement.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        iconElement.classList.remove('fa-eye-slash');
        iconElement.classList.add('fa-eye');
    }
}

/**
 * Obtener y mostrar contraseña desencriptada (para CRUD de usuarios)
 */
async function togglePassword(userId, element) {
    const passwordSpan = element.previousElementSibling;

    if (passwordSpan.textContent !== '********') {
        // Ocultar contraseña
        passwordSpan.textContent = '********';
        element.classList.remove('fa-eye-slash');
        element.classList.add('fa-eye');
        return;
    }

    try {
        const response = await fetch(`/admin/usuarios/get-password/${userId}`);
        const data = await response.json();

        if (data.success) {
            passwordSpan.textContent = data.password;
            element.classList.remove('fa-eye');
            element.classList.add('fa-eye-slash');
        } else {
            showAlert('Error al obtener la contraseña', 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al obtener la contraseña', 'danger');
    }
}

// ============================================
// VALIDACIÓN DE FORMULARIOS
// ============================================

/**
 * Validar formulario de registro
 */
function validateRegistroForm(form) {
    const password = form.querySelector('[name="password"]').value;
    const passwordConfirm = form.querySelector('[name="password_confirm"]').value;

    if (password !== passwordConfirm) {
        showAlert('Las contraseñas no coinciden', 'danger');
        return false;
    }

    if (password.length < 6) {
        showAlert('La contraseña debe tener al menos 6 caracteres', 'danger');
        return false;
    }

    return true;
}

/**
 * Validar archivo antes de subir
 */
function validateFile(input, maxSizeMB = 5) {
    const file = input.files[0];
    if (!file) return false;

    const allowedExtensions = ['pdf', 'jpg', 'jpeg', 'png'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        showAlert('Tipo de archivo no permitido. Solo PDF, JPG, JPEG, PNG', 'danger');
        input.value = '';
        return false;
    }

    const maxSize = maxSizeMB * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert(`El archivo no debe superar ${maxSizeMB}MB`, 'danger');
        input.value = '';
        return false;
    }

    return true;
}

// ============================================
// CAROUSEL
// ============================================

class Carousel {
    constructor(element) {
        this.element = element;
        this.items = element.querySelectorAll('.carousel-item');
        this.currentIndex = 0;
        this.interval = null;

        this.init();
    }

    init() {
        if (this.items.length > 0) {
            this.items[0].classList.add('active');
            this.start();
        }
    }

    next() {
        this.items[this.currentIndex].classList.remove('active');
        this.currentIndex = (this.currentIndex + 1) % this.items.length;
        this.items[this.currentIndex].classList.add('active');
    }

    prev() {
        this.items[this.currentIndex].classList.remove('active');
        this.currentIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
        this.items[this.currentIndex].classList.add('active');
    }

    start() {
        this.interval = setInterval(() => this.next(), 5000);
    }

    stop() {
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
}

// ============================================
// FILTROS DE TABLAS
// ============================================

/**
 * Filtrar tabla en tiempo real
 */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (!input || !table) return;

    input.addEventListener('keyup', function() {
        const filter = this.value.toUpperCase();
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let found = false;

            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell) {
                    const textValue = cell.textContent || cell.innerText;
                    if (textValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }

            rows[i].style.display = found ? '' : 'none';
        }
    });
}

// ============================================
// CONFIRMACIONES DE ELIMINACIÓN
// ============================================

/**
 * Agregar confirmación a botones de eliminación
 */
function setupDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') ||
                          '¿Está seguro de que desea eliminar este elemento?';

            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// ============================================
// CARGA DE DOCUMENTOS
// ============================================

/**
 * Preview de archivo seleccionado
 */
function setupFilePreview() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const previewElement = this.nextElementSibling;
                if (previewElement && previewElement.classList.contains('file-preview')) {
                    previewElement.textContent = `Archivo seleccionado: ${file.name} (${formatFileSize(file.size)})`;
                }
            }
        });
    });
}

/**
 * Formatear tamaño de archivo
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ============================================
// SELECTOR DEPENDIENTE (Colegio -> Grupos)
// ============================================

/**
 * Actualizar grupos según colegio seleccionado
 */
async function updateGruposByColegio(colegioId, grupoSelectId) {
    const grupoSelect = document.getElementById(grupoSelectId);
    if (!grupoSelect) return;

    grupoSelect.innerHTML = '<option value="">Cargando...</option>';

    try {
        const response = await fetch(`/api/grupos/by-colegio/${colegioId}`);
        const grupos = await response.json();

        grupoSelect.innerHTML = '<option value="">Seleccione un grupo</option>';

        grupos.forEach(grupo => {
            const option = document.createElement('option');
            option.value = grupo.id;
            option.textContent = grupo.nombre;
            grupoSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar grupos:', error);
        grupoSelect.innerHTML = '<option value="">Error al cargar grupos</option>';
    }
}

// ============================================
// INICIALIZACIÓN AL CARGAR LA PÁGINA
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar carousel
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => new Carousel(carousel));

    // Configurar confirmaciones de eliminación
    setupDeleteConfirmations();

    // Configurar preview de archivos
    setupFilePreview();

    // Auto-cerrar alertas después de 5 segundos (excepto las permanentes)
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Agregar efecto de loading a formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            }
        });
    });
});

// ============================================
// EXPORTAR FUNCIONES GLOBALES
// ============================================

window.togglePasswordInput = togglePasswordInput;
window.togglePassword = togglePassword;
window.validateRegistroForm = validateRegistroForm;
window.validateFile = validateFile;
window.filterTable = filterTable;
window.updateGruposByColegio = updateGruposByColegio;
window.confirmAction = confirmAction;
window.showAlert = showAlert;
