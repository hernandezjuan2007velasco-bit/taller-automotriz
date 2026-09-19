# Convenciones de Git y Control de Versiones

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

## 1. Estrategia de Ramificaci?n (GitFlow Simplificado)

El repositorio opera con tres ramas permanentes y ramas de ciclo de vida corto:

```
main (Producci?n estable)
  ? (Release / Hotfix)
develop (Integraci?n continua)
  ? (Pull Requests aprobados)
feature/asistencia-* | bugfix/* | docs/*
```

- `main`: C?digo probado y desplegado en producci?n (Render / TiDB Cloud). Protegido contra commits directos.
- `develop`: Rama base de desarrollo donde convergen las nuevas caracter?sticas.
- `feature/<modulo>-<descripcion>`: Ramas para desarrollo de nuevas funciones (ej: `feature/asistencia-export-excel`).
- `bugfix/<modulo>-<descripcion>`: Correcciones sobre desarrollo (ej: `bugfix/instructor-ficha-selector`).
- `hotfix/<descripcion>`: Correcciones urgentes aplicadas directamente sobre `main` y luego integradas a `develop`.

## 2. Convenci?n de Commits Sem?nticos

Se adopta el est?ndar de *Conventional Commits*:

`tipo(alcance): descripci?n breve en imperativo`

| Tipo | Prop?sito | Ejemplo |
|---|---|---|
| `feat` | Nueva caracter?stica | `feat(qr): implementar rotaci?n HMAC cada 30 segundos` |
| `fix` | Correcci?n de bug | `fix(instructor): corregir propiedad ficha.numero en selector` |
| `docs` | Cambios en documentaci?n | `docs(domain): agregar mapa de entidades y reglas de negocio` |
| `refactor` | Refactorizaci?n de c?digo sin cambio de comportamiento | `refactor(db): agregar pool de conexiones MySQL` |
| `sec` | Ajuste de seguridad | `sec(env): purgar credenciales quemadas en scripts de test` |
| `test` | Incorporaci?n o ajuste de pruebas | `test(templates): validar renderizado de todas las vistas` |

## 3. Pol?ticas de Pull Request (PR)

1. Todo PR hacia `main` o `develop` debe contar con revisi?n aprobada.
2. Los commits deben estar rebasados y libres de conflictos.
3. Se proh?be el uso de `git push --force` en ramas compartidas.
