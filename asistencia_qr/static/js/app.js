/**
 * Asistencia QR · SENA — JavaScript principal
 * Lógica de UI: toasts, contadores animados, theme toggle, polling QR, lista en vivo
 */

/* ============================================================
   TOASTS — Notificaciones flotantes
============================================================ */
function showToast(msg, tipo = 'success') {
    const stack = document.getElementById('toast-stack');
    if (!stack) return;
    const t = document.createElement('div');
    t.className = 'toast';
    const iconClass = tipo === 'error' ? 'ic error' : 'ic';
    const iconPath = tipo === 'error'
        ? '<path d="M18 6L6 18M6 6l12 12" stroke="#fff" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        : '<path d="M20 6L9 17l-5-5" stroke="#fff" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>';
    t.innerHTML = `<span class="${iconClass}"><svg class="icon" viewBox="0 0 24 24">${iconPath}</svg></span><span>${msg}</span>`;
    stack.appendChild(t);
    setTimeout(() => {
        t.style.opacity = '0';
        t.style.transform = 'translateY(10px) scale(.96)';
        t.style.transition = 'all .35s ease';
        setTimeout(() => t.remove(), 350);
    }, 3200);
}

/* ============================================================
   RIPPLE — Efecto visual en botones
============================================================ */
function ripple(e) {
    const btn = e.currentTarget;
    const rect = btn.getBoundingClientRect();
    const circle = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    circle.className = 'ripple';
    circle.style.width = circle.style.height = size + 'px';
    circle.style.left = (e.clientX - rect.left - size / 2) + 'px';
    circle.style.top = (e.clientY - rect.top - size / 2) + 'px';
    btn.appendChild(circle);
    setTimeout(() => circle.remove(), 600);
}

// Agregar ripple a todos los botones
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', ripple);
    });
});

/* ============================================================
   CONTADORES ANIMADOS — Para las métricas
============================================================ */
function animateCounters(scope) {
    (scope || document).querySelectorAll('.val[data-count]').forEach(el => {
        if (el.dataset.done) return;
        el.dataset.done = '1';
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const dur = 900;
        const start = performance.now();

        function frame(now) {
            const p = Math.min(1, (now - start) / dur);
            const eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(target * eased) + suffix;
            if (p < 1) requestAnimationFrame(frame);
        }
        requestAnimationFrame(frame);
    });
}

document.addEventListener('DOMContentLoaded', () => animateCounters(document));

/* ============================================================
   DARK MODE — Toggle tema claro/oscuro
============================================================ */
function initThemeToggle() {
    const btn = document.getElementById('theme-toggle-btn');
    if (!btn) return;

    const iconEl = btn.querySelector('.theme-icon');
    const labelEl = btn.querySelector('.theme-label');

    let currentTheme = localStorage.getItem('theme') || 'light';
    applyTheme(currentTheme);

    btn.addEventListener('click', () => {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        applyTheme(currentTheme);
        localStorage.setItem('theme', currentTheme);
    });

    function applyTheme(mode) {
        if (mode === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            if (iconEl) iconEl.innerHTML = '<use href="#ic-sun"/>';
            if (labelEl) labelEl.textContent = 'Modo claro';
        } else {
            document.documentElement.removeAttribute('data-theme');
            if (iconEl) iconEl.innerHTML = '<use href="#ic-moon"/>';
            if (labelEl) labelEl.textContent = 'Modo oscuro';
        }
    }
}

document.addEventListener('DOMContentLoaded', initThemeToggle);

/* ============================================================
   SIDEBAR — Collapse toggle
============================================================ */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.toggle('collapsed');
}

/* ============================================================
   ADMIN TABS — Cambiar pestaña en panel admin
============================================================ */
function showAdminTab(name, el) {
    document.querySelectorAll('.subtab').forEach(t => t.classList.remove('active'));
    if (el) el.classList.add('active');
    ['dashboard', 'fichas', 'usuarios', 'auditoria', 'config'].forEach(n => {
        const tab = document.getElementById('admin-' + n);
        if (tab) tab.style.display = n === name ? 'block' : 'none';
    });
    if (window.history && window.history.pushState) {
        const url = new URL(window.location);
        url.searchParams.set('tab', name);
        window.history.pushState({ path: url.href }, '', url.href);
    }
}

/* ============================================================
   MODALS — Control de apertura y cierre accesible
============================================================ */
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
        const autofocusEl = modal.querySelector('input:not([type=hidden]), select, textarea');
        if (autofocusEl) setTimeout(() => autofocusEl.focus(), 100);
    }
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }
}

// Cerrar modales con Escape y al hacer clic en el backdrop
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-backdrop.open').forEach(m => closeModal(m.id));
    }
});

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-backdrop')) {
        closeModal(e.target.id);
    }
});

/* ============================================================
   CLIPBOARD — Copiado rápido con toast
============================================================ */
async function copiarAlPortapapeles(texto, mensaje = 'Enlace copiado al portapapeles') {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(texto);
        } else {
            const temp = document.createElement('textarea');
            temp.value = texto;
            temp.style.position = 'fixed';
            temp.style.left = '-9999px';
            document.body.appendChild(temp);
            temp.select();
            document.execCommand('copy');
            document.body.removeChild(temp);
        }
        showToast(mensaje, 'success');
    } catch (err) {
        showToast('No se pudo copiar automáticamente', 'error');
    }
}

/* ============================================================
   MODO PROYECTOR — Pantalla Completa QR
============================================================ */
function toggleModoProyector() {
    const card = document.querySelector('.qr-card');
    if (!card) return;
    
    if (card.classList.contains('fullscreen-qr-mode')) {
        card.classList.remove('fullscreen-qr-mode');
        document.body.style.overflow = '';
        const btn = document.getElementById('close-proyector-btn');
        if (btn) btn.remove();
    } else {
        card.classList.add('fullscreen-qr-mode');
        document.body.style.overflow = 'hidden';
        if (!document.getElementById('close-proyector-btn')) {
            const btn = document.createElement('button');
            btn.id = 'close-proyector-btn';
            btn.className = 'fullscreen-close-btn';
            btn.innerHTML = '<svg class="icon" style="width:16px;height:16px;stroke:#fff"><use href="#ic-x"/></svg> Salir de pantalla completa';
            btn.onclick = toggleModoProyector;
            card.appendChild(btn);
        }
    }
}

/* ============================================================
   CORREGIR PANEL — Toggle en historial
============================================================ */
function toggleCorregir(btn) {
    const panel = btn.closest('tr').nextElementSibling.querySelector('.corregir-panel');
    if (panel) panel.classList.toggle('open');
}

/* ============================================================
   NOTE BOX — Toggle en alertas
============================================================ */
function toggleNote(btn) {
    const box = btn.closest('.alert-body').querySelector('.note-box');
    if (box) box.classList.toggle('open');
}

/* ============================================================
   QR POLLING — Actualiza la imagen QR cada 30 segundos
============================================================ */
let qrPollingInterval = null;
let qrCountdown = 30;

function initQrPolling() {
    const qrImagen = document.getElementById('qr-imagen');
    const qrTimer = document.getElementById('qr-timer');
    const qrCodigo = document.getElementById('qr-codigo');

    if (!qrImagen || !qrTimer) return;

    qrCountdown = 30;
    updateTimerDisplay();

    // Polling: cada segundo actualiza el countdown, cada 30s pide nuevo QR
    qrPollingInterval = setInterval(() => {
        qrCountdown--;
        updateTimerDisplay();

        if (qrCountdown <= 0) {
            fetchNuevoQr();
            qrCountdown = 30;
        }
    }, 1000);

    // Fetch inmediato al cargar
    fetchNuevoQr();

    function updateTimerDisplay() {
        const s = String(qrCountdown).padStart(2, '0');
        qrTimer.textContent = `00:${s}`;
    }

    function fetchNuevoQr() {
        fetch('/instructor/sesion/qr')
            .then(r => r.json())
            .then(data => {
                if (data.imagen_base64) {
                    // Animación de flip
                    const wrap = qrImagen.parentElement;
                    wrap.classList.add('refreshing');
                    setTimeout(() => wrap.classList.remove('refreshing'), 600);

                    qrImagen.src = 'data:image/png;base64,' + data.imagen_base64;
                }
                if (data.codigo && qrCodigo) {
                    qrCodigo.textContent = data.codigo;
                }
            })
            .catch(err => console.error('Error al actualizar QR:', err));
    }
}

/* ============================================================
   LISTA EN VIVO — Polling de registros de asistencia
============================================================ */
let registrosPollingInterval = null;

function initRegistrosPolling() {
    const lista = document.getElementById('lista-asistentes');
    const contador = document.getElementById('attend-cnt');
    const emptyState = document.getElementById('asistentes-empty') || document.getElementById('empty-asistentes');

    if (!lista) return;

    let registrosAnteriores = 0;

    registrosPollingInterval = setInterval(() => {
        fetch('/instructor/sesion/registros')
            .then(r => r.json())
            .then(data => {
                if (!data.registros) return;

                const registros = data.registros;
                const total = data.total_aprendices || 0;

                // Actualizar contador
                if (contador) {
                    contador.textContent = `${registros.length} de ${total} aprendices registrados`;
                }

                // Mostrar/ocultar empty state
                if (emptyState) {
                    emptyState.style.display = registros.length === 0 ? 'flex' : 'none';
                }
                if (lista) {
                    lista.style.display = registros.length === 0 ? 'none' : 'block';
                }

                // Si hay nuevos registros, mostrar toast
                if (registros.length > registrosAnteriores && registrosAnteriores > 0) {
                    const nuevos = registros.slice(registrosAnteriores);
                    nuevos.forEach(r => {
                        showToast(`${r.nombre.split(' ')[0]} registró su asistencia`);
                    });
                }

                // Reconstruir la lista
                lista.innerHTML = registros.map((r, i) => {
                    const isNew = i >= registrosAnteriores && registrosAnteriores > 0;
                    return `
                        <div class="attend-row ${isNew ? 'new' : ''}">
                            <div class="mini-avatar">${r.iniciales}</div>
                            <div class="info">
                                <div class="name">${r.nombre}</div>
                                <div class="doc">CC ${r.documento}</div>
                            </div>
                            <span class="badge badge-${r.estado === 'corregido' ? 'warning' : 'success'}">
                                <span class="dot"></span>${r.estado === 'corregido' ? 'Corregido' : 'A tiempo'}
                            </span>
                            <span class="time">${r.hora}</span>
                        </div>
                    `;
                }).join('');

                // Quitar highlight después de 2 segundos
                if (registros.length > registrosAnteriores) {
                    setTimeout(() => {
                        document.querySelectorAll('.attend-row.new').forEach(row => {
                            row.classList.remove('new');
                        });
                    }, 2000);
                }

                registrosAnteriores = registros.length;
            })
            .catch(err => console.error('Error al obtener registros:', err));
    }, 5000);

    // Fetch inmediato
    document.querySelector('[data-trigger="fetch-registros"]')?.click();
}

/* ============================================================
   APRENDIZ — La lógica de confirmación se gestiona en 
   views/aprendiz/escanear.html para controlar las transiciones de vista
   (#view-form, #view-success, #view-expired, #view-error).
============================================================ */

/* ============================================================
   INICIALIZACIÓN
============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    // Iniciar polling de QR si estamos en la pantalla de sesión
    if (document.getElementById('qr-imagen')) {
        initQrPolling();
    }

    // Iniciar polling de registros si estamos en la pantalla de sesión
    if (document.getElementById('lista-asistentes')) {
        initRegistrosPolling();
    }

    // Aplicar tema guardado
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
});
