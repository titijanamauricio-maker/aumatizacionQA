# TC-005 — Tipo de prueba Servicios Web

<table style="border-collapse:collapse; width:100%; font-family:'Segoe UI',Arial,Helvetica,sans-serif;">
  <thead>
    <tr style="background-color:#E3F1FB;">
      <th style="padding:7px 10px; text-align:left; border-bottom:2px solid #B9D4E8; color:#2E5E9E; font-size:14px;">Campo</th>
      <th style="padding:7px 10px; text-align:left; border-bottom:2px solid #B9D4E8; color:#2E5E9E; font-size:14px;">Valor</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color:#FAFBFC;">
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>ID del TC</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">TC-005</td>
    </tr>
    <tr>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Título</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">Tipo de prueba Servicios Web</td>
    </tr>
    <tr style="background-color:#FAFBFC;">
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Tipo</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">Funcional</td>
    </tr>
    <tr>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Módulo</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">pruebas_funcionales</td>
    </tr>
    <tr style="background-color:#FAFBFC;">
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Ambiente</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">QA (http://127.0.0.1:8001)</td>
    </tr>
  </tbody>
</table>

---

## 1. Objetivo

Verificar el escenario de automatización: Tipo de prueba Servicios Web

---

## 2. Precondiciones

- El sistema responde en http://127.0.0.1:8001.

---

## 3. Pasos

1. Given I open the system page
2. And I am in the Pruebas module
3. When I click "Pruebas funcionales"

---

## 4. Resultado esperado

- Then the following test types appear: Servicios Web
