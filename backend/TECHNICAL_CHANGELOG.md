# Registro Técnico y Arquitectónico - Nexus-v0.6.1 (Bitácora de Depuración y Optimización)

Este documento guarda la traza íntegra de todos los bugs, correcciones y rediseños sistémicos realizados a nivel de código durante la estabilización pre-producción del **Proyecto Nexus v0.6.1**.

## 1. Restauración y Estética (UI/UX)
- **Reversión de CSS**: Se descartó la versión "Clean Design" (blanca/minimalista extrema) y se aplicó un hard-reset en `index.css` regenerando los estilos originales "Azul/Naranja".
- **Tipografía**: Se restituyó _DM Sans_ como fuente primaria en los headers e inputs.
- **Ventana de Previsualización**: 
  - Se optimizó y ensanchó el cuadro principal (`max-height: 1200px`) debido a que las propuestas generadas eran tan grandes (12-15 páginas) que hacer scroll se había vuelto muy impráctico.
  - Se implementó limpieza inteligente anti-HTML inyectado desde el backend para que la aplicación no se "rompiera" al recibir tablas pesadas.

## 2. Refactorización del Backend y Saneamiento de Rutas (`main.py`)
- **Limpieza de variables zombie**: Eliminación sistemática de dependencias obsoletas (`duracion_estimada`, `beneficiarios`) requeridas originalmente por `expand_seed_idea` pero extirpadas del frontend en la nueva UI, previniendo errores 500 al compilar.
- **Redirección Estática Root**: Mapeo directo de `@app.get("/")` para leer `static/index.html` sin forzar al usuario a ir a `/app`, optimizando la experiencia de entrada local.

## 3. Resolución de Motor PDF (ReportLab) e Integración Markdown
- **Depuración del Truncamiento y Fallos en Tablas (`pdf_engine.py`)**: 
  - El motor colapsaba arrojando _NameError: 'celdas'_ en `hacer_tabla_desde_markdown` porque se interrumpió la indexación del string en la detección. Corregido.
  - **Sanitización Hardcore**: Caracteres especiales (`&`, `<`, `>`, etc.) generados naturalmente por respuestas IA de corte técnico colapsaban a ReportLab y daban el infame bug de _"PDF no se puede generar"_. Se implementó `.replace(...)` manual a nivel celular en todas las listas Markdown e inputs de párrafos, usando `&amp;` de manera pasiva.
  - Persistencia sincrónica en PDF Final (Enlace a descarga inmediata): Reparación de un error fatal que obligaba al usuario a "hacer un cambio con IA" antes de permitir la descarga. Se reinsertó el estado global al inicializarse la expansión.

## 4. Cerebras (Qwen) y Control Total Antitruncamientos (`rhetoric_engine.py`)
- **El Gran Problema de Truncamiento**: Cerebras, al procesar más de 8-10 páginas, detenía abruptamente la API en sus 4,096 tokens predeterminados.
- **Acción Token Límite (`ai_client.py`)**: Aumento drástico del payload `max_tokens` a **16384** en el modelo Qwen `qwen-3-235b-a22b-instruct-2507`.
- **Estrategia Anti-Abuso (Red de Seguridad 85%)**: Ante recortes intermitentes de la IA en su paso maestro de (Rewrite/Polishing), se codificó un bloque de contención vital:
  - Si la última zona del prompt no se expone a la salida.
  - Si la salida de la propuesta es menor al 85% (_truncamiento silente_) de la proposición original en partes...
  - **Decisión**: Se aborta la edición AI y se reemplaza sin parpadear la respuesta con el conglomerado "Crudo", para salvaguardar el contenido denso/crítico en la salida del PDF. A la basura las respuestas mutiladas.

## 5. Edición Estricta (El Guardián del Contexto)
- **Instrucción de Rewrite "Inquebrantable"**: En vez de que el LLM del Frontend retornara únicamente los "cambios" que sugería el usuario (por ejemplo: _"Pon más énfasis en IA en esta sección"_ y devuelva 3 oraciones), se reescribió el template central del prompt en `main.py` bajo un axioma `PROHIBICIÓN ABSOLUTA`. El modelo fue constreñido sistemáticamente a retornar el documento entero y reestructurado de arriba hacia abajo sin omisión alguna tras la inserción del refactor humano.

Todo el ecosistema Nexus se ha migrado, blindado, validado bajo fuego por parte de los Logs de Uvicorn, y compilado estáticamente para los financiamientos MGA.

- **AntiGravity - 2026**
