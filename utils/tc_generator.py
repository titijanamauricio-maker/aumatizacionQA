"""Genera archivos de Test Case (TC) a partir de los escenarios de Gherkin en features/."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.driver_helper import BASE_URL

FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "reports" / "casos_de_prueba"


def _feature_scenarios(feature_path):
    scenarios = []
    feature_name = feature_path.stem
    current = None
    for raw in feature_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("Scenario:"):
            if current:
                scenarios.append(current)
            current = {"feature": feature_name, "name": line[len("Scenario:"):].strip(), "steps": []}
        elif current is not None and (line.startswith(("Given", "When", "Then", "And", "But"))):
            current["steps"].append(line)
    if current:
        scenarios.append(current)
    return scenarios


def generar_casos_de_prueba():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for feature_path in sorted(FEATURES_DIR.glob("*.feature")):
        for i, scenario in enumerate(_feature_scenarios(feature_path), start=1):
            n += 1
            tc_id = f"TC-{n:03d}"
            title = scenario["name"]
            module = scenario["feature"]
            steps = scenario["steps"]
            acciones = [s for s in steps if not s.lower().startswith("then")]
            pasos = "\n".join(f"{j}. {s}" for j, s in enumerate(acciones, start=1))
            resultado = "\n".join(
                f"- {s}" for s in steps if s.lower().startswith("then")
            ) or "- El sistema completa el escenario sin errores detectados."
            contenido = f"""# {tc_id} — {title}

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
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">{tc_id}</td>
    </tr>
    <tr>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Título</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">{title}</td>
    </tr>
    <tr style="background-color:#FAFBFC;">
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Tipo</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">Funcional</td>
    </tr>
    <tr>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Módulo</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">{module}</td>
    </tr>
    <tr style="background-color:#FAFBFC;">
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;"><b>Ambiente</b></td>
      <td style="padding:5px 10px; border-bottom:1px solid #E3EBF2;">QA ({BASE_URL})</td>
    </tr>
  </tbody>
</table>

---

## 1. Objetivo

Verificar el escenario de automatización: {title}

---

## 2. Precondiciones

- El sistema responde en {BASE_URL}.

---

## 3. Pasos

{pasos}

---

## 4. Resultado esperado

{resultado}
"""
            path = OUTPUT_DIR / f"{tc_id}_{_slug(title)}.md"
            path.write_text(contenido, encoding="utf-8")
    return n


def _slug(texto):
    return "".join(c if c.isalnum() or c in "-_ " else "_" for c in texto).strip()[:40].replace(" ", "_")


if __name__ == "__main__":
    total = generar_casos_de_prueba()
    print(f"Generados {total} casos de prueba en {OUTPUT_DIR}")
