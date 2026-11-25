"""Ambiente de behave: driver de Selenium, capturas y reportes automáticos."""
from behave.model import Status

from utils import report_builder
from utils.driver_helper import crear_driver


def before_all(context):
    context.driver = crear_driver()
    context.report_entries = []


def after_scenario(context, scenario):
    try:
        captura = report_builder.guardar_captura(context.driver, scenario)
    except Exception:
        captura = None
    status = "PASS" if scenario.status == Status.passed else "FAIL"
    bug = None
    if status == "FAIL":
        try:
            bug = report_builder.generar_bug_report(scenario, captura)
        except Exception:
            bug = None
    context.report_entries.append(
        {
            "scenario": scenario.name,
            "status": status,
            "screenshot": captura,
            "bug": bug,
        }
    )


def after_all(context):
    if getattr(context, "driver", None):
        try:
            context.driver.quit()
        except Exception:
            pass
    report_builder.escribir_reporte(getattr(context, "report_entries", []))
