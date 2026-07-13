# Scouting App
App de scouting en Streamlit.

## Inicio rapido en Windows

Este proyecto ya tiene un entorno virtual en `.venv`. En este equipo, los alias globales `python` y `streamlit` no resuelven bien desde PowerShell, asi que conviene ejecutar todo con el interprete del proyecto.

### 1. Instalar dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Iniciar la app

Opción recomendada en Windows:

```powershell
./run_app.cmd
```

Si preferis PowerShell y tu equipo permite ejecutar scripts:

```powershell
.\run_app.ps1
```

Ese script:

- libera el puerto `8502` si quedó una instancia vieja de Streamlit
- abre una sola URL estable en el navegador
- arranca la app con el `.venv` correcto

`run_app.cmd` hace el mismo arranque sin depender de la Execution Policy de PowerShell.

Opción manual:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Scoutingapp.py
```

El proyecto ahora fija Streamlit en `http://localhost:8502` mediante `.streamlit/config.toml`, para evitar que el navegador quede apuntando a un puerto distinto.

## Leer Google Sheets en local

`localhost` si puede leer Google Drive y Google Sheets. Lo que necesita no es otro host, sino credenciales validas del service account.

Tenés tres opciones soportadas por el codigo:

1. Guardar el JSON del service account en `credentials/credentials.json`
2. Crear `.streamlit/secrets.toml` con la clave `GOOGLE_SERVICE_ACCOUNT_JSON`
3. Definir la variable de entorno `GOOGLE_SERVICE_ACCOUNT_JSON`

Ejemplo de `.streamlit/secrets.toml`:

```toml
GOOGLE_SERVICE_ACCOUNT_JSON = '{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"tu-service-account@tu-proyecto.iam.gserviceaccount.com","client_id":"...","token_uri":"https://oauth2.googleapis.com/token"}'
```

Ademas, la planilla `Scouting_DB` tiene que estar compartida con el `client_email` de ese service account. Si no esta compartida, Streamlit arranca pero Google rechaza la lectura.

## Deploy en Streamlit Community Cloud

La app publica `https://scoutingapp-eoc.streamlit.app/` puede fallar con `Oh no.` si el entorno remoto cambia o si los secretos del deploy se vacian o quedan invalidos.

Este repo ahora fija Python en `3.11` con `runtime.txt`, para evitar que Community Cloud use automaticamente una version mas nueva sin validacion previa.

Para volver a levantar la URL publica:

1. Entrá a la app en Streamlit Community Cloud.
2. Abrí `Settings` > `Secrets`.
3. Pegá el contenido de tu secreto `GOOGLE_SERVICE_ACCOUNT_JSON` en formato TOML.
4. Guardá los cambios.
5. Ejecutá `Reboot app` o redeploy desde el repo.

Importante: `.streamlit/secrets.toml` no debe commitearse al repo. Para el deploy remoto, los secretos viven en la configuracion de la app en Streamlit Cloud, no en GitHub.

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
