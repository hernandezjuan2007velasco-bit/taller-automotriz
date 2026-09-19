# Vista General de Arquitectura (Modelo C4)

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

El sistema **Asistencia QR** sigue una arquitectura limpia basada en el patr?n arquitect?nico **Modelo-Vista-Controlador (MVC)** modularizado mediante Blueprints de Flask.

---

## 1. Nivel 1: Diagrama de Contexto del Sistema

```mermaid
graph TD
    Instructor["Instructor SENA<br/>[Persona]"]
    Aprendiz["Aprendiz SENA<br/>[Persona]"]
    Admin["Administrador del Sistema<br/>[Persona]"]
    
    Sistema["Sistema Asistencia QR<br/>[Software System]"]
    
    TiDB["TiDB Cloud Serverless<br/>[External Database System]"]
    
    Instructor -->|Genera sesi?n, proyecta QR y consulta alertas| Sistema
    Aprendiz -->|Escanea c?digo QR y confirma presencia| Sistema
    Admin -->|Gestiona usuarios, fichas y par?metros| Sistema
    
    Sistema -->|Persiste datos sobre conexi?n TLS 1.2+| TiDB
```

---

## 2. Nivel 2: Diagrama de Contenedores

```mermaid
graph TD
    subgraph Browser ["Navegador Cliente (Desktop / M?vil)"]
        SPA["HTML5 + CSS3 + Vanilla JS<br/>(Polling AJAX, Toasts, Dark Mode)"]
    end
    
    subgraph AppServer ["Servidor Web & Aplicaci?n (Flask / Gunicorn)"]
        Router["WSGI Router"]
        Controllers["Flask Blueprints<br/>(Auth, Instructor, Aprendiz, Admin)"]
        Security["M?dulo de Seguridad<br/>(HMAC, Subred, Passwords)"]
        Models["Modelos de Datos & Pool de Conexiones<br/>(mysql.connector.pooling)"]
    end
    
    subgraph CloudDB ["Base de Datos en la Nube"]
        DB[(TiDB Cloud / MySQL)]
    end
    
    SPA -->|HTTPS / REST / JSON / Forms| Router
    Router --> Controllers
    Controllers --> Security
    Controllers --> Models
    Models -->|MySQL Protocol + TLS / Port 4000| DB
```

---

## 3. Nivel 3: Diagrama de Componentes (Controladores)

- `auth_controller.py`: Maneja login, logout y decorador de autorizaci?n `@requiere_rol`.
- `instructor_controller.py`: Coordina la apertura de sesiones, generaci?n de im?genes QR en base64 v?a `qrcode`, polling de registros en tiempo real, correcciones manuales y exportaci?n a Excel con `openpyxl`.
- `aprendiz_controller.py`: Recibe el c?digo ef?mero y orquesta las 5 validaciones anti-fraude antes de registrar la asistencia.
- `admin_controller.py`: Controla la gesti?n de fichas, usuarios, auditor?a forense y par?metros globales.
