"""Generadores de reportes: informe detallado (Word) y reporte HTML resumen."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
DETALLADOS_DIR = REPORTS_DIR / "informes"
RESUMENES_DIR = REPORTS_DIR / "execuciones"


def _fecha_fin(ejecucion):
    return ejecucion.get("fecha_fin") or datetime.now().isoformat(timespec="seconds")


def _resumen(ejecucion):
    casos = ejecucion.get("casos", [])
    return {
        "total": len(casos),
        "pass": sum(1 for c in casos if c.get("estado") == "PASS"),
        "fail": sum(1 for c in casos if c.get("estado") == "FAIL"),
        "skipped": sum(1 for c in casos if c.get("estado") in ("SKIPPED", "NOT RUN")),
    }


def generar_reporte_html(ejecucion):
    """Genera un reporte HTML con la tabla de estados de los casos."""
    RESUMENES_DIR.mkdir(parents=True, exist_ok=True)
    casos = ejecucion.get("casos", [])
    resumen = _resumen(ejecucion)

    def fila_caso(c):
        estado = c.get("estado", "")
        clase = "estado"
        if estado in ("PASS", "FAIL"):
            clase += f" estado-{estado}"
        return (
            f"<tr><td>{c.get('id', '')}</td><td>{c.get('nombre', '')}</td>"
            f"<td>{c.get('tipo', ejecucion.get('tipo', ''))}</td>"
            f"<td class=\"{clase}\">{estado}</td>"
            f"<td>{c.get('mensaje', '')}</td></tr>"
        )

    filas = "".join(fila_caso(c) for c in casos)
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Reporte de automatización — {ejecucion.get('suite', '')}</title>
<style>
  :root {{
    --bg: #f6f8fa;
    --card: #ffffff;
    --line: #dfe3e8;
    --text: #24292f;
    --muted: #57606a;
    --pass: #1f7a3a;
    --fail: #c9382b;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 3rem auto;
    padding: 0 1.5rem;
    max-width: 980px;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    color: var(--text);
    background: var(--bg);
    line-height: 1.5;
  }}
  h1 {{
    font-size: 1.5rem;
    margin: 0 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--line);
  }}
  .bloque {{
    margin: 0 0 1.75rem;
  }}
  .bloque h2 {{
    font-size: 1.15rem;
    margin: 0 0 0.6rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--line);
  }}
  .meta {{
    color: var(--muted);
    font-size: 0.95rem;
  }}
  .tabla-wrap {{
    margin-top: 1.5rem;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 6px;
    box-shadow: 0 1px 2px rgba(24, 35, 49, 0.05);
    overflow-x: auto;
  }}
  table {{
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    font-size: 0.95rem;
  }}
  th {{
    background: #eef2f4;
    color: var(--text);
    text-align: left;
    font-weight: 500;
    padding: 0.7rem 0.85rem;
    border-bottom: 1px solid var(--line);
    white-space: nowrap;
  }}
  td {{
    padding: 0.7rem 0.85rem;
    border-bottom: 1px solid var(--line);
  }}
  tbody tr:last-child td {{
    border-bottom: none;
  }}
  tbody tr:nth-child(even) td {{
    background: #fafbfc;
  }}
  .estado {{
    font-weight: 600;
  }}
  .estado-PASS {{
    color: var(--pass);
  }}
  .estado-FAIL {{
    color: var(--fail);
  }}
  footer {{
    margin-top: 2rem;
    color: var(--muted);
    font-size: 0.85rem;
  }}
</style>
</head>
<body>
<h1>Reporte de automatización — {ejecucion.get('suite', '')}</h1>
<section class="bloque">
<h2>Resumen</h2>
<p class="meta">Tipo: {ejecucion.get('tipo', '')} &middot; Correo: {ejecucion.get('email', '') or '(sin correo ingresado)'} &middot; Fecha de inicio: {ejecucion.get('fecha_inicio', '')} &middot; Fecha de finalización: {_fecha_fin(ejecucion)} &middot; Duración: {ejecucion.get('duracion_seg', '')} s</p>
<p class="meta">Total: {resumen['total']} &middot; PASS: {resumen['pass']} &middot; FAIL: {resumen['fail']}
&middot; SKIPPED/NOT RUN: {resumen['skipped']} &middot; Estado global: {ejecucion.get('estado', '')}</p>
</section>
<section class="bloque">
<h2>Detalle de casos</h2>
<div class="tabla-wrap">
<table>
<thead><tr><th>ID</th><th>Nombre</th><th>Tipo/Suite</th><th>Estado</th><th>Observación</th></tr></thead>
<tbody>
{filas}
</tbody>
</table>
</div>
</section>
<footer>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} — Orquestador de Pruebas QA.</footer>
</body>
</html>"""
    path = RESUMENES_DIR / f"{ejecucion['id']}.html"
    path.write_text(html, encoding="utf-8")
    return path


def _estilo(doc, nombre):
    try:
        return doc.styles[nombre]
    except KeyError:
        return None


def _llenar_encabezado_tabla(celda, rgb):
    """Pinta el llenado de una celda de encabezado de tabla."""
    try:
        celda.shading.fill = rgb
    except AttributeError:
        from docx.oxml import ns

        tcPr = celda._tc.get_or_add_tcPr()
        shd = tcPr.find(ns.qn("w:shd"))
        if shd is None:
            shd = tcPr.makeelement(ns.qn("w:shd"), {})
            tcPr.append(shd)
        shd.set(ns.qn("w:val"), "clear")
        shd.set(ns.qn("w:fill"), "%02X%02X%02X" % tuple(rgb))


def _configurar_estilos(doc):
    """Ajusta los estilos de la plantilla para un diseño más prolijo y legible."""
    color_verde = RGBColor(0x1D, 0x7A, 0x3E)
    color_rojo = RGBColor(0xC9, 0x38, 0x2B)
    color_oscuro = RGBColor(0x24, 0x29, 0x2F)
    color_claro = RGBColor(0xE6, 0xF1, 0xED)

    normal = _estilo(doc, "Normal")
    if normal is not None:
        normal.font.name = "Calibri"
        normal.font.size = Pt(11)
        normal.paragraph_format.space_after = Pt(6)
        normal.paragraph_format.line_spacing = 1.15

    titulo = _estilo(doc, "Title") or _estilo(doc, "Heading 1")
    if titulo is not None:
        titulo.font.bold = True
        titulo.font.size = Pt(20)
        titulo.font.color.rgb = color_oscuro
        titulo.paragraph_format.space_after = Pt(12)

    for nombre, color in (("Heading 1", color_verde), ("Heading 2", color_rojo)):
        est = _estilo(doc, nombre)
        if est is None:
            continue
        est.font.bold = True
        est.font.size = Pt(14)
        est.font.color.rgb = color
        est.paragraph_format.space_before = Pt(18)
        est.paragraph_format.space_after = Pt(8)


def generar_informe_detallado(ejecucion):
    """Genera el informe detallado en Word (.docx) con los datos de la ejecución."""
    DETALLADOS_DIR.mkdir(parents=True, exist_ok=True)
    casos = ejecucion.get("casos", [])
    resumen = _resumen(ejecucion)
    doc = Document()
    _configurar_estilos(doc)
    doc.add_heading("Informe detallado — Automatización de Pruebas QA", 0)

    p = doc.add_paragraph()
    p.add_run(f"ID de ejecución: {ejecucion.get('id', '')}").bold = True
    doc.add_paragraph(f"Suite/categoría: {ejecucion.get('suite', '')}")
    doc.add_paragraph(f"Tipo de pruebas: {ejecucion.get('tipo', '')}")
    doc.add_paragraph(f"Correo destinatario: {ejecucion.get('email', '') or '(sin correo ingresado)'}")
    doc.add_paragraph(f"Fecha de inicio: {ejecucion.get('fecha_inicio', '')}")
    doc.add_paragraph(f"Fecha de finalización: {_fecha_fin(ejecucion)}")
    doc.add_paragraph(f"Duración: {ejecucion.get('duracion_seg', '')} s")
    doc.add_paragraph()

    doc.add_heading("Resumen", 1)
    doc.add_paragraph(
        f"Total de casos: {resumen['total']} · PASS: {resumen['pass']} · FAIL: {resumen['fail']}"
        f" · SKIPPED/NOT RUN: {resumen['skipped']} · Estado global: {ejecucion.get('estado', '')}"
    )
    doc.add_paragraph()

    doc.add_heading("Detalle por caso", 1)
    table = doc.add_table(rows=len(casos) + 1, cols=5)
    table.style = "Table Grid"
    try:
        table.autofit = True
    except Exception:
        pass

    header = table.rows[0].cells
    for i, texto in enumerate(("ID", "Nombre", "Estado", "Mensaje", "Duración (s)")):
        celda = header[i]
        celda.text = texto
        for run in celda.paragraphs[0].runs:
            run.bold = True
        _llenar_encabezado_tabla(celda, RGBColor(0xEA, 0xF3, 0xEC))

    for fila, caso in enumerate(casos, start=1):
        celdas = table.rows[fila].cells
        celdas[0].text = caso.get("id", "")
        celdas[1].text = caso.get("nombre", "")
        celdas[2].text = caso.get("estado", "")
        celdas[3].text = caso.get("mensaje", "")
        if caso.get("capturas"):
            celdas[3].text += "\nEvidencias: " + ", ".join(caso["capturas"])
        celdas[4].text = str(caso.get("duracion_seg", ""))
    doc.add_paragraph()

    path = DETALLADOS_DIR / f"{ejecucion['id']}.docx"
    doc.save(str(path))
    return path


def generar_reporte_pdf(ejecucion):
    """Genera el informe detallado en PDF."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas

    DETALLADOS_DIR.mkdir(parents=True, exist_ok=True)
    path = DETALLADOS_DIR / f"{ejecucion['id']}.pdf"

    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle(f"Informe — Automatización — {ejecucion.get('suite', '')}")
    y = A4[1] - 25 * mm
    c.setFont("Helvetica-Bold", 20)
    c.drawString(20 * mm, y, f"Informe de Automatización — {ejecucion.get('suite', '')}")

    def linea(texto, fuente="Helvetica", tamaño=11, negrita=False):
        nonlocal y
        if y < 45 * mm:
            c.showPage()
            y = A4[1] - 25 * mm
        c.setFont(f"{fuente}-Bold" if negrita else fuente, tamaño)
        c.drawString(20 * mm, y, texto)

    def salto(puntos):
        nonlocal y
        y -= puntos

    salto(12)
    linea(f"ID de ejecución: {ejecucion.get('id', '')}")
    salto(9)
    linea(f"Tipo de pruebas: {ejecucion.get('tipo', '')}")
    salto(9)
    linea(f"Suite/categoría: {ejecucion.get('suite', '')}")
    salto(9)
    linea(f"Correo destinatario: {ejecucion.get('email', '') or '(sin correo ingresado)'}")
    salto(9)
    linea(f"Fecha de inicio: {ejecucion.get('fecha_inicio', '')}")
    salto(9)
    linea(f"Fecha de finalización: {_fecha_fin(ejecucion)}")
    salto(9)
    linea(f"Duración: {ejecucion.get('duracion_seg', '')} s")
    salto(18)

    resumen = _resumen(ejecucion)
    linea("Resumen", negrita=True, tamaño=13)
    salto(9)
    linea(
        f"Total: {resumen['total']} · PASS: {resumen['pass']} · FAIL: {resumen['fail']}"
        f" · SKIPPED/NOT RUN: {resumen['skipped']} · Estado global: {ejecucion.get('estado', '')}"
    )
    salto(18)

    linea("Detalle por caso", negrita=True, tamaño=13)
    salto(9)
    for caso in ejecucion.get("casos", []):
        linea(
            f"• {caso.get('id', '')}: {caso.get('nombre', '')}"
            f" — Estado: {caso.get('estado', '')}"
            f" — {caso.get('mensaje', '')[:90]}",
            tamaño=10,
        )
        salto(7)

    salto(10)
    linea(f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} — Orquestador de Pruebas QA.", tamaño=10)
    c.save()
    return path
