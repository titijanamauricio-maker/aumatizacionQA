"""Orquestador de Automatización de Pruebas QA — API de ejecución y resultados."""

from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar directamente: python backend/orquestador.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import os
import re
import smtplib
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from email.message import EmailMessage

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import automatizacion, reportes
from utils import report_builder

app = FastAPI(title="Orquestador — Automatización de Pruebas QA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TAREAS = {}
_executor = ThreadPoolExecutor(max_workers=3)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class PeticionEjecucion(BaseModel):
    tipo: str = "funcional"
    suite: str = "Smoke"
    email: str = ""
    modo_visual: bool = False
    timeout_seg: int = 10


def _validar_tipo(tipo):
    if tipo not in ("funcional", "no funcional"):
        raise HTTPException(422, "Tipo de pruebas no válido. Use 'funcional' o 'no funcional'.")


def _validar_email(email):
    if email and not EMAIL_RE.match(email):
        raise HTTPException(422, f"Formato de correo no válido: {email}")


def _enviar_reportes(tarea):
    """Envía los reportes adjuntados por correo (SMTP). Sin SMTP_HOST, queda pendiente."""
    if not tarea.get("email"):
        return "pendiente (sin correo ingresado)"
    if not os.environ.get("SMTP_HOST"):
        return "pendiente (SMTP_HOST no configurado)"
    msg = EmailMessage()
    msg["Subject"] = (
        f"Reporte de automatización – {tarea['suite']} – {tarea['fecha_fin'][:10]}"
    )
    msg["From"] = os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER") or "automatizacion@localhost"
    msg["To"] = tarea["email"]
    msg.set_content(
        "Resultados de la ejecución automatizada.\n"
        f"Suite: {tarea['suite']} · Tipo: {tarea['tipo']} · Casos: {len(tarea['casos'])}\n"
        f"Fecha de finalización: {tarea['fecha_fin']}"
    )
    adjuntos = (("reporte_html", "text", "html"), ("informe_detallado", "application", "docx"), ("reporte_pdf", "application", "pdf"))
    for campo, maintype, subtype in adjuntos:
        ruta = tarea.get(campo)
        if ruta:
            archivo = Path(ruta)
            msg.add_attachment(
                archivo.read_bytes(),
                maintype=maintype,
                subtype=subtype,
                filename=archivo.name,
            )
    try:
        with smtplib.SMTP(
            os.environ.get("SMTP_HOST"), int(os.environ.get("SMTP_PORT", "25")), timeout=30
        ) as servidor:
            usuario = os.environ.get("SMTP_USER")
            if usuario:
                servidor.login(usuario, os.environ.get("SMTP_PASS", ""))
            servidor.send_message(msg)
        return "enviado"
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"


def _registrar_historial(tarea):
    """Registra los casos ejecutados en el historial del sistema (public/historial.json)."""
    try:
        ruta = report_builder.PUBLIC_HISTORIAL
        entradas = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else []
        for caso in tarea.get("casos", []):
            entradas.append(
                {
                    "scenario": f"{caso['id']} — {caso['nombre']}",
                    "status": caso["estado"],
                    "screenshot": caso["capturas"][0] if caso["capturas"] else None,
                    "bug": None,
                }
            )
        report_builder.escribir_reporte(entradas)
        return True
    except Exception as exc:  # noqa: BLE001
        tarea["historial_error"] = str(exc)
        return False


def _ejecutar_en_segundo_plano(execution_id, tipo, suite, modo_visual, timeout_seg):
    tarea = TAREAS[execution_id]
    tarea["estado"] = "EN_CURSO"
    tarea["fecha_inicio"] = datetime.now().isoformat(timespec="seconds")
    tarea["modo_visual"] = modo_visual
    tarea["timeout_seg"] = timeout_seg
    tarea["casos"] = [
        {
            "id": eid,
            "nombre": next(
                (e["nombre"] for e in automatizacion.EJERCICIOS if e["id"] == eid), eid
            ),
            "estado": "PENDIENTE",
            "capturas": [],
        }
        for eid in automatizacion.SUITE_CASOS.get(suite, [])
    ]

    def marcar_progreso(ejercicio):
        """Marca el caso que se está ejecutando como EN_CURSO (visible en la UI)."""
        for caso in tarea["casos"]:
            if caso["id"] == ejercicio["id"]:
                caso["estado"] = "EN_CURSO"

    casos = automatizacion.ejecutar_suite(
        suite, tipo, progreso=marcar_progreso, modo_visual=modo_visual,
        timeout_seg=timeout_seg,
    )
    for resultado in casos:
        for caso in tarea["casos"]:
            if caso["id"] == resultado["id"]:
                caso.update(resultado)
                break
    fin = datetime.now()
    tarea["fecha_fin"] = fin.isoformat(timespec="seconds")
    try:
        inicio = datetime.fromisoformat(tarea["fecha_inicio"])
        tarea["duracion_seg"] = round((fin - inicio).total_seconds(), 2)
    except ValueError:
        tarea["duracion_seg"] = 0
    tarea["estado"] = "FALLIDA" if any(c["estado"] == "FAIL" for c in casos) else "FINALIZADA"

    try:
        tarea["reporte_html"] = str(reportes.generar_reporte_html(tarea))
        tarea["informe_detallado"] = str(reportes.generar_informe_detallado(tarea))
        tarea["reporte_pdf"] = str(reportes.generar_reporte_pdf(tarea))
    except Exception as exc:  # noqa: BLE001
        tarea["reporte_html"] = None
        tarea["informe_detallado"] = None
        tarea["reporte_pdf"] = None

    _registrar_historial(tarea)
    tarea["envio"] = _enviar_reportes(tarea)


@app.post("/ejecutar", status_code=202)
def iniciar_ejecucion(peticion: PeticionEjecucion):
    if peticion.suite not in automatizacion.SUITES:
        raise HTTPException(422, f"Suite no válida. Opciones: {automatizacion.SUITES}")
    _validar_tipo(peticion.tipo)
    _validar_email(peticion.email)
    if not (1 <= peticion.timeout_seg <= 10):
        raise HTTPException(422, "El tiempo de espera debe estar entre 1 y 10 segundos.")
    execution_id = f"EXE-{uuid.uuid4().hex[:8].upper()}"
    TAREAS[execution_id] = {
        "id": execution_id,
        "estado": "PENDIENTE",
        "tipo": peticion.tipo,
        "suite": peticion.suite,
        "email": peticion.email or os.environ.get("SMTP_TO", ""),
        "modo_visual": peticion.modo_visual,
        "timeout_seg": peticion.timeout_seg,
        "reporte_html": None,
        "informe_detallado": None,
        "reporte_pdf": None,
        "casos": [],
        "duracion_seg": 0,
    }
    _executor.submit(_ejecutar_en_segundo_plano, execution_id, peticion.tipo, peticion.suite, peticion.modo_visual, peticion.timeout_seg)
    return {"execution_id": execution_id, "estado": "PENDIENTE"}


@app.get("/estado/{execution_id}")
def obtener_estado(execution_id: str):
    tarea = TAREAS.get(execution_id)
    if tarea is None:
        raise HTTPException(404, "Ejecución no encontrada")
    return tarea


@app.get("/ejecuciones")
def listar_ejecuciones():
    """Lista las ejecuciones registradas (para mostrar en la interfaz web)."""
    return list(TAREAS.values())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
