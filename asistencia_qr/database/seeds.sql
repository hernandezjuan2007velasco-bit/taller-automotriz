USE asistencia_qr;

-- Hash of 'sena2026' using werkzeug's generate_password_hash('sena2026')
-- En Python: from werkzeug.security import generate_password_hash; generate_password_hash('sena2026')
-- Resultado precomputado:
SET @password = 'scrypt:32768:8:1$K5FqjSxk9R$81d4b64f9f74a00888df546df0e61d82f7c00e6a1005fbc358beaf2535efcfcc87af9f4b642e078cba0c9b634cc3f5de019e09d17d057790b9b3cc180bb29d93';

-- Usuarios (Administrador y Instructores)
INSERT INTO usuarios (nombre, documento, password_hash, rol, centro, estado) VALUES
('Rodrigo Muñoz', '1075000001', @password, 'admin', 'Neiva', 'activo'),
('Diana Rojas', '1075000002', @password, 'instructor', 'Neiva', 'activo'),
('Javier Coronado', '1075000003', @password, 'instructor', 'Neiva', 'activo'),
('Liliana Artunduaga', '1075000004', @password, 'instructor', 'Pitalito', 'desactivado');

-- Obtener IDs de instructores para usarlos después
SET @id_diana = (SELECT id FROM usuarios WHERE documento = '1075000002');

-- Fichas
INSERT INTO fichas (numero, programa, sede, instructor_id) VALUES
('2830145', 'Análisis y Desarrollo de Software', 'Neiva', @id_diana);

SET @id_ficha = (SELECT id FROM fichas WHERE numero = '2830145');

-- Aprendices
INSERT INTO usuarios (nombre, documento, password_hash, rol, centro, estado) VALUES
('Juan Esteban Perdomo', '1075342198', @password, 'aprendiz', 'Neiva', 'activo'),
('Laura Sofía Trujillo', '1075361027', @password, 'aprendiz', 'Neiva', 'activo'),
('Camilo Andrés Vargas', '1075398204', @password, 'aprendiz', 'Neiva', 'activo'),
('Valentina Cerquera', '1075401152', @password, 'aprendiz', 'Neiva', 'activo'),
('Sebastián Ortiz Polanía', '1075417765', @password, 'aprendiz', 'Neiva', 'activo'),
('María Fernanda Guzmán', '1075420981', @password, 'aprendiz', 'Neiva', 'activo'),
('Andrés Felipe Ospina', '1075433410', @password, 'aprendiz', 'Neiva', 'activo'),
('Natalia Ximena Bermeo', '1075447792', @password, 'aprendiz', 'Neiva', 'activo'),
('Cristian David Muñoz', '1075455310', @password, 'aprendiz', 'Neiva', 'activo'),
('Ricardo Gómez Salazar', '1075462014', @password, 'aprendiz', 'Neiva', 'activo'),
('Paula Andrea León', '1075479903', @password, 'aprendiz', 'Neiva', 'activo');

-- Relación ficha_aprendiz
INSERT INTO ficha_aprendiz (ficha_id, aprendiz_id)
SELECT @id_ficha, id FROM usuarios WHERE rol = 'aprendiz';

-- Alertas (Ejemplos de Mockup)
SET @id_cristian = (SELECT id FROM usuarios WHERE documento = '1075455310');
SET @id_andres = (SELECT id FROM usuarios WHERE documento = '1075433410');
SET @id_natalia = (SELECT id FROM usuarios WHERE documento = '1075447792');

INSERT INTO alertas (aprendiz_id, ficha_id, tipo, descripcion, porcentaje_riesgo, estado) VALUES
(@id_cristian, @id_ficha, 'riesgo_alto', 'Inasistencia consecutiva crítica', 86, 'activa'),
(@id_andres, @id_ficha, 'riesgo_moderado', 'Inasistencia repetitiva, bajando rendimiento', 55, 'activa'),
(@id_natalia, @id_ficha, 'riesgo_moderado', 'Faltas recurrentes injustificadas', 48, 'activa');

-- Auditoría
INSERT INTO auditoria (usuario_id, ip_origen, accion, resultado, detalle) VALUES
(1, '192.168.1.10', 'Inicio de sesión', 'exitoso', 'El administrador inició sesión correctamente'),
(@id_diana, '192.168.1.15', 'Inicio de sesión', 'exitoso', 'Instructor inició sesión'),
(@id_diana, '192.168.1.15', 'Creación de sesión', 'exitoso', 'Sesión iniciada para ficha 2830145'),
(@id_cristian, '192.168.1.20', 'Registro de asistencia', 'fallido', 'IP fuera de la subred del instructor');
