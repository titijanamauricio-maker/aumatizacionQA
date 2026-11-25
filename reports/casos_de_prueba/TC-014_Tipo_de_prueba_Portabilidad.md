# TC-014

| Campo | Detalle |
|---|---|
| **ID DEL TC** | TC-014 |
| **TÍTULO** | Tipo de prueba Portabilidad |
| **TIPO** | Funcional |
| **MÓDULO** | pruebas_nofuncionales |
| **AMBIENTE** | QA (http://localhost:5175) |

### 1. Objetivo

| ¿QUÉ SE QUIERE VALIDAR? | Verificar el escenario de automatización: Tipo de prueba Portabilidad |

### 2. Precondiciones

| Estado inicial | El sistema responde en http://localhost:5175 |

### 4. Pasos y resultados esperados

1. Given I open the system page
2. And I am in the Pruebas module
3. When I click "Pruebas no funcionales"
4. Then the following test types appear: Portabilidad
