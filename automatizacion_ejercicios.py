"""Automatización Selenium con Python — 3 ejercicios seleccionados.

Requisitos mínimos cumplidos por este script:
- Utiliza Selenium WebDriver con Python (crear via utils.driver_helper).
- Selecciona únicamente 3 ejercicios (ver EJERCICIOS_SELECCIONADOS).
- Implementa al menos 2 asserts (validaciones) por cada ejercicio.
- Implementa al menos 1 captura de pantalla por cada ejercicio.
- Utiliza diferentes tipos de localizadores: ID, Name, XPath y CSS Selector.

Ejecutar:
    python automatizacion_ejercicios.py

El sistema automatizado debe estar corriendo en BASE_URL
(utils/driver_helper.py: http://localhost:5174).
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.driver_helper import BASE_URL, crear_driver

# --- Selección de ejercicios: se seleccionan únicamente 3 -------------------
EJERCICIOS_SELECCIONADOS = 3

TIMEOUT_SEGUNDOS = 15
SCREENSHOTS_DIR = Path(__file__).resolve().parent / "reports" / "screenshots" / "ejercicios"


def wait_for(driver, locator, timeout=TIMEOUT_SEGUNDOS):
    """Espera a que un elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def guardar_captura_ejercicio(driver, exercise_id):
    """Guarda una captura de pantalla por ejercicio y la devuelve."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOTS_DIR / f"{exercise_id}_{stamp}.png"
    driver.save_screenshot(str(path))
    return path


def _ejercicios_por_id():
    return {e["id"]: e for e in EJERCICIOS}


def guardar_resumen(resultados, capturas):
    """Escribe el resumen de la ejecución en reports/automatizacion_ejercicios.md."""
    from utils import report_builder

    by_id = _ejercicios_por_id()
    lineas = [
        "# Resumen de Automatización — Ejercicios Selenium",
        f"- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"- Sistema automatizado: {BASE_URL}",
        f"- Ejercicios seleccionados: {EJERCICIOS_SELECCIONADOS}",
        "",
        "| Ejercicio | Estado | Captura |",
        "|---|---|---|",
    ]
    for (eid, ok), shot in zip(resultados, capturas):
        rel = (
            shot.relative_to(report_builder.REPORTS_DIR).as_posix() if shot else "-"
        )
        lineas.append(f"| {eid} — {by_id[eid]['name']} | {'PASS' if ok else 'FAIL'} | {rel} |")
    fallidos = [eid for eid, ok in resultados if not ok]
    lineas.append("")
    lineas.append(f"Ejercicios fallidos: {fallidos if fallidos else 'ninguno'}.")
    path = report_builder.REPORTS_DIR / "automatizacion_ejercicios.md"
    path.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return path


def registrar_en_historial(resultados, capturas):
    """Registra los ejercicios en el historial del sistema (public/historial.json)."""
    from utils import report_builder

    by_id = _ejercicios_por_id()
    entradas = [
        {
            "scenario": f"{eid} — {by_id[eid]['name']}",
            "status": "PASS" if ok else "FAIL",
            "screenshot": str(shot) if shot else None,
            "bug": None,
        }
        for (eid, ok), shot in zip(resultados, capturas)
    ]
    try:
        report_builder.escribir_reporte(entradas)
    except Exception as exc:  # noqa: BLE001
        print(f"[Automatización] No se pudo registrar el historial: {exc}")
        return False
    return True


def ejercicio_001(driver):
    """EJ-001 — Abrir el sistema y verificar el título 'Pruebas QA' del sidebar."""
    driver.get(BASE_URL)

    # Validación 1 — XPath: título del brand del sidebar.
    brand = wait_for(
        driver, (By.XPATH, "//aside//p[normalize-space() = 'Pruebas QA']")
    )
    assert "pruebas qa" in brand.text.strip().lower()

    # Validación 2 — XPath: encabezado principal "Pruebas".
    h1 = wait_for(driver, (By.XPATH, "//main//h1[normalize-space() = 'Pruebas']"))
    assert h1.is_displayed()

    # Validación 3 — ID: título de la app (id agregado al app para automatizar).
    assert driver.find_element(By.ID, "titulo-app").text.strip() == "Pruebas QA"

    # Validación 4 — CSS Selector: elementos p del aside.
    assert driver.find_elements(By.CSS_SELECTOR, "aside p")

    shot = guardar_captura_ejercicio(driver, "EJ-001")
    print(f"[EJ-001] OK — captura: {shot.name}")
    return shot


def ejercicio_002(driver):
    """EJ-002 — Entrar al módulo Pruebas y verificar el encabezado."""
    driver.get(BASE_URL)
    wait_for(driver, (By.XPATH, "//aside//p[normalize-space() = 'Pruebas QA']"))

    # Validación 1 — ID: botón del módulo Pruebas (id agregado al app).
    btn = wait_for(driver, (By.ID, "btn-modulo-pruebas"))
    btn.click()

    # Validación 2 — NAME: encabezado del módulo (name agregado al app).
    h1 = wait_for(driver, (By.NAME, "titulo_pruebas"))
    assert h1.text.strip() == "Pruebas"

    # Validación 3 — XPath: descripción de la vista Pruebas.
    desc = wait_for(
        driver,
        (
            By.XPATH,
            "//main//p[normalize-space() = 'Automatización del sistema con "
            "pruebas funcionales y no funcionales.']",
        ),
    )
    assert desc.is_displayed()

    # Validación 4 — CSS Selector: ID del encabezado.
    assert driver.find_element(By.CSS_SELECTOR, "#titulo-pruebas").text.strip() == "Pruebas"

    shot = guardar_captura_ejercicio(driver, "EJ-002")
    print(f"[EJ-002] OK — captura: {shot.name}")
    return shot


def ejercicio_003(driver):
    """EJ-003 — Verificar los botones de pruebas funcionales y no funcionales."""
    driver.get(BASE_URL)
    wait_for(driver, (By.ID, "btn-modulo-pruebas")).click()
    wait_for(driver, (By.NAME, "titulo_pruebas"))

    # Validación 1 — CSS Selector: botón "Pruebas funcionales".
    btn_funcionales = wait_for(driver, (By.CSS_SELECTOR, "#btn-pruebas-funcionales"))
    assert "pruebas funcionales" in btn_funcionales.text.strip().lower()

    # Validación 2 — CSS Selector: botón "Pruebas no funcionales".
    btn_nofuncionales = wait_for(driver, (By.CSS_SELECTOR, "#btn-pruebas-no-funcionales"))
    assert "pruebas no funcionales" in btn_nofuncionales.text.strip().lower()

    shot = guardar_captura_ejercicio(driver, "EJ-003")
    print(f"[EJ-003] OK — captura: {shot.name}")
    return shot


EJERCICIOS = [
    {
        "id": "EJ-001",
        "name": "Abrir el sistema y verificar el título 'Pruebas QA' del sidebar",
        "func": ejercicio_001,
    },
    {
        "id": "EJ-002",
        "name": "Entrar al módulo Pruebas y verificar el encabezado 'Pruebas'",
        "func": ejercicio_002,
    },
    {
        "id": "EJ-003",
        "name": "Ver los botones de pruebas funcionales y no funcionales",
        "func": ejercicio_003,
    },
]

assert len(EJERCICIOS) == EJERCICIOS_SELECCIONADOS, (
    f"Se seleccionan únicamente {EJERCICIOS_SELECCIONADOS} ejercicios."
)


def main():
    driver = crear_driver()
    resultados = []
    capturas = []
    try:
        for ejercicio in EJERCICIOS:
            print(f"\n=== {ejercicio['id']} — {ejercicio['name']} ===")
            shot = None
            try:
                shot = ejercicio["func"](driver)
                resultados.append((ejercicio["id"], True))
            except Exception as exc:  # noqa: BLE001
                resultados.append((ejercicio["id"], False))
                print(f"[{ejercicio['id']}] FAIL — {exc}")
                try:
                    shot = guardar_captura_ejercicio(driver, ejercicio["id"])
                    print(f"[{ejercicio['id']}] captura de fallo: {shot.name}")
                except Exception:  # noqa: BLE001
                    pass
            capturas.append(shot)
    finally:
        driver.quit()

    print("\n--- Resumen ---")
    for eid, ok in resultados:
        print(f"{eid}: {'PASS' if ok else 'FAIL'}")

    resumen = guardar_resumen(resultados, capturas)
    print(f"Resumen guardado: {resumen.name}")
    registrar_en_historial(resultados, capturas)

    fallidos = [eid for eid, ok in resultados if not ok]
    if fallidos:
        print(f"\nEjercicios fallidos: {fallidos}")
        return 1
    print(f"\nTodos los ejercicios pasaron ({len(resultados)}/{len(resultados)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
