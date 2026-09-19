# 🚗 Sistema de Gestión de Soporte Técnico Automotriz

Plataforma integral y moderna para la digitalización del ciclo completo de reparación de vehículos en talleres mecánicos.

---

## 🌟 Características Principales

- **Seguridad y Roles**: Autenticación JWT con roles diferenciados para **Administrador (Jefe de Taller)** y **Técnico (Mecánico)**.
- **Catálogo de Clientes y Vehículos**: Registro completo con validación única de documentos, placas y VIN.
- **Ciclo de Vida de Órdenes de Servicio**: Flujo de estados estricto y auditable:
  $$\text{RECEIVED} \longrightarrow \text{IN\_DIAGNOSIS} \longrightarrow \text{IN\_REPAIR} \longrightarrow \text{READY} \longrightarrow \text{DELIVERED}$$
- **Asignación de Mecánicos**: Control de concurrencia que impide asignar más de una orden activa al mismo técnico.
- **Diagnósticos e Intervenciones**: Registro detallado de hallazgos, componentes a reparar, horas de labor y repuestos consumidos.
- **Control de Garantías**: Emisión de garantías sobre mano de obra (`LABOR`) o partes (`PART`) con cálculo automático de vencimiento y consulta de validez en tiempo real.
- **Historial Clínico (*Timeline*)**: Vista cronológica completa de todos los ingresos, diagnósticos, intervenciones y garantías por vehículo.
- **Panel de Control (*Dashboard*)**: Métricas clave en tiempo real, conteo por estados y estado de ocupación de los mecánicos.

---

## 🚀 Modos de Ejecución

### Opción 1: Modo Rápido / Desarrollo Local (Recomendado para visualización inmediata)

El frontend incluye un **motor inteligente de demostración (*Mock DB*)** que permite utilizar y probar el 100% de la funcionalidad de la aplicación de inmediato en el navegador, incluso sin necesidad de tener Docker o MySQL instalados.

1. Abre una terminal en la carpeta `frontend/`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Abre en tu navegador la URL:
   [http://localhost:4173](http://localhost:4173) o la que indique la consola.

---

### Opción 2: Modo Completo con Docker Compose (Full Stack)

Inicia simultáneamente la **Base de Datos (MySQL 8.4)**, el **Backend API (Go)** y el **Frontend (React + Nginx)**:

1. Asegúrate de tener **Docker Desktop** en ejecución.
2. En la raíz del proyecto ejecuta:
   ```bash
   docker compose up --build
   ```
3. Acceso a los servicios:
   - **Frontend Web**: [http://localhost:3000](http://localhost:3000)
   - **Backend API REST**: [http://localhost:8080/api/health](http://localhost:8080/api/health)
   - **Base de Datos MySQL**: Puerto `3306`

---

## 🔑 Credenciales de Acceso Predeterminadas

| Rol | Usuario | Contraseña | Perfil / Especialidad |
|---|---|---|---|
| **Administrador** | `admin` | `admin123` | Jefe de Taller (Acceso Total) |
| **Técnico 1** | `tecnico1` | `admin123` | Juan Pérez (Mecánica General y Frenos) |
| **Técnico 2** | `tecnico2` | `admin123` | Andrés López (Diagnóstico Eléctrico) |

> 💡 *En la pantalla de inicio de sesión cuentas con botones de **Acceso Rápido** para autocompletar estas credenciales con un solo clic.*

---

## 🧪 Pruebas Automatizadas

Para ejecutar la suite de pruebas unitarias y cobertura en el frontend:
```bash
cd frontend
npm test
```
Para compilar la versión de producción:
```bash
cd frontend
npm run build
```

---

## 📁 Arquitectura del Proyecto

```text
├── backend/          # API REST en Go 1.25 (Clean Architecture / Hexagonal)
│   ├── cmd/server/   # Punto de entrada HTTP
│   └── internal/     # Dominio, Casos de Uso, Repositorios MySQL y Transporte
├── database/         # Migraciones DDL versionadas (0001 a 0011) y scripts de seed
├── frontend/         # SPA React 18 + TypeScript + Vite + Tokens CSS
│   └── src/          # Features, Servicios, Componentes y Contexto de Sesión
├── docs/             # PRD detallado de requerimientos
├── docker-compose.yml# Orquestación de contenedores Full-Stack
└── start.bat         # Asistente de inicio rápido para Windows
```
