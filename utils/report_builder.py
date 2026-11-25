"""Construye el reporte de ejecución: capturas de pantalla, casos de prueba y reportes de bugs."""
import json
from datetime import datetime
from pathlib import Path

from utils.driver_helper import BASE_URL

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
BUGS_DIR = REPORTS_DIR / "bugs"
PUBLIC_HISTORIAL = Path(__file__).resolve().parent.parent / "public" / "historial.json"


def inicializar_directorios():
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    BUGS_DIR.mkdir(parents=True, exist_ok=True)


def _nombre_seguro(texto):
    return (
        "".join(c if c.isalnum() or c in "-_. " else "_" for c in texto)
        .strip()[:50]
        or "escenario"
    )


def guardar_captura(driver, scenario):
    """Toma una captura de pantalla de lo que está haciendo Selenium."""
    inicializar_directorios()
    nombre = f"{_nombre_seguro(scenario.name)}_{abs(id(scenario)) % 1000}.png"
    path = SCREENSHOTS_DIR / nombre
    driver.save_screenshot(str(path))
    return path


def generar_bug_report(scenario, screenshot_path):
    """Genera un reporte de bug al estilo de Bug_report_template_ejemplo.md."""
    BUGS_DIR.mkdir(parents=True, exist_ok=True)
    nombre = f"BUG-{_nombre_seguro(scenario.name)}.md"
    path = BUGS_DIR / nombre
    status_name = getattr(scenario.status, "name", scenario.status)
    steps = "\n".join(
        f"{i}. {step.name} — {getattr(step, 'status', '')}"
        for i, step in enumerate(scenario.steps, 1)
    )
    contenido = f"""# Bug Report

## BUG-{_nombre_seguro(scenario.name)} · Bug Report

| Campo | Detalle |
|---|---|
| **Title** | Fallo detectado automáticamente en: {scenario.name} |
| **Descripción** | El escenario de prueba '{scenario.name}' no cumplió el resultado esperado durante la ejecución automatizada de '{BASE_URL}'. |
| **Pasos** | {steps} |
| **RESULTADO ACTUAL** | El escenario falló con estado: {status_name}. |
| **RESULTADO ESPERADO** | El escenario debe pasar durante la ejecución de behave. |
| **PRIORIDAD** | Media (escala 1-5) |
| **SEVERIDAD** | Media (escala 1-5) |
| **AMBIENTE** | Chrome / Windows 10 |
| **ADJUNTOS** | {screenshot_path} |
"""
    path.write_text(contenido, encoding="utf-8")
    return path


def escribir_reporte(entradas):
    """Escribe el reporte principal con los casos de prueba (escenarios)."""
    inicializar_directorios()
    lineas = [
        f"# Reporte de Ejecución — Sistema Fábrica de Fideos (Pruebas QA) - {BASE_URL}",
        f"- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"- Casos de prueba ejecutados: {len(entradas)}",
        "",
        "| Caso de prueba | Estado | Captura | Reporte de bug |",
        "|---|---|---|---|",
    ]
    for e in entradas:
        captura = (
            f"[ver]({Path(e['screenshot']).relative_to(REPORTS_DIR)})"
            if e["screenshot"]
            else "-"
        )
        bug = (
            f"[ver]({Path(e['bug']).relative_to(REPORTS_DIR)})" if e["bug"] else "-"
        )
        lineas.append(f"| {e['scenario']} | {e['status']} | {captura} | {bug} |")
    reporte = REPORTS_DIR / "reporte.md"
    reporte.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    # Resultados para el módulo Historial (consumido por la app en runtime).
    entradas_json = [
        {
            "scenario": e["scenario"],
            "status": e["status"],
            "screenshot": str(e["screenshot"]) if e["screenshot"] else None,
            "bug": str(e["bug"]) if e["bug"] else None,
        }
        for e in entradas
    ]
    PUBLIC_HISTORIAL.write_text(
        json.dumps(entradas_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return reporte
