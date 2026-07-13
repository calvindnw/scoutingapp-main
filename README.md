# Scouting App
App de scouting en Streamlit.

## Inicio rapido en Windows

Este proyecto ya tiene un entorno virtual en `.venv`. En este equipo, los alias globales `python` y `streamlit` no resuelven bien desde PowerShell, asi que conviene ejecutar todo con el interprete del proyecto.

### 1. Instalar dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Iniciar la app

```powershell
.\.venv\Scripts\python.exe -m streamlit run Scoutingapp.py
```

### 3. Abrir la URL local

Normalmente Streamlit levanta en una de estas URLs:

- `http://localhost:8501`
- `http://localhost:8502`

## Si aparece la pantalla "Oh no"

Esa pantalla suele indicar que el frontend del navegador ya no puede hablar con el backend de Streamlit. Lo mas comun es una de estas causas:

- Se cerro la terminal donde estaba corriendo Streamlit.
- Se ejecuto `streamlit run` fuera del `.venv` correcto.
- El comando se lanzo con `python` o `streamlit` globales, pero esos alias no existen en Windows en este equipo.

Volve a iniciar la app con este comando:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Scoutingapp.py
```
