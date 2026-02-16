# create_pr.ps1
# Script para crear un Pull Request en GitHub pidiendo el token en tiempo de ejecución.
# Uso: Ejecutar en la raíz del repo: PowerShell -ExecutionPolicy Bypass -File .\create_pr.ps1

$owner = "calvindnw"
$repo = "scoutingapp-main"
$head = "feat/add-player-fields"
$base = "main"
$title = "feat: add player fields + player reports view"
$body = @'
Añade tres campos al esquema de jugadores y una vista de informes por jugador.

Qué incluye
- Añade campos de jugador: `video_url`, `telefono`, `representante`.
- Captura los campos en el formulario de creación y en el formulario de edición.
- Usa rango dinámico (`col_letter`) para `ws.update` y evitar desalineos con Sheets.
- Muestra `video_url`, `telefono` y `representante` en la ficha del jugador.
- Inserta una vista de informes específica del jugador (AgGrid paginado y seleccionable) entre la sección de edición y el formulario “Cargar nuevo informe”.
- Archivo modificado: `Scoutingapp.py`
- Rama: `feat/add-player-fields`

Checklist
- [ ] Verificar que la hoja `Jugadores` en Google Sheets contiene (o se le añaden) las columnas nuevas al final.
- [ ] Crear un jugador nuevo desde la UI y comprobar que la fila en Sheets incluye las 3 columnas nuevas (en el mismo orden).
- [ ] Editar un jugador existente y comprobar que `ws.update` actualiza la fila correcta sin desplazar columnas.
- [ ] Abrir la ficha de un jugador con informes: verificar que la sección “🗂️ Informes cargados sobre este jugador” muestra el grid y que al seleccionar una fila se despliegan los detalles.
- [ ] Probar crear un nuevo informe después de la vista (asegurar que el flujo de carga sigue funcionando).

Notas: la rama es feat/add-player-fields.
'@

Write-Host "Este script creará un Pull Request en https://github.com/$owner/$repo desde la rama '$head' hacia '$base'."
Write-Host "Por favor, pega tu Personal Access Token (se solicitará de forma segura y no se almacenará en disco)."

# Leer token de forma segura
$secureToken = Read-Host -Prompt 'Pegá tu GitHub Personal Access Token (secreto) y presioná Enter' -AsSecureString

try {
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
    $token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

    $headers = {
        @{ Authorization = "token $token"; Accept = "application/vnd.github+json" }
    }

    $payload = @{
        title = $title
        head  = $head
        base  = $base
        body  = $body
    } | ConvertTo-Json -Depth 10

    $uri = "https://api.github.com/repos/$owner/$repo/pulls"

    Write-Host "Creando PR..."
    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers @{ Authorization = "token $token"; Accept = "application/vnd.github+json" } -Body $payload -ContentType "application/json"

    if ($null -ne $response.html_url) {
        Write-Host "PR creado:" $response.html_url
    } else {
        Write-Host "Respuesta inesperada:" ($response | ConvertTo-Json)
    }

} catch {
    Write-Error "Error al crear PR: $_"
} finally {
    # limpiar variable temporal
    $token = $null
}
