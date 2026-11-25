# CASOS DE PRUEBA

## Plantilla para diseño y ejecución

*TQA • Documento base para prácticas e integrador*

| 01 · DISEÑAR EL TC | 02 · EJECUTAR LA PRUEBA |
|---|---|
| Definir qué se quiere comprobar y cómo. | Registrar qué ocurrió realmente. |

*Solo incluye diseño y ejecución. La trazabilidad se incorporará más adelante.*

---

## PARTE 1 · PLANTILLA PARA CREAR EL CASO DE PRUEBA

*Completar antes de ejecutar la prueba.*

| | | | |
|---|---|---|---|
| **ID DEL TC** | TC-001 | **PRIORIDAD** | Alta / Media / Baja |
| **TÍTULO** | [Nombre claro del comportamiento] | **TIPO** | Funcional / Negativa / Regresión / etc. |
| **MÓDULO** | [Módulo o funcionalidad] | **AMBIENTE** | QA / Staging / Local |

### 1. Objetivo

| | |
|---|---|
| **¿QUÉ SE QUIERE VALIDAR?** | [Comportamiento específico que se desea comprobar.] |

### 2. Precondiciones

| | |
|---|---|
| **Estado inicial** | [Qué debe estar preparado antes de comenzar.] |
| **Usuario / permisos** | [Tipo de usuario y permisos necesarios.] |
| **Configuración** | [Configuraciones o dependencias necesarias.] |

### 3. Datos de prueba

| | |
|---|---|
| **Dato** | [Nombre del dato] |
| **Valor** | [Valor utilizado] |
| **Origen** | [Generado / preparado / ambiente] |
| **Observación** | [Dato especial o condición relevante] |

### 4. Pasos y resultados esperados

*Los pasos deben ser reproducibles: otro tester debería poder ejecutarlos sin pedir aclaraciones.*

| # | Paso / acción | Dato utilizado | Resultado esperado |
|:---:|---|---|---|
| 1 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |
| 2 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |
| 3 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |
| 4 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |
| 5 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |
| 6 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |
| 7 | [Acción concreta] | [Dato] | [Comportamiento observable esperado] |

### 5. Resultado esperado final

| | |
|---|---|
| **CRITERIO DE ÉXITO** | [Qué debe ocurrir para considerar correcto el caso.] |

---

## PARTE 2 · PLANTILLA PARA EJECUTAR LA PRUEBA

*Completar durante o inmediatamente después de ejecutar el TC.*

| | | | |
|---|---|---|---|
| **ID DEL TC** | TC-001 | **EJECUTADO POR** | [Nombre del tester] |
| **FECHA** | [dd/mm/aaaa] | **HORA** | [hh:mm] |
| **AMBIENTE** | [QA / Staging / Local] | **VERSIÓN** | [Build / versión] |

### 1. Resultado de la ejecución

- [ ] **PASS**
- [ ] **FAIL**
- [ ] **BLOCKED**
- [ ] **NOT RUN**

### 2. Resultado observado

| | |
|---|---|
| **¿QUÉ OCURRIÓ REALMENTE?** | [Describir el comportamiento observado.] |

| | |
|---|---|
| **COMPARACIÓN** | [¿Coincide con lo esperado? Si no, describir la diferencia.] |

### 3. Registro de ejecución por paso

| # | Paso ejecutado | Resultado observado | Estado | Observación |
|:---:|---|---|---|---|
| 1 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |
| 2 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |
| 3 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |
| 4 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |
| 5 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |
| 6 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |
| 7 | [Acción realizada] | [Qué ocurrió] | PASS / FAIL / N/A | [Detalle] |

### 4. Evidencia

| | |
|---|---|
| **Tipo** | Captura / Video / Log / Otro |
| **Nombre o referencia** | [evidencia_TC001_01.png] |
| **Descripción** | [Qué demuestra la evidencia.] |

### 5. Si el resultado es FAIL

| | |
|---|---|
| **DESVIACIÓN ENCONTRADA** | [Qué no coincidió con lo esperado.] |

| | |
|---|---|
| **REFERENCIA DEL DEFECTO** | [BUG-001 / N/A] |

### 6. Observaciones de ejecución

| | |
|---|---|
| **OBSERVACIONES** | [Información adicional relevante.] |

---

## Reglas de uso

- El TC se diseña primero; el resultado observado se registra durante la ejecución.
- El resultado esperado debe estar definido antes de ejecutar.
- **PASS** = coincide; **FAIL** = diferencia verificable; **BLOCKED** = no se pudo ejecutar; **NOT RUN** = aún no ejecutado.
- Las evidencias deben permitir entender el resultado.
- El TC debe ser claro, concreto y reproducible por otro tester.
