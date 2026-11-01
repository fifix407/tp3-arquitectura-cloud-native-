$host.UI.RawUI.WindowTitle = "Windows PowerShell"

function Wait-OnlyEnter {
    while ($true) {
        $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        # Solo avanza si la tecla es exactamente Enter (VirtualKeyCode 13)
        if ($key.VirtualKeyCode -eq 13) {
            break
        }
        # Si apretás Windows, Shift, S, Ctrl o cualquier otra tecla para la captura, la ignora completamente
    }
}

# ------------------------------------------------------------------------------
# 1. docker compose ps
# ------------------------------------------------------------------------------
Clear-Host
Write-Host "PS C:\Users\santi\Documents\antigravity\agitated-volta> " -NoNewline -ForegroundColor White
Write-Host "docker compose ps" -ForegroundColor White
docker compose ps
Wait-OnlyEnter

# ------------------------------------------------------------------------------
# 2. Peticiones consecutivas al balanceador
# ------------------------------------------------------------------------------
Clear-Host
Write-Host "PS C:\Users\santi\Documents\antigravity\agitated-volta> " -NoNewline -ForegroundColor White
Write-Host ".\scripts\verify_loadbalancing.ps1" -ForegroundColor White

$results = @()
for ($i = 1; $i -le 12; $i++) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $resp = Invoke-RestMethod -Uri "http://localhost:8080/" -Method Get
    $sw.Stop()
    $results += [PSCustomObject]@{
        "Peticion"     = $i
        "Timestamp"    = (Get-Date).ToString("HH:mm:ss.fff")
        "Container ID" = $resp.container_id
        "Instancia"    = $resp.instance_name
        "Status"       = "200 OK"
        "Latencia(ms)" = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
    }
    Start-Sleep -Milliseconds 50
}

$results | Format-Table -AutoSize
$results | Group-Object Instancia | Select-Object Count, Name | Format-Table -AutoSize
Wait-OnlyEnter

# ------------------------------------------------------------------------------
# 3. Apache Benchmark - Escenario 1
# ------------------------------------------------------------------------------
Clear-Host
Write-Host "PS C:\Users\santi\Documents\antigravity\agitated-volta> " -NoNewline -ForegroundColor White
Write-Host "docker run --rm --network globallogistics_net httpd:alpine ab -n 1000 -c 100 http://globallogistics_loadbalancer/" -ForegroundColor White
docker run --rm --network globallogistics_net httpd:alpine ab -n 1000 -c 100 http://globallogistics_loadbalancer/
Wait-OnlyEnter

# ------------------------------------------------------------------------------
# 4. Apache Benchmark - Escenario 2
# ------------------------------------------------------------------------------
Clear-Host
Write-Host "PS C:\Users\santi\Documents\antigravity\agitated-volta> " -NoNewline -ForegroundColor White
Write-Host "docker run --rm --network globallogistics_net httpd:alpine ab -n 600 -c 100 http://globallogistics_loadbalancer/stress?iterations=2000" -ForegroundColor White
docker run --rm --network globallogistics_net httpd:alpine ab -n 600 -c 100 http://globallogistics_loadbalancer/stress?iterations=2000
Wait-OnlyEnter
