import { useEffect, useState } from 'react'

const modules = [
  { id: 'pruebas', label: 'Pruebas' },
  { id: 'historial', label: 'Historial' },
  { id: 'reportes', label: 'Reportes' },
]

const ORQUESTADOR_URL =
  import.meta.env.VITE_ORQUESTADOR_URL || 'http://localhost:8000'

const SUITES_PRUEBAS = [
  'Smoke',
  'Sanity',
  'Regression',
  'Integración',
  'End-to-End',
  'Performance',
  'Carga',
  'Rendimiento',
  'Carga de estrés',
]

const ETIQUETAS_ESTADO_EJECUCION = {
  PENDIENTE: 'Pendiente',
  EN_CURSO: 'En curso',
  FINALIZADA: 'Finalizada',
  FALLIDA: 'Fallida',
}

const COLORES_ESTADO_EJECUCION = {
  PENDIENTE: 'border-[var(--border)] bg-[var(--social-bg)] text-[var(--text)]',
  EN_CURSO: 'border-[var(--accent-border)] bg-[var(--accent-bg)] text-[var(--accent)]',
  FINALIZADA: 'border-[var(--accent-border)] bg-[var(--accent-bg)] text-[var(--accent)]',
  FALLIDA: 'border-[var(--border)] bg-[var(--code-bg)] text-[var(--text-h)]',
}

const PUNTOS_ESTADO_EJECUCION = {
  PENDIENTE: 'bg-[var(--border)]',
  EN_CURSO: 'bg-[var(--accent)] animate-pulse',
  FINALIZADA: 'bg-[var(--accent)]',
  FALLIDA: 'bg-[var(--text-h)]',
}

const PUNTOS_ESTADO_CASO = {
  PENDIENTE: 'bg-[var(--border)]',
  EN_CURSO: 'bg-[var(--accent)] animate-pulse',
  PASS: 'bg-[var(--accent)]',
  FAIL: 'bg-[var(--text-h)]',
  SKIPPED: 'bg-[var(--social-bg)]',
  NOT_RUN: 'bg-[var(--text)]',
}

const ETIQUETAS_ESTADO_CASO = {
  PENDIENTE: 'Pendiente',
  EN_CURSO: 'En curso',
  PASS: 'PASS',
  FAIL: 'FAIL',
  SKIPPED: 'SKIPPED',
  NOT_RUN: 'NOT RUN',
}

function progresoEjecucion(tarea) {
  const casos = tarea.casos || []
  if (casos.length === 0) return 0
  const terminados = casos.filter((c) =>
    ['PASS', 'FAIL', 'SKIPPED', 'NOT RUN'].includes(c.estado)
  ).length
  const enCurso = casos.some((c) => c.estado === 'EN_CURSO') ? 0.5 : 0
  return Math.min(1, (terminados + enCurso) / casos.length)
}

function Sidebar({ activeModule, setActiveModule }) {
  return (
    <aside className="flex w-[276px] shrink-0 flex-col border-r border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-[#141620]">
      <div className="border-b border-gray-200 px-4 pb-4 pt-4 dark:border-gray-800">
        <p id="titulo-app" className="truncate text-sm font-semibold text-[var(--text-h)]">
          Pruebas QA
        </p>
        <p id="subtitulo-app" className="mt-1 truncate text-xs font-medium text-[var(--text)] opacity-70">
          Fábrica de Fideos &quot;EL PRINCIPE&quot;
        </p>
      </div>
      <nav className="flex-1 overflow-y-auto px-3 py-3">
        <p className="mb-2 px-3 text-[11px] font-medium uppercase tracking-wide text-[var(--text)] opacity-60">
          Módulos
        </p>
        <ul className="flex flex-col gap-0.5">
          {modules.map((m) => {
            const active = m.id === activeModule
            return (
              <li key={m.id}>
                <button
                  type="button"
                  id={`btn-modulo-${m.id}`}
                  name={`btn_modulo_${m.id}`}
                  onClick={() => setActiveModule(m.id)}
                  aria-current={active ? 'page' : undefined}
                  className={`flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
                    active
                      ? 'bg-[#e9e9ec] font-medium text-[var(--text-h)] dark:bg-[#2c3142]'
                      : 'text-[var(--text)] hover:bg-gray-100 dark:hover:bg-[#1e2130]'
                  }`}
                >
                  {m.label}
                </button>
              </li>
            )
          })}
        </ul>
      </nav>
    </aside>
  )
}

function PruebasView() {
  const [seccion, setSeccion] = useState(null)
  const [tipoNofuncional, setTipoNofuncional] = useState(null)

  const tiposNoFuncionales = [
    { id: 'recuperacion', label: 'Recuperación', desc: 'Validación de la recuperación de disponibilidad tras fallos' },
    { id: 'rendimiento', label: 'Rendimiento', desc: 'Validación del tiempo de carga y respuesta del sistema' },
    { id: 'carga_estres', label: 'Carga de estrés', desc: 'Validación del sistema bajo carga de estrés (cargas repetidas)' },
  ]

  const seleccionarNofuncional = (id) =>
    setTipoNofuncional((actual) => (actual === id ? null : id))

  // --- Ejecución de pruebas desde la interfaz (frontend) --------------------
  const [tipoPruebas, setTipoPruebas] = useState('funcional')
  const [email, setEmail] = useState('')
  const [suite, setSuite] = useState('Smoke')
  const [executionId, setExecutionId] = useState(null)
  const [estadoEjecucion, setEstadoEjecucion] = useState(null)
  const [resumenEjecucion, setResumenEjecucion] = useState(null)
  const [ejecuciones, setEjecuciones] = useState([])
  const [detalleEjecucion, setDetalleEjecucion] = useState(null)
  const [modoVisual, setModoVisual] = useState(false)
  const [timeoutEjec, setTimeoutEjec] = useState('10')

  const ejecutarPruebas = async () => {
    try {
      const resp = await fetch(`${ORQUESTADOR_URL}/ejecutar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo: tipoPruebas, suite, email, modo_visual: modoVisual, timeout_seg: Number(timeoutEjec) }),
      })
      const data = await resp.json()
      if (!resp.ok) {
        throw new Error(data.detail || 'Error al iniciar la ejecución')
      }
      setExecutionId(data.execution_id)
      setEstadoEjecucion('EN_CURSO')
    } catch (error) {
      setEstadoEjecucion('FALLIDA')
      setResumenEjecucion({ error: String(error) })
    }
  }

  useEffect(() => {
    if (estadoEjecucion !== 'EN_CURSO' || !executionId) return undefined
    const timer = setInterval(async () => {
      try {
        const resp = await fetch(`${ORQUESTADOR_URL}/estado/${executionId}`)
        const data = await resp.json()
        setEstadoEjecucion(data.estado)
        setDetalleEjecucion(data)
      } catch {
        // El orquestador aún no responde; se reintenta en el siguiente tick.
      }
    }, 3000)
    return () => clearInterval(timer)
  }, [estadoEjecucion, executionId])

  useEffect(() => {
    const cargarEjecuciones = async () => {
      try {
        const resp = await fetch(`${ORQUESTADOR_URL}/ejecuciones`)
        const data = await resp.json()
        setEjecuciones(Array.isArray(data) ? data : [])
      } catch {
        // El orquestador aún no responde.
      }
    }
    cargarEjecuciones()
    const timer = setInterval(cargarEjecuciones, 5000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    if (
      (estadoEjecucion === 'FINALIZADA' || estadoEjecucion === 'FALLIDA') &&
      executionId
    ) {
      fetch(`${ORQUESTADOR_URL}/estado/${executionId}`)
        .then((resp) => resp.json())
        .then((data) => {
          const casos = data.casos || []
          setResumenEjecucion({
            total: casos.length,
            pass: casos.filter((c) => c.estado === 'PASS').length,
            fail: casos.filter((c) => c.estado === 'FAIL').length,
            duracion: data.duracion_seg,
          })
        })
        .catch(() => {})
    }
  }, [estadoEjecucion, executionId])

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <h1 id="titulo-pruebas" name="titulo_pruebas" className="text-3xl font-semibold tracking-tight text-[var(--text-h)]">
        Pruebas
      </h1>
      <p id="descripcion-pruebas" className="mt-2 max-w-xl text-[var(--text)]">
        Automatización del sistema con pruebas funcionales y no funcionales.
      </p>
      <div className="mt-6 flex flex-wrap gap-3">
        <button
          type="button"
          id="btn-pruebas-funcionales"
          name="btn_pruebas_funcionales"
          onClick={() => {
            setTipoPruebas('funcional')
            setSeccion((s) => (s === 'funcionales' ? null : 'funcionales'))
          }}
          className={`rounded-lg border px-4 py-2 text-sm font-medium transition ${
            seccion === 'funcionales'
              ? 'border-[var(--accent)] bg-[var(--accent-bg)] text-[var(--text-h)]'
              : 'border-[var(--border)] bg-white text-[var(--text)] dark:bg-[#1d212b]'
          }`}
        >
          Pruebas funcionales
        </button>
        <button
          type="button"
          id="btn-pruebas-no-funcionales"
          name="btn_pruebas_no_funcionales"
          onClick={() => {
            setTipoPruebas('no funcional')
            setSeccion(
              (s) => (s === 'no-funcionales' ? null : 'no-funcionales'),
            )
          }}
          className={`rounded-lg border px-4 py-2 text-sm font-medium transition ${
            seccion === 'no-funcionales'
              ? 'border-[var(--accent)] bg-[var(--accent-bg)] text-[var(--text-h)]'
              : 'border-[var(--border)] bg-white text-[var(--text)] dark:bg-[#1d212b]'
          }`}
        >
          Pruebas no funcionales
        </button>
      </div>
      <div className="mt-6 rounded-xl border border-[var(--border)] p-4">
        <h2 className="text-sm font-semibold text-[var(--text-h)]">
          Ejecutar pruebas
        </h2>
        <p className="mt-1 text-xs text-[var(--text)] opacity-70">
          Enlace del sistema:{' '}
          <a id="enlace-sistema" name="enlace_sistema" href="http://localhost:5173" target="_blank" rel="noreferrer">
            http://localhost:5173
          </a>
        </p>
        <div className="mt-3 flex flex-wrap gap-3">
          <label htmlFor="email-pruebas" className="sr-only">
            Correo destinatario
          </label>
          <input
            id="email-pruebas"
            name="email_pruebas"
            type="email"
            placeholder="correo destinatario (opcional)"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full max-w-md rounded-lg border border-[var(--border)] bg-white px-3 py-2 text-sm text-[var(--text)] dark:bg-[#1d212b] dark:text-white"
          />
          <label htmlFor="suite-pruebas" className="sr-only">
            Suite de pruebas
          </label>
          <select
            id="suite-pruebas"
            name="suite_pruebas"
            value={suite}
            onChange={(e) => setSuite(e.target.value)}
            className="rounded-lg border border-[var(--border)] bg-white px-3 py-2 text-sm text-[var(--text)] dark:bg-[#1d212b] dark:text-white"
          >
            {SUITES_PRUEBAS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <label htmlFor="modo-ejecucion" className="sr-only">
          Modo de ejecución
        </label>
        <select
          id="modo-ejecucion"
          name="modo_ejecucion"
          value={modoVisual ? 'visual' : 'fondo'}
          onChange={(e) => setModoVisual(e.target.value === 'visual')}
          className="rounded-lg border border-[var(--border)] bg-white px-3 py-2 text-sm text-[var(--text)] dark:bg-[#1d212b] dark:text-white"
        >
          <option value="fondo">Ejecutar en segundo plano (oculto)</option>
          <option value="visual">Ver lo que está haciendo (navegador visible)</option>
        </select>
        <label htmlFor="timeout-ejecucion" className="sr-only">
          Tiempo de espera
        </label>
        <select
          id="timeout-ejecucion"
          name="timeout_ejecucion"
          value={timeoutEjec}
          onChange={(e) => setTimeoutEjec(e.target.value)}
          className="rounded-lg border border-[var(--border)] bg-white px-3 py-2 text-sm text-[var(--text)] dark:bg-[#1d212b] dark:text-white"
        >
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((t) => (
            <option key={t} value={t}>
              {t} s
            </option>
          ))}
        </select>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <button
            type="button"
            id="btn-ejecutar"
            name="btn_ejecutar"
            onClick={ejecutarPruebas}
            disabled={estadoEjecucion === 'EN_CURSO'}
            className="rounded-lg border border-[var(--accent)] bg-[var(--accent-bg)] px-4 py-2 text-sm font-medium text-[var(--text-h)] transition hover:opacity-90 disabled:opacity-60"
          >
            {estadoEjecucion === 'EN_CURSO' ? 'Ejecutando...' : 'Ejecutar prueba'}
          </button>
          {estadoEjecucion && (
            <span
              id="estado-ejecucion"
              name="estado_ejecucion"
              className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold ${
                COLORES_ESTADO_EJECUCION[estadoEjecucion] || ''
              }`}
            >
              <span
                className={`h-2 w-2 shrink-0 rounded-full ${
                  PUNTOS_ESTADO_EJECUCION[estadoEjecucion] || ''
                }`}
              />
              {ETIQUETAS_ESTADO_EJECUCION[estadoEjecucion] || estadoEjecucion}
            </span>
          )}
          {resumenEjecucion && (
            <span
              id="resumen-ejecucion"
              name="resumen_ejecucion"
              className="text-xs text-[var(--text)]"
            >
              Total: {resumenEjecucion.total} · PASS: {resumenEjecucion.pass} ·
              FAIL: {resumenEjecucion.fail}
              {resumenEjecucion.error
                ? ` · Error: ${resumenEjecucion.error}`
                : ''}
            </span>
          )}
          {estadoEjecucion === 'EN_CURSO' && detalleEjecucion && (
            <div
              id="barra-progreso-ejecucion"
              name="barra_progreso_ejecucion"
              className="mt-3 rounded-lg border border-[var(--border)] bg-[var(--bg)] p-3 shadow-sm"
            >
              <div className="flex items-center justify-between text-xs text-[var(--text)]">
                <span id="texto-progreso-ejecucion" name="texto_progreso_ejecucion">
                  Ejecutando — {detalleEjecucion.casos.filter((c) => c.estado === 'PASS' || c.estado === 'FAIL').length}/{detalleEjecucion.casos.length} casos
                </span>
                <span className="font-semibold">{Math.round(progresoEjecucion(detalleEjecucion) * 100)}%</span>
              </div>
              <div className="mt-2 h-3 rounded-full bg-[var(--social-bg)] shadow-inner">
                <div
                  className="h-3 rounded-full bg-[var(--accent)] transition-all duration-500"
                  style={{
                    width: `${Math.round(progresoEjecucion(detalleEjecucion) * 100)}%`,
                  }}
                />
              </div>
              <ul className="mt-2 space-y-2">
                {detalleEjecucion.casos.map((c) => (
                  <li
                    key={c.id}
                    id={`caso-${c.id}`}
                    name={`caso_${c.id}`}
                    className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-xs text-[var(--text)] shadow-sm transition hover:shadow-md"
                  >
                    <span
                      className={`h-2.5 w-2.5 shrink-0 rounded-full ${
                        PUNTOS_ESTADO_CASO[c.estado] || 'bg-[var(--border)]'
                      }`}
                    />
                    <span className="font-medium">{c.id}</span>
                    <span className="opacity-70">
                      {ETIQUETAS_ESTADO_CASO[c.estado] || c.estado}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <div className="mt-3 rounded-xl border border-[var(--border)] bg-[var(--bg)] p-4">
          <div className="flex items-center justify-between gap-2">
            <h3 className="text-sm font-semibold tracking-wide text-[var(--text-h)]">
              Ejecuciones
            </h3>
            <span className="text-[11px] text-[var(--text)]">
              {ejecuciones.length} últimas ejecuciones
            </span>
          </div>
          {ejecuciones.length === 0 ? (
            <p className="mt-3 rounded-lg border border-dashed border-[var(--border)] bg-[var(--bg)] px-3 py-4 text-center text-xs text-[var(--text)]">
              Sin ejecuciones recientes
            </p>
          ) : (
            <ul className="mt-3 space-y-2">
              {ejecuciones.slice(-5).map((e) => {
                const casos = e.casos || []
                const total = casos.length
                const pass = casos.filter((c) => c.estado === 'PASS').length
                const fail = casos.filter((c) => c.estado === 'FAIL').length
                const estadoEtiqueta = {
                  PENDIENTE: 'Pendiente',
                  EN_CURSO: 'En curso',
                  FINALIZADA: 'Finalizada',
                  FALLIDA: 'Fallida',
                }[e.estado] || e.estado
                const estadoClase =
                  e.estado === 'FINALIZADA' || e.estado === 'EN_CURSO'
                    ? 'bg-[var(--accent-bg)] border-[var(--accent-border)] text-[var(--accent)]'
                    : e.estado === 'FALLIDA'
                      ? 'bg-[var(--code-bg)] border-[var(--border)] text-[var(--text-h)]'
                      : 'bg-[var(--social-bg)] border-[var(--border)] text-[var(--text)]'
                return (
                  <li
                    key={e.id}
                    id={`ejecucion-${e.id}`}
                    name={`ejecucion_${e.id}`}
                    className="rounded-xl border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-xs text-[var(--text-h)] shadow-sm transition hover:shadow-md"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <p className="font-semibold">{e.id}</p>
                        <p className="mt-0.5 text-[var(--text)]">
                          Suite: <span className="font-medium">{e.suite}</span> · Tipo:{' '}
                          <span className="font-medium">{e.tipo}</span>
                        </p>
                      </div>
                      <span
                        className={`shrink-0 rounded-full border px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${estadoClase}`}
                      >
                        {estadoEtiqueta}
                      </span>
                    </div>
                    <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-[var(--text)]">
                      {total > 0 && (
                        <span>
                          Casos:{' '}
                          <span className="font-medium">{total}</span>
                        </span>
                      )}
                      {total > 0 && (
                        <span>
                          <span className="font-medium">{pass}</span> PASS · <span className="font-medium">{fail}</span> FAIL
                        </span>
                      )}
                      {e.duracion_seg ? <span>Dura: {e.duracion_seg} s</span> : null}
                      {e.fecha_inicio ? <span>Inició: {e.fecha_inicio}</span> : null}
                    </div>
                  </li>
                )
              })}
            </ul>
          )}
        </div>
      </div>
      {seccion === 'no-funcionales' && (
        <ul id="lista-tipos-nofuncionales" className="mt-6 max-w-2xl space-y-2 pl-6 text-sm text-[var(--text)]">
          {tiposNoFuncionales.map((t) => {
            const activo = tipoNofuncional === t.id
            return (
              <li key={t.id}>
                <button
                  type="button"
                  id={`tipo-nofuncional-${t.id}`}
                  name={`tipo_nofuncional_${t.id}`}
                  onClick={() => seleccionarNofuncional(t.id)}
                  aria-pressed={activo}
                  className={`text-left ${activo ? 'font-medium underline' : ''}`}
                >
                  {t.label}
                </button>
                {activo && (
                  <span id={`detalle-tipo-nofuncional-${t.id}`} name={`detalle_tipo_nofuncional_${t.id}`} className="ml-2 text-[var(--text)] opacity-80">
                    — {t.desc}
                  </span>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}

function HistorialView() {
  const [entradas, setEntradas] = useState([])

  useEffect(() => {
    fetch('/historial.json')
      .then((resp) => resp.json())
      .then((data) => setEntradas(data))
      .catch(() => setEntradas([]))
  }, [])

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-3xl font-semibold tracking-tight text-[var(--text-h)]">
        Historial
      </h1>
      <p className="mt-2 text-[var(--text)]">
        Registro de las pruebas ejecutadas en el sistema.
      </p>
      <div className="mt-8 rounded-xl border border-[var(--border)] p-5">
        <h2 className="text-sm font-semibold text-[var(--text-h)]">
          Entradas registradas
        </h2>
        {entradas.length === 0 ? (
          <ul className="mt-2 space-y-1 text-sm text-[var(--text)]">
            <li>Sin entradas registradas aún.</li>
          </ul>
        ) : (
          <ul className="mt-2 space-y-1 text-sm text-[var(--text)]">
            {entradas.map((e, i) => (
              <li key={i}>
                {e.status} — {e.scenario}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

function ReportesView() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-3xl font-semibold tracking-tight text-[var(--text-h)]">
        Reportes
      </h1>
      <p className="mt-2 text-[var(--text)]">
        Reportes generados por el módulo de pruebas.
      </p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-[var(--border)] p-5">
          <h2 className="text-sm font-semibold text-[var(--text-h)]">
            Reportes generados
          </h2>
          <p className="mt-1 text-sm text-[var(--text)]">
            Sin reportes generados aún.
          </p>
        </div>
        <div className="rounded-xl border border-[var(--border)] p-5">
          <h2 className="text-sm font-semibold text-[var(--text-h)]">
            Estado del módulo
          </h2>
          <p className="mt-1 text-sm text-[var(--text)]">
            Abierto para generar reportes.
          </p>
        </div>
      </div>
      <div className="mt-8 flex flex-wrap gap-3">
        <a
          href="/Bug_report_template_ejemplo.md"
          download
          className="rounded-lg border border-[var(--border)] bg-white px-4 py-2 text-sm font-medium text-[var(--text)] transition hover:bg-gray-100 dark:bg-[#1d212b] dark:text-white dark:hover:bg-[#232731]"
        >
          Descargar plantilla de Bug Report
        </a>
        <a
          href="/Plantilla_TC_y_Ejecucion_TQA.md"
          download
          className="rounded-lg border border-[var(--border)] bg-white px-4 py-2 text-sm font-medium text-[var(--text)] transition hover:bg-gray-100 dark:bg-[#1d212b] dark:text-white dark:hover:bg-[#232731]"
        >
          Descargar plantilla de Caso de Prueba (TC)
        </a>
      </div>
    </div>
  )
}

function App() {
  const [activeModule, setActiveModule] = useState('pruebas')

  return (
    <div className="flex h-screen bg-[var(--bg)]">
      <Sidebar
        activeModule={activeModule}
        setActiveModule={setActiveModule}
      />
      <main className="flex-1 min-w-0 overflow-y-auto bg-[var(--bg)] text-[var(--text)]">
        {activeModule === 'pruebas' && <PruebasView />}
        {activeModule === 'historial' && <HistorialView />}
        {activeModule === 'reportes' && <ReportesView />}
      </main>
    </div>
  )
}

export default App
