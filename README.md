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

El proyecto ahora fija Streamlit en `http://localhost:8502` mediante `.streamlit/config.toml`, para evitar que el navegador quede apuntando a un puerto distinto.

### 3. Abrir la URL local

Abrí esta URL fija:

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

Si alguna vez `8502` esta ocupado, cerrá la otra app que lo esté usando o cambiá el puerto en `.streamlit/config.toml`.
