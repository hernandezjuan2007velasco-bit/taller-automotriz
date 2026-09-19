CREATE DATABASE IF NOT EXISTS asistencia_qr;
USE asistencia_qr;

CREATE TABLE IF NOT EXISTS configuracion (
    clave VARCHAR(50) PRIMARY KEY,
    valor VARCHAR(255) NOT NULL,
    descripcion TEXT
);

INSERT IGNORE INTO configuracion (clave, valor, descripcion) VALUES
('qr_rotacion_segundos', '30', 'Tiempo de rotación del código QR en segundos'),
('umbral_alerta_moderada', '10', 'Porcentaje de inasistencia para alerta moderada'),
('umbral_alerta_alta', '3', 'Cantidad de inasistencias consecutivas para alerta alta');

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('instructor', 'admin', 'aprendiz') NOT NULL,
    centro VARCHAR(100) NOT NULL,
    estado ENUM('activo', 'desactivado') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fichas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL UNIQUE,
    programa VARCHAR(150) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    instructor_id INT NOT NULL,
    estado ENUM('activa', 'suspendida', 'finalizada', 'archivada') DEFAULT 'activa',
    fecha_apertura DATE,
    fecha_cierre DATE,
    FOREIGN KEY (instructor_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS ficha_aprendiz (
    ficha_id INT NOT NULL,
    aprendiz_id INT NOT NULL,
    PRIMARY KEY (ficha_id, aprendiz_id),
    FOREIGN KEY (ficha_id) REFERENCES fichas(id),
    FOREIGN KEY (aprendiz_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS sesiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ficha_id INT NOT NULL,
    instructor_id INT NOT NULL,
    codigo_actual VARCHAR(100),
    codigo_timestamp INT,
    ip_instructor VARCHAR(45) NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME,
    estado ENUM('activa', 'cerrada') DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ficha_id) REFERENCES fichas(id),
    FOREIGN KEY (instructor_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sesion_id INT NOT NULL,
    aprendiz_id INT NOT NULL,
    hora_registro TIME,
    ip_registro VARCHAR(45),
    estado ENUM('presente', 'ausente', 'corregido') DEFAULT 'presente',
    motivo_correccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_sesion_aprendiz (sesion_id, aprendiz_id),
    FOREIGN KEY (sesion_id) REFERENCES sesiones(id),
    FOREIGN KEY (aprendiz_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aprendiz_id INT NOT NULL,
    ficha_id INT NOT NULL,
    tipo ENUM('riesgo_alto', 'riesgo_moderado') NOT NULL,
    descripcion TEXT NOT NULL,
    porcentaje_riesgo INT NOT NULL,
    estado ENUM('activa', 'atendida') DEFAULT 'activa',
    nota_seguimiento TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aprendiz_id) REFERENCES usuarios(id),
    FOREIGN KEY (ficha_id) REFERENCES fichas(id)
);

CREATE TABLE IF NOT EXISTS auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    ip_origen VARCHAR(45) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    resultado ENUM('exitoso', 'fallido') NOT NULL,
    detalle TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
