# Script para verificar el balanceo Round-Robin e IDs de instancia
$hostUrl = "http://localhost:8080/"
Write-Host "Verificando balanceo de carga en $hostUrl..." -ForegroundColor Cyan

$requests = 15
$results = @()

for ($i = 1; $i -le $requests; $i++) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $resp = Invoke-RestMethod -Uri $hostUrl -Method Get -TimeoutSec 5
        $sw.Stop()
        $results += [PSCustomObject]@{
            "Req #"        = $i
            "Timestamp"    = (Get-Date).ToString("HH:mm:ss.fff")
            "Container ID" = $resp.container_id
            "Instancia"    = $resp.instance_name
            "Status HTTP"  = 200
            "Latencia(ms)" = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
        }
    }
    catch {
        $sw.Stop()
        $results += [PSCustomObject]@{
            "Req #"        = $i
            "Timestamp"    = (Get-Date).ToString("HH:mm:ss.fff")
            "Container ID" = "ERROR"
            "Instancia"    = "ERROR"
            "Status HTTP"  = $_.Exception.Response.StatusCode.value__
            "Latencia(ms)" = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
        }
    }
    Start-Sleep -Milliseconds 100
}

$results | Format-Table -AutoSize
Write-Host "`nDistribución total por instancia:" -ForegroundColor Green
$results | Group-Object Instancia | Select-Object Count, Name | Format-Table -AutoSize
