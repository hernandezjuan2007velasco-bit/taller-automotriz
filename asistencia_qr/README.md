# Sistema de Control de Asistencia QR ? SENA

Sistema web automatizado y seguro para el registro de asistencia presencial y prevenci?n temprana de deserci?n en ambientes de formaci?n del **SENA (Servicio Nacional de Aprendizaje - Regional Huila)**.

Implementa un mecanismo **anti-fraude con c?digos QR din?micos criptogr?ficos (HMAC-SHA256)** que rotan cada 30 segundos, geocercado l?gico por subred IP y consolidaci?n autom?tica de inasistencias.

---

## ?? Documentaci?n de Ingenier?a de Software (00 a 06)

Toda la documentaci?n t?cnica institucional del proyecto est? estructurada bajo el est?ndar oficial SENA ADSO dentro de la carpeta [`docs/`](./docs/):

- **[00 - Gobierno Documental y Git](./docs/00-governance/):** Reglas de documentaci?n, convenciones GitFlow, seguridad de secretos y criterios DoR/DoD.
- **[01 - Contexto y Alcance](./docs/01-context/):** Problem?tica, justificaci?n institucional, l?mites y glosario del dominio.
- **[02 - Dominio y Reglas de Negocio](./docs/02-domain/):** Bounded contexts, entidades, invariantes y cat?logo de eventos.
- **[03 - Producto y Roadmap](./docs/03-product/):** Visi?n del producto, propuesta de valor, roadmap evolutivo y Product Backlog.
- **[04 - Requisitos e Historias de Usuario](./docs/04-requirements/):** Requisitos funcionales (RF-01 a RF-15), RNF, historias de usuario Gherkin y matriz de trazabilidad.
- **[05 - Arquitectura y ADRs](./docs/05-architecture/):** Diagramas C4, topolog?a de despliegue, aspectos transversales y decisiones de arquitectura (ADR).
- **[06 - Datos y Diccionario](./docs/06-data/):** Modelo Entidad-Relaci?n, diccionario de datos de las 8 tablas y migraciones.

---

## ?? Puesta en Marcha (Entorno Local)

### 1. Requisitos Previos
- Python 3.11 o superior.
- Conectividad a internet (para sincronizaci?n con TiDB Cloud Serverless sobre TLS).

### 2. Instalaci?n de Dependencias
```bash
pip install Flask mysql-connector-python "qrcode[pil]" Werkzeug python-dotenv certifi openpyxl
```

### 3. Configuraci?n de Variables de Entorno
Crea un archivo `.env` en la ra?z del proyecto tomando como plantilla `.env.example`:
```ini
FLASK_DEBUG=True
SECRET_KEY=clave-secreta-desarrollo-sena
QR_HMAC_SECRET=clave-secreta-hmac-antifraude

MYSQL_HOST=gateway01.us-east-1.prod.aws.tidbcloud.com
MYSQL_PORT=4000
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contrase?a
MYSQL_DB=asistencia_qr
```

### 4. Inicializar y Verificar Base de Datos
```bash
# Probar conexi?n con pool de conexiones
python test_db.py

# Verificar que todas las plantillas Jinja2 compilen
python test_templates.py
```

### 5. Iniciar Servidor de Desarrollo
```bash
python app.py
```
Abre tu navegador en `http://localhost:5000`.

---

## ?? Credenciales de Prueba Precargadas

| Rol | Documento | Contrase?a | Vista Principal |
|---|---|---|---|
| **Administrador** | `1075000001` | `sena2026` | Panel de Administraci?n (`/admin/panel`) |
| **Instructor** | `1075000002` | `sena2026` | Generador de Sesi?n QR (`/instructor/sesion`) |
| **Aprendiz** | `1075342198` | `sena2026` | Escaneo de Asistencia (`/aprendiz/escanear`) |
