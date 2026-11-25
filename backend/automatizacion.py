"""Motor de automatización — ejercicios (casos) Selenium + generadores de resultados.

Usa Selenium WebDriver con Python para ejecutar los casos definidos en EJERCICIOS.
Cada caso ejecuta asserts (validaciones) y guarda capturas de pantalla.
"""

from __future__ import annotations

import time
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.driver_helper import BASE_URL, crear_driver

TIMEOUT_SEGUNDOS = 15
SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots" / "ejercicios"


def wait_for(driver, locator, timeout=None):
    """Espera la visibilidad de un elemento y lo devuelve."""
    if timeout is None:
        timeout = TIMEOUT_SEGUNDOS
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def guardar_captura(driver, nombre):
    """Guarda una captura de pantalla y devuelve su ruta."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    path = SCREENSHOTS_DIR / nombre
    driver.save_screenshot(str(path))
    return str(path)


def ejercicio_001(driver):
    """EJ-001 — Abrir el sistema y verificar el título 'Pruebas QA' del sidebar."""
    driver.get(BASE_URL)

    brand = wait_for(driver, (By.XPATH, "//aside//p[normalize-space() = 'Pruebas QA']"))
    assert "pruebas qa" in brand.text.strip().lower()

    h1 = wait_for(driver, (By.XPATH, "//main//h1[normalize-space() = 'Pruebas']"))
    assert h1.is_displayed()

    assert driver.find_element(By.ID, "titulo-app").text.strip() == "Pruebas QA"

    assert driver.find_elements(By.CSS_SELECTOR, "aside p")

    return True, "Validaciones: brand XPath, encabezado Pruebas XPath, ID titulo-app, CSS aside p", [
        guardar_captura(driver, "EJ-001.png")
    ]


def ejercicio_002(driver):
    """EJ-002 — Entrar al módulo Pruebas y verificar el encabezado."""
    driver.get(BASE_URL)
    wait_for(driver, (By.XPATH, "//aside//p[normalize-space() = 'Pruebas QA']"))

    wait_for(driver, (By.ID, "btn-modulo-pruebas")).click()

    h1 = wait_for(driver, (By.NAME, "titulo_pruebas"))
    assert h1.text.strip() == "Pruebas"

    desc = wait_for(
        driver,
        (
            By.XPATH,
            "//main//p[normalize-space() = 'Automatización del sistema con "
            "pruebas funcionales y no funcionales.']",
        ),
    )
    assert desc.is_displayed()

    assert driver.find_element(By.CSS_SELECTOR, "#titulo-pruebas").text.strip() == "Pruebas"

    return True, "Validaciones: ID btn-modulo-pruebas, NAME titulo_pruebas, XPath descripción, CSS #titulo-pruebas", [
        guardar_captura(driver, "EJ-002.png")
    ]


def ejercicio_003(driver):
    """EJ-003 — Verificar los botones de pruebas funcionales y no funcionales."""
    driver.get(BASE_URL)
    wait_for(driver, (By.ID, "btn-modulo-pruebas")).click()
    wait_for(driver, (By.NAME, "titulo_pruebas"))

    btn_funcionales = wait_for(driver, (By.CSS_SELECTOR, "#btn-pruebas-funcionales"))
    assert "pruebas funcionales" in btn_funcionales.text.strip().lower()

    btn_nofuncionales = wait_for(driver, (By.CSS_SELECTOR, "#btn-pruebas-no-funcionales"))
    assert "pruebas no funcionales" in btn_nofuncionales.text.strip().lower()

    return True, "Validaciones: CSS #btn-pruebas-funcionales y #btn-pruebas-no-funcionales", [
        guardar_captura(driver, "EJ-003.png")
    ]


def ejercicio_004(driver):
    """EJ-004 — Verificar rendimiento del sistema (prueba no funcional)."""
    inicio = time.time()
    driver.get(BASE_URL)
    wait_for(driver, (By.XPATH, "//aside//p[normalize-space() = 'Pruebas QA']"))
    duracion = time.time() - inicio
    assert duracion < 15, f"Tiempo de carga demasiado alto: {duracion:.2f}s"
    assert driver.find_element(By.ID, "titulo-app").text.strip() == "Pruebas QA"
    return True, f"Tiempo de carga: {duracion:.2f} s", [guardar_captura(driver, "EJ-004.png")]


def ejercicio_005(driver):
    """EJ-005 — Verificar respuesta repetida del sistema (prueba no funcional)."""
    tiempos = []
    for _ in range(2):
        inicio = time.time()
        driver.get(BASE_URL)
        wait_for(driver, (By.ID, "titulo-app"))
        tiempos.append(round(time.time() - inicio, 2))
    assert all(t < 15 for t in tiempos), f"Tiempos fuera de rango: {tiempos}"
    return True, f"Cargas verificadas (2): {tiempos}", [guardar_captura(driver, "EJ-005.png")]


def ejercicio_006(driver):
    """EJ-006 — Abrir la página del sistema y verificar que se carga."""
    driver.get(BASE_URL)
    wait_for(driver, (By.TAG_NAME, "body"))
    assert driver.current_url.startswith(BASE_URL), (
        f"URL inesperada: {driver.current_url}"
    )
    return True, f"Página cargada: {driver.current_url}", [
        guardar_captura(driver, "EJ-006.png")
    ]


def ejercicio_007(driver):
    """EJ-007 — Verificar el tiempo de carga del sistema (Rendimiento)."""
    inicio = time.time()
    driver.get(BASE_URL)
    wait_for(driver, (By.TAG_NAME, "body"))
    duracion = time.time() - inicio
    assert duracion < 10, f"Tiempo de carga demasiado alto: {duracion:.2f}s"
    return True, f"Tiempo de carga: {duracion:.2f} s", [guardar_captura(driver, "EJ-007.png")]


def ejercicio_008(driver):
    """EJ-008 — Generar carga de estrés: carga repetida y verifica respuesta."""
    tiempos = []
    for _ in range(5):
        inicio = time.time()
        driver.get(BASE_URL)
        wait_for(driver, (By.TAG_NAME, "body"))
        tiempos.append(round(time.time() - inicio, 2))
    assert all(t < 10 for t in tiempos), f"Tiempos fuera de rango: {tiempos}"
    return True, f"Cargas bajo carga de estrés (5): {tiempos}", [guardar_captura(driver, "EJ-008.png")]


def ejercicio_009(driver):
    """EJ-009 — Caso de prueba que falla (demostración de estado FAIL)."""
    driver.get(BASE_URL)
    wait_for(driver, (By.TAG_NAME, "body"))
    assert driver.find_element(By.ID, "elemento-que-no-existe"), "Elemento esperado ausente en el sistema"


EJERCICIOS = [
    {
        "id": "EJ-001",
        "nombre": "Abrir el sistema y verificar el título 'Pruebas QA' del sidebar",
        "func": ejercicio_001,
    },
    {
        "id": "EJ-002",
        "nombre": "Entrar al módulo Pruebas y verificar el encabezado 'Pruebas'",
        "func": ejercicio_002,
    },
    {
        "id": "EJ-003",
        "nombre": "Ver los botones de pruebas funcionales y no funcionales",
        "func": ejercicio_003,
    },
    {
        "id": "EJ-004",
        "nombre": "Verificar el tiempo de carga del sistema (pruebas no funcionales)",
        "func": ejercicio_004,
    },
    {
        "id": "EJ-005",
        "nombre": "Verificar la respuesta repetida del sistema (pruebas no funcionales)",
        "func": ejercicio_005,
    },
    {
        "id": "EJ-006",
        "nombre": "Abrir la página del sistema (http://127.0.0.1:8001) y verificar que se carga",
        "func": ejercicio_006,
    },
    {
        "id": "EJ-007",
        "nombre": "Verificar el tiempo de carga del sistema (pruebas no funcionales - Rendimiento)",
        "func": ejercicio_007,
    },
    {
        "id": "EJ-008",
        "nombre": "Generar carga de estrés y verificar la respuesta del sistema (Carga de estrés)",
        "func": ejercicio_008,
    },
    {
        "id": "EJ-009",
        "nombre": "Caso de prueba que falla (demostración de estado FAIL)",
        "func": ejercicio_009,
    },
]

# Suites disponibles en la interfaz y los casos que los ejecutan.
SUITE_CASOS = {
    "Smoke": ["EJ-006"],
    "Sanity": ["EJ-006"],
    "Regression": ["EJ-006"],
    "Integración": ["EJ-006"],
    "End-to-End": ["EJ-006"],
    "Performance": ["EJ-006"],
    "Carga": ["EJ-006"],
    "Rendimiento": ["EJ-007"],
    "Carga de estrés": ["EJ-008"],
}
SUITES = list(SUITE_CASOS)


def ejecutar_ejercicio(ejercicio, driver):
    """Ejecuta un ejercicio con el driver dado y devuelve su resultado."""
    inicio = time.time()
    capturas = []
    try:
        ok, mensaje, capturas = ejercicio["func"](driver)
        estado = "PASS" if ok else "FAIL"
    except Exception as exc:  # noqa: BLE001
        estado, mensaje = "FAIL", f"{type(exc).__name__}: {exc}"
    return {
        "id": ejercicio["id"],
        "nombre": ejercicio["nombre"],
        "estado": estado,
        "mensaje": mensaje,
        "duracion_seg": round(time.time() - inicio, 2),
        "capturas": capturas,
    }


def ejecutar_suite(suite, tipo="funcional", progreso=None, modo_visual=False, timeout_seg=None):
    """Ejecuta los casos de una suite con un navegador (Selenium).

    ``modo_visual=True`` abre el navegador visible (para ver lo que está
    haciendo); ``modo_visual=False`` (modo de fondo, por defecto) lo
    ejecuta sin mostrarse. ``timeout_seg`` (1-10) ajusta el tiempo de
    espera de los elementos.
    """
    global TIMEOUT_SEGUNDOS
    if timeout_seg is not None:
        TIMEOUT_SEGUNDOS = timeout_seg
    driver = crear_driver("chrome", headless=not modo_visual)
    casos = []
    try:
        for eid in SUITE_CASOS.get(suite, []):
            ejercicio = next((e for e in EJERCICIOS if e["id"] == eid), None)
            if ejercicio is None:
                continue
            if progreso is not None:
                progreso(ejercicio)
            resultado = ejecutar_ejercicio(ejercicio, driver)
            resultado["tipo"] = tipo
            casos.append(resultado)
    finally:
        driver.quit()
    return casos
