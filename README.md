# 🗺️ Bitácora Geográfica / BitaGeo v.1.0.0

**Autor:** Néstor Bentaberry  
**Institución:** CERP del Suroeste – Profesorado de Informática  
**Año:** 2025  

## 🎯 Propósito del proyecto

Bitácora Geográfica (BitaGeo) es una aplicación web desarrollada en **Python y Flask** que permite registrar observaciones territoriales y visualizar datos en gráficos dinámicos. Surge como una herramienta educativa en contexto abierto, pensada para **apoyar proyectos de aula y exploración territorial** en el campo de la Geografía escolar y de las ciencias sociales.

El objetivo central es integrar la **recolección de datos locales** con la **visualización gráfica**, promoviendo en los estudiantes una comprensión empírica del territorio a través del uso de tecnologías abiertas y accesibles.

---

## 🧠 Diseño y desarrollo

El proyecto se diseñó en forma modular, separando las capas de **lógica, interfaz y datos**.  
Se emplearon dos categorías principales de librerías:

- **Flask** → para la interfaz web y el enrutamiento.  
- **Matplotlib** → para la representación gráfica de los datos.

Además, se usó **CSV** como medio de persistencia simple, garantizando transparencia y portabilidad.  
La estructura del repositorio sigue una organización clara y reproducible:

```
/bitaGeo/
│
├── app.py                # Control principal de la aplicación Flask
├── static/               # Recursos estáticos (CSS, JS, imágenes)
├── templates/            # Vistas HTML con Jinja2
├── data/                 # Archivo CSV con registros de ejemplo
├── tests/                # Pruebas básicas con pytest
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación y ejecución

### Requisitos
- Python 3.11 o superior  
- PowerShell (en sistemas Windows)

### Pasos de ejecución
```powershell
py -m venv venv
.env\Scripts\Activate.ps1
py -m pip install flask matplotlib
py app.py
```

Abrir el navegador en:  
👉 http://127.0.0.1:5000

---

## 📊 Funcionalidades principales

- Registro y edición de observaciones geográficas o territoriales.  
- Visualización gráfica automática de los registros cargados.  
- Interfaz web simple y comprensible para contextos educativos.  
- Persistencia local mediante archivo CSV.  

---

## 🧩 Pruebas unitarias

El directorio `/tests` incluye **cinco pruebas con pytest**, que verifican:
- La carga y lectura del CSV.  
- El correcto funcionamiento de la función de registro.  
- La respuesta del servidor Flask.  
- La generación de gráficos válidos con Matplotlib.  
- El manejo de rutas principales.

---

## 🧱 Decisiones de diseño

Se priorizó un entorno **ligero, reproducible y pedagógico**, evitando dependencias externas o servicios de terceros.  
La elección de Flask permitió construir una **interfaz web educativa** con bajo costo computacional, adecuada para entornos escolares y de laboratorio.  
El uso de Matplotlib favoreció la integración directa de **gráficos sencillos** en la aplicación, vinculando programación con observación y análisis de datos.
Por defecto, las longitudes se interpretan positivas (Este) salvo que se indique hemisferio.
En el contexto uruguayo, las coordenadas pertenecen al hemisferio Oeste (valores negativos).

---

## 💬 Uso de herramientas de IA

Durante el proceso se recurrió a **asistencia de inteligencia artificial** para optimizar partes del código, principalmente en:

- Implementación de la interfaz web con Flask.  
- Ajustes de compatibilidad entre rutas y plantillas.  
- Estructura del gráfico generado con Matplotlib.  
- Verificación sintáctica y depuración de errores menores.

Todas las soluciones sugeridas fueron **revisadas, comprendidas y validadas** de manera personal, garantizando la autoría y el sentido pedagógico del proyecto.

---

## 📚 Fundamento didáctico

El desarrollo de Bitácora Geográfica permitió integrar **pensamiento computacional, análisis territorial y alfabetización digital**.  
El proyecto promueve en el aula una mirada interdisciplinaria: los estudiantes pueden **registrar datos reales, procesarlos y visualizar patrones** vinculados al entorno social o geográfico cercano.

Desde la perspectiva docente, la herramienta habilita una forma concreta de **enseñar Geografía desde la evidencia y el método**, articulando lo tecnológico con lo social.

---

## 🔍 Reflexión final

El proceso de creación exigió aplicar conocimientos de programación, lógica y diseño web, pero sobre todo **comprender cómo la tecnología puede ponerse al servicio del conocimiento geográfico**.  
El acompañamiento de herramientas de IA fue una oportunidad para aprender a validar, adaptar y evaluar soluciones automáticas sin perder la responsabilidad humana sobre el resultado.

Bitácora Geográfica se consolida así como un **producto educativo replicable y mejorable**, orientado a fomentar el análisis territorial con base empírica y tecnológica.
