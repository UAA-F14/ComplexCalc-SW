# AGENTS.md — ComplexCalc (guía para agentes)

Calculadora GUI (CustomTkinter) que resuelve sistemas complejos **Ax = b** con entrada rectangular
(`3+4j`, `2+1i`) o fasorial (`10L30`, `10∠30°`), salida polar + rectangular y calculadora auxiliar.

**Regla de oro:** lee solo el módulo que vas a cambiar (tabla de abajo). Ningún archivo pasa de ~140 líneas.

## Comandos (desde `code/`)
| Qué | Comando |
|---|---|
| Ejecutar | `python main.py` |
| Tests | `python -m unittest discover -s ../tests` |
| Compilar exe | `python packaging/build.py` (tests + PyInstaller → `code/dist/`) |
| Deps | `pip install -r requirements.txt` (dev: `requirements-dev.txt`) |

## Mapa de módulos
Dependencias: `ui/*` → `core/*` y `paths.py`. **`core/` nunca importa `ui/`** (ni tkinter).

### core/ — lógica pura, sin UI (cubierta por tests)
| Archivo | Qué hace | API pública |
|---|---|---|
| `core/formatting.py` | Formato de complejos | `complejo_a_fasor(z)` → `"r L ang°"`; `complejo_rect(z)` → `"a + bj"`; `format_rect_result(z)` (calculadora) |
| `core/parsing.py` | Texto → complejo | `parse_value(text)` (una celda); `evaluate_expression(text)` (expresión con `+ - * / ^` y fasores) |
| `core/solver.py` | Resuelve Ax=b | `solve_from_strings(A_strs, b_strs, max_size=10)` → dict (`A,b,x` numpy; `*_polar`, `*_rect` str; `timestamp`, `size`) |
| `core/storage.py` | Persistencia | `save_system(result, saved_file, exported_py)`; `load_saved_items(path)`; `rect_to_complex(s)` |
| `core/calculator.py` | Fachada `FasorCalculatorCore` | mismos métodos que arriba, con rutas/`max_size` guardados en la instancia (lo usa la UI) |
| `core/__init__.py` | Re-exporta la API | `from core import FasorCalculatorCore, parse_value, ...` |

### ui/ — mixins que `ui/app.py` ensambla en una sola clase `FasorCalculator`
Todos los mixins comparten `self` (estado en la tabla "Estado compartido").
| Archivo | Qué hace | Métodos principales |
|---|---|---|
| `ui/app.py` | Ventana principal; solo orden de construcción | `__init__` |
| `ui/header.py` | Barra de tema/idioma + título y logo | `build_topbar`, `build_header` |
| `ui/matrix_panel.py` | Matriz A / vector b, tamaño, ejemplo, **Solve** | `build_matrix_panel`, `build_matrix`, `fill_entries`, `load_default_example`, `solve`, `change_size`, `_themed_size_dialog` |
| `ui/history_panel.py` | Historial y sistemas guardados | `build_history_panel`, `build_saved_buttons`, `add_to_history_view`, `load_saved_systems`, `load_saved_option`, `import_from_file` |
| `ui/calc_panel.py` | Calculadora AUX (teclado, `=`, `⇄`, copiar) | `build_calc_panel`, `calc_button_click` (constantes `KEYPAD`, `OPERATORS`) |
| `ui/menu_bar.py` | Menú File/Help + diálogo About | `build_menu_bar`, `show_about_dialog` |
| `ui/theming.py` | Temas de color | `setup_colors`, `change_theme`, `apply_theme`, `THEME_NAMES` |
| `ui/i18n.py` | Idiomas EN/ES | `t(key, **kw)`, `change_language`, `_RETEXT` (widgets a re-textear) |
| `ui/widgets.py` | Helpers compartidos | `logo_image(size)`, `center_over(dlg, parent)` |
| `ui/meta.py` | Versión, fecha, repo, créditos | `APP_VERSION`, `LAST_UPDATED`, `CREATORS`, ... |

### Raíz y datos
| Ruta | Contenido |
|---|---|
| `main.py` | Punto de entrada |
| `paths.py` | `resource_path()`, `DATA_DIR`, `SAVED_FILE`, `EXPORT_FILE` (distingue dev vs ejecutable) |
| `resources/` | **Solo lectura, se empaqueta:** `themes.json`, `languages.json`, `HK.jpg` (icono), `IE.png` (logo) |
| `data/` | **Escribible, NO se empaqueta:** `saved_systems.txt` (JSON por entrada, separadas por línea en blanco), `exported_systems.py` (generado) |
| `packaging/` | `UI_ComplexCalc.spec` (PyInstaller) y `build.py` |
| `../tests/` | `test_parsing.py`, `test_solver.py`, `test_storage.py`, `test_formatting.py`, `test_resources.py` |

## Dónde tocar según la tarea
| Quiero... | Archivo(s) |
|---|---|
| Aceptar otra sintaxis de número/fasor | `core/parsing.py` (+ test en `tests/test_parsing.py`) |
| Cambiar cifras/formato de salida | `core/formatting.py` |
| Cambiar cómo se resuelve o validar tamaños | `core/solver.py` |
| Cambiar formato del archivo de guardados/export | `core/storage.py` |
| Agregar/cambiar botón de la calculadora | `ui/calc_panel.py` |
| Cambiar la matriz, el ejemplo o el botón Solve | `ui/matrix_panel.py` |
| Cambiar historial / lista de guardados / importar | `ui/history_panel.py` |
| Agregar un tema o color | `resources/themes.json` (mismas claves en todos) + `THEME_NAMES` en `ui/theming.py` |
| Agregar/editar un texto visible | `resources/languages.json` en **en y es** (+ `_RETEXT` en `ui/i18n.py` si el widget cambia al vuelo) |
| Subir versión / créditos | `ui/meta.py` |
| Agregar un panel nuevo | nuevo `ui/<panel>_panel.py` con un mixin, sumarlo a la herencia y a `__init__` en `ui/app.py` |
| Cambiar cómo se compila | `packaging/UI_ComplexCalc.spec` (y `.github/workflows/build.yml` si cambia el comando) |

## Estado compartido (atributos de `self`)
`self.core` (FasorCalculatorCore) · `self.size` (n de la matriz) · `self.entries_A` / `self.entries_b` (CTkEntry) ·
`self.saved_items` (lista de dicts cargados) · `self.saved_filename` · `self.current_colors` / `self.themes` · `self.lang` ·
widgets con referencia para re-textear: `btn_*`, `*_label`, `calc_guide_label`, `calc_copy_button`.

## Convenciones y trampas
- Todo texto visible pasa por `self.t("clave")`; no escribas strings de usuario en el código (excepción actual: encabezados "SOLUTION"/"Solution:" del historial).
- Tras crear widgets nuevos, llama `self.apply_theme()` (ya lo hace `build_matrix`). Los colores salen de `self.current_colors`.
- El **orden de `pack()`** en `ui/app.py` define el layout; respétalo al agregar paneles.
- `core/` lanza excepciones limpias (`ValueError`, etc.); la UI las muestra con `messagebox`. Los tests exigen que ninguna entrada inválida lance algo no capturable.
- `evaluate_expression` usa `eval` con `__builtins__` vacío tras reescribir fasores; no relajar esa sanitización.
- Pathing: nunca uses `Path(__file__)` para recursos/datos fuera de `paths.py`; en el ejecutable `__file__` apunta a un temporal.
- Formato `complejo_rect` de números reales es `"a + 0j"` (antes devolvía `None`).

## Compilación (PyInstaller)
- Un solo spec para Windows/Linux/macOS (`packaging/UI_ComplexCalc.spec`); compila para el SO donde corre. Rutas relativas a `SPECPATH`, se puede invocar desde cualquier carpeta.
- Entrada: `main.py`. `core/` y `ui/` se detectan por imports estáticos. `resources/` va en `datas`; los assets de customtkinter con `collect_data_files`.
- `hiddenimports=["PIL._tkinter_finder"]` es **obligatorio**: sin él el ejecutable falla al abrir (`ImageTk`).
- `data/` no se empaqueta: el ejecutable lo crea **junto al .exe** (`paths.DATA_DIR`) para que los guardados persistan (en onefile, `_MEIPASS` se borra al cerrar).
- CI: `.github/workflows/build.yml` ejecuta `pyinstaller packaging/UI_ComplexCalc.spec` desde `code/` y sube `code/dist/UI_ComplexCalc(.exe)`.
- Archivo nuevo en `resources/` → ya queda incluido. Módulo con import dinámico → añádelo a `hiddenimports`.
- Linux necesita `python3-tk` del sistema para compilar.
