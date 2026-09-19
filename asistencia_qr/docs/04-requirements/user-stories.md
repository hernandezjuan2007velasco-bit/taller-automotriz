# Historias de Usuario (HU) con Criterios Gherkin

> Estado: ?? Estable | ?ltima actualizaci?n: 2026-09-18
> Autor: Equipo de Desarrollo | Equipo: An?lisis y Desarrollo de Software (SENA)

---

### HU-01: Generaci?n de QR de Asistencia Din?mico
**Como** instructor de formaci?n presencial  
**Quiero** generar y proyectar una sesi?n de asistencia con c?digo QR que rota cada 30 segundos  
**Para** permitir que los aprendices registren su llegada sin riesgo de fraude por capturas de pantalla compartidas.

```gherkin
Escenario: Apertura exitosa de sesi?n y proyecci?n de QR
  Dado que el instructor ha iniciado sesi?n y selecciona la ficha "2830145"
  Cuando hace clic en "Iniciar sesi?n de asistencia"
  Entonces el sistema registra la IP del instructor y crea la sesi?n en estado "activa"
  Y proyecta el c?digo QR con una cuenta regresiva circular de 30 segundos
  Y actualiza autom?ticamente la imagen del QR al expirar cada per?odo
```

---

### HU-02: Confirmaci?n de Asistencia del Aprendiz
**Como** aprendiz presente en el ambiente de formaci?n  
**Quiero** escanear el c?digo QR con mi tel?fono m?vil  
**Para** certificar mi puntualidad y asistencia a la clase del d?a.

```gherkin
Escenario: Registro exitoso de asistencia
  Dado que el aprendiz est? matriculado en la ficha "2830145"
  Y est? conectado a la red local del aula
  Cuando escanea el c?digo QR vigente o digita el c?digo de 3 partes (ej: 3-58274901-A7F3E2B1)
  Entonces el sistema valida la firma HMAC y registra el estado "presente" con la hora exacta
  Y muestra la tarjeta verde de confirmaci?n con los datos de la ficha y hora
  Y aparece autom?ticamente en la lista de registros en vivo del instructor
```

```gherkin
Escenario: Rechazo por c?digo QR expirado
  Dado que un aprendiz intenta enviar un c?digo QR que fue generado hace m?s de 60 segundos
  Cuando presiona "Confirmar asistencia"
  Entonces el sistema rechaza la solicitud
  Y muestra la pantalla de advertencia: "El c?digo QR es inv?lido o ya expir?. Escanea el nuevo c?digo."
  Y registra el intento fallido en la bit?cora de auditor?a
```

---

### HU-03: Cierre Autom?tico de Sesi?n e Inasistencias
**Como** instructor de formaci?n  
**Quiero** cerrar la ventana de asistencia al iniciar la clase formal  
**Para** consolidar autom?ticamente como inasistentes a quienes no llegaron a tiempo.

```gherkin
Escenario: Cierre de ventana y asignaci?n masiva de ausencias
  Dado que la sesi?n de la ficha "2830145" tiene 25 aprendices matriculados y 22 registraron asistencia
  Cuando el instructor pulsa el bot?n "Cerrar ventana"
  Entonces el sistema ejecuta una transacci?n at?mica que inserta estado "ausente" para los 3 aprendices faltantes
  Y actualiza el estado de la sesi?n a "cerrada"
  Y deshabilita la generaci?n de nuevos c?digos QR para dicha sesi?n
```

---

### HU-04: Alerta Temprana de Deserci?n
**Como** instructor l?der de ficha  
**Quiero** visualizar de forma destacada a los aprendices con riesgo de deserci?n  
**Para** intervenir pedag?gicamente antes de que alcancen el l?mite reglamentario de faltas.

```gherkin
Escenario: Visualizaci?n de aprendiz en riesgo alto
  Dado que el aprendiz "Cristian David Mu?oz" ha acumulado 3 inasistencias consecutivas
  Cuando el instructor ingresa al m?dulo "Alertas de deserci?n"
  Entonces el sistema muestra una tarjeta con indicador rojo de "Riesgo alto"
  Y permite al instructor redactar una "Nota de seguimiento" y marcar la alerta como atendida
```
